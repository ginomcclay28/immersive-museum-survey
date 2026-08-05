const fs = require('fs');
const path = require('path');
const sharp = require('sharp');

const assetsDir = path.resolve(__dirname, 'assets');
const shouldResize = process.argv.includes('--resize');
const imageExtensions = new Set(['.jpg', '.jpeg', '.png', '.webp']);

function outputOptions(pipeline, format) {
  if (format === 'jpeg') return pipeline.jpeg({ quality: 90, mozjpeg: true });
  if (format === 'png') return pipeline.png({ compressionLevel: 9, adaptiveFiltering: true });
  if (format === 'webp') return pipeline.webp({ quality: 90, effort: 5 });
  return pipeline;
}

function wait(milliseconds) {
  return new Promise((resolve) => setTimeout(resolve, milliseconds));
}

async function renameWithRetry(source, destination) {
  for (let attempt = 0; attempt < 12; attempt += 1) {
    try {
      fs.renameSync(source, destination);
      return true;
    } catch (error) {
      if (!['EBUSY', 'EPERM', 'EACCES'].includes(error.code) || attempt === 11) return false;
      await wait(250);
    }
  }
  return false;
}

async function main() {
  const files = fs.readdirSync(assetsDir)
    .filter((name) => !name.includes('.fhd-temp') && !name.includes('.fhd-backup'))
    .filter((name) => imageExtensions.has(path.extname(name).toLowerCase()))
    .sort();

  const oversized = [];
  let totalBefore = 0;
  let totalAfter = 0;

  for (const name of files) {
    const filePath = path.join(assetsDir, name);
    const statBefore = fs.statSync(filePath);
    totalBefore += statBefore.size;

    const metadata = await sharp(filePath).metadata();
    const width = metadata.autoOrient?.width ?? metadata.width;
    const height = metadata.autoOrient?.height ?? metadata.height;
    const canFillFhd = width >= 1920 && height >= 1080;
    const isOversized = canFillFhd && (width !== 1920 || height !== 1080);

    if (!isOversized) {
      totalAfter += statBefore.size;
      continue;
    }

    const item = {
      name,
      before: `${width}x${height}`,
      beforeMB: +(statBefore.size / 1048576).toFixed(2),
    };

    if (shouldResize) {
      const tempPath = `${filePath}.fhd-temp${path.extname(name)}`;
      let pipeline = sharp(filePath)
        .rotate()
        .resize({ width: 1920, height: 1080, fit: 'cover', position: 'centre', withoutEnlargement: true, kernel: 'lanczos3' })
        .toColourspace('srgb');
      pipeline = outputOptions(pipeline, metadata.format);
      await pipeline.toFile(tempPath);
      const backupPath = `${filePath}.fhd-backup`;
      const backupCreated = await renameWithRetry(filePath, backupPath);
      if (!backupCreated) {
        fs.unlinkSync(tempPath);
        item.skipped = 'file locked';
        totalAfter += statBefore.size;
        oversized.push(item);
        continue;
      }
      try {
        const replacementMoved = await renameWithRetry(tempPath, filePath);
        if (!replacementMoved) throw new Error(`Could not move resized file into place: ${name}`);
        fs.unlinkSync(backupPath);
      } catch (error) {
        if (fs.existsSync(filePath)) fs.unlinkSync(filePath);
        fs.renameSync(backupPath, filePath);
        throw error;
      }

      const resultMetadata = await sharp(filePath).metadata();
      const statAfter = fs.statSync(filePath);
      item.after = `${resultMetadata.width}x${resultMetadata.height}`;
      item.afterMB = +(statAfter.size / 1048576).toFixed(2);
      totalAfter += statAfter.size;
    } else {
      item.target = '1920x1080 cover';
      totalAfter += statBefore.size;
    }

    oversized.push(item);
  }

  console.log(JSON.stringify({
    mode: shouldResize ? 'resize' : 'audit',
    images: files.length,
    oversized: oversized.length,
    totalBeforeMB: +(totalBefore / 1048576).toFixed(2),
    totalAfterMB: +(totalAfter / 1048576).toFixed(2),
    files: oversized,
  }, null, 2));
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
