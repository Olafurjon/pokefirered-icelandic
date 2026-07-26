$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$backup = Join-Path $root "graphics\title_screen\rollback_vasaskrimsli_title_test"

$files = @(
    "graphics\title_screen\copyright_press_start.png",
    "graphics\title_screen\copyright_press_start.4bpp",
    "graphics\title_screen\copyright_press_start.4bpp.lz",
    "graphics\title_screen\copyright_press_start.bin",
    "graphics\title_screen\copyright_press_start.bin.lz",
    "graphics\title_screen\firered\game_title_logo.png",
    "graphics\title_screen\firered\game_title_logo.8bpp",
    "graphics\title_screen\firered\game_title_logo.8bpp.lz",
    "graphics\title_screen\firered\game_title_logo.gbapal",
    "graphics\title_screen\firered\game_title_logo.bin",
    "graphics\title_screen\firered\game_title_logo.bin.lz"
)

foreach ($file in $files) {
    $backupName = $file -replace "[\\/:]", "__"
    $src = Join-Path $backup $backupName
    $dst = Join-Path $root $file
    if (-not (Test-Path -LiteralPath $src)) {
        throw "Missing backup file: $src"
    }
    Copy-Item -LiteralPath $src -Destination $dst -Force
}

Write-Host "Restored original title-screen assets from $backup"
Write-Host "Run: wsl make modern -j8"
