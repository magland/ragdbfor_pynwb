An NWBFile represents a single session of an experiment, containing data and metadata. Data can be accessed from the DANDI archive either by downloading or streaming.

**Downloading Data:**
*   **Using DANDI Web UI:** Navigate to the desired dataset on the DANDI archive, select the desired file, and download. Example provided for dataset `000004`.
*   **Programmatically:** Use the `dandi` Python module.

    ```python
    from dandi.download import download
    download("https://api.dandiarchive.org/api/assets/0f57f0b0-f021-42bb-8eaa-56cd482e2a29/download/", ".")
    ```

**Opening NWB Files:**
Use `pynwb.NWBHDF5IO` to read NWB data.

```python
from pynwb import read_nwb
filepath = "sub-P11HMH_ses-20061101_ecephys+image.nwb" # example file path
nwbfile = read_nwb(filepath)
nwbfile
```

Or using a context manager:

```python
from pynwb import NWBHDF5IO
with NWBHDF5IO(filepath, mode="r") as io2:
    nwbfile2 = io2.read()
    # data accessible here
# data not accessible here
```

**Accessing Stimulus Data:**
Stimulus data is stored in `NWBFile.stimulus`.

```python
nwbfile.stimulus
stimulus_presentation = nwbfile.stimulus["StimulusPresentation"]
all_stimulus_data = stimulus_presentation.data[:]
```

Stimulus data can be 3D or 4D (grayscale or RGB). Data arrays are read lazily. Use slicing to read portions of the data:

```python
frame_index = 31
image = stimulus_presentation.data[frame_index]
# Reverse the last dimension because the data were stored in BGR instead of RGB
image = image[..., ::-1]
import matplotlib.pyplot as plt
plt.imshow(image, aspect="auto")
```

**Accessing Single Unit Data:**
Single unit data is stored in a `pynwb.misc.Units` object.

```python
units = nwbfile.units
units_df = units.to_dataframe() # view as pandas DataFrame
units_df.head()
spike_times = units["spike_times"][0] # access spike times
```

**Visualizing Spiking Activity:**

```python
import numpy as np
before = 1.0  # in seconds
after = 3.0

# Get the stimulus times for all stimuli
stim_on_times = stimulus_presentation.get_timestamps()

for unit in range(3):
    unit_spike_times = nwbfile.units["spike_times"][unit]
    trial_spikes = []
    for time in stim_on_times:
        aligned_spikes = unit_spike_times - time
        aligned_spikes = aligned_spikes[
            (-before < aligned_spikes) & (aligned_spikes < after)
        ]
        trial_spikes.append(aligned_spikes)
    fig, axs = plt.subplots(2, 1, sharex="all")
    plt.xlabel("time (s)")
    axs[0].eventplot(trial_spikes)

    axs[0].set_ylabel("trial")
    axs[0].set_title("unit {}".format(unit))
    axs[0].axvline(0, color=[0.5, 0.5, 0.5])

    axs[1].hist(np.hstack(trial_spikes), 30)
    axs[1].axvline(0, color=[0.5, 0.5, 0.5])
```

**Accessing Trials:**
Trials are stored as a `pynwb.epoch.TimeIntervals` object.

```python
trials_df = nwbfile.trials.to_dataframe()
trials_df.head()
```

**Visualizing trials related to stimuli:**
```python
stim_on_times_landscapes = trials_df[trials_df.category_name == "landscapes"].stim_on_time
for time in stim_on_times_landscapes.iloc[:3]:
    img = np.squeeze(stimulus_presentation.data[np.where(stimulus_presentation.timestamps[:] == time)])
    # Reverse the last dimension because the data were stored in BGR instead of RGB
    img = img[..., ::-1]
    plt.figure()
    plt.imshow(img, aspect="auto")
```

**Closing NWB Files:**
Close files after use.

```python
nwbfile.get_read_io().close()
```