This document is a tutorial on how to store behavioral data in an NWB file using the `pynwb.behavior` module. The general workflow involves creating objects for time series, spatial data, or time intervals, storing them inside a behavior interface object (e.g., `Position`, `CompassDirection`, `BehavioralTimeSeries`, `BehavioralEvents`, `BehavioralEpochs`, `PupilTracking`, `EyeTracking`), and then adding these interface objects to a behavior processing module within the NWB file.

**Key Classes and Their Usage:**

*   **`SpatialSeries`**: Represents data in space, like position or direction over time. Subclass of `TimeSeries`.

    ```python
    position_data = np.array([np.linspace(0, 10, 50), np.linspace(0, 8, 50)]).T
    timestamps = np.linspace(0, 50) / 200
    position_spatial_series = SpatialSeries(
        name="SpatialSeries",
        description="Position (x, y) in an open field.",
        data=position_data,
        timestamps=timestamps,
        reference_frame="(0,0) is bottom left corner",
    )
    ```

*   **`Position`**: Stores position data measured over time. Holds one or more `SpatialSeries` objects.

    ```python
    position = Position(spatial_series=position_spatial_series)
    ```

*   **`CompassDirection`**:  Stores view angle data measured over time, using `SpatialSeries`.

    ```python
    view_angle_data = np.linspace(0, 4, 50)
    direction_spatial_series = SpatialSeries(
        name="SpatialSeries",
        description="View angle of the subject measured in radians.",
        data=view_angle_data,
        timestamps=timestamps,
        reference_frame="straight ahead",
        unit="radians",
    )
    direction = CompassDirection(
        spatial_series=direction_spatial_series, name="CompassDirection"
    )
    ```

*   **`BehavioralTimeSeries`**: Stores continuous behavior data, such as speed.

    ```python
    speed_data = np.linspace(0, 0.4, 50)
    speed_time_series = TimeSeries(
        name="speed",
        data=speed_data,
        timestamps=timestamps,
        description="The speed of the subject measured over time.",
        unit="m/s",
    )
    behavioral_time_series = BehavioralTimeSeries(
        time_series=speed_time_series,
        name="BehavioralTimeSeries",
    )
    ```

*   **`BehavioralEvents`**: Stores behavioral events, like reward times and amounts.

    ```python
    reward_amount = [1.0, 1.5, 1.0, 1.5]
    events_timestamps = [1.0, 2.0, 5.0, 6.0]
    time_series = TimeSeries(
        name="lever_presses",
        data=reward_amount,
        timestamps=events_timestamps,
        description="The water amount the subject received as a reward.",
        unit="ml",
    )
    behavioral_events = BehavioralEvents(time_series=time_series, name="BehavioralEvents")
    ```

*   **`BehavioralEpochs`**: Stores intervals of behavior data, like running or sleeping intervals using `IntervalSeries`. Consider using `TimeIntervals` instead.

    ```python
    run_intervals = IntervalSeries(
        name="running",
        description="Intervals when the animal was running.",
        data=[1, -1, 1, -1, 1, -1],
        timestamps=[0.5, 1.5, 3.5, 4.0, 7.0, 7.3],
    )
    behavioral_epochs = BehavioralEpochs(name="BehavioralEpochs")
    behavioral_epochs.add_interval_series(run_intervals)

    sleep_intervals = IntervalSeries(
        name="sleeping",
        description="Intervals when the animal was sleeping.",
        data=[1, -1, 1, -1],
        timestamps=[15.0, 30.0, 60.0, 95.0],
    )
    behavioral_epochs.add_interval_series(sleep_intervals)
    ```

*   **`TimeIntervals`**: Represents time intervals with more flexibility using a DynamicTable, allowing for custom columns. Often preferred over `BehavioralEpochs` and `IntervalSeries`.

    ```python
    sleep_intervals = TimeIntervals(
        name="sleep_intervals",
        description="Intervals when the animal was sleeping.",
    )
    sleep_intervals.add_column(name="stage", description="The stage of sleep.")
    sleep_intervals.add_row(start_time=0.3, stop_time=0.35, stage=1)
    sleep_intervals.add_row(start_time=0.7, stop_time=0.9, stage=2)
    sleep_intervals.add_row(start_time=1.3, stop_time=3.0, stage=3)

    nwbfile.add_time_intervals(sleep_intervals)
    ```

*   **`PupilTracking`**: Stores eye-tracking data representing pupil size, holding `TimeSeries` objects for pupil features.

    ```python
    pupil_diameter = TimeSeries(
        name="pupil_diameter",
        description="Pupil diameter extracted from the video of the right eye.",
        data=np.linspace(0.001, 0.002, 50),
        timestamps=timestamps,
        unit="meters",
    )

    pupil_tracking = PupilTracking(time_series=pupil_diameter, name="PupilTracking")
    ```

*   **`EyeTracking`**: Stores eye-tracking data representing gaze direction, consisting of `SpatialSeries` objects for gaze positions.

    ```python
    right_eye_position = np.linspace(-20, 30, 50)
    right_eye_positions = SpatialSeries(
        name="right_eye_position",
        description="The position of the right eye measured in degrees.",
        data=right_eye_position,
        timestamps=timestamps,
        reference_frame="bottom left",
        unit="degrees",
    )

    eye_tracking = EyeTracking(name="EyeTracking", spatial_series=right_eye_positions)

    left_eye_position = np.linspace(-2, 20, 50)
    left_eye_positions = SpatialSeries(
        name="left_eye_position",
        description="The position of the left eye measured in degrees.",
        data=left_eye_position,
        timestamps=timestamps,
        reference_frame="bottom left",
        unit="degrees",
    )
    eye_tracking.add_spatial_series(spatial_series=left_eye_positions)
    ```

**General Steps:**

1.  **Create an NWBFile:**

    ```python
    from datetime import datetime
    from uuid import uuid4

    from dateutil.tz import tzlocal
    from pynwb import NWBFile

    nwbfile = NWBFile(
        session_description="my first synthetic recording",
        identifier=str(uuid4()),
        session_start_time=datetime.now(tzlocal()),
        experimenter=[
            "Baggins, Bilbo",
        ],
        lab="Bag End Laboratory",
        institution="University of Middle Earth at the Shire",
        experiment_description="I went on an adventure to reclaim vast treasures.",
        session_id="LONELYMTN001",
    )
    ```

2.  **Create a Behavior Processing Module:**

    ```python
    behavior_module = nwbfile.create_processing_module(
        name="behavior", description="Processed behavioral data"
    )
    ```

3.  **Add Behavior Interfaces to the Module:**

    ```python
    behavior_module.add(position)  # Example with Position object
    behavior_module.add(direction)
    behavior_module.add(behavioral_time_series)
    behavior_module.add(behavioral_events)
    behavior_module.add(behavioral_epochs)
    behavior_module.add(pupil_tracking)
    behavior_module.add(eye_tracking)
    ```

4.  **Write to an NWB File:**

    ```python
    from pynwb import NWBHDF5IO

    with NWBHDF5IO("behavioral_tutorial.nwb", "w") as io:
        io.write(nwbfile)
    ```

5.  **Read and Access Data:**

    ```python
    with NWBHDF5IO("behavioral_tutorial.nwb", "r") as io:
        read_nwbfile = io.read()
        behavior_module = read_nwbfile.processing["behavior"]
        print(f"Available data interfaces: {list(behavior_module.values())}")

        # Accessing SpatialSeries data:
        print(read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"])
        print(read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"].data[:]) # Read all data
        print(read_nwbfile.processing["behavior"]["Position"]["SpatialSeries"].data[:2]) # Read a portion of data
    ```
