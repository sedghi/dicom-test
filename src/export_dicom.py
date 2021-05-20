from pydicom import Dataset
from pydicom.uid import ExplicitVRLittleEndian, generate_uid, PYDICOM_IMPLEMENTATION_UID
from pydicom._storage_sopclass_uids import SecondaryCaptureImageStorage
from pydicom.dataset import FileMetaDataset
from pydicom import dcmread
from utils import safe_mkdirs 
import os


def export_dicom(
    pixel_data,
    series_number,
    rows,
    columns,
    number_of_frames,
    instance_number,
    study_instance_uid,
    series_instance_uid,
    series_description,
    reference_dicom,
    output_dir,  # for debugging
    file_name,  # for debugging
):
    """Generates a Secondary Capture DICOM file based on the provided pixelData, and
    a reference metadata from a reference DICOM file.


    Args:
        pixel_data (NumpyArray): PixelData for the dicom, containing a rotated MIP
        series_number (Number): dicom SeriesNumber
        rows (Number): image number of rows
        columns (Number): image number of columns
        number_of_frames (Number): DICOM number of frames
        instance_number (Number): DICOM InstanceNumber
        study_instance_uid (String): DICOM StudyInstanceUID
        series_instance_uid (String): DICOM SeriesInstanceUID
        series_description (String): DICOM Series Description
        reference_dicom (String): Reference DICOM path, which will be used to extract the needed metadata 
        dicomweb_client (Class): DICOMWeb client
        output_dir (String): Output directory to store on local (used for debugging)
    """

    dcm = dcmread(reference_dicom)
    SOPInstanceUID = generate_uid()

    file_meta = FileMetaDataset()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = SOPInstanceUID
    file_meta.ImplementationClassUID = PYDICOM_IMPLEMENTATION_UID

    ds = Dataset()
    ds.file_meta = file_meta
    ds.InstanceCreationDate = dcm.InstanceCreationDate
    ds.StationName = "ohif"
    ds.PatientName = "ohif-cornerstone-test"
    ds.PatientID = dcm.PatientID
    ds.PatientBirthDate = dcm.PatientBirthDate
    ds.PatientSex = dcm.PatientSex
    # ds.BodyPartExamined = dcm.BodyPartExamined 

    ds.StudyInstanceUID = study_instance_uid
    ds.StudyDescription = dcm.StudyDescription
    ds.SeriesDescription = f"{series_description}"
    ds.StudyDate = dcm.StudyDate
    ds.StudyTime = dcm.StudyTime
    ds.ReferringPhysicianName = dcm.ReferringPhysicianName
    ds.StudyID = dcm.StudyID
    ds.AccessionNumber = dcm.AccessionNumber
    ds.FrameOfReferenceUID = dcm.FrameOfReferenceUID
    
    # In order for slices to appear in the same order we need position metadata
    # we are faking the imagepositionPatient for each slice by adding the instance_number
    ds.ImageOrientationPatient = dcm.ImageOrientationPatient
    ds.ImagePositionPatient = [dcm.ImagePositionPatient[0],
                               dcm.ImagePositionPatient[1], 
                               dcm.ImagePositionPatient[2]+instance_number]

    ds.Modality = "MR"
    ds.SeriesInstanceUID = series_instance_uid
    ds.SeriesNumber = series_number

    ds.NumberOfFrames = number_of_frames

    ds.Rows = rows
    ds.Columns = columns
    ds.SamplesPerPixel = 1
    ds.PixelSpacing = [1 ,1]
    ds.PhotometricInterpretation = 'MONOCHROME2'
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 8
    ds.PixelRepresentation = 0

    ds.PixelData = pixel_data.tobytes()

    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = SOPInstanceUID

    # for debugging
    safe_mkdirs(output_dir)
    ds.save_as(
        filename=os.path.join(output_dir, "{}.dcm".format(file_name)),
        write_like_original=False,
    )
