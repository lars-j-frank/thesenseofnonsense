param(
    [Parameter(Mandatory = $true)][string]$MdPath,
    [string]$Stem = ""
)
$ErrorActionPreference = "Stop"
. (Join-Path $PSScriptRoot "writing-lib.ps1")
Ensure-Pandoc

if (-not [System.IO.Path]::IsPathRooted($MdPath)) {
    $MdPath = Join-Path (Get-RepoRoot) $MdPath
}
if (-not (Test-Path -LiteralPath $MdPath)) { throw "Markdown not found: $MdPath" }

$Stem = Resolve-Stem -MdPath $MdPath -Stem $Stem
$dir = Get-WritingDir
$docx = Join-Path $dir "$Stem.docx"
$stampPath = Join-Path $dir ".sync\$Stem.json"

$raw = Get-Content -LiteralPath $MdPath -Raw -Encoding UTF8
$parts = Split-FrontMatter -Text $raw
# Strip cache-bust query strings so pandoc can resolve local images
$body = [regex]::Replace($parts.Body, '(\[[^\]]*\]\([^)\?]+\))\?v=\d+', '$1')
$body = [regex]::Replace($body, '(src="[^"\?]+\.png)\?v=\d+"', '$1"')
$tmp = Join-Path $env:TEMP "sense-docx-$Stem.md"
Set-Content -LiteralPath $tmp -Value $body -Encoding UTF8

$resourcePath = Split-Path $MdPath -Parent
$oldEap = $ErrorActionPreference
$ErrorActionPreference = "Continue"
& pandoc $tmp -o $docx --resource-path=$resourcePath 2>&1 | Out-Null
$ErrorActionPreference = $oldEap
Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
if (-not (Test-Path -LiteralPath $docx) -or ((Get-Item -LiteralPath $docx).Length -lt 500)) {
    throw "pandoc md->docx failed for $Stem"
}

$rel = $MdPath
$root = Get-RepoRoot
if ($MdPath.StartsWith($root, [System.StringComparison]::OrdinalIgnoreCase)) {
    $rel = $MdPath.Substring($root.Length).TrimStart('\', '/')
}

$hash = Get-FileSha256 -Path $docx
Write-Stamp -Path $stampPath -Stamp ([pscustomobject]@{
        last_export_hash = $hash
        last_import_hash = $hash
        last_export_utc  = (Get-Date).ToUniversalTime().ToString("o")
        last_import_utc  = (Get-Date).ToUniversalTime().ToString("o")
        stem             = $Stem
        md_path          = $rel.Replace('\', '/')
    })
Write-Host "Exported: $docx"
