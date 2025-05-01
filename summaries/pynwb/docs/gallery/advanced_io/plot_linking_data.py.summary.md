# Modular Data Storage using External Files in PyNWB

PyNWB supports several approaches to linking data between files:

## External Links
- Allow integration of data stored in external HDF5 files with NWB data files
- Useful for scenarios like recording multiple data streams to separate files during acquisition and later linking them together
- Same strategies work for Soft Links (pointing to objects in the same file) as for External Links (pointing to objects in external files)
- **Warning**: External links can break if files are moved, renamed, or permissions change

## Linking Methods

### 1. Linking to Select Datasets
```python
# Open file with data to link to
io1 = NWBHDF5IO(filename1, "r")
nwbfile1 = io1.read()
timeseries_1 = nwbfile1.get_acquisition("test_timeseries1")
timeseries_1_data = timeseries_1.data

# Create new TimeSeries using existing data
test_ts4 = TimeSeries(
    name="test_timeseries4",
    data=timeseries_1_data,  # Links to external data
    unit="SIunit",
    timestamps=timestamps,
)

# For explicit control over linking behavior:
from hdmf.backends.hdf5.h5_utils import H5DataIO
test_ts5 = TimeSeries(
    name="test_timeseries5",
    data=H5DataIO(data=timeseries_1_data, link_data=True),  # Explicit link
    unit="SIunit",
    timestamps=timestamps,
)

# Write with linking as default
with NWBHDF5IO(filename4, "w") as io4:
    io4.write(nwbfile4, link_data=True)
```

### 2. Linking to Whole Containers
```python
from pynwb import get_manager
manager = get_manager()

# Open files and get container objects
io1 = NWBHDF5IO(filename1, "r", manager=manager)
nwbfile1 = io1.read()
timeseries_1 = nwbfile1.get_acquisition("test_timeseries1")

io2 = NWBHDF5IO(filename2, "r", manager=manager)
nwbfile2 = io2.read()
timeseries_2 = nwbfile2.get_acquisition("test_timeseries2")

# Create new file and add existing timeseries
nwbfile3 = NWBFile(
    session_description="demonstrate external files",
    identifier=str(uuid4()),
    session_start_time=start_time,
)
nwbfile3.add_acquisition(timeseries_1)  # Will be linked
nwbfile3.add_acquisition(timeseries_2)  # Will be linked

# Write the new file with external links
with NWBHDF5IO(filename3, "w", manager=manager) as io3:
    io3.write(nwbfile3)
```

## Additional Features

### Copying an NWBFile for Linking
- Use `NWBFile.copy()` to create a shallow copy with links to data in original file

### Creating a Single File for Sharing
- Use `HDF5IO.export()` (or `NWBHDF5IO.export()`) to copy a file and resolve all external links

### Splitting Large Data Across Multiple HDF5 Files
```python
# Create empty expandable dataset
data = H5DataIO(maxshape=(None, 10),
                dtype=np.float32,
                shape=(0, 10),
                chunks=(1000, 10))

# Create TimeSeries with empty dataset
time_series = TimeSeries(name='example_timeseries',
                         data=data,
                         starting_time=0.0,
                         rate=1.0,
                         unit='mV')

# Use h5py family driver to split into multiple files
chunk_size = 1024**2  # 1MB per file
filename_pattern = 'family_nwb_file_%d.nwb'

with h5py.File(name=filename_pattern, mode='w', driver='family', memb_size=chunk_size) as f:
    with NWBHDF5IO(file=f, mode='w') as io:
        io.write(nwbfile)
        
        # Iteratively write data
        for i in range(10):
            start_index = i * 1000
            stop_index = start_index + 1000
            data.dataset.resize((stop_index, 10))
            data.dataset[start_index: stop_index, :] = i
            
# Reading requires same driver and memb_size
with h5py.File(name=filename_pattern, mode='r', driver='family', memb_size=chunk_size) as f:
    with NWBHDF5IO(file=f, mode='r') as io:
        nwbfile = io.read()
```

Notes on family driver:
- Filename must contain printf-style integer format code (e.g., '%d')
- Same memb_size parameter must be used for both reading and writing
- DANDI archive may not support NWB files split using this method