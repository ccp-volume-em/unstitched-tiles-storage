# TODO

- [x] Add a second scene / coordinate system, so the output has two:
  - **original** (or `stage` / `sem`): tiles as acquired, with no transformations (identity transforms if needed)
  - **stitched**: the registered scene, with the per-tile transformations

  Done as `stitched` and `unstitched` (named so `stitched` also sorts first, as napari-ome-zarr 0.11 shows the alphabetically first). The original positions aren't stored in the source tiffs, so the notebooks set them on a nominal grid from the filename's Y/X index.
