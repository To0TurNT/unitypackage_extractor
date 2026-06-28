import tarsafe
import tempfile
import sys
import os
import time
import shutil
import stat
import re
from pathlib import Path

def _progress(done, total, label, name=''):
  try:
    cols = shutil.get_terminal_size((80, 20)).columns
    pct = (done / total * 100) if total else 100.0
    line = f"{label} {pct:5.1f}% ({done}/{total})"
    if name:
      line += "  " + name
    line = line[:cols - 1]                    # truncate so it can't wrap ('\r' only works on one line)
    pad = max(0, _progress.last - len(line))  # clear leftovers from a longer previous line
    sys.stdout.write("\r" + line + " " * pad)
    sys.stdout.flush()
    _progress.last = len(line)
  except Exception:
    pass
_progress.last = 0

def _progressDone():
  if _progress.last:
    try:
      sys.stdout.write("\n")
      sys.stdout.flush()
    except Exception:
      pass
    _progress.last = 0

def _moveOverwrite(src, dst):
  try:
    os.replace(src, dst)
    return
  except OSError:
    pass
  try:
    if os.path.exists(dst):
      os.chmod(dst, stat.S_IWRITE) # read-only so it can be replaced
      os.remove(dst)
  except OSError:
    pass
  shutil.move(src, dst)

_TEMP_PREFIX = ".upkg_tmp_"

def extractPackage(packagePath, outputPath=None, encoding='utf-8'):
  if not outputPath:
    outputPath = os.getcwd() # If not explicitly set, WindowsPath("") has no parents, and causes the escape test to fail
  os.makedirs(outputPath, exist_ok=True)
  # Sweep scratch dirs stranded by a previously hard-killed run (our prefix only)
  try:
    for e in os.scandir(outputPath):
      if e.is_dir() and e.name.startswith(_TEMP_PREFIX):
        shutil.rmtree(e.path, ignore_errors=True)
  except OSError:
    pass
  with tempfile.TemporaryDirectory(dir=outputPath, prefix=_TEMP_PREFIX) as tmpDir:
    # Phase 1: unpack the archive into the temp dir, reporting progress per member.
    with tarsafe.open(name=packagePath, encoding=encoding) as upkg:
      members = upkg.getmembers()
      total = len(members)
      def _trackedMembers():
        for i, member in enumerate(members, 1):
          _progress(i, total, "Unpacking")
          yield member
      upkg.extractall(tmpDir, members=_trackedMembers())
    _progressDone()
    # Phase 2: move each asset from the temp dir to its real path under outputPath.
    entries = [e for e in os.scandir(tmpDir) if e.is_dir()]
    totalAssets = len(entries)
    for i, dirEntry in enumerate(entries, 1):
      assetEntryDir = f"{tmpDir}/{dirEntry.name}"
      pathnameFile = f"{assetEntryDir}/pathname"
      assetFile = f"{assetEntryDir}/asset"
      metaFile = f"{assetEntryDir}/asset.meta"
      hasAsset = os.path.exists(assetFile)
      hasMeta = os.path.exists(metaFile)
      # Need a pathname to know where it goes, plus an asset or a .meta to write.
      # File entries have asset (+ .meta); folder entries have only pathname + .meta.
      if not os.path.exists(pathnameFile) or (not hasAsset and not hasMeta):
        _progress(i, totalAssets, "Extracting")
        continue #Nothing placeable in this entry
      # Get the path to output to from /pathname
      with open(pathnameFile, encoding=encoding) as f:
        pathname = f.readline().rstrip('\r\n') #Remove trailing newline (handles \n and \r\n, and empty file)
        # Replace windows reserved chars with '_' that arent '/'
        if os.name == 'nt':
          pathname = re.sub(r'[\>\:\"\|\?\*]', '_', pathname)
      if not pathname: #Blank pathname, nothing we can place
        _progress(i, totalAssets, "Extracting")
        continue
      # Figure out final path, make sure that it's inside the write directory
      assetOutPath = os.path.join(outputPath, pathname)
      if Path(outputPath).resolve() not in Path(assetOutPath).resolve().parents:
        _progressDone() # break the progress line so the warning is readable
        print(f"WARNING: Skipping '{dirEntry.name}' as '{assetOutPath}' is outside of '{outputPath}'.")
        continue
      # Extract to the pathname
      if hasAsset:
        os.makedirs(os.path.dirname(assetOutPath), exist_ok=True) #Make the dirs up to the given folder
        _moveOverwrite(assetFile, assetOutPath)
        if hasMeta:
          _moveOverwrite(metaFile, f"{assetOutPath}.meta")
      else:
        # Folder entry: recreate the directory
        os.makedirs(assetOutPath, exist_ok=True)
        _moveOverwrite(metaFile, f"{assetOutPath}.meta")
      _progress(i, totalAssets, "Extracting", pathname)
    _progressDone()

class UsageError(Exception):
  """Raised for a missing/invalid invocation; shown as a plain message, not a traceback."""

def _progName():
  if getattr(sys, 'frozen', False):
    return os.path.basename(sys.argv[0]) # e.g. UnityPackageExtractor.exe
  return "python -m unitypackage_extractor"

def cli(args):
  if not args:
    raise UsageError(f"No .unitypackage path was given.\n\nUSAGE: {_progName()} [XXX.unitypackage] (optional/output/path)")
  print("TurNT_ Unity Package Extractor")
  startTime = time.time()
  extractPackage(args[0], args[1] if len(args) > 1 else "")
  print("--- Finished in %s seconds ---" % (time.time() - startTime))

def _pause():
  try:
    if os.name == 'nt':
      os.system("pause")
    elif sys.stdin and sys.stdin.isatty():
      input("Press Enter to continue . . .")
  except Exception:
    pass

def main(args):
  for stream in (sys.stdout, sys.stderr):
    try:
      stream.reconfigure(errors='replace')
    except Exception:
      pass
  try:
    cli(args)
  except UsageError as e:
    print(e, file=sys.stderr)
    _pause()
    return 2
  except Exception:
    import traceback
    traceback.print_exc()
    _pause() # pause on error
    return 1
  return 0

if __name__ == "__main__":
  sys.exit(main(sys.argv[1:]))