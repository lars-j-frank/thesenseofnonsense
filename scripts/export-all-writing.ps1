# Export every tracked article body to Documents\writing\larsjf\*.docx
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "writing-lib.ps1")
Ensure-Pandoc

$root = Get-RepoRoot
$n = 0
foreach ($item in Get-ArticleManifest) {
    $md = Join-Path $root $item.Rel
    if (-not (Test-Path -LiteralPath $md)) {
        Write-Warning "Missing: $($item.Rel)"
        continue
    }
    & (Join-Path $PSScriptRoot "export-docx.ps1") -MdPath $md -Stem $item.Stem
    $n++
}
Write-Host "Exported $n articles to $(Get-WritingDir)"
