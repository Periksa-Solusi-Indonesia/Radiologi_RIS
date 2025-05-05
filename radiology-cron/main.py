import os
import datetime
from pydicom.dataset import FileDataset
import pydicom

# Path ke folder worklist (relative ke posisi script)
WORKLIST_PATH = "../worklists"

# Data pasien dummy (bisa banyak)
dummy_orders = [
    {
        "patient_name": "HANIFAH^SUTAN",
        "patient_id": "P000123",
        "accession_number": "RAD-20250505-0001",
        "modality": "CT",
        "ae_title": "CT01",
        "date": "20250505",
        "time": "081500"
    },
    {
        "patient_name": "DOE^JOHN",
        "patient_id": "P000124",
        "accession_number": "RAD-20250505-0002",
        "modality": "MR",
        "ae_title": "MR01",
        "date": "20250505",
        "time": "090000"
    }
]

def generate_dcm(order):
    now = datetime.datetime.now()
    filename = f"ORD-{order['accession_number']}.dcm"
    filepath = os.path.join(WORKLIST_PATH, filename)

    file_meta = pydicom.Dataset()
    ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Set karakter encoding
    ds.SpecificCharacterSet = "ISO_IR 100"  # Latin-1

    # Informasi pasien
    ds.PatientName = order['patient_name']
    ds.PatientID = order['patient_id']
    ds.AccessionNumber = order['accession_number']

    # Worklist detail (harus pakai Sequence)
    sps_item = pydicom.Dataset()
    sps_item.Modality = order.get('modality', 'CT')
    sps_item.ScheduledStationAETitle = order.get('ae_title', 'CT01')
    sps_item.ScheduledProcedureStepStartDate = order.get("date", now.strftime('%Y%m%d'))
    sps_item.ScheduledProcedureStepStartTime = order.get("time", now.strftime('%H%M%S'))
    sps_item.ScheduledPerformingPhysicianName = "DR.SIMULASI"

    ds.ScheduledProcedureStepSequence = [sps_item]

    # DICOM Metadata
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = "1.2.840.10008.5.1.4.31"  # Modality Worklist Information Model - FIND

    ds.save_as(filepath)
    print(f"✔ Generated dummy worklist: {filepath}")


def main():
    for order in dummy_orders:
        generate_dcm(order)

if __name__ == "__main__":
    main()
