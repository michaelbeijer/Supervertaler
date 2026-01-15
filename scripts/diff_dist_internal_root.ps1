param(
    [string]$CoreDir = "dist\Supervertaler-core\_internal",
    [string]$FullDir = "dist\Supervertaler-full\_internal",
    [switch]$DllOnly
)

$ErrorActionPreference = 'Stop'

function Get-Names([string]$path) {
    if (!(Test-Path $path)) {
        throw "Path not found: $path"
    }

    $items = Get-ChildItem -LiteralPath $path -File
    if ($DllOnly) {
        $items = $items | Where-Object { $_.Extension -ieq '.dll' }
    }

    return $items | ForEach-Object { $_.Name.ToLowerInvariant() }
}

$core = (Get-Names $CoreDir) | Sort-Object
$full = (Get-Names $FullDir) | Sort-Object

$onlyCore = Compare-Object -ReferenceObject $core -DifferenceObject $full -PassThru | Where-Object { $_.SideIndicator -eq '<=' } | Sort-Object
$onlyFull = Compare-Object -ReferenceObject $core -DifferenceObject $full -PassThru | Where-Object { $_.SideIndicator -eq '=>' } | Sort-Object

"Core root: $CoreDir"
"Full root: $FullDir"

""; "--- Only in CORE ---"
$onlyCore

""; "--- Only in FULL ---"
$onlyFull
