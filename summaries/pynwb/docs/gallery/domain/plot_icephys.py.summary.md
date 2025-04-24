This document describes how to store intracellular electrophysiology data in NWB using pynwb. It covers the representation of stimuli and responses, electrode and device metadata, and the organization of experimental metadata in hierarchical tables.

**Key Concepts:**

*   **PatchClampSeries:** Base class for representing intracellular stimulus and response data.
*   **IntracellularElectrode:** Represents an intracellular electrode.
*   **Device:** Represents the device used for recording.
*   **Metadata Tables:** Organize experimental metadata hierarchically to avoid duplication.

**Metadata Table Hierarchy:**

1.  **IntracellularRecordingsTable:** Relates electrode, stimulus, and response pairs.
2.  **SimultaneousRecordingsTable:** Groups intracellular recordings recorded simultaneously (sweeps).
3.  **SequentialRecordingsTable:** Groups simultaneous recordings (sweep sequences).
4.  **RepetitionsTable:** Groups sequential recordings (runs).
5.  **ExperimentalConditionsTable:** Groups repetitions belonging to the same experimental conditions.

**Usage Examples:**

*   **Creating an NWBFile:**

    ```python
    from pynwb import NWBFile
    from datetime import datetime
    from dateutil.tz import tzlocal
    from uuid import uuid4

    nwbfile = NWBFile(
        session_description="my first synthetic recording",
        identifier=str(uuid4()),
        session_start_time=datetime.now(tzlocal()),
        experimenter=["Baggins, Bilbo"],
        lab="Bag End Laboratory",
        institution="University of Middle Earth at the Shire",
        experiment_description="I went on an adventure to reclaim vast treasures.",
        session_id="LONELYMTN001",
    )
    ```

*   **Creating a Device:**

    ```python
    device = nwbfile.create_device(name="Heka ITC-1600")
    ```

*   **Creating an Intracellular Electrode:**

    ```python
    electrode = nwbfile.create_icephys_electrode(
        name="elec0", description="a mock intracellular electrode", device=device
    )
    ```

*   **Creating Stimulus and Response Data:**

    ```python
    from pynwb.icephys import VoltageClampStimulusSeries, VoltageClampSeries, CurrentClampSeries, CurrentClampStimulusSeries, IZeroClampSeries
    import numpy as np

    stimulus = VoltageClampStimulusSeries(
        name="ccss",
        data=[1, 2, 3, 4, 5],
        starting_time=123.6,
        rate=10e3,
        electrode=electrode,
        gain=0.02,
        sweep_number=np.uint64(15),
    )

    response = VoltageClampSeries(
        name="vcs",
        data=[0.1, 0.2, 0.3, 0.4, 0.5],
        conversion=1e-12,
        resolution=np.nan,
        starting_time=123.6,
        rate=20e3,
        electrode=electrode,
        gain=0.02,
        capacitance_slow=100e-12,
        resistance_comp_correction=70.0,
        sweep_number=np.uint64(15),
    )

    ccs = CurrentClampSeries(
        name="ccs",
        data=[0.1, 0.2, 0.3, 0.4, 0.5],
        conversion=1e-12,
        resolution=np.nan,
        starting_time=123.6,
        rate=20e3,
        electrode=electrode,
        gain=0.02,
        bias_current=1e-12,
        bridge_balance=70e6,
        capacitance_compensation=1e-12,
        sweep_number=np.uint(16)
    )

    ccss = CurrentClampStimulusSeries(
        name="ccss",
        data=[1, 2, 3, 4, 5],
        starting_time=123.6,
        rate=10e3,
        electrode=electrode,
        gain=0.02,
        sweep_number=np.uint(16),
    )

    # IZeroClampSeries is used when the current is clamped to 0.
    izcs = IZeroClampSeries(
        name="izcs",
        data=[0.1, 0.2, 0.3, 0.4, 0.5],
        electrode=electrode,
        gain=0.02,
        resolution=np.nan,
        conversion=1e-12,
        starting_time=345.6,
        rate=20e3,
        sweep_number=np.uint(17),
    )

    ```

*   **Adding an Intracellular Recording:**

    ```python
    rowindex = nwbfile.add_intracellular_recording(
        electrode=electrode, stimulus=stimulus, response=response, id=10
    )
    ```

*   **Adding a Simultaneous Recording:**

    ```python
    rowindex = nwbfile.add_icephys_simultaneous_recording(
        recordings=[rowindex, rowindex2, rowindex3],
        id=12,
        simultaneous_recording_tag="LabTag1",
    )
    ```

*   **Adding a Sequential Recording:**

    ```python
    rowindex = nwbfile.add_icephys_sequential_recording(
        simultaneous_recordings=[0], stimulus_type="square", id=15
    )
    ```

*   **Adding a Repetition:**

    ```python
    rowindex = nwbfile.add_icephys_repetition(sequential_recordings=[0], id=17)
    ```

*   **Adding an Experimental Condition:**

    ```python
    rowindex = nwbfile.add_icephys_experimental_condition(repetitions=[0], id=19)
    ```

*   **Adding Custom Columns to Tables:**

    ```python
    nwbfile.intracellular_recordings.add_column(
        name="recording_tag",
        data=["A1", "A2", "A3"],
        description="String with a recording tag",
    )
    ```

*   **Adding a Category to the IntracellularRecordingsTable:**

    ```python
    from pynwb.core import DynamicTable, VectorData

    location_column = VectorData(
        name="location",
        data=["Mordor", "Gondor", "Rohan"],
        description="Recording location in Middle Earth",
    )

    lab_category = DynamicTable(
        name="recording_lab_data",
        description="category table for lab-specific recording metadata",
        colnames=["location"],
        columns=[location_column],
    )
    nwbfile.intracellular_recordings.add_category(category=lab_category)
    ```

*   **Adding a column to a subcategory table:**

    ```python
       nwbfile.intracellular_recordings.add_column(
            name="voltage_threshold",
            data=[0.1, 0.12, 0.13],
            description="Just an example column on the electrodes category table",
            category="electrodes",
        )
    ```

*   **Adding a stimulus template:**
   ```python
   from pynwb.core import TimeSeriesReference
   from pynwb.base import TimeSeriesReferenceVectorData

    stimulus_template = VoltageClampStimulusSeries(
        name="ccst",
        data=[0, 1, 2, 3, 4],
        starting_time=0.0,
        rate=10e3,
        electrode=electrode,
        gain=0.02,
    )
    nwbfile.add_stimulus_template(stimulus_template)

    nwbfile.intracellular_recordings.add_column(
        name="stimulus_template",
        data=[TimeSeriesReference(0, 5, stimulus_template),  # (start_index, index_count, stimulus_template)
            TimeSeriesReference(1, 3, stimulus_template),
            TimeSeriesReference.empty(stimulus_template)],  # if there was no data for that recording, use empty reference
        description="Column storing the reference to the stimulus template for the recording (rows).",
        category="stimuli",
        col_cls=TimeSeriesReferenceVectorData
    )
   ```

*   **Writing and Reading an NWBFile:**

    ```python
    from pynwb import NWBHDF5IO

    testpath = "test_icephys_file.nwb"
    with NWBHDF5IO(testpath, "w") as io:
        io.write(nwbfile)

    with NWBHDF5IO(testpath, "r") as io:
        infile = io.read()
    ```

*   **Accessing the tables:**

    ```python
    import pandas as pd
    pd.set_option("display.max_columns", 6)
    nwbfile.intracellular_recordings.to_dataframe()
    nwbfile.icephys_simultaneous_recordings.to_dataframe()
    nwbfile.icephys_sequential_recordings.to_dataframe()
    nwbfile.icephys_repetitions.to_dataframe()
    nwbfile.icephys_experimental_conditions.to_dataframe()
    ```

*   **Important Notes:**
    *   All metadata tables are optional and automatically created when data is added.
    *   Higher-level tables link to lower-level tables; tables cannot be excluded from the top down.
    *   `add_intracellular_recording` can automatically add electrode, stimulus and/or response objects to the NWBFile.
    *   Ids must be unique within the IntracellularRecordings, SimultaneousRecordings, SequentialRecordingsTable, RepetitionsTable and ExperimentalConditionsTable tables.
    *   Time ranges for stimulus and/or response can be specified using `stimulus_start_index`, `stimulus_index_count`, `response_start_index`, and `response_index_count`.
    *   Row indices are used for referencing between tables, not the ids.
