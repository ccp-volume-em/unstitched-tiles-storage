# unstitched-tiles-storage

Example notebooks for storing unstitched image tiles as OME-Zarr, with the tile positions stored as transformations.

## Notebooks

Both notebooks write the example tiles in `data/example_cells` as an OME-Zarr 0.6 scene: one multiscale image per tile, plus a translation per tile into each of two scene coordinate systems:

- `stitched` (the default view): the registered tile positions, read from the tiffs' XPosition/YPosition tags
- `unstitched`: the original (acquisition) tile positions. These aren't stored in the tiffs, so the notebooks set them on a nominal grid from the filename's Y/X index (`<Y>_<X>_<Z>`) and a `grid_step`; replace these with the real stage positions where known.

The notebooks differ only in the library used:

- `notebooks/create-tiles.ipynb`: `ome-zarr` / `ome-zarr-models`, writes `output/tiles.ome.zarr`
- `notebooks/create-tiles-ngff-zarr.ipynb`: `ngff-zarr`, writes `output/tiles-ngff.ome.zarr`

Each notebook runs in well under a minute.

## Setup

Create the conda environment (conda-forge only):

```
conda env create -f environment.yml
```

To rebuild it from scratch after changing `environment.yml`:

```
conda env remove -n unstitched-zarr-env
conda env create -f environment.yml
```

The zarr packages (`zarr`, `ome-zarr`, `ome-zarr-models`, `ngff-zarr`) need recent versions; minimum versions are pinned in `environment.yml`.

## Running the notebooks

The environment includes `ipykernel`, so it can run as a notebook kernel.

- **PyCharm / VS Code**: open the notebook and choose the `unstitched-zarr-env` interpreter (`<conda>/envs/unstitched-zarr-env/python.exe`) as the kernel.
- **Jupyter Lab/Notebook**: the environment doesn't include Jupyter itself. Either install it in the environment (`conda install -n unstitched-zarr-env jupyterlab`) and start it from there, or register the environment as a named kernel for a Jupyter installed elsewhere:

  ```
  conda activate unstitched-zarr-env
  python -m ipykernel install --user --name unstitched-zarr-env --display-name "unstitched-zarr-env"
  ```

Run the notebooks from the `notebooks` folder: input and output paths are relative (`../data`, `../output`).

## Viewing in napari

napari-ome-zarr (>= 0.11) reads OME-Zarr 0.6 scenes, but always shows the alphabetically first coordinate system, with no way to select another. `scripts/view_scene.py` opens a scene with a dropdown to select the coordinate system. Run it in an environment with napari and napari-ome-zarr:

```
python scripts/view_scene.py output/tiles.ome.zarr
```

Without a path, it opens a folder picker. It also loads each 3-channel 8-bit tile as a single RGB layer, instead of a layer per channel, as napari is slow to add many layers.

Alternatively, the `fused-scene` branch of [ccp-volume-em/napari-ome-zarr](https://github.com/ccp-volume-em/napari-ome-zarr/tree/fused-scene) ([PR](https://github.com/ome/napari-ome-zarr/pull/175)) adds a reader that fuses all tiles into a single layer per scene coordinate system (only the first, `stitched`, visible), using the full OME-Zarr 0.6 coordinate transformations. Install it in the napari environment, and open a scene with its fused reader:

```
pip install "napari-ome-zarr @ git+https://github.com/ccp-volume-em/napari-ome-zarr.git@fused-scene"
napari --plugin napari-ome-zarr.get_fused_reader output/tiles.ome.zarr
```

The default reader (`--plugin napari-ome-zarr`) still shows a layer per tile.

With this branch installed, `view_scene.py --fused` shows the fused layer, with the dropdown to select the coordinate system:

```
python scripts/view_scene.py --fused output/tiles.ome.zarr
```

## Troubleshooting

**The notebook hangs or does nothing, with no error.** The kernel is probably running a different Python. Check with this in the first cell:

```python
import sys; sys.executable
```

It should point into `unstitched-zarr-env`. A common cause is a user-level `python3` kernelspec (created by `ipykernel install --user` without `--name`) that overrides every environment's own kernel. Run `jupyter kernelspec list` inside the environment: `python3` should point to the environment's own `share/jupyter/kernels`. If it points to `%APPDATA%\jupyter\kernels\python3` (Windows) or `~/.local/share/jupyter/kernels/python3` (Linux), remove that folder.

**Python crashes silently on import (Windows).** MKL with conda-forge's `llvm-openmp` can crash on any linear-algebra call (`0xc06d007f`), for example when importing `ngff_zarr`. `environment.yml` uses OpenBLAS (`libblas=*=*openblas`) to avoid this.
