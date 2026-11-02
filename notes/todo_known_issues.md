# Known issues and TODO

Fused viewing of the tile scenes depends on
[ome/napari-ome-zarr#175](https://github.com/ome/napari-ome-zarr/pull/175) (opt-in fused scene reader, open since
2026-10-31, from `ccp-volume-em/napari-ome-zarr` branch `fused-scene`; pushing to it updates the PR), and for
`byDimension` scenes on [clbarnes/transformnd#93](https://github.com/clbarnes/transformnd/pull/93)
(`ByDimension.to_affine()`, merged 2026-11-01, released in transformnd 0.10.0).
Local test setup: conda env `napari-fused-env` (a clone of `napari-env`, with editable installs of the clones
`C:/Users/Y/PycharmProjects/napari-ome-zarr` and `C:/Users/Y/PycharmProjects/transformnd`), and
`output/tiles-bydimension.ome.zarr` (`tiles.ome.zarr` with its translations as `byDimension` transformations).

## Known issues

### byDimension scenes need transformnd 0.10, which ome-zarr doesn't allow yet
transformnd before 0.10.0 has no `ByDimension.to_affine()`, so napari-ome-zarr's `Scene` raises "Affine
transformation could not be computed" for any scene using `byDimension`, fused or not. ome-zarr (0.21.0 and main)
requires `transformnd>=0.9.2,<0.10.0`, so pip still installs 0.9.2; `napari-fused-env` has the fix (editable
clone). `test_by_dimension` in the napari-ome-zarr branch stays `xfail(strict=True)` until ome-zarr allows 0.10.

### Fused reader: what it doesn't check
Images are fused by channel position, only if their channel names and dtypes match (otherwise kept as separate
layers, with a warning). Images without channel names can't be checked. Label ids are not made unique across
tiles: overlapping labels show the last non-zero value.

### Cloned conda envs run the original env's Python
`conda create --clone` copies pip's `.exe` launchers unchanged, with the original env's python path in them:
`napari` in `napari-fused-env` ran `napari-env`'s napari-ome-zarr. Fixed there by regenerating the 63 launchers
with distlib's ScriptMaker. For a new clone, use `python -m napari ...` or regenerate the launchers.

## In progress

- **napari-ome-zarr#175: waiting for review.** Its CI waits for a maintainer to approve it (first PR from the
  ccp-volume-em fork); pre-commit.ci passes.

## TODO

ESSENTIAL

- [ ] **Review comments on napari-ome-zarr#175** - change and push to `ccp-volume-em/napari-ome-zarr` branch
      `fused-scene`. Before pushing, run all its pre-commit hooks with their pinned versions, not only
      isort/black/flake8: mypy 2.1.0 in both configurations (default, and `--disallow-untyped-defs`, both
      `--ignore-missing-imports`, no site-packages) and seed-isort-config 2.2.0 (new third-party imports go in
      `.isort.cfg`) caught the first push.
- [ ] **ome-zarr released allowing transformnd 0.10** - left to the ome-zarr-py maintainers, who raised the cap
      before (#662, #692). Then update transformnd in the napari env(s), and in the `fused-scene` branch remove
      the xfail of `test_by_dimension` (its strict XPASS fails the tests as a reminder), require
      `transformnd>=0.10.0` and that ome-zarr version in `pyproject.toml`. Checked 2026-11-02 with transformnd
      0.10.1 forced in: all 37 napari-ome-zarr tests pass, `test_by_dimension` included.

MINOR

- [ ] **napari-ome-zarr#175 merged and released** - point the README's "Viewing in napari" to the released
      napari-ome-zarr instead of the `fused-scene` branch (`--plugin napari-ome-zarr.get_fused_reader`, and
      `view_scene.py --fused`, which imports `FusedScene`).
- [ ] **Clean up the local test setup** - once both PRs are settled: `conda env remove -n napari-fused-env`,
      delete the two clones and `output/tiles-bydimension.ome.zarr`.

## Done

- **Second scene coordinate system** - the output has two: `stitched` (the registered scene, with the per-tile
  transformations; the default view) and `unstitched` (tiles as acquired). Named so `stitched` also sorts first,
  as napari-ome-zarr 0.11 shows the alphabetically first. The original positions aren't stored in the source
  tiffs, so the notebooks set them on a nominal grid from the filename's Y/X index.
- **Fused scene viewing** - `view_scene.py --fused` and the `fused-scene` branch's
  `napari-ome-zarr.get_fused_reader` show each coordinate system as a single layer per channel, for the
  notebooks' output as is (no separate notebook needed); verified against the tiffs' positions (16 of 16 tiles).
