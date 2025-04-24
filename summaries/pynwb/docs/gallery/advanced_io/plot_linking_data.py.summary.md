PyNWB supports modular data storage using external links to integrate data from multiple files. This is useful when recording multiple data streams during data acquisition and saving each stream to a separate HDF5 file, which can then be linked into a single NWB file. The same approach works for other NWBContainers as well, e.g. TimeSeries.

**Creating external links:**

External links point to data in other files and can become invalid if the files are modified.

**Example:** Creating two TimeSeries in separate files and linking them into a single NWBFile.

1.  **Create test data:**
    *   Create two NWBFiles, `nwbfile1` and `nwbfile2`.
    *   Add a TimeSeries (`test_ts1` and `test_ts2`) to each file with sample data and timestamps.
    *   Write each NWBFile to a separate file (`external1_example.nwb` and `external2_example.nwb`).

2.  **Linking to select datasets:**
    *   Create a new NWBFile (`nwbfile4`).
    *   Open the first file (`external1_example.nwb`) and retrieve the `test_timeseries1` TimeSeries.
    *   Access the timeseries data with `timeseries_1.data`.
    *   Create a new TimeSeries (`test_ts4`) in `nwbfile4` and assign the data from `timeseries_1.data` and timestamps.
    *   Alternatively, use `H5DataIO` to explicitly specify linking:

        ```python
        from hdmf.backends.hdf5.h5_utils import H5DataIO

        test_ts5 = TimeSeries(
            name="test_timeseries5",
            data=H5DataIO(data=timeseries_1_data, link_data=True),
            unit="SIunit",
            timestamps=timestamps,
        )
        nwbfile4.add_acquisition(test_ts5)
        ```

    *   Write the new NWBFile (`nwbfile4`) to a file (`external_linkdataset_example.nwb`) using `link_data=True` in `io.write` to link the data instead of copying it.

3.  **Linking to whole containers:**
    *   Use `get_manager()` to manage linking. This allows the backend to automatically detect that the TimeSeries have already been written to another file and will create external links for us.
    *   Open the first two files (`external1_example.nwb` and `external2_example.nwb`) and retrieve the TimeSeries objects (`test_timeseries1` and `test_timeseries2`) with manager passed into `NWBHDF5IO`.
    *   Create a new NWBFile (`nwbfile3`).
    *   Add the existing TimeSeries objects to the new NWBFile.

        ```python
        from pynwb import get_manager

        manager = get_manager()

        io1 = NWBHDF5IO(filename1, "r", manager=manager)
        nwbfile1 = io1.read()
        timeseries_1 = nwbfile1.get_acquisition("test_timeseries1")

        io2 = NWBHDF5IO(filename2, "r", manager=manager)
        nwbfile2 = io2.read()
        timeseries_2 = nwbfile2.get_acquisition("test_timeseries2")

        nwbfile3 = NWBFile(
            session_description="demonstrate external files",
            identifier=str(uuid4()),
            session_start_time=start_time,
        )
        nwbfile3.add_acquisition(timeseries_1)
        nwbfile3.add_acquisition(timeseries_2)

        with NWBHDF5IO(filename3, "w", manager=manager) as io3:
            io3.write(nwbfile3)
        io1.close()
        io2.close()
        ```

    *   Write the new NWBFile (`nwbfile3`) to a file (`external_linkcontainer_example.nwb`).  The two timeseries would be linked instead of copied.

**Copying an NWBFile for linking:**

The `NWBFile.copy()` method creates a shallow copy of an NWBFile with links to the original data.

**Creating a single file for sharing:**

The `HDF5IO.export()` method copies a file and resolves all external links, creating a single file with all the data.

**Automatically splitting large data across multiple HDF5 files:**

Use the `family` driver in `h5py` to split an NWB file into multiple files.

1.  Create the NWBFile as usual, using `H5DataIO` and `maxshape` to define an expandable dataset so that additional data can be written iteratively later on.
2.  Open the file with `h5py` using the `family` driver, specifying the `memb_size` (chunk size) of the individual files.  The filename must include a printf-style integer format code (e.g. `%d`).
3. Use `NWBHDF5IO` to write to the h5py file object.
4.  Optionally, write data iteratively. For example:

```python
import h5py
from pynwb import  NWBHDF5IO

chunk_size = 1024**2  # 1MB just for testing
filename_pattern = 'family_nwb_file_%d.nwb'

with h5py.File(name=filename_pattern, mode='w', driver='family', memb_size=chunk_size) as f:
    with NWBHDF5IO(file=f, mode='w') as io:
        io.write(nwbfile)

        for i in range(10):
            start_index = i * 1000
            stop_index = start_index + 1000
            data.dataset.resize((stop_index, 10))
            data.dataset[start_index: stop_index , :] = i
```
5.  To read a file written with the family driver, open the file with `h5py` using the `family` driver and the same `memb_size` and then use `NWBHDF5IO` to read data normally.

