# Zarr IO for NWB Files

Zarr provides an alternative backend for NWB files, optimized for large datasets and cloud storage. It offers chunked, compressed N-dimensional arrays with support for concurrent reads and writes.

## Features
- Only loads data into memory when needed (like HDF5)
- Optimized for cloud storage (S3, etc.)
- Supports parallel computing
- Note: Creates many files which may cause issues on traditional file systems due to directory limitations

## Installation and Requirements
Zarr functionality is provided by the `hdmf-zarr` package.

## Basic Usage

### Creating an NWB File with Zarr

```python
from datetime import datetime
from dateutil.tz import tzlocal
import numpy as np
from pynwb import NWBFile, TimeSeries
from numcodecs import Blosc
from hdmf_zarr import ZarrDataIO, NWBZarrIO
import os

# Create the NWBFile
nwbfile = NWBFile(
    session_description="my first synthetic recording",
    identifier="EXAMPLE_ID",
    session_start_time=datetime.now(tzlocal()),
    session_id="LONELYMTN",
)
```

### Dataset Configuration

Replace `H5DataIO` with `ZarrDataIO` to configure chunking and compression:

```python
# Configure data with compression
data_with_zarr_data_io = ZarrDataIO(
    data=np.random.randn(100, 100),
    chunks=(10, 10),
    fillvalue=0,
    compressor=Blosc(cname='zstd', clevel=3, shuffle=Blosc.SHUFFLE)
)

# Add to the NWBFile
nwbfile.add_acquisition(
    TimeSeries(
        name="synthetic_timeseries",
        data=data_with_zarr_data_io,
        unit="m",
        rate=10e3,
    )
)
```

### Writing to Zarr

```python
path = "zarr_tutorial.nwb.zarr"
absolute_path = os.path.abspath(path)
with NWBZarrIO(path=path, mode="w") as io:
    io.write(nwbfile)
```

### Reading from Zarr

```python
with NWBZarrIO(path=absolute_path, mode="r") as io:
    read_nwbfile = io.read()
```

Using absolute paths can help ensure links and references work properly, though relative paths can also be used.