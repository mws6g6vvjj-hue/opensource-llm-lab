param([switch]$Test, [switch]$ServerOnly)
$ErrorActionPreference = 'Stop'
$projectRoot = $PSScriptRoot
$runtimeRoot = Join-Path $projectRoot '.runtime'
$ollamaExe = Join-Path $runtimeRoot 'ollama/ollama.exe'
if (-not (Test-Path -LiteralPath $ollamaExe)) {
    throw 'Run setup.ps1 first.'
}
$env:OLLAMA_MODELS = Join-Path $runtimeRoot 'models'
$env:OLLAMA_HOST = '127.0.0.1:11434'
$env:OLLAMA_NO_CLOUD = '1'
New-Item -ItemType Directory -Force -Path (Join-Path $projectRoot 'logs') | Out-Null
try {
    $null = Invoke-RestMethod 'http://127.0.0.1:11434/api/version' -TimeoutSec 3
} catch {
    Start-Process -FilePath $ollamaExe -ArgumentList 'serve' -WindowStyle Hidden -PassThru `
        -RedirectStandardOutput (Join-Path $projectRoot 'logs/ollama-out.log') `
        -RedirectStandardError (Join-Path $projectRoot 'logs/ollama-error.log') | Out-Null
    $ready = $false
    for ($attempt = 0; $attempt -lt 30; $attempt++) {
        Start-Sleep -Seconds 1
        try {
            $null = Invoke-RestMethod 'http://127.0.0.1:11434/api/version' -TimeoutSec 2
            $ready = $true
            break
        } catch {}
    }
    if (-not $ready) { throw 'Ollama did not start. Check logs/ollama-error.log.' }
}
$tags = Invoke-RestMethod 'http://127.0.0.1:11434/api/tags'
if ('qwen2.5:1.5b' -notin @($tags.models.name)) {
    & $ollamaExe pull 'qwen2.5:1.5b'
    if ($LASTEXITCODE -ne 0) { throw 'Model download failed.' }
}
if ($ServerOnly) { return }
if ($Test) { & python (Join-Path $projectRoot 'chat.py') --test }
else { & python (Join-Path $projectRoot 'chat.py') }
if ($LASTEXITCODE -ne 0) { throw 'Chat program failed.' }
