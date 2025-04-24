This document provides a tutorial on querying intracellular electrophysiology (ICEphys) metadata in NWB files using pandas. It uses the `pynwb.icephys` module.
**Key Concepts and Usage:**
*   **ICEphys Metadata Hierarchy:** The metadata is organized as a hierarchy of DynamicTables: `ExperimentalConditionsTable` -> `RepetitionsTable` -> `SequentialRecordingsTable` -> `SimultaneousRecordingsTable` -> `IntracellularRecordingsTable`. Not all tables may exist in a file.
*   **Accessing Tables:**
    *   `nwbfile.get_icephys_meta_parent_table()`: Returns the root table of the hierarchy.
    *   `nwbfile.intracellular_recordings`, `nwbfile.icephys_simultaneous_recordings`, etc.: Access specific tables via NWBFile properties. Returns `None` if the table doesn't exist. Use these properties instead of the `get_*` methods for retrieving tables.  The `get_*` methods create tables if they do not exist, and should be used when populating an NWBFile.
*   **Inspecting Table Relationships:**
    *   `table.has_foreign_columns()`: Checks if a table has foreign key columns.
    *   `table.get_foreign_columns()`: Returns the foreign key columns.
    *   `table.get_linked_tables()`: Returns a list of links defined from a table to other tables. Useful for understanding table relationships. Each link contains the *source_table*, *source_column*, and *target_table*.
*   **Converting to pandas DataFrames:**
    *   `table.to_dataframe(index=False)`: Converts a table to a pandas DataFrame. If `index=False` links to other tables are resolved, and the related rows are included as DataFrame objects.
    *   `table.to_dataframe(index=True)`: Converts a table to a pandas DataFrame, representing foreign key links as lists of row indices (integers). This avoids loading the linked tables into memory.
    *   `nwbfile.intracellular_recordings.to_dataframe(ignore_category_ids=True, electrode_refs_as_objectids=True, stimulus_refs_as_objectids=True, response_refs_as_objectids=True)`: Converts the IntracellularRecordingsTable to a pandas DataFrame with options for ignoring category IDs and converting references to ObjectIds.
*   **Hierarchical DataFrames:**
    *   `hdmf.common.hierarchicaltable.to_hierarchical_dataframe(root_table)`: Transforms the hierarchical tables into a single pandas DataFrame. The hierarchy is represented as a pandas MultiIndex on the rows.
    *   `hdmf.common.hierarchicaltable.drop_id_columns(dataframe, inplace=False)`: Removes "id" columns from a DataFrame.
    *   `hdmf.common.hierarchicaltable.flatten_column_index(dataframe, inplace=True)`: Flattens the MultiIndex on the columns of a DataFrame into a regular Index of tuples.
*   **Expanding TimeSeriesReference Columns:** The tutorial demonstrates how to expand TimeSeriesReference columns into separate columns for `start`, `count`, and `timeseries`.
*   **Adding Stimulus/Response Metadata:** It shows how to add columns with the names, neurodata types, gain, rates, starting times and object ids of the stimulus and response TimeSeries objects.
*   **Example Queries:**
    *   Given a response, get the stimulus.
    *   Given a response, load the associated data (using `TimeSeriesReference` object to get data, indices, timestamps).
    *   Get a list of all stimulus types.
    *   Given a stimulus type, get all corresponding intracellular recordings.
*   **Accessing TimeSeries Data:** Use `TimeSeriesReference` objects to access data.
    *   `ref = icephys_meta_df[("responses", "response")][0]` Get the TimeSeriesReference
    *   `ref.isvalid()`
    *   `ref.idx_start`
    *   `ref.count`
    *   `ref.timeseries.name`
    *   `ref.timestamps`
    *   `ref.data`

**Example Setup:**

```python
from pynwb.testing.icephys_testutils import create_icephys_testfile

test_filename = "icephys_pandas_testfile.nwb"
nwbfile = create_icephys_testfile(
    filename=test_filename,  # Write the file to disk for testing
    add_custom_columns=True,  # Add a custom column to each metadata table
    randomize_data=True,  # Randomize the data in the simulus and response
    with_missing_stimulus=True,  # Don't include the stimulus for row 0 and 10
)
```
