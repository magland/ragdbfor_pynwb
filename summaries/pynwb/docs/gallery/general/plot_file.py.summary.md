This document provides a basic introduction to working with NWB files using PyNWB, covering the creation, reading, and appending operations.

**Core Concepts:**

*   **NWBFile:** Represents a single experimental session. Requires `session_description`, `identifier` (UUID), and `session_start_time`. Stores timeseries datasets, modules, and metadata.
*   **TimeSeries:** Stores time series data with `data`, `timestamps` (or `rate` and `starting_time`), `name`, and `unit`.  Subtypes include `ElectricalSeries`, `SpikeEventSeries`, `PatchClampSeries`, `ImageSeries`, `OpticalSeries`, `SpatialSeries`, `AnnotationSeries` and others. Can be added to an NWBFile using `add_acquisition`, `add_stimulus`, or `add_stimulus_template`.
*   **Processing Modules:** Group analyses. Created using `nwbfile.create_processing_module(name, description)`. Standard module names are "behavior", "ecephys", "icephys", "ophys", "ogen", and "misc".
*   **Subject:** Stores information about the experimental subject, including `age`, `species`, `genotype`, `sex`, and `description`. Added to the NWBFile via `nwbfile.subject = subject`.
*   **TimeIntervals:** Stores tabular metadata like trials, electrodes and sorted units.

**Usage Examples:**

1.  **Creating an NWBFile:**

    ```python
    from datetime import datetime
    from uuid import uuid4
    from dateutil import tz
    from pynwb import NWBFile

    session_start_time = datetime(2018, 4, 25, 2, 30, 3, tzinfo=tz.gettz("US/Pacific"))
    nwbfile = NWBFile(
        session_description="Mouse exploring an open field",
        identifier=str(uuid4()),
        session_start_time=session_start_time,
        session_id="session_1234",
        experimenter=["Baggins, Bilbo"],
        lab="Bag End Laboratory",
        institution="University of Middle Earth at the Shire",
        experiment_description="I went on an adventure to reclaim vast treasures.",
        keywords=["behavior", "exploration", "wanderlust"],
        related_publications="doi:10.1016/j.neuron.2016.12.011",
    )
    ```

2.  **Adding a Subject:**

    ```python
    from pynwb.file import Subject

    subject = Subject(
        subject_id="001",
        age="P90D",
        description="mouse 5",
        species="Mus musculus",
        sex="M",
    )
    nwbfile.subject = subject
    ```

3.  **Creating and Adding a TimeSeries:**

    ```python
    import numpy as np
    from pynwb import TimeSeries

    data = np.arange(100, 200, 10)
    time_series_with_timestamps = TimeSeries(
        name="test_timeseries",
        description="an example time series",
        data=data,
        unit="m",
        timestamps=np.arange(10.),
    )
    nwbfile.add_acquisition(time_series_with_timestamps)
    ```
4.  **Creating and Adding an AnnotationSeries:**
    ```python
    from pynwb.misc import AnnotationSeries

    annotations = AnnotationSeries(
    name='airpuffs',
    data=['Left Airpuff', 'Right Airpuff', 'Right Airpuff'],
    description='Airpuff events delivered to the animal',
    timestamps=[1.0, 3.0, 8.0],
    )

    nwbfile.add_stimulus(annotations)
    ```

5.  **Creating and Adding SpatialSeries in Behavior Processing Module:**

    ```python
    from pynwb.behavior import SpatialSeries, Position
    # create fake data with shape (50, 2)
    position_data = np.array([np.linspace(0, 10, 50), np.linspace(0, 8, 50)]).T
    position_timestamps = np.linspace(0, 50).astype(float) / 200

    spatial_series_obj = SpatialSeries(
        name="SpatialSeries",
        description="(x,y) position in open field",
        data=position_data,
        timestamps=position_timestamps,
        reference_frame="(0,0) is bottom left corner",
    )
    position_obj = Position(spatial_series=spatial_series_obj)

    behavior_module = nwbfile.create_processing_module(
        name="behavior", description="processed behavioral data"
    )
    behavior_module.add(position_obj)
    ```

6.  **Adding Trials:**

    ```python
    nwbfile.add_trial_column(
        name="correct",
        description="whether the trial was correct",
    )
    nwbfile.add_trial(start_time=1.0, stop_time=5.0, correct=True)
    nwbfile.add_trial(start_time=6.0, stop_time=10.0, correct=False)
    ```

7.  **Writing an NWBFile:**

    ```python
    from pynwb import NWBHDF5IO

    io = NWBHDF5IO("basics_tutorial.nwb", mode="w")
    io.write(nwbfile)
    io.close()

    # Or using a context manager:
    with NWBHDF5IO("basics_tutorial.nwb", "w") as io:
        io.write(nwbfile)
    ```

8.  **Reading an NWBFile:**

    ```python
    from pynwb import NWBHDF5IO

    with NWBHDF5IO("basics_tutorial.nwb", "r") as io:
        read_nwbfile = io.read()
        print(read_nwbfile.acquisition["test_timeseries"])
        print(read_nwbfile.acquisition["test_timeseries"].data[:]) #Read data from TimeSeries
        print(read_nwbfile.processing["behavior"]) #Accessing processing module
        print(read_nwbfile.processing["behavior"]["Position"]) #Accessing Position
        print(read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"]) #Accessing SpatialSeries
    ```

9.  **Appending to an NWBFile:**

    ```python
    from pynwb import NWBHDF5IO, TimeSeries
    import numpy as np

    io = NWBHDF5IO("basics_tutorial.nwb", mode="a")
    nwbfile = io.read()

    data = np.arange(100, 200, 10)
    timestamps = np.arange(10.)
    new_time_series = TimeSeries(
        name="new_time_series",
        description="a new time series",
        data=data,
        timestamps=timestamps,
        unit="n.a.",
    )
    nwbfile.add_acquisition(new_time_series)

    io.write(nwbfile)
    io.close()
    ```

**Important Notes:**

*   Use keyword arguments when creating NWBFile objects.
*   `NWBHDF5IO` is used for reading and writing NWB files.
*   Data is read passively from the file and is only loaded into memory when requested (e.g., using `[:]` operator or slicing).
*   NWB only supports appending to files; removal or modification of existing data is not allowed.
