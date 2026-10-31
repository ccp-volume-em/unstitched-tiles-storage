# Known issues and TODO

Fused viewing of the tile scenes depends on two upstream PRs, both open since 2026-10-31:
[ome/napari-ome-zarr#175](https://github.com/ome/napari-ome-zarr/pull/175) (opt-in fused scene reader, from
`ccp-volume-em/napari-ome-zarr` branch `fused-scene`) and
[clbarnes/transformnd#93](https://github.com/clbarnes/transformnd/pull/93) (`ByDimension.to_affine()`, from
`ccp-volume-em/transformnd` branch `by-dimension-to-affine`). Pushing to those branches updates the PRs.
Local test setup: conda env `napari-fused-env` (a clone of `napari-env`, with editable installs of the clones
`C:/Users/Y/PycharmProjects/napari-ome-zarr` and `C:/Users/Y/PycharmProjects/transformnd`), and
`output/tiles-bydimension.ome.zarr` (`tiles.ome.zarr` with its translations as `byDimension` transformations).

## Known issues

### byDimension scenes need transformnd#93
Released transformnd (0.9.2) has no `ByDimension.to_affine()`, so napari-ome-zarr's `Scene` raises "Affine
transformation could not be computed" for any scene using `byDimension`, fused or not. `napari-fused-env` has the
fix; `test_by_dimension` in the napari-ome-zarr branch is `xfail(strict=True)` until it is released.

### Fused reader: what it doesn't check
Images are fused by channel position, only if their channel names and dtypes match (otherwise kept as separate
layers, with a warning). Images without channel names can't be checked. Label ids are not made unique across
tiles: overlapping labels show the last non-zero value.

### Cloned conda envs run the original env's Python
`conda create --clone` copies pip's `.exe` launchers unchanged, with the original env's python path in them:
`napari` in `napari-fused-env` ran `napari-env`'s napari-ome-zarr. Fixed there by regenerating the 63 launchers
with distlib's ScriptMaker. For a new clone, use `python -m napari ...` or regenerate the launchers.

## In progress

- **napari-ome-zarr#175 and transformnd#93: waiting for review.** Both CI workflows wait for a maintainer to
  approve them (first PRs from the ccp-volume-em forks). #175's pre-commit.ci passes; #93's lint steps
  (ruff 0.15.12, mypy 1.20.2, pydoclint 0.8.6) and tests pass locally.

## TODO

ESSENTIAL

- [ ] **Review comments on napari-ome-zarr#175** - change and push to `ccp-volume-em/napari-ome-zarr` branch
      `fused-scene`. Before pushing, run all its pre-commit hooks with their pinned versions, not only
      isort/black/flake8: mypy 2.1.0 in both configurations (default, and `--disallow-untyped-defs`, both
      `--ignore-missing-imports`, no site-packages) and seed-isort-config 2.2.0 (new third-party imports go in
      `.isort.cfg`) caught the first push.
- [ ] **Review comments on transformnd#93** - change and push to `ccp-volume-em/transformnd` branch
      `by-dimension-to-affine`; check with its pinned linters (`just lint`, versions in `uv.lock`).
- [ ] **transformnd#93 merged and released** - update transformnd in the napari env(s); in the napari-ome-zarr
      branch, remove the xfail of `test_by_dimension` (its strict XPASS fails the tests as a reminder) and require
      the released transformnd version in `pyproject.toml`.

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
