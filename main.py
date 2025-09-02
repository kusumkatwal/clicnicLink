import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data_ingestion.fhir_ingestion.synthea_loader import load_fhir_resources
from data_ingestion.fhir_ingestion.transform import (
    transform_patients,
    attach_conditions,
    attach_observations
)

if __name__ == "__main__":
    path = "data/synthea/output/fhir"
    fhir = load_fhir_resources(path)

    # Step 1: Transform Patient data
    patients = transform_patients(fhir["Patient"])

    # Step 2: Attach related Conditions and Observations
    attach_conditions(fhir["Condition"], patients)
    attach_observations(fhir["Observation"], patients)

    # Step 3: Preview
    for pid, pdata in list(patients.items()):  # Show first 3 patients
        print(pdata)
