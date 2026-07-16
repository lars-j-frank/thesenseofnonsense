# Shared helpers for Hugo article <-> Word DOCX round-trip (Lars writing drop zone).
# Drop zone mirrors the Whitepaper studio pattern: Documents\writing\larsjf (Drive-synced).

$script:RepoRoot = Split-Path $PSScriptRoot -Parent
$script:WritingDir = Join-Path $env:USERPROFILE "Documents\writing\larsjf"

function Get-WritingDir {
    New-Item -ItemType Directory -Path $script:WritingDir -Force | Out-Null
    New-Item -ItemType Directory -Path (Join-Path $script:WritingDir ".sync") -Force | Out-Null
    return $script:WritingDir
}

function Get-RepoRoot { $script:RepoRoot }

function Ensure-Pandoc {
    if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
        throw "pandoc not found on PATH. Install from https://pandoc.org/"
    }
}

function Get-FileSha256 {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Wait-FileStable {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [int]$Retries = 6,
        [int]$DelayMs = 400
    )
    if (-not (Test-Path -LiteralPath $Path)) { return $false }
    if ((Split-Path $Path -Leaf).StartsWith("~$")) { return $false }
    $prev = -1
    for ($i = 0; $i -lt $Retries; $i++) {
        $len = (Get-Item -LiteralPath $Path).Length
        if ($len -eq $prev -and $len -gt 0) { return $true }
        $prev = $len
        Start-Sleep -Milliseconds $DelayMs
    }
    return $true
}

function Split-FrontMatter {
    param([Parameter(Mandatory = $true)][string]$Text)
    if ($Text -match "(?s)^(---\r?\n.*?\r?\n---\r?\n)(.*)$") {
        return @{ FrontMatter = $Matches[1]; Body = $Matches[2] }
    }
    return @{ FrontMatter = ""; Body = $Text }
}

function Read-Stamp {
    param([Parameter(Mandatory = $true)][string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        return [pscustomobject]@{
            last_export_hash = $null
            last_import_hash = $null
            last_export_utc  = $null
            last_import_utc  = $null
            stem             = $null
            md_path          = $null
        }
    }
    return (Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json)
}

function Write-Stamp {
    param(
        [Parameter(Mandatory = $true)][string]$Path,
        [Parameter(Mandatory = $true)]$Stamp
    )
    $parent = Split-Path $Path -Parent
    New-Item -ItemType Directory -Path $parent -Force | Out-Null
    ($Stamp | ConvertTo-Json) | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Resolve-Stem {
    param(
        [Parameter(Mandatory = $true)][string]$MdPath,
        [string]$Stem = ""
    )
    if ($Stem) { return $Stem }
    $leaf = Split-Path $MdPath -Leaf
    if ($leaf -ieq "index.md") {
        return (Split-Path (Split-Path $MdPath -Parent) -Leaf)
    }
    if ($leaf -ieq "about.md") { return "about" }
    return [System.IO.Path]::GetFileNameWithoutExtension($leaf)
}

function Get-ArticleManifest {
    # Relative paths from repo root -> stem
    return @(
        @{ Stem = "part-1-the-billion-dollar-detour"; Rel = "content\series\the-tier-files\part-1-the-billion-dollar-detour\index.md" }
        @{ Stem = "part-2-the-eight-million-dollar-regulator"; Rel = "content\series\the-tier-files\part-2-the-eight-million-dollar-regulator\index.md" }
        @{ Stem = "part-3-the-climate-fund-that-became-a-bank"; Rel = "content\series\the-tier-files\part-3-the-climate-fund-that-became-a-bank\index.md" }
        @{ Stem = "part-4-the-float"; Rel = "content\series\the-tier-files\part-4-the-float\index.md" }
        @{ Stem = "part-5-paid-in-alberta-claimed-everywhere"; Rel = "content\series\the-tier-files\part-5-paid-in-alberta-claimed-everywhere\index.md" }
        @{ Stem = "part-6-the-small-world"; Rel = "content\series\the-tier-files\part-6-the-small-world\index.md" }
        @{ Stem = "part-7-the-companies-the-board-pays-itself"; Rel = "content\series\the-tier-files\part-7-the-companies-the-board-pays-itself\index.md" }
        @{ Stem = "the-missing-year"; Rel = "content\essays\the-missing-year\index.md" }
        @{ Stem = "what-era-announced"; Rel = "content\essays\what-era-announced\index.md" }
        @{ Stem = "nineteen-recommendations"; Rel = "content\essays\nineteen-recommendations\index.md" }
        @{ Stem = "eighty-cents-of-the-dollar"; Rel = "content\essays\eighty-cents-of-the-dollar\index.md" }
        @{ Stem = "about"; Rel = "content\about.md" }
    )
}
