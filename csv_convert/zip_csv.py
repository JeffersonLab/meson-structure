#!/usr/bin/env python3
"""Compress CSV file(s) to ``<name>.zip`` with maximum DEFLATE compression and
verify the result.

Usage:
    zip_csv.py <file.csv> [<file2.csv> ...]

For each input it:
  - writes ``<input>.zip`` using ``ZIP_DEFLATED`` at ``compresslevel=9`` (the max
    the ``.zip`` container supports, so ``pandas.read_csv(compression='zip')``
    can read it — unlike ``python3 -m zipfile -c`` which STORES uncompressed);
  - verifies the archive: ``testzip()`` CRC check of every entry, a non-empty
    entry list, and a non-empty zip file;
  - on any failure removes the partial ``<input>.zip``.

It does NOT delete the source CSV. The caller (the ``zip_csv`` bash helper in the
job scripts) removes the original CSV only after this verification passes and its
own ``-s`` non-empty check. Exit status is non-zero if ANY input fails.
"""
import os
import sys
import zipfile


def zip_and_verify(csv_path: str) -> bool:
    """Return True iff <csv_path>.zip was written and passed verification."""
    zip_path = csv_path + ".zip"
    try:
        with zipfile.ZipFile(zip_path, "w",
                             compression=zipfile.ZIP_DEFLATED,
                             compresslevel=9) as zf:
            zf.write(csv_path, arcname=os.path.basename(csv_path))
        # Verify: CRC of every entry, non-empty entry list, non-empty file.
        with zipfile.ZipFile(zip_path) as zf:
            crc_ok = zf.testzip() is None
            has_entries = len(zf.namelist()) > 0
        if not (crc_ok and has_entries and os.path.getsize(zip_path) > 0):
            raise RuntimeError(
                f"verification failed (crc_ok={crc_ok}, entries={has_entries})")
    except Exception as exc:
        sys.stderr.write(f"[zip_csv] FAILED {csv_path}: {exc}\n")
        try:
            os.remove(zip_path)  # never leave a partial/corrupt archive behind
        except OSError:
            pass
        return False
    return True


def main(argv) -> int:
    if not argv:
        sys.stderr.write("usage: zip_csv.py <file.csv> [<file2.csv> ...]\n")
        return 2
    all_ok = True
    for path in argv:
        if not zip_and_verify(path):
            all_ok = False
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
