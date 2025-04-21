import requests
import os
import datetime
from dotenv import load_dotenv
from pydicom.dataset import Dataset, FileDataset
import pydicom

load_dotenv()

API_URL = os.getenv("API_URL")
API_TOKEN = os.getenv("API_TOKEN")
WORKLIST_PATH = os.getenv("WORKLIST_PATH", "./worklists")

def fetch_orders():
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    response = requests.get(API_URL, headers=headers)
    response.raise_for_status()
    return response.json()

def generate_dcm(order):
    now = datetime.datetime.now()
    filename = f"ORD-{order['accession_number']}.dcm"
    filepath = os.path.join(WORKLIST_PATH, filename)

    file_meta = pydicom.Dataset()
    ds = FileDataset(filepath, {}, file_meta=file_meta, preamble=b"\0" * 128)

    ds.PatientName = order['patient_name']  # format: LAST^FIRST
    ds.PatientID = order['patient_id'] # nomer rekam medis
    ds.AccessionNumber = order['accession_number'] # log_status / reg radiologi
    ds.Modality = order.get('modality', 'CT')
    ds.ScheduledStationAETitle = order.get('ae_title', 'CT01')
    ds.ScheduledProcedureStepStartDate = order.get("date", now.strftime('%Y%m%d'))
    ds.ScheduledProcedureStepStartTime = order.get("time", now.strftime('%H%M%S'))

    ds.StudyInstanceUID = pydicom.uid.generate_uid()
    ds.SeriesInstanceUID = pydicom.uid.generate_uid()
    ds.SOPInstanceUID = pydicom.uid.generate_uid()
    ds.SOPClassUID = "1.2.840.10008.5.1.4.31"

    ds.save_as(filepath)
    print(f"✔ Generated: {filepath}")

def main():
    try:
        orders = fetch_orders()
        for order in orders:
            generate_dcm(order)
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()