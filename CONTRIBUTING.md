# Contributing

Here's how to run all the development stuff.

## Setup Development Environment
* `pyenv global 3.7.6-amd64` (or whatever the latest is pyinstaller supports, sometimes it's not up to date)
* `pipenv install --dev`

## Building (local)

We build a x64 and an x86 binary. Use a Python interpreter of the matching bitness
(e.g. via `pyenv`) for each:

* `pip install . pyinstaller`
* `pyinstaller --onefile --name UnityPackageExtractor unitypackage_extractor/extractor.py` (or `python -m PyInstaller`, idk why but `pyinstaller` doesn't work sometimes)
* The binary lands at `dist/UnityPackageExtractor.exe`. Repeat with an x86 interpreter for the 32-bit build.

## Testing
* `pipenv run pytest -v` in the root directory

## Releasing
Releases are built and published automatically by the
[`Release Build`](.github/workflows/build.yaml) workflow when a `v*` tag is pushed.

* Bump `version` in `setup.py`.
* Add a new `## [x.y.z] - YYYY-MM-DD` section to `CHANGELOG.md` documenting the
  changes relative to upstream (under `### Added` / `### Changed` / `### Fixed`),
  and add a matching `[x.y.z]: …/compare/vA.B.C...vx.y.z` link at the bottom.
* Commit those changes, then tag and push:
  * `git tag vX.Y.Z`
  * `git push origin master --tags`
* The workflow builds the x64/x86 exes and publishes a GitHub Release with
  `unitypackage_extractor-x64.zip` / `-x86.zip` attached.

### Publishing to PyPI (optional)
Refer to [the python docs on packaging for clarification](https://packaging.python.org/tutorials/packaging-projects/).
* `python setup.py sdist bdist_wheel` - Create a source distribution and a binary wheel distribution into `dist/`
* `twine upload dist/unitypackage_extractor-x.x.x*` - Upload all `dist/` files to PyPI of a given version