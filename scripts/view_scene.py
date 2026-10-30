"""Open an OME-Zarr 0.6 scene in napari, with a dropdown to select the scene coordinate system.

napari-ome-zarr (0.11) always shows the alphabetically first coordinate system, without a way to select another.
Run in an environment with napari and napari-ome-zarr >= 0.11, e.g.:

    python scripts/view_scene.py output/tiles-ngff.ome.zarr

Without a path, a folder picker asks for the OME-Zarr scene to open.
"""
import sys
from itertools import groupby

import dask.array as da
import napari
import numpy as np
import zarr
from napari.qt import get_qapp
from napari_ome_zarr.ome_zarr_reader import Scene
from ome_zarr import OMEZarrScene
from qtpy.QtWidgets import QComboBox, QFileDialog


def merge_rgb(layers):
    # the reader makes a layer per channel (named '<image>: <channel>'); napari's cost is per layer,
    # so combine each 3-channel 8-bit image into a single RGB layer
    for name, image_layers in groupby(layers, key=lambda layer_data: layer_data[1]['name'].split(': ')[0]):
        image_layers = list(image_layers)
        if len(image_layers) == 3 and all(data[0].dtype == np.uint8 for data, _, _ in image_layers):
            data = [da.stack(levels, axis=-1) for levels in zip(*(data for data, _, _ in image_layers))]
            meta = {key: value for key, value in image_layers[0][1].items()
                    if key not in ('name', 'colormap', 'contrast_limits', 'blending')}
            yield data, {**meta, 'name': name, 'rgb': True}, 'image'
        else:
            yield from image_layers


def load_scene(viewer, group, coordinate_system):
    viewer.layers.clear()
    for layer_data in merge_rgb(Scene(group).to_layer_data(('', coordinate_system))):
        viewer.add_layer(napari.layers.Layer.create(*layer_data))
    viewer.reset_view()


def main(path=None):
    if not path:
        get_qapp()
        path = QFileDialog.getExistingDirectory(None, 'Open OME-Zarr scene')
        if not path:
            return
    group = zarr.open_group(path, mode='r')
    coordinate_systems = [cs.name for cs in OMEZarrScene.from_ome_zarr(group).coordinate_systems]

    viewer = napari.Viewer()
    selector = QComboBox()
    selector.addItems(coordinate_systems)
    selector.currentTextChanged.connect(lambda name: load_scene(viewer, group, name))
    viewer.window.add_dock_widget(selector, name='Coordinate system', area='right')
    load_scene(viewer, group, coordinate_systems[0])
    napari.run()


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
