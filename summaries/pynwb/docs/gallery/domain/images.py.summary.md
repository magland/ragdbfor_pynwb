This document describes how to store image data in NWB files using the `pynwb.image` module.

**Key Classes:**

*   **OpticalSeries:** For time series of images presented as stimuli. Add to NWBFile using `nwbfile.add_stimulus()`. Requires `name`, `distance`, `field_of_view`, and `orientation`.
    ```python
    optical_series = OpticalSeries(
        name="StimulusPresentation",
        distance=0.7,
        field_of_view=[0.2, 0.3, 0.7],
        orientation="lower left",
        data=image_data,
        unit="n.a.",
        format="raw",
        starting_frame=[0.0],
        rate=1.0,
        comments="no comments",
        description="The images presented to the subject as stimuli"
    )
    nwbfile.add_stimulus(optical_series)
    ```

*   **AbstractFeatureSeries:** For storing features of visual stimuli (e.g., luminance, contrast). Add to NWBFile using `nwbfile.add_stimulus()`.
    ```python
    abstract_feature_series = AbstractFeatureSeries(
        name="StimulusFeatures",
        data=feature_data,
        timestamps=np.linspace(0, 1, 200),
        description="Features of the visual stimuli",
        features=["luminance", "contrast", "spatial frequency"],
        feature_units=["n.a.", "n.a.", "cycles/degree"]
    )
    nwbfile.add_stimulus(abstract_feature_series)
    ```

*   **ImageSeries:** For general time series of images acquired during the experiment. Add to NWBFile using `nwbfile.add_acquisition()`.
    ```python
    behavior_images = ImageSeries(
        name="ImageSeries",
        data=image_data,
        description="Image data of an animal moving in environment.",
        unit="n.a.",
        format="raw",
        rate=1.0,
        starting_time=0.0,
    )
    nwbfile.add_acquisition(behavior_images)
    ```

    *   **External Files:** Can store links to external image or video files using the `external_file` attribute. Use `starting_frame` to indicate the frame each file contains. The file path must be relative to the NWB file. Either `external_file` or `data` must be specified, but not both. Timestamps can be set using the `timestamps` property for variable sampling rates.
        ```python
        behavior_external_file = ImageSeries(
            name="ExternalFiles",
            description="Behavior video of animal moving in environment.",
            unit="n.a.",
            external_file=external_file,
            format="external",
            starting_frame=[0, 2, 4],
            timestamps=timestamps,
        )
        nwbfile.add_acquisition(behavior_external_file)
        ```

*   **GrayscaleImage, RGBImage, RGBAImage:** For static images.  Specify `description` and `resolution` (pixels/cm).
    ```python
    rgba_logo = RGBAImage(
        name="pynwb_RGBA_logo",
        data=np.array(img),
        resolution=70.0,
        description="RGBA version of the PyNWB logo."
    )
    ```

*   **Images:** A container for static images (GrayscaleImage, RGBImage, RGBAImage).

*   **IndexSeries:** Efficiently store time series of repeated images by referencing unique images in an `Images` container.
    ```python
    from pynwb.base import ImageReferences
    from pynwb.image import GrayscaleImage, Images, IndexSeries, RGBImage

    images = Images(
        name="raccoons",
        images=[rgb_logo, gs_logo],
        description="A collection of raccoons.",
        order_of_images=ImageReferences("order_of_images", [rgb_logo, gs_logo]),
    )

    idx_series = IndexSeries(
        name="stimuli",
        data=[0, 1, 0, 1],
        indexed_images=images,
        unit="N/A",
        timestamps=[0.1, 0.2, 0.3, 0.4],
    )
    ```

**General Usage:**

*   Use `NWBHDF5IO` to write and read NWB files.
*   Acquired data (e.g., ImageSeries) is added using `nwbfile.add_acquisition()`.
*   Stimulus data (e.g., OpticalSeries, AbstractFeatureSeries) is added using `nwbfile.add_stimulus()`.

**Reading Data:**

```python
with NWBHDF5IO(nwbfile_path, "r") as io:
    read_nwbfile = io.read()
    print(read_nwbfile.acquisition["ImageSeries"])
    print(read_nwbfile.stimulus["StimulusPresentation"].data[:])
```
