# unstitched-tiles-storage

Example notebooks for storing unstitched image tiles as OME-Zarr, with the tile positions stored as transformations.

## Notebooks

Both notebooks write the example tiles in `data/example_cells` as an OME-Zarr 0.6 scene: one multiscale image per tile, plus a translation per tile into a `stitched` coordinate system. They differ only in the library used:

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

## Troubleshooting

**The notebook hangs or does nothing, with no error.** The kernel is probably running a different Python. Check with this in the first cell:

```python
import sys; sys.executable
```

It should point into `unstitched-zarr-env`. A common cause is a user-level `python3` kernelspec (created by `ipykernel install --user` without `--name`) that overrides every environment's own kernel. Run `jupyter kernelspec list` inside the environment: `python3` should point to the environment's own `share/jupyter/kernels`. If it points to `%APPDATA%\jupyter\kernels\python3` (Windows) or `~/.local/share/jupyter/kernels/python3` (Linux), remove that folder.

**Python crashes silently on import (Windows).** MKL with conda-forge's `llvm-openmp` can crash on any linear-algebra call (`0xc06d007f`), for example when importing `ngff_zarr`. `environment.yml` uses OpenBLAS (`libblas=*=*openblas`) to avoid this.
