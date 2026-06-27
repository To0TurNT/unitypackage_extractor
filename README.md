<p align="center">
    <a href="https://github.com/To0TurNT/unitypackage_extractor/actions" target="_blank"><img alt="build status" src="https://github.com/To0TurNT/unitypackage_extractor/workflows/Package%20Tests/badge.svg"></a>
    <a href="https://pypi.org/project/unitypackage_extractor/" target="_blank"><img alt="pypi python versions" src="https://img.shields.io/pypi/pyversions/unitypackage_extractor.svg"></a>
</p>

# Unity Package Extractor

Extract your .unitypackage

> **This is a fork** of [Cobertos/unitypackage_extractor](https://github.com/Cobertos/unitypackage_extractor)
> (base **v1.1.0**), maintained by [To0TurNT](https://github.com/To0TurNT). See the
> full list of changes in [CHANGELOG.md](CHANGELOG.md). Highlights over upstream:
>
> * **Two-phase progress readout** — live `Unpacking …` then `Extracting … <asset>` instead of one line per file.
> * **`.meta` files are extracted** alongside each asset (and for folders), so re-importing into Unity preserves the original GUIDs.
> * **Cross-drive extraction fixed** (`WinError 17` / `WinError 5`) — the scratch dir is created on the same volume as the output.
> * **Overwrites on re-extract** instead of failing, including read-only files.
> * **More robust** — survives non-ASCII asset names, malformed `pathname` entries, and sweeps stranded scratch dirs.
> * **Console stays open on error** for the standalone `.exe` / shell verb, so the traceback is readable.

## Usage without Python

* Download the [unitypackage_extractor.zip](https://github.com/To0TurNT/unitypackage_extractor/releases/latest) from the Releases tab (`x64` for most machines, `x86` for 32-bit).
* Extract into a new directory
* Drag and drop your `.unitypackage` onto `UnityPackageExtractor.exe` OR
* Run from the command line with `UnityPackageExtractor.exe [path/to/your/package.unitypackage] (optional/output/path)`

### Right-click context menu (optional, Windows)

To extract a `.unitypackage` straight from Explorer with a right-click **Extract Unitypackage** entry:

* Place the executable at `C:\tools\UnityPackageExtractor.exe` (create the `tools` folder if needed). To use a different location, edit the path inside the `.reg` first.
* Double-click [`optional/unitypackage_extractor.reg`](optional/unitypackage_extractor.reg) and confirm the prompt to merge it into the registry.
* Right-click any `.unitypackage` → **Extract Unitypackage**. It extracts next to the package.

To remove the entry later, delete the `HKEY_CLASSES_ROOT\SystemFileAssociations\.unityPackage\shell\Unitypackage_Extractor` key (e.g. with the included uninstall `.reg` or `regedit`).

## Usage with Python 3.6+

* `pip install unitypackage_extractor`

* From the command line `python -m unitypackage_extractor [path/to/your/package.unitypackage] (optional/output/path)`

* OR in your Python file:
```python
from unitypackage_extractor.extractor import extractPackage

extractPackage("path/to/your/package.unitypackage", outputPath="optional/output/path")
```

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md).

## Credits
Original project by [Cobertos](https://cobertos.com) — see
[Cobertos/unitypackage_extractor](https://github.com/Cobertos/unitypackage_extractor).
Licensed under [MIT](LICENSE.txt).
