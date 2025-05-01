# PyNWB ICEphys Metadata Querying Tutorial

This tutorial demonstrates how to use pandas to query experiment metadata for intracellular electrophysiology (ICEphys) experiments using PyNWB.

## ICEphys Metadata Tables Structure

The ICEphys metadata in NWBFiles consists of a hierarchy of DynamicTables:
- ExperimentalConditionsTable
- RepetitionsTable
- SequentialRecordingsTable
- SimultaneousRecordingsTable
- IntracellularRecordingsTable

Not all tables may exist in a given NWBFile - users might exclude tables from the top of the hierarchy.

## Accessing ICEphys Metadata Tables

### Get the parent table
```python
root_table = nwbfile.get_icephys_meta_parent_table()
```

### Get specific ICEphys tables
Access tables via NWBFile properties:
```python
# Check if a table exists
nwbfile.icephys_sequential_recordings is not None

# Access tables with properties
nwbfile.intracellular_recordings
nwbfile.icephys_simultaneous_recordings
nwbfile.icephys_sequential_recordings
nwbfile.icephys_repetitions
nwbfile.icephys_experimental_conditions
```

⚠️ Use properties rather than get methods to just retrieve tables. Get methods can automatically add missing tables.

### Inspect table hierarchy
```python
# Check for foreign columns
root_table.has_foreign_columns()
root_table.get_foreign_columns()

# Get linked tables
linked_tables = root_table.get_linked_tables()
```

## Converting ICEphys Metadata to Pandas DataFrames

### Using Nested DataFrames
```python
# Convert table to DataFrame with nested references resolved
exp_cond_df = root_table.to_dataframe()

# Special options for IntracellularRecordingsTable
ir_df = nwbfile.intracellular_recordings.to_dataframe(
    ignore_category_ids=True,
    electrode_refs_as_objectids=True,
    stimulus_refs_as_objectids=True,
    response_refs_as_objectids=True,
)
```

### Using Indexed DataFrames
```python
# Convert to DataFrame without resolving references
root_table.to_dataframe(index=True)

# Access specific rows from related tables
root_table["repetitions"][0]  # Look up repetitions for first condition

# Follow table links manually
target_table = root_table["repetitions"].target.table
target_table[[0, 1]]
```

### Creating a Single Hierarchical DataFrame
```python
from hdmf.common.hierarchicaltable import to_hierarchical_dataframe

# Create a single DataFrame from the hierarchical tables
icephys_meta_df = to_hierarchical_dataframe(root_table)

# Additional processing to make the DataFrame more useful
from hdmf.common.hierarchicaltable import drop_id_columns, flatten_column_index

# Reset index to turn MultiIndex into columns
icephys_meta_df.reset_index(inplace=True)

# Flatten column structure
flatten_column_index(dataframe=icephys_meta_df, max_levels=2, inplace=True)

# Remove ID columns for better visualization
drid_icephys_meta_df = drop_id_columns(dataframe=icephys_meta_df, inplace=False)
```

## Data Preparation Techniques

### Expanding TimeSeriesReference columns
```python
# Expand stimulus references to separate columns
stimulus_df = pandas.DataFrame(
    icephys_meta_df[("stimuli", "stimulus")].tolist(),
    columns=[("stimuli", "idx_start"), ("stimuli", "count"), ("stimuli", "timeseries")],
    index=icephys_meta_df.index,
)
icephys_meta_df = pandas.concat([icephys_meta_df, stimulus_df], axis=1)

# Add columns with TimeSeries metadata
col = ("stimuli", "name")
icephys_meta_df[col] = [getattr(s, "name", None) for s in icephys_meta_df[("stimuli", "timeseries")]]

# Add multiple fields in bulk
for field in ["neurodata_type", "gain", "rate", "starting_time", "object_id"]:
    col = ("stimuli", field)
    icephys_meta_df[col] = [getattr(s, field, None) for s in icephys_meta_df[("stimuli", "timeseries")]]
```

## Common Metadata Queries

### Get stimulus for a response
```python
response = nwbfile.get_acquisition("vcs_9")
icephys_meta_df[icephys_meta_df[("responses", "object_id")] == response.object_id]
```

### Load data from a TimeSeriesReference
```python
ref = icephys_meta_df[("responses", "response")][0]
ref_data = ref.data  # Get the selected response data values
ref.timestamps  # Get timestamps
```

### Get all unique stimulus types
```python
unique_stimulus_types = np.unique(icephys_meta_df[("sequential_recordings", "stimulus_type")])
```

### Get all recordings for a stimulus type
```python
query_res_df = icephys_meta_df[
    icephys_meta_df[("sequential_recordings", "stimulus_type")] == "StimType_1"
]
```