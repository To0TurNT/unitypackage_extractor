# Changelog

All notable changes in this fork are documented in this file.

This is a fork of [Cobertos/unitypackage_extractor](https://github.com/Cobertos/unitypackage_extractor)
(base: **v1.1.0**). The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project aims to
follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2026-06-27

Changes relative to upstream v1.1.0.

### Added
- **Extraction progress.** A two-phase, in-place (`\r`) progress readout:
  `Unpacking … %` while the archive is unpacked to a temp dir, then
  `Extracting … %  <asset path>` while files are moved into place. Replaces the
  previous one-line-per-file logging.
- **`.meta` extraction.** Each asset's companion `asset.meta` is now written next
  to the asset (e.g. `Foo.shader` **and** `Foo.shader.meta`), so re-importing the
  extracted files into Unity preserves the original GUIDs. Folder-only entries
  (which carry a `.meta` but no `asset`) are also recreated as directories with
  their `.meta` kept, so folder GUIDs survive re-import too.
- **Console stays open on error.** When run as the standalone `.exe`
  (double-click / drag-and-drop) or via a `python -m unitypackage_extractor`
  shell verb, a failure now prints the traceback and waits for a keypress so the
  message is readable before the window closes. Successful runs close
  immediately (no keypress).

### Changed
- **Unified entry point.** `cli()` is now wrapped by a `main()` that handles
  top-level errors and the keep-open-on-error behavior; both
  `python -m unitypackage_extractor` (`__main__.py`) and the built exe call it.
  Library use via `extractPackage()` is unchanged.
- **Overwrite on re-extract.** Extracting into a folder that already contains
  previously extracted output now overwrites the existing files (including
  read-only ones) instead of failing, via `os.replace` with a
  clear-readonly + remove + move fallback.

### Fixed
- **Cross-drive extraction failure (`WinError 17` / `WinError 5`).** The extractor
  unpacked to the system temp dir (usually `C:`) and then moved each asset to the
  output. When the output was on a different drive (e.g. `G:`), `shutil.move`
  fell back to copy-then-delete and could abort the entire extraction partway —
  either on the cross-drive rename (`WinError 17`) or while deleting a
  read-only/locked temp file (`WinError 5: Access is denied`). The temp directory
  is now created on the **same volume as the output**, so each asset moves with a
  fast intra-volume rename (which also succeeds on read-only files).
- **Crash on non-ASCII asset names.** Printing an asset path containing characters
  outside the active console code page (e.g. Japanese filenames in a `cp1252`
  console) raised `UnicodeEncodeError` and aborted extraction mid-run. Console
  output now replaces unencodable characters instead of crashing; the filenames
  written to disk are unaffected.
- **Crash on malformed `pathname` entries.** An empty `pathname` file raised
  `IndexError` and aborted the whole extraction; such entries are now skipped.
  Trailing newlines are also stripped robustly (`\r\n` as well as `\n`).
- **Stranded scratch directory.** Because the temp dir now lives on the output
  volume, a hard-killed run could leave a `.upkg_tmp_*` folder behind. Each run
  now sweeps its own leftover scratch dirs from the output folder before starting.
  (Normal errors and Ctrl-C already clean up on their own.)

[1.2.0]: https://github.com/To0TurNT/unitypackage_extractor/compare/v1.1.0...v1.2.0
