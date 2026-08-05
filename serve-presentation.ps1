param([switch]$NoBrowser)

$ErrorActionPreference = 'Stop'
$presentationRoot = [System.IO.Path]::GetFullPath((Split-Path -Parent $PSCommandPath))
$presentationRootPrefix = $presentationRoot.TrimEnd('\') + '\'
$presentationPort = 8765
$presentationUrl = "http://127.0.0.1:$presentationPort/index.html"

$mimeTypes = @{
  '.html' = 'text/html; charset=utf-8'
  '.js'   = 'text/javascript; charset=utf-8'
  '.css'  = 'text/css; charset=utf-8'
  '.json' = 'application/json; charset=utf-8'
  '.jpg'  = 'image/jpeg'
  '.jpeg' = 'image/jpeg'
  '.png'  = 'image/png'
  '.webp' = 'image/webp'
  '.svg'  = 'image/svg+xml'
  '.ico'  = 'image/x-icon'
}

$server = [System.Net.Sockets.TcpListener]::new([System.Net.IPAddress]::Loopback, $presentationPort)
try {
  $server.Start()
} catch {
  if (-not $NoBrowser) { Start-Process $presentationUrl }
  exit 0
}

Write-Host "Presentation: $presentationUrl"
Write-Host 'Keep this window open while presenting. Press Ctrl+C to stop.'
if (-not $NoBrowser) { Start-Process $presentationUrl }

try {
  while ($true) {
    $client = $server.AcceptTcpClient()
    try {
      $stream = $client.GetStream()
      $reader = [System.IO.StreamReader]::new($stream, [System.Text.Encoding]::ASCII, $false, 1024, $true)
      $requestLine = $reader.ReadLine()
      while (($headerLine = $reader.ReadLine()) -ne $null -and $headerLine -ne '') { }

      if ([string]::IsNullOrWhiteSpace($requestLine)) { continue }
      $requestTarget = $requestLine.Split(' ')[1]
      $requestPath = [System.Uri]::UnescapeDataString(([System.Uri]("http://127.0.0.1" + $requestTarget)).AbsolutePath).TrimStart('/')
      if ([string]::IsNullOrWhiteSpace($requestPath)) { $requestPath = 'index.html' }

      $localPath = $requestPath.Replace('/', [System.IO.Path]::DirectorySeparatorChar)
      $filePath = [System.IO.Path]::GetFullPath([System.IO.Path]::Combine($presentationRoot, $localPath))
      $isInsideRoot = $filePath.StartsWith($presentationRootPrefix, [System.StringComparison]::OrdinalIgnoreCase)

      if (-not $isInsideRoot) {
        $status = '403 Forbidden'
        $body = [System.Text.Encoding]::UTF8.GetBytes('Forbidden')
        $contentType = 'text/plain; charset=utf-8'
      } elseif (-not (Test-Path -LiteralPath $filePath -PathType Leaf)) {
        $status = '404 Not Found'
        $body = [System.Text.Encoding]::UTF8.GetBytes('Not Found')
        $contentType = 'text/plain; charset=utf-8'
      } else {
        $status = '200 OK'
        $body = [System.IO.File]::ReadAllBytes($filePath)
        $extension = [System.IO.Path]::GetExtension($filePath).ToLowerInvariant()
        $contentType = if ($mimeTypes.ContainsKey($extension)) { $mimeTypes[$extension] } else { 'application/octet-stream' }
      }

      $responseHeader = "HTTP/1.1 $status`r`nContent-Type: $contentType`r`nContent-Length: $($body.Length)`r`nCache-Control: no-cache`r`nConnection: close`r`n`r`n"
      $headerBytes = [System.Text.Encoding]::ASCII.GetBytes($responseHeader)
      $stream.Write($headerBytes, 0, $headerBytes.Length)
      $stream.Write($body, 0, $body.Length)
      $stream.Flush()
    } catch {
      # Ignore a single failed request and keep the presentation server running.
    } finally {
      $client.Close()
    }
  }
} finally {
  $server.Stop()
}
