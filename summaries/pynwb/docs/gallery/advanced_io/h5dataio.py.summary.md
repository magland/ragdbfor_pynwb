# Defining HDF5 Dataset I/O Settings in PyNWB

This document demonstrates how to customize HDF5 storage options like chunking and compression in PyNWB using `H5DataIO`.

## Core Concepts

- Use `H5DataIO` from `hdmf.backends.hdf5.h5_utils` to wrap data arrays while keeping Container classes independent from I/O backend
- `H5DataIO` enables customization of HDF5 features like chunking, compression, and resizable arrays

## Basic Usage Pattern

1. Import the necessary wrapper:
```python
from hdmf.backends.hdf5.h5_utils import H5DataIO
```

2. Wrap your data arrays with `H5DataIO` before passing to NWB objects:
```python
# Standard usage
test_ts = TimeSeries(
    name="regular_timeseries",
    data=data,
    unit="SIunit", 
    timestamps=timestamps
)

# With compression
test_ts = TimeSeries(
    name="compressed_timeseries",
    data=H5DataIO(data=data, compression=True),  # Compression added here
    unit="SIunit",
    timestamps=timestamps
)
```

## Chunking Example

```python
wrapped_data = H5DataIO(
    data=data,
    chunks=True,  # Enable chunking
    maxshape=(None, 10),  # Make time dimension unlimited/resizable
)
```

## Compression Example

```python
wrapped_data = H5DataIO(
    data=data,
    compression="gzip",  # Use GZip compression
    compression_opts=4,  # Optional compression level
)
```

## Advanced Features

- **Resizable Arrays**: Use `maxshape` parameter to define which dimensions can be resized
- **Fill Value**: Set `fillvalue` for uninitialized portions of datasets
- **Additional Filters**: `shuffle` and `fletcher32` I/O filters are also supported
- **H5py Dataset Handling**: Control how existing h5py.Dataset objects are handled with `link_data` parameter

## Dynamic Filters with hdf5plugin

Install additional compression filters:
```python
pip install hdf5plugin
```

Example using Z Standard algorithm:
```python
import hdf5plugin
wrapped_data = H5DataIO(
    data=data,
    **hdf5plugin.Zstd(clevel=3),
    allow_plugin_filters=True
)
```

Reading data with these features requires no special handling - all I/O settings are applied transparently.