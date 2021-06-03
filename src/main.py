import sys 
sys.path.append('../src')

from pathlib import Path
import numpy as np
from pydicom.uid import generate_uid


# local
from export_dicom import export_dicom

# for debugging
series_number = 999
output_name = "synthetic_dicom"
output_dir = Path(__file__).parent  / "data"
sample_dicom = Path(__file__).parent / "sample_dicom_petct.dcm"

# tags
SERIES_INSTANCE_UID_TAG = "0020000E"
SERIES_DESCRIPTION_TAG = "0008103E"

project_root = Path(__file__).parent.parent




def make_dicom():
    
    pixel_data = np.zeros((100, 100, 10))

    # study_instance_uid = generate_uid()
    study_instance_uid = "1.2.826.0.1.3680043.8.498.89515756153419402831179022658541245246"
    # series_instance_uid = generate_uid()
    series_instance_uid = "1.2.826.0.1.3680043.8.498.94866033580937989770888665857070522827"

    instance_number = 1
    start = 0
    length = int(100/10)
    for i in np.arange(10):
        pixel_data[:, start: start + length, i] = 255 
        start += length

        # exporting DICOMs based on the pixeldata and a reference metadata
        export_dicom(
            pixel_data=pixel_data[...,i].astype("uint8"),
            reference_dicom=sample_dicom,
            rows=pixel_data.shape[0],
            columns=pixel_data.shape[1],
            study_instance_uid=study_instance_uid,
            series_instance_uid=series_instance_uid,
            series_number=series_number,
            instance_number=instance_number,
            series_description=output_name,
            file_name=f"{output_name}-{generate_uid()}",
            output_dir=output_dir,
        )
        instance_number += 1






if __name__ == "__main__":
    make_dicom()
