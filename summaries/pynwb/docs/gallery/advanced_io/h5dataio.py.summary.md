To customize HDF5 dataset I/O options like chunking and compression in PyNWB, wrap data arrays with `H5DataIO`. This keeps the Container classes independent of the I/O backend.

**Basic Usage:**

```python
from hdmf.backends.hdf5.h5_utils import H5DataIO
import numpy as np
from pynwb import TimeSeries, NWBFile
from datetime import datetime
from dateutil.tz import tzlocal

start_time = datetime(2017, 4, 3, 11, tzinfo=tzlocal())

nwbfile = NWBFile(
    session_description="demonstrate advanced HDF5 I/O features",
    identifier="NWB123",
    session_start_time=start_time,
)


data = np.arange(100, 200, 10)
timestamps = np.arange(10)

# Default TimeSeries
test_ts = TimeSeries(
    name="test_regular_timeseries",
    data=data,
    unit="SIunit",
    timestamps=timestamps,
)
nwbfile.add_acquisition(test_ts)

# Compressed TimeSeries
test_ts = TimeSeries(
    name="test_compressed_timeseries",
    data=H5DataIO(data=data, compression=True),
    unit="SIunit",
    timestamps=timestamps,
)
nwbfile.add_acquisition(test_ts)
```

**Chunking:**

Chunking stores arrays in multiple buffers. Using chunking allows optimization of data locality for I/O operations and enables the application of filters (e.g., compression) on a per-chunk basis.
Enable chunking and resizable arrays.

```python
data = np.arange(10000).reshape((1000, 10))
wrapped_data = H5DataIO(
    data=data,
    chunks=True,  # Enable chunking
    maxshape=(None, 10),  # Make the time dimension unlimited and hence resizable
)

test_ts = TimeSeries(
    name="test_chunked_timeseries",
    data=wrapped_data,
    unit="SIunit",
    starting_time=0.0,
    rate=10.0,
)
nwbfile.add_acquisition(test_ts)
```

Specifying `fillvalue` can define the value used when reading uninitialized portions of the dataset.

**Compression and Other I/O Filters:**

HDF5 supports I/O filters (e.g., compression) applied transparently. Filters operate per-chunk, requiring chunking.

```python
wrapped_data = H5DataIO(
    data=data,
    compression="gzip",  # Use GZip
    compression_opts=4,  # Optional GZip aggression option
)

test_ts = TimeSeries(
    name="test_gzipped_timeseries",
    data=wrapped_data,
    unit="SIunit",
    starting_time=0.0,
    rate=10.0,
)
nwbfile.add_acquisition(test_ts)
```

`H5DataIO` also enables the `shuffle` and `fletcher32` HDF5 I/O filters.

**Writing and Reading Data:**

```python
from pynwb import NWBHDF5IO

with NWBHDF5IO("advanced_io_example.nwb", "w") as io:
    io.write(nwbfile)

io = NWBHDF5IO("advanced_io_example.nwb", "r")
nwbfile = io.read()

for k, v in nwbfile.acquisition.items():
    print(
        "name=%s, chunks=%s, compression=%s, maxshape=%s"
        % (k, v.data.chunks, v.data.compression, v.data.maxshape)
    )
io.close()
```

**Wrapping `h5py.Datasets`:**

`H5DataIO` customizes how `h5py.Dataset` objects are handled via the `link_data` parameter. If set to `True`, a `SoftLink` or `ExternalLink` is created. If set to `False`, the dataset is copied (without attributes, soft links, external links, or references).  All settings except `link_data` are ignored when wrapping an `h5py.Dataset`.

**Dynamically Loaded Filters**

Install additional compression filters such as Z Standard via `pip install hdf5plugin`

```python
import hdf5plugin
from hdmf.backends.hdf5.h5_utils import H5DataIO

from pynwb.file import TimeSeries

wrapped_data = H5DataIO(
    data=data,
    **hdf5plugin.Zstd(clevel=3),  # set the compression and compression_opts parameters
    allow_plugin_filters=True,
)

test_ts = TimeSeries(
    name="test_gzipped_timeseries",
    data=wrapped_data,
    unit="SIunit",
    starting_time=0.0,
    rate=10.0,
)
```
