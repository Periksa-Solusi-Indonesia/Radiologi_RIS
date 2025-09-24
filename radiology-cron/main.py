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

# Default configuration
DEFAULT_CONFIG = {
    "max_studies_per_hour": 50,
    "default_modalities": ["CT", "MR", "XR", "US"],
    "default_ae_titles": {
        "CT": "CT01",
        "MR": "MR01", 
        "XR": "XR01",
        "US": "US01"
    },
    "character_set": "ISO_IR 100",
    "performing_physician": "DR.RADIOLOGI"
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
    """Simulate HIS/RIS integration - replace with actual API call"""
    today = datetime.datetime.now().strftime('%Y%m%d')
    
    # Simulated data from HIS/RIS
    return [
        {
            "patient_name": "INDONESIA^PERIKSA",
            "patient_id": "P000123",
            "accession_number": f"RAD-{today}-0001",
            "modality": "CT",
            "ae_title": "CT01",
            "date": today,
            "time": "081500",
            "study_description": "CT THORAX CONTRAST"
        },
        {
            "patient_name": "DOE^JOHN",
            "patient_id": "P000124", 
            "accession_number": f"RAD-{today}-0002",
            "modality": "MR",
            "ae_title": "MR01",
            "date": today,
            "time": "090000",
            "study_description": "MR BRAIN"
        }
    ]

def generate_worklist_dcm(order, config):
    """Generate DICOM worklist file"""
    filename = f"ORD-{order['accession_number']}.dcm"
    filepath = os.path.join(WORKLIST_PATH, filename)

    file_meta = pydicom.Dataset()
    ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)

    # Character encoding
    ds.SpecificCharacterSet = config.get('character_set', 'ISO_IR 100')

    # Patient information
    ds.PatientName = order['patient_name']
    ds.PatientID = order['patient_id']
    ds.AccessionNumber = order['accession_number']

    # Scheduled Procedure Step
    sps_item = pydicom.Dataset()
    sps_item.Modality = order.get('modality', 'CT')
    sps_item.ScheduledStationAETitle = order.get('ae_title', 'CT01')
    sps_item.ScheduledProcedureStepStartDate = order.get("date")
    sps_item.ScheduledProcedureStepStartTime = order.get("time")
    sps_item.ScheduledPerformingPhysicianName = config.get('performing_physician', 'DR.RADIOLOGI')
    sps_item.ScheduledProcedureStepDescription = order.get('study_description', '')

    ds.ScheduledProcedureStepSequence = [sps_item]

    # DICOM UIDs
    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = "1.2.840.10008.5.1.4.31"

    try:
        ds.save_as(filepath)
        logger.info(f"Generated worklist: {filename}")
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
    """Main execution function"""
    logger.info("Starting worklist generation")
    
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
    
    logger.info(f"Generated {success_count}/{len(orders)} worklist files")

if __name__ == "__main__":
    main()
