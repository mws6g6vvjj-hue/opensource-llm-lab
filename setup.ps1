$ErrorActionPreference = 'Stop'
$releaseVersion = 'v0.40.16'
$runtimeRoot = Join-Path $PSScriptRoot '.runtime'
$archive = Join-Path $runtimeRoot 'ollama-windows-amd64.zip'
$installDir = Join-Path $runtimeRoot 'ollama'
New-Item -ItemType Directory -Force -Path $runtimeRoot, $installDir | Out-Null
if (-not (Test-Path -LiteralPath (Join-Path $installDir 'ollama.exe'))) {
    Invoke-WebRequest "https://github.com/ollama/ollama/releases/download/$releaseVersion/ollama-windows-amd64.zip" -OutFile $archive
    $expectedHash = '50fcf5ad54277f2fa5d173ebfc93bcb017adbc0c9ef2314daabc96ca9e6aa64e'
    if ((Get-FileHash -LiteralPath $archive -Algorithm SHA256).Hash.ToLower() -ne $expectedHash) {
        throw 'The Ollama archive checksum does not match the official release.'
    }
    Expand-Archive -LiteralPath $archive -DestinationPath $installDir -Force
}
Write-Host 'Ollama is installed. Run: .\start.ps1'
