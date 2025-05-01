# Parallel I/O using MPI in PyNWB

PyNWB supports parallel I/O using the Message Passing Interface (MPI) through its HDF5 storage backend. This functionality requires:

- `hdf5` and `h5py` installed with MPI driver support
- `mpi4py` installed
- Basic PyNWB installation is not sufficient for this functionality

## Key Example: Parallel Read/Write

The following workflow demonstrates parallel I/O with PyNWB:

1. **Create a dataset for parallel write** - A TimeSeries with space for 4 timestamps
2. **Write to the file in parallel using MPI** - Each MPI rank (process) writes data for a different timestamp
3. **Read from the file in parallel using MPI** - Each rank reads one time step from the file

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

# Create file on one rank, instantiating the dataset without writing data
if rank == 0:
    nwbfile = NWBFile("aa", "aa", start_time)
    data = H5DataIO(shape=(4,), maxshape=(4,), dtype=np.dtype("int"))

    nwbfile.add_acquisition(
        TimeSeries(name="ts_name", description="desc", data=data, rate=100.0, unit="m")
    )
    with NWBHDF5IO(fname, "w") as io:
        io.write(nwbfile)

# Write to dataset in parallel
with NWBHDF5IO(fname, "a", comm=MPI.COMM_WORLD) as io:
    nwbfile = io.read()
    print(rank)
    nwbfile.acquisition["ts_name"].data[rank] = rank

# Read from dataset in parallel
with NWBHDF5IO(fname, "r", comm=MPI.COMM_WORLD) as io:
    print(io.read().acquisition["ts_name"].data[rank])
```

Note that the `H5DataIO` class can be used to specify additional data layout parameters such as chunking and compression.