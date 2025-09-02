import os
import json

def load_fhir_resources(fhir_folder_path):
    data = {}
    file_count = 0

    for filename in os.listdir(fhir_folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(fhir_folder_path, filename)
            with open(file_path, "r") as f:
                try:
                    resource = json.load(f)
                    if resource["resourceType"] == "Bundle":
                        for entry in resource.get("entry", []):
                            inner = entry.get("resource", {})
                            rtype = inner.get("resourceType")
                            if rtype:
                                data.setdefault(rtype, []).append(inner)
                                file_count += 1
                    else:
                        rtype = resource.get("resourceType")
                        if rtype:
                            data.setdefault(rtype, []).append(resource)
                            file_count += 1
                except Exception as e:
                    print(f"⚠️ Error in {filename}: {e}")

    print(f"✅ Loaded {file_count} resources from {fhir_folder_path}")
    for key in data:
        print(f" - {key}: {len(data[key])}")
    return data
