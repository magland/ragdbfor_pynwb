Parallel I/O using MPI is supported by the HDF5 storage backend in pynwb. Using this feature requires installing ``hdf5`` and ``h5py`` against an MPI driver, and installing ``mpi4py``.

Example:

1.  **Instantiate a dataset for parallel write**: Create `TimeSeries` with 4 timestamps for parallel writing.
2.  **Write in parallel using MPI**: Assumes 4 MPI ranks, each writing data for a different timestamp.
3.  **Read in parallel using MPI**: Each of the 4 MPI ranks reads one time step from the file.

```python
from mpi4py import MPI
import numpy as np
from dateutil import tz
from pynwb import NWBHDF5IO, NWBFile, TimeSeries
from datetime import datetime
from hdmf.backends.hdf5.h5_utils import H5DataIO

start_time = datetime(2018, 4, 25, 2, 30, 3, tzinfo=tz.gettz("US/Pacific"))
fname = "test_parallel_pynwb.nwb"
rank = MPI.COMM_WORLD.rank  # The process ID (integer 0-3 for 4-process run)

# Create file on one rank.
if rank == 0:
    nwbfile = NWBFile("aa", "aa", start_time)
    data = H5DataIO(shape=(4,), maxshape=(4,), dtype=np.dtype("int"))

    nwbfile.add_acquisition(
        TimeSeries(name="ts_name", description="desc", data=data, rate=100.0, unit="m")
    )
    with NWBHDF5IO(fname, "w") as io:
        io.write(nwbfile)

# write to dataset in parallel
with NWBHDF5IO(fname, "a", comm=MPI.COMM_WORLD) as io:
    nwbfile = io.read()
    print(rank)
    nwbfile.acquisition["ts_name"].data[rank] = rank

# read from dataset in parallel
with NWBHDF5IO(fname, "r", comm=MPI.COMM_WORLD) as io:
    print(io.read().acquisition["ts_name"].data[rank])
```

`H5DataIO` can be used to specify details about data layout, like chunking and compression.
