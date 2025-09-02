# fhir_ingestion/transform.py

def transform_patients(patients):
    transformed = {}
    for patient in patients:
        pid = patient.get("id")
        name_parts = patient.get("name", [{}])[0]
        full_name = f"{name_parts.get('given', [''])[0]} {name_parts.get('family', '')}".strip()

        transformed[pid] = {
            "id": pid,
            "name": full_name,
            "gender": patient.get("gender"),
            "birthDate": patient.get("birthDate"),
            "conditions": [],
            "observations": []
        }
    return transformed

def extract_patient_id(ref) :
    print (ref)
    if ref.startswith("Patient/"):
        ref.replace("Patient/", "")
    if ref.startswith("urn:uuid:"):
        n=9
        print("here", ref[n:])
        return ref[n:]
        
    return ref

def attach_conditions(conditions, patients_dict):
    for condition in conditions:
        ref = condition.get("subject", {}).get("reference", "")
        pid = extract_patient_id(ref)
        if pid in patients_dict:
            display = (
                condition.get("code", {})
                .get("coding", [{}])[0]
                .get("display", "Unknown")
            )
            patients_dict[pid]["conditions"].append(display)
        # else:
            # print(f"⚠️ Condition {condition.get('id')} references unknown patient {pid}")

def attach_observations(observations, patients_dict):
    for obs in observations:
        ref = obs.get("subject", {}).get("reference", "")
        pid = extract_patient_id(ref)
        if pid in patients_dict:
            display = (
                obs.get("code", {})
                .get("coding", [{}])[0]
                .get("display", "Unknown")
            )
            patients_dict[pid]["observations"].append(display)

