# Adding/Removing Containers in PyNWB

## Adding Objects to an NWB File (Read/Write Mode)

PyNWB supports adding container objects to existing NWB files. The process is:

1. Open the file with `NWBHDF5IO` in read/write mode (`mode='r+'` or `mode='a'`)
2. Read the `NWBFile`
3. Add container objects to the `NWBFile`
4. Write the modified `NWBFile` using the same `NWBHDF5IO` object

```python
with NWBHDF5IO(filename, "r+") as io:
    read_nwbfile = io.read()
    
    # Create and add a TimeSeries
    test_ts = TimeSeries(
        name="test_timeseries", 
        data=data, 
        unit="m", 
        timestamps=timestamps
    )
    read_nwbfile.add_acquisition(test_ts)
    
    # Write the modified NWBFile
    io.write(read_nwbfile)
```

**Note**: This method cannot remove objects from an NWB file.

## Exporting to a New File Path

Use the `NWBHDF5IO.export` method to read data from an existing NWB file, modify it (add or remove objects), and write to a new file path.

To remove containers, use the `pop` method on any `LabelledDict` object:
- `NWBFile.acquisition`
- `NWBFile.processing` 
- `NWBFile.analysis`
- `NWBFile.scratch`
- `NWBFile.devices`
- `NWBFile.stimulus`
- `NWBFile.stimulus_template`
- And others like `electrode_groups`, `imaging_planes`, etc.

Example of removing and adding objects:

```python
with NWBHDF5IO(filename, mode="r") as read_io:
    read_nwbfile = read_io.read()

    # Add a new TimeSeries
    test_ts3 = TimeSeries(
        name="test_timeseries3", 
        data=data3,
        unit="m", 
        timestamps=timestamps3
    )
    read_nwbfile.processing["behavior"].add(test_ts3)

    # Remove TimeSeries from acquisition
    read_nwbfile.acquisition.pop("test_timeseries1")

    # Remove TimeSeries from processing module
    read_nwbfile.processing["behavior"].data_interfaces.pop("test_timeseries2")

    # Export to new file
    with NWBHDF5IO(export_filename, mode="w") as export_io:
        export_io.export(src_io=read_io, nwbfile=read_nwbfile)
```

**Note**: `TimeIntervals` objects (like `NWBFile.epochs`, `NWBFile.trials`) cannot be removed from `NWBFile.intervals`.

**Warning**: Removing objects may break links and references within the file and across files.

## Exporting with New Object IDs

To generate new object IDs when exporting (rather than copying the IDs from the original file):

```python
with NWBHDF5IO(filename, mode="r") as read_io:
    read_nwbfile = read_io.read()
    read_nwbfile.generate_new_id()  # Generate new IDs for all objects
    
    with NWBHDF5IO(export_filename, mode="w") as export_io:
        export_io.export(src_io=read_io, nwbfile=read_nwbfile)
```