const slides = [
  ['teamLab Borderless','Azabudai Hills, Tokyo','Japan','โลกศิลปะไร้พรมแดนที่ผลงานเคลื่อนข้ามห้อง เชื่อมโยง และเปลี่ยนแปลงร่วมกับผู้ชม'],
  ['teamLab Planets TOKYO','Toyosu, Tokyo','Japan','ประสบการณ์ Body Immersive ที่ให้ร่างกายเดินลุยน้ำและหลอมรวมเข้าไปในโลกของงานศิลปะ'],
  ['teamLab Botanical Garden Osaka','Nagai Botanical Garden, Osaka','Japan','เปลี่ยนสวนพฤกษศาสตร์ยามค่ำคืนให้เป็นศิลปะที่ผันแปรตามธรรมชาติ ฤดูกาล และผู้ชม'],
  ['teamLab SuperNature Macao','The Venetian Macao, Cotai','Macao SAR, China','พื้นที่สามมิติขนาดใหญ่ที่ทำให้ขอบเขตระหว่างร่างกาย งานศิลปะ และสิ่งแวดล้อมเลือนหาย'],
  ['teamLab Massless Beijing','Chaoyang Joy City, Beijing','China','สำรวจสภาวะไร้มวลผ่านแสง สี และภาพดิจิทัลที่ท้าทายการรับรู้ทางกายภาพ'],
  ['teamLab Phenomena Abu Dhabi','Saadiyat Cultural District, Abu Dhabi','United Arab Emirates','สร้างปรากฏการณ์จากแสง พื้นที่ และสิ่งแวดล้อม ซึ่งเปลี่ยนแปลงอย่างต่อเนื่องต่อหน้าผู้ชม','H-LtAoy1V44'],
  ['teamLab Biovortex Kyoto','Kyoto','Japan','ให้ร่างกายรับรู้และคิดเชิงมิติผ่านงานศิลปะที่เปลี่ยนตามผู้ชมและเชื่อมต่อกันเป็นระบบนิเวศ'],
  ['Museum of the Future','Dubai','United Arab Emirates','พาผู้ชมเดินทางสู่ปี 2071 ผ่านนิทรรศการ โรงละคร immersive และฉากอนาคตที่ต้องมีส่วนร่วม'],
  ['Mercer Labs — Museum of Art and Technology','15 Broadway, New York','United States','หลอมรวมศิลปะ เทคโนโลยี และประสาทสัมผัสใน 15 ห้องทดลองที่ผู้ชมสัมผัสและเปลี่ยนแปลงงานได้'],
  ['Superblue Miami','Allapattah, Miami, Florida','United States','รวมผลงานขนาดใหญ่จากศิลปินร่วมสมัย ให้ผู้ชมมีส่วนเติมเต็มงานผ่านแสง เสียง การเคลื่อนไหว และชีพจร'],
  ['AURA Invalides','Dôme des Invalides, Paris','France','ปลุกสถาปัตยกรรมโดมให้มีชีวิตด้วยวิดีโอแมปปิง แสง และดนตรีออร์เคสตราที่เผยรายละเอียดของสถานที่'],
  ['ARTECHOUSE DC','Southwest Washington, D.C.','United States','ใช้สถาปัตยกรรมเป็นผืนผ้าใบสำหรับศิลปะดิจิทัลหมุนเวียน เชื่อมศิลปะ วิทยาศาสตร์ และเทคโนโลยี'],
  ['Illuminarium','AREA15, Las Vegas, Nevada','United States','สร้างการเดินทางเชิงภาพยนตร์ด้วยภาพฉายเลเซอร์ 4K เสียงเฉพาะจุด พื้นสั่น และกลิ่นโดยไม่ใช้แว่น'],
  ['TIMEWALK Exhibition','Immerse LDN, ExCeL London Waterfront','England','พาผู้ชมเดินทางผ่านอารยธรรมโบราณด้วยภาพฉาย 360 องศา เสียงเชิงพื้นที่ และการเล่าเรื่องแบบภาพยนตร์ที่โอบล้อมทุกประสาทสัมผัส'],
  ['Infinity Mirrored Room — The Souls of Millions of Light Years Away','The Broad, Los Angeles','United States','ใช้กระจกและแสงซ้ำต่อเนื่องสร้างภาพลวงตาไร้ขอบเขต กระตุ้นประสาทสัมผัสและการรับรู้ตัวตน'],
  ['Rain Room','Sharjah Art Foundation, Sharjah','United Arab Emirates','ให้ผู้ชมเดินกลางฝนโดยไม่เปียก เมื่อระบบติดตามร่างกายหยุดสายน้ำและเชื่อมมนุษย์กับธรรมชาติผ่านเทคโนโลยี'],
  ['Deep Space 8K','Ars Electronica Center, Linz','Austria','สร้างโลกเสมือนที่เดินเข้าไปได้ด้วยภาพฉาย 8K เต็มผนังและพื้น พร้อมระบบติดตามเลเซอร์แบบโต้ตอบ'],
  ['Nxt Museum','Amsterdam-Noord, Amsterdam','Netherlands','ใช้ศิลปะสื่อใหม่ขนาดใหญ่ตั้งคำถามว่าเทคโนโลยีกำลังเปลี่ยนมนุษย์และสังคมอย่างไร'],
  ['AMAZE Amsterdam','Elementenstraat 25, Amsterdam','Netherlands','เส้นทางโสตทัศน์หลายห้องที่หลอมรวมแสง เสียง และวิชวลแบบเทศกาลจากวัฒนธรรมดนตรีอิเล็กทรอนิกส์ดัตช์'],
  ['Moco Museum — Digital Immersive Art','Museumplein, Amsterdam','Netherlands','ใช้แสง สี กระจก และโลกดิจิทัลสำรวจความเชื่อมโยงระหว่างผู้คนและความเป็นไปได้ของอนาคตร่วมกัน'],
  ['Van Gogh Alive','The Lume Melbourne, Melbourne','Australia','เล่าชีวิตและผลงาน Van Gogh ด้วยภาพขนาดมหึมา สีเคลื่อนไหว และดนตรีที่ครอบคลุมทุกพื้นผิว'],
  ['The Obliteration Room','Queensland Art Gallery, Brisbane','Australia','ให้ผู้ชมร่วมเปลี่ยนห้องสีขาวด้วยสติกเกอร์จุดสี จนพื้นที่ค่อย ๆ ถูกสร้างใหม่โดยส่วนรวม'],
  ['Atelier des Lumières','11th arrondissement, Paris','France','เปลี่ยนโรงหล่อเก่าเป็นผืนผ้าใบ 360 องศา ให้ผู้ชมเดินเข้าไปอยู่ท่ามกลางภาพวาดและดนตรี'],
  ['Bassins des Lumières','Base sous-marine, Bordeaux','France','ใช้ผนังมหึมาและเงาสะท้อนบนอ่างน้ำของฐานเรือดำน้ำสร้างภูมิทัศน์ภาพและเสียงรอบตัว'],
  ['Carrières des Lumières','Les Baux-de-Provence','France','ฉายงานศิลปะบนผนังหินมหึมาของเหมือง ให้สถาปัตยกรรมธรรมชาติเป็นส่วนหนึ่งของเรื่องราว'],
  ['Fabrique des Lumières','Westergas, Amsterdam','Netherlands','ปลุกงานศิลปะให้มีชีวิตทั่วผนังและพื้นโรงงานก๊าซเก่า ด้วยภาพดิจิทัลและเสียงหลายมิติ'],
  ['Phoenix des Lumières','Phoenix West, Dortmund','Germany','เปลี่ยนโถงอุตสาหกรรมเดิมให้เป็นจอภาพขนาดใหญ่ที่แสง ภาพเคลื่อนไหว และดนตรีทำงานร่วมกัน'],
  ['Bunker des Lumières','Seongsan, Jeju Island','South Korea','เปลี่ยนบังเกอร์ลับไร้แสงให้เป็นเขาวงกตของภาพฉาย ดนตรี และเทคโนโลยีที่ห่อหุ้มผู้ชม'],
  ['Frameless London','Marble Arch, London','United Kingdom','พาผู้ชมก้าวเข้าไปในผลงานชิ้นเอกผ่านภาพฉายเต็มผนัง แอนิเมชัน และดนตรีในสี่แกลเลอรี'],
  ['Lightroom — David Hockney: Bigger & Closer','King’s Cross, London','United Kingdom','สำรวจโลกผ่านสายตา David Hockney ด้วยภาพฉายสูงสี่ชั้น เสียงบรรยาย และดนตรีตลอดหกบท'],
  ['Outernet London','The Now Building, London','United Kingdom','เล่าเรื่องดิจิทัลด้วยจอ LED 16K โอบล้อม 360 องศา ผสานเสียงเชิงทิศทางและปฏิสัมพันธ์'],
  ['Dalí Cybernetics','IDEAL Centre d’Arts Digitals, Barcelona','Spain','พาผู้ชมเข้าสู่จักรวาลเหนือจริงของ Dalí ผ่านภาพฉาย 360 องศา งานโต้ตอบ โฮโลแกรม และ VR'],
];

const localImages = [
  'assets/01-teamlab-borderless.jpg',
  'assets/02-teamlab-planets.jpg',
  'assets/03-teamlab-botanical-osaka.jpg',
  'assets/04-teamlab-supernature-macao.jpg',
  'assets/05-teamlab-massless-beijing.jpg',
  'assets/06-user-replacement.png',
  'assets/31-biovortex-user-v2.png',
  'assets/40-museum-of-the-future.jpg',
  'assets/20-user-replacement.png',
  'assets/22-superblue-user.png',
  'assets/36-aura-user.png',
  'assets/25-artechouse-dc.webp',
  'assets/24-illuminarium-user.png',
  'assets/14-timewalk-press-original.jpg',
  'assets/28-infinity-user.png',
  'assets/24-rain-user-v2.png',
  'assets/31-deep-space-user.png',
  'assets/32-nxt-user.png',
  'assets/19-amaze-official.jpg',
  'assets/35-moco-digital-fhd.jpg',
  'assets/29-van-gogh-user-v2.png',
  'assets/29-obliteration-user.png',
  'assets/09-user-replacement.png',
  'assets/10-user-replacement.png',
  'assets/11-user-replacement.png',
  'assets/12-user-replacement.png',
  'assets/13-phoenix-des-lumieres.webp',
  'assets/15-bunker-des-lumieres.jpg',
  'assets/16-user-replacement.png',
  'assets/17-lightroom-hockney.jpg',
  'assets/18-user-replacement.png',
  'assets/34-dali-user.png',
];

const slideVideos = {
  0: [
    'IiXnprnBMeQ',
    '4zvI8-zLJLg',
  ],
  1: [
    'dArt0C4JH_I',
    'Y1MAL3dQqPw',
  ],
  2: [
    'CbVxr6qGIgc',
  ],
  3: [
    'Q2ZLhxEX3ak',
  ],
  4: [
    'nmj_2arKUZ4',
    'MAIH9blr6js',
    'Vy6JQM9V9FQ',
  ],
  5: [
    'SUpwj2vS4d8',
    'H-LtAoy1V44',
    'lqD-Uk4vfWM',
    'Yzdy_W21de4',
    'L-B0o9smbSU',
    'KeY4q5S6f7w',
    'njYxXHqb-K4',
  ],
  6: [
    'QPFNjSQ5u44',
    'YgYizEJesjE',
  ],
  8: [
    'Mc2q595Fzj8',
  ],
  9: [
    'Sia96h3lUUQ',
  ],
  10: [
    'QJwYTHzisYk',
  ],
  11: [
    'X4Ftbu9Frcc',
    'AL_so-YkDeQ',
  ],
  12: [
    'Bs4rYc7e6ys',
  ],
  13: [
    'AELoS_uBDUU',
  ],
  15: [
    '-z9hGdh_hHM',
    'FslABAyj2OA',
  ],
  16: [
    'fe1eqKsIL-U',
    'C6ATZIlSMUE',
  ],
  17: [
    'jLMIh5mfaRY',
    'I3Yg2GsZN70',
  ],
  18: [
    '-taUrnavw5c',
  ],
  20: [
    'dZkQSjZYsgc',
    'yMDD58iR8qo',
    '1A7TiOJS54Y',
    'Lxmh5m8hm8g',
  ],
  21: [
    '-xNzr-fJHQw',
    'LegJq5tNLyg',
  ],
};

let current = Math.max(0, Math.min(slides.length - 1, Number(location.hash.slice(1)) - 1 || 0));
const el = document.getElementById('slide');
const counter = document.getElementById('counter');
const videoModal = document.getElementById('video-modal');
const videoPlayer = document.getElementById('video-player');
const videoClose = document.getElementById('video-close');
const visitorCount = document.getElementById('visitor-count');
const visitorCountValue = document.getElementById('visitor-count-value');
const visitorStats = { site: 'ginomcclay28.github.io', path: '/immersive-museum-survey' };
let lastVideoTrigger = null;

async function loadVisitorCount() {
  const apiBase = 'https://page-views-api.ratneshc.com/api/v1';
  const params = new URLSearchParams(visitorStats);
  const isLocalPreview = location.protocol === 'file:' || ['localhost', '127.0.0.1'].includes(location.hostname);

  try {
    if (!isLocalPreview) {
      const trackResponse = await fetch(`${apiBase}/track?${params}`, { cache: 'no-store' });
      if (!trackResponse.ok) throw new Error(`Counter tracking failed: ${trackResponse.status}`);
    }

    const response = await fetch(`${apiBase}/views?${params}`, { cache: 'no-store' });
    if (!response.ok) throw new Error(`Counter loading failed: ${response.status}`);
    const data = await response.json();
    const views = Number(data.views);
    if (!Number.isFinite(views)) throw new Error('Counter returned an invalid value');

    visitorCountValue.textContent = new Intl.NumberFormat('en-US').format(views);
    visitorCount.title = `${visitorCountValue.textContent} website views`;
  } catch (error) {
    visitorCountValue.textContent = '—';
    visitorCount.classList.add('is-unavailable');
    console.warn(error);
  }
}

function openVideo(videoId, title, trigger) {
  lastVideoTrigger = trigger;
  videoPlayer.title = `${title} — YouTube video`;
  const playerOrigin = /^https?:$/.test(location.protocol)
    ? `&origin=${encodeURIComponent(location.origin)}`
    : '';
  videoPlayer.src = `https://www.youtube.com/embed/${encodeURIComponent(videoId)}?autoplay=1&rel=0&vq=hd1080${playerOrigin}`;
  videoModal.classList.add('is-open');
  videoModal.setAttribute('aria-hidden', 'false');
  document.body.classList.add('video-open');
  videoClose.focus();
}

function closeVideo() {
  if (!videoModal.classList.contains('is-open')) return;
  videoModal.classList.remove('is-open');
  videoModal.setAttribute('aria-hidden', 'true');
  document.body.classList.remove('video-open');
  videoPlayer.src = '';
  lastVideoTrigger?.focus();
  lastVideoTrigger = null;
}

function render(index) {
  closeVideo();
  current = (index + slides.length) % slides.length;
  const [title, venue, country, concept, videoId] = slides[current];
  const videos = slideVideos[current] || (videoId ? [videoId] : []);
  const src = `${localImages[current]}?v=20260805-video-library-03`;

  el.classList.remove('is-changing');
  el.innerHTML = `
    <div class="media count-1">
      <figure><img src="${src}" alt="${title}" loading="eager"></figure>
    </div>
    <div class="identity">
      <p class="eyebrow">
        <span>Global case study &middot; ${String(current + 1).padStart(2, '0')}</span>
      </p>
      <h1>${title}</h1>
      <p class="concept">${concept}</p>
      <p class="place"><strong>${venue}</strong>${country}</p>
      ${videos.length ? `<div class="video-list count-${videos.length}" aria-label="วิดีโอของ ${title}">
        ${videos.map((id, videoIndex) => `<button class="video-thumbnail" type="button" data-video-id="${id}" aria-label="เล่นวิดีโอ ${videoIndex + 1} ของ ${title}">
          <img src="https://i.ytimg.com/vi/${id}/mqdefault.jpg" alt="" loading="eager">
          <span class="thumbnail-play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M9 7.2 17 12l-8 4.8z"/></svg></span>
        </button>`).join('')}
      </div>` : ''}
    </div>`;

  el.querySelectorAll('.video-thumbnail').forEach((trigger, videoIndex) => {
    trigger.addEventListener('click', () => openVideo(trigger.dataset.videoId, `${title} — Video ${videoIndex + 1}`, trigger));
  });

  counter.textContent = `${current + 1} / ${slides.length}`;
  visitorCount.hidden = current !== 0;
  location.hash = current + 1;
  requestAnimationFrame(() => el.classList.add('is-changing'));
}

function move(delta){ render(current + delta); }
async function toggleFullscreen() {
  try {
    if (document.fullscreenElement) {
      await document.exitFullscreen();
    } else if (typeof document.documentElement.requestFullscreen === 'function') {
      await document.documentElement.requestFullscreen();
    } else {
      document.documentElement.classList.toggle('fullscreen-fallback');
    }
  } catch (_) {
    document.documentElement.classList.toggle('fullscreen-fallback');
  }
}
document.getElementById('prev').addEventListener('click',()=>move(-1));
document.getElementById('next').addEventListener('click',()=>move(1));
document.getElementById('fullscreen').addEventListener('click', toggleFullscreen);
videoClose.addEventListener('click', closeVideo);
videoModal.addEventListener('click', (e) => { if (e.target === videoModal) closeVideo(); });
document.addEventListener('keydown',(e)=>{
  if (videoModal.classList.contains('is-open')) {
    if (e.key === 'Escape') { e.preventDefault(); closeVideo(); }
    return;
  }
  if(['ArrowRight','PageDown',' '].includes(e.key)){ e.preventDefault(); move(1); }
  if(['ArrowLeft','PageUp'].includes(e.key)){ e.preventDefault(); move(-1); }
  if(e.key.toLowerCase()==='f'){ e.preventDefault(); toggleFullscreen(); }
  if(e.key==='Home') render(0);
  if(e.key==='End') render(slides.length-1);
});
window.addEventListener('hashchange',()=>{const n=Number(location.hash.slice(1)); if(n && n-1!==current) render(n-1)});
document.title = 'Immersive Exhibition / Museum \u2014 Global Survey';
document.getElementById('prev').textContent = '\u2190';
document.getElementById('prev').setAttribute('aria-label', '\u0e2a\u0e44\u0e25\u0e14\u0e4c\u0e01\u0e48\u0e2d\u0e19\u0e2b\u0e19\u0e49\u0e32');
document.getElementById('next').textContent = '\u2192';
document.getElementById('next').setAttribute('aria-label', '\u0e2a\u0e44\u0e25\u0e14\u0e4c\u0e16\u0e31\u0e14\u0e44\u0e1b');
document.getElementById('fullscreen').setAttribute('aria-label', '\u0e40\u0e15\u0e47\u0e21\u0e2b\u0e19\u0e49\u0e32\u0e08\u0e2d');
render(current);
loadVisitorCount();
