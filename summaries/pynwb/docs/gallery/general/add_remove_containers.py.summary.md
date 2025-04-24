This document explains how to add and remove containers (e.g., TimeSeries) from an existing NWB file using pynwb.

**Adding Objects to an NWB File (Read/Write Mode):**

1.  Open the NWB file with `NWBHDF5IO` in read/write mode (`mode='r+'` or `mode='a'`).
2.  Read the `NWBFile` object.
3.  Add container objects (e.g., `TimeSeries`) to the `NWBFile` object using methods like `add_acquisition()`.
4.  Write the modified `NWBFile` back to the same file using the same `NWBHDF5IO` object.

```python
import datetime
import numpy as np
from pynwb import NWBHDF5IO, NWBFile, TimeSeries

# Create and write a test NWB file
nwbfile = NWBFile(session_description="test", identifier="NWB123", session_start_time=datetime.datetime.now(datetime.timezone.utc))
filename = "nwbfile.nwb"
with NWBHDF5IO(filename, "w") as io:
    io.write(nwbfile)

# Open the NWB file in r+ mode
with NWBHDF5IO(filename, "r+") as io:
    read_nwbfile = io.read()

    # Create a TimeSeries and add it to the file under the acquisition group
    data = list(range(100, 200, 10))
    timestamps = np.arange(10, dtype=float)
    test_ts = TimeSeries(name="test_timeseries", data=data, unit="m", timestamps=timestamps)
    read_nwbfile.add_acquisition(test_ts)

    # Write the modified NWB file
    io.write(read_nwbfile)
```

**Limitations:**

*   The destination file path must be the same as the source file path.
*   It is not possible to **remove** objects from an NWB file using *only* this method.

**Exporting to a New File Path:**

Use `NWBHDF5IO.export()` to read data, modify it (additions or removals), and write it to a new file.

*   Removals are done using `LabelledDict.pop()` on containers like `NWBFile.acquisition`, `NWBFile.processing` and within processing modules via `NWBFile.processing["module_name"].data_interfaces.pop()`.
*   Other attributes on which pop can be called are: `NWBFile.analysis`, `NWBFile.processing`, `NWBFile.scratch`, `NWBFile.devices`, `NWBFile.stimulus`, `NWBFile.stimulus_template`, `NWBFile.electrode_groups`, `NWBFile.imaging_planes`, `NWBFile.icephys_electrodes`, `NWBFile.ogen_sites`, and `NWBFile.lab_meta_data`

```python
# Create and write a test NWB file with a TimeSeries in the acquisition group and behavior processing module
nwbfile = NWBFile(session_description="test", identifier="NWB123", session_start_time=datetime.datetime.now(datetime.timezone.utc))
data1 = list(range(100, 200, 10))
timestamps1 = np.arange(10, dtype=float)
test_ts1 = TimeSeries(name="test_timeseries1", data=data1, unit="m", timestamps=timestamps1)
nwbfile.add_acquisition(test_ts1)

# Create a processing module for processed behavioral data
nwbfile.create_processing_module(name="behavior", description="processed behavioral data")
data2 = list(range(100, 200, 10))
timestamps2 = np.arange(10, dtype=float)
test_ts2 = TimeSeries(name="test_timeseries2", data=data2, unit="m", timestamps=timestamps2)
nwbfile.processing["behavior"].add(test_ts2)

filename = "nwbfile.nwb"
with NWBHDF5IO(filename, "w") as io:
    io.write(nwbfile)
# Read the written file
export_filename = "exported_nwbfile.nwb"
with NWBHDF5IO(filename, mode="r") as read_io:
    read_nwbfile = read_io.read()

    # Add a new TimeSeries to the behavior processing module
    data3 = list(range(100, 200, 10))
    timestamps3 = np.arange(10, dtype=float)
    test_ts3 = TimeSeries(name="test_timeseries3", data=data3, unit="m", timestamps=timestamps3)
    read_nwbfile.processing["behavior"].add(test_ts3)

    # Use the pop method to remove the original TimeSeries from the acquisition group
    read_nwbfile.acquisition.pop("test_timeseries1")

    # Use the pop method to remove a TimeSeries from a processing module
    read_nwbfile.processing["behavior"].data_interfaces.pop("test_timeseries2")

    # Export to a new file
    with NWBHDF5IO(export_filename, mode="w") as export_io:
        export_io.export(src_io=read_io, nwbfile=read_nwbfile)
```

**Important Notes:**

*   `TimeIntervals` objects (e.g., `NWBFile.epochs`, `NWBFile.trials`) cannot be removed from `NWBFile.intervals` using `pop()`.
*   Removing objects can break links and references. Use caution when removing heavily referenced items like `Device`, `ElectrodeGroup`, electrodes table, and `PlaneSegmentation` table.

**Exporting with New Object IDs:**

To generate new object IDs in the exported file, call `AbstractContainer.generate_new_id()` on the `NWBFile` object *before* exporting.  This will regenerate the object IDs for the root NWBFile object and all sub-objects contained within it.

```python
export_filename = "exported_nwbfile.nwb"
with NWBHDF5IO(filename, mode="r") as read_io:
    read_nwbfile = read_io.read()
    read_nwbfile.generate_new_id()

    with NWBHDF5IO(export_filename, mode="w") as export_io:
        export_io.export(src_io=read_io, nwbfile=read_nwbfile)
```
