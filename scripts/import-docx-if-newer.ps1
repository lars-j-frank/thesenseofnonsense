param(
    [Parameter(Mandatory = $true)][string]$MdPath,
    [string]$Stem = "",
    [switch]$Force
)
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "writing-lib.ps1")
Ensure-Pandoc

if (-not [System.IO.Path]::IsPathRooted($MdPath)) {
    $MdPath = Join-Path (Get-RepoRoot) $MdPath
}

$Stem = Resolve-Stem -MdPath $MdPath -Stem $Stem
$dir = Get-WritingDir
$docx = Join-Path $dir "$Stem.docx"
$stampPath = Join-Path $dir ".sync\$Stem.json"

if (-not (Test-Path -LiteralPath $docx)) {
    Write-Host "No DOCX yet: $docx"
    exit 0
}
if (-not (Wait-FileStable -Path $docx)) { throw "DOCX locked or unstable: $docx" }

$hash = Get-FileSha256 -Path $docx
$stamp = Read-Stamp -Path $stampPath
$needsImport = $Force -or (-not $stamp.last_export_hash) -or ($hash -ne $stamp.last_export_hash)
if (-not $needsImport) {
    Write-Host "Unchanged: $Stem"
    exit 0
}
if ($stamp.last_import_hash -and ($hash -eq $stamp.last_import_hash) -and (-not $Force)) {
    Write-Host "Already imported: $Stem"
    exit 0
}

$tmp = Join-Path $env:TEMP "sense-import-$Stem.md"
& pandoc $docx -t markdown -o $tmp
if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $tmp)) {
    throw "pandoc docx->md failed for $Stem"
}
$body = Get-Content -LiteralPath $tmp -Raw -Encoding UTF8
Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue

$existingFm = ""
if (Test-Path -LiteralPath $MdPath) {
    $existingFm = (Split-FrontMatter -Text (Get-Content -LiteralPath $MdPath -Raw -Encoding UTF8)).FrontMatter
}
$out = $existingFm + $body
if (-not $out.EndsWith("`n")) { $out += "`n" }

$parent = Split-Path $MdPath -Parent
if ($parent -and -not (Test-Path -LiteralPath $parent)) {
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
}
Set-Content -LiteralPath $MdPath -Value $out -Encoding UTF8

$rel = $MdPath
$root = Get-RepoRoot
if ($MdPath.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
    $rel = $MdPath.Substring($root.Length).TrimStart('\', '/')
}

$stamp | Add-Member -NotePropertyName last_import_hash -NotePropertyValue $hash -Force
$stamp | Add-Member -NotePropertyName last_import_utc -NotePropertyValue ((Get-Date).ToUniversalTime().ToString("o")) -Force
$stamp | Add-Member -NotePropertyName stem -NotePropertyValue $Stem -Force
$stamp | Add-Member -NotePropertyName md_path -NotePropertyValue ($rel.Replace('\', '/')) -Force
if (-not $stamp.last_export_hash) {
    $stamp | Add-Member -NotePropertyName last_export_hash -NotePropertyValue $hash -Force
}
Write-Stamp -Path $stampPath -Stamp $stamp
Write-Host "Imported Word edits -> $MdPath"
