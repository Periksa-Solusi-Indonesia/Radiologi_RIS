import os
import datetime
import json
import logging
from pydicom.dataset import FileDataset
import pydicom

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Path ke folder worklist
WORKLIST_PATH = "../worklists"
CONFIG_PATH = "config.json"

# Default configuration for USG LOGIQ F5
DEFAULT_CONFIG = {
    "max_studies_per_hour": 30,
    "default_modalities": ["US"],
    "default_ae_titles": {
        "US": "LOGIQF5"
    },
    "character_set": "ISO_IR 100",
    "performing_physician": "DR.RADIOLOGI",
    "usg_logiq_f5": {
        "station_name": "USG_LOGIQ_F5",
        "manufacturer": "GE Healthcare",
        "model": "LOGIQ F5",
        "software_version": "R1.0.0",
        "default_procedure_codes": {
            "abdomen": "US_ABD",
            "pelvis": "US_PEL", 
            "obstetric": "US_OB",
            "gynecology": "US_GYN",
            "thyroid": "US_THY",
            "breast": "US_BRE"
        }
    }
}

def load_config():
    """Load configuration from file or create default"""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        with open(CONFIG_PATH, 'w') as f:
            json.dump(DEFAULT_CONFIG, f, indent=2)
        return DEFAULT_CONFIG

def get_his_data():
    """Simulate HIS/RIS integration for USG LOGIQ F5"""
    now = datetime.datetime.now()
    today = now.strftime('%Y%m%d')
    current_time = now.strftime('%H%M%S')  # Format HHMMSS untuk DICOM
    
    # Short date format for accession number (last 6 digits: YYMMDD)
    short_date = today[2:]  # 20251002 -> 251002

    # USG LOGIQ F5 specific procedures
    return [
        {
            "patient_name": "INDONESIA^PERIKSA",
            "patient_id": "P000123",
            "accession_number": f"US{short_date}001",  # US251002001 (11 chars)
            "modality": "US",
            "ae_title": "LOGIQF5",
            "date": today,
            "time": current_time,  # Menggunakan waktu saat ini
            "study_description": "USG ABDOMEN",
            "procedure_code": "US_ABD"
        },
        {
            "patient_name": "DOE^JANE",
            "patient_id": "P000124",
            "accession_number": f"US{short_date}002",  # US251002002 (11 chars)
            "modality": "US",
            "ae_title": "LOGIQF5",
            "date": today,
            "time": current_time,  # Menggunakan waktu saat ini
            "study_description": "USG OBSTETRI",
            "procedure_code": "US_OB"
        }
    ]

def generate_worklist_dcm(order, config):
    """Generate DICOM worklist file for USG LOGIQ F5"""
    filename = f"{order['accession_number']}.dcm"
    filepath = os.path.join(WORKLIST_PATH, filename)

    # Create basic DICOM file meta information
    file_meta = pydicom.Dataset()
    file_meta.MediaStorageSOPClassUID = "1.2.840.10008.5.1.4.31"  # Modality Worklist
    file_meta.MediaStorageSOPInstanceUID = pydicom.uid.generate_uid()
    file_meta.TransferSyntaxUID = pydicom.uid.ExplicitVRLittleEndian
    file_meta.ImplementationClassUID = "1.2.3.4.5.6.7"
    file_meta.ImplementationVersionName = "PYDICOM_WORKLIST_1.0"

    ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)
    ds.is_little_endian = True
    ds.is_implicit_VR = False

    # Character encoding
    ds.SpecificCharacterSet = config.get('character_set', 'ISO_IR 100')

    # Required DICOM tags for worklist
    ds.StudyDate = order.get("date")
    ds.StudyTime = order.get("time")
    ds.AccessionNumber = order['accession_number'][:16]  # SH VR max 16 chars
    ds.Modality = "US"
    ds.ReferringPhysicianName = ""
    ds.StudyDescription = order.get('study_description', '')[:64]  # LO VR max 64 chars
    ds.PatientName = order['patient_name'][:64]  # PN VR max 64 chars
    ds.PatientID = order['patient_id'][:16]  # LO VR max 16 chars
    ds.PatientBirthDate = ""
    ds.PatientSex = ""
    ds.RequestingPhysician = config.get('performing_physician', 'DR.RADIOLOGI')[:64]  # PN VR max 64 chars

    # Scheduled Procedure Step Sequence
    sps_item = pydicom.Dataset()
    sps_item.Modality = "US"
    sps_item.ScheduledStationAETitle = "LOGIQF5"
    sps_item.ScheduledStationName = config.get('usg_logiq_f5', {}).get('station_name', 'USG_LOGIQ_F5')
    sps_item.ScheduledProcedureStepStartDate = order.get("date")
    sps_item.ScheduledProcedureStepStartTime = order.get("time")
    sps_item.ScheduledPerformingPhysicianName = config.get('performing_physician', 'DR.RADIOLOGI')
    sps_item.ScheduledProcedureStepDescription = order.get('study_description', '')
    sps_item.RequestedProcedureID = order.get('procedure_code', 'US_GEN')

    ds.ScheduledProcedureStepSequence = [sps_item]

    # DICOM UIDs for Modality Worklist
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = "1.2.840.10008.5.1.4.31"  # Modality Worklist Information Model SOP Class

    try:
        ds.save_as(filepath)
        logger.info(f"Generated USG LOGIQ F5 worklist: {filename}")
        return True
    except Exception as e:
        logger.error(f"Failed to generate {filename}: {e}")
        return False

def cleanup_old_worklists():
    """Remove worklists older than 24 hours"""
    if not os.path.exists(WORKLIST_PATH):
        return
        
    cutoff_time = datetime.datetime.now() - datetime.timedelta(hours=24)
    removed_count = 0
    
    for filename in os.listdir(WORKLIST_PATH):
        if filename.endswith('.dcm'):
            filepath = os.path.join(WORKLIST_PATH, filename)
            file_time = datetime.datetime.fromtimestamp(os.path.getmtime(filepath))
            if file_time < cutoff_time:
                os.remove(filepath)
                removed_count += 1
                
    if removed_count > 0:
        logger.info(f"Cleaned up {removed_count} old worklist files")

def main():
    """Main execution function for USG LOGIQ F5"""
    logger.info("Starting USG LOGIQ F5 worklist generation")
    
    # Ensure worklist directory exists
    os.makedirs(WORKLIST_PATH, exist_ok=True)
    
    # Load configuration
    config = load_config()
    
    # Cleanup old files
    cleanup_old_worklists()
    
    # Get data from HIS/RIS
    orders = get_his_data()
    
    # Generate worklist files
    success_count = 0
    for order in orders:
        if generate_worklist_dcm(order, config):
            success_count += 1
    
    logger.info(f"Generated {success_count}/{len(orders)} USG LOGIQ F5 worklist files")

if __name__ == "__main__":
    main()
