# Always run before editing Hugo content: pull Word edits if DOCX hash changed.
# Same idea as Whitepaper import-docx-if-newer before build.
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "writing-lib.ps1")
Ensure-Pandoc

$root = Get-RepoRoot
$imported = 0
$checked = 0
foreach ($item in Get-ArticleManifest) {
    $md = Join-Path $root $item.Rel
    $docx = Join-Path (Get-WritingDir) "$($item.Stem).docx"
    if (-not (Test-Path -LiteralPath $docx)) { continue }
    $checked++
    $before = if (Test-Path -LiteralPath $md) { Get-FileSha256 -Path $md } else { $null }
    & (Join-Path $PSScriptRoot "import-docx-if-newer.ps1") -MdPath $md -Stem $item.Stem
    $after = if (Test-Path -LiteralPath $md) { Get-FileSha256 -Path $md } else { $null }
    if ($before -and $after -and ($before -ne $after)) { $imported++ }
}
Write-Host "Checked $checked DOCX files; imported edits into $imported markdown file(s)."
if ($imported -gt 0) { exit 2 } else { exit 0 }
