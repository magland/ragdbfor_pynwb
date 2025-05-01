# Intracellular Electrophysiology in NWB

NWB supports storage of intracellular electrophysiology data through a hierarchical structure of metadata tables and specialized TimeSeries classes.

## Core Components

### TimeSeries Classes
- **Stimulus Data**: `VoltageClampStimulusSeries` and `CurrentClampStimulusSeries`
- **Response Data**: `VoltageClampSeries`, `CurrentClampSeries`, and `IZeroClampSeries`

### Base Components
- `Device`: Represents recording hardware (e.g., amplifier)
- `IntracellularElectrode`: Represents the electrode used for recording

### Metadata Table Hierarchy
1. **IntracellularRecordingsTable**: Relates electrode, stimulus and response pairs
2. **SimultaneousRecordingsTable**: Groups recordings done simultaneously (sweeps)
3. **SequentialRecordingsTable**: Groups simultaneous recordings (sweep sequences)
4. **RepetitionsTable**: Groups sequential recordings (runs)
5. **ExperimentalConditionsTable**: Groups repetitions under the same conditions

## Basic Usage Example

```python
# Create device and electrode
device = nwbfile.create_device(name="Heka ITC-1600")
electrode = nwbfile.create_icephys_electrode(
    name="elec0", description="intracellular electrode", device=device
)

# Create stimulus and response
stimulus = VoltageClampStimulusSeries(
    name="stimulus", data=[1, 2, 3, 4, 5], starting_time=123.6,
    rate=10e3, electrode=electrode, gain=0.02
)
response = VoltageClampSeries(
    name="response", data=[0.1, 0.2, 0.3, 0.4, 0.5],
    conversion=1e-12, resolution=np.nan, starting_time=123.6,
    rate=20e3, electrode=electrode, gain=0.02,
    capacitance_slow=100e-12, resistance_comp_correction=70.0
)

# Add recording to hierarchical tables
ir_index = nwbfile.add_intracellular_recording(
    electrode=electrode, stimulus=stimulus, response=response
)

sweep_index = nwbfile.add_icephys_simultaneous_recording(recordings=[ir_index])

sequence_index = nwbfile.add_icephys_sequential_recording(
    simultaneous_recordings=[sweep_index], stimulus_type="square"
)

run_index = nwbfile.add_icephys_repetition(sequential_recordings=[sequence_index])

nwbfile.add_icephys_experimental_condition(repetitions=[run_index])
```

## Key Features

- **Optional Time Ranges**: Specify relevant time ranges using `_start_index` and `_index_count`
- **Partial Recordings**: Recordings can have just a stimulus or response
- **Custom Metadata**: Add custom columns to any table through `add_column()` method
- **Stimulus Templates**: Store idealized versions of stimuli in addition to recorded versions
- **Indexing and Referencing**: Tables reference each other by row indices (not IDs)

## Customization

```python
# Add custom column to IntracellularRecordingsTable
nwbfile.intracellular_recordings.add_column(
    name="recording_tag", data=["A1", "A2", "A3"],
    description="String with a recording tag"
)

# Add custom category to IntracellularRecordingsTable
location_column = VectorData(
    name="location", data=["Mordor", "Gondor", "Rohan"],
    description="Recording location in Middle Earth"
)
lab_category = DynamicTable(
    name="recording_lab_data",
    description="category table for lab-specific recording metadata",
    colnames=["location"], columns=[location_column]
)
nwbfile.intracellular_recordings.add_category(category=lab_category)
```

For analysis, tables can be easily converted to pandas DataFrames using the `to_dataframe()` method.