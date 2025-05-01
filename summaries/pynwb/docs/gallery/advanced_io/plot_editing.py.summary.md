# Editing NWB Files

## Overview
This guide explains how to edit NWB files in-place using pynwb. Carefully editing existing files is possible, but making a backup and validating after changes is highly recommended.

## Editing Datasets
To edit datasets in HDF5-based NWB files:

1. Open the file in read/write mode with `"r+"` or `"a"`
2. Modify dataset values directly

```python
with NWBHDF5IO("test_edit.nwb", "r+") as io:
    nwbfile = io.read()
    # Modify first 10 rows
    nwbfile.acquisition["synthetic_timeseries"].data[:10] = 0.0
```

You can also edit dataset attributes:

```python
with NWBHDF5IO("test_edit.nwb", "r+") as io:
    nwbfile = io.read()
    nwbfile.acquisition["synthetic_timeseries"].data.attrs["unit"] = "volts"
```

## Flexible Datasets
To create resizable datasets, use `H5DataIO` with the `maxshape` parameter:

```python
from hdmf.backends.hdf5.h5_utils import H5DataIO

# Create dataset with unlimited first dimension
data_io = H5DataIO(data=np.random.randn(100, 100), maxshape=(None, 100))

nwbfile.add_acquisition(
    TimeSeries(
        name="synthetic_timeseries",
        description="Random values",
        data=data_io,
        unit="m",
        rate=10e3,
    )
)
```

Resize a flexible dataset:

```python
with NWBHDF5IO("test_edit2.nwb", "r+") as io:
    nwbfile = io.read()
    nwbfile.acquisition["synthetic_timeseries"].data.resize((200, 100))
```

## Editing Groups Using h5py
For group edits, use h5py directly:

```python
import h5py

with h5py.File("test_edit.nwb", "r+") as f:
    f["acquisition"]["synthetic_timeseries"].attrs["description"] = "Random values in volts"
```

## Renaming or Moving Groups/Datasets
Use the `move` method in h5py:

```python
with h5py.File("test_edit.nwb", "r+") as f:
    # Rename
    f["acquisition"].move("synthetic_timeseries", "synthetic_timeseries_renamed")
    
    # Move to different location
    f["acquisition"].move(
        "synthetic_timeseries_renamed",
        "/analysis/synthetic_timeseries_renamed",
    )
```

## Adding Datasets to Existing Groups
Use `set_modified()` to add new datasets to existing groups:

```python
with NWBHDF5IO("test_edit3.nwb", "a") as io:
    nwbfile = io.read()
    nwbfile.subject.genotype = "Sst-IRES-Cre"
    nwbfile.subject.set_modified()  # Mark the container as modified
    io.write(nwbfile)
```

Note: Some modifications (changing fixed shape, datatype, compression, etc.) can't be done in-place and require exporting to a new file.