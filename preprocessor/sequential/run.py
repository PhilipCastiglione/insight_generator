import os
import time

from dotenv import load_dotenv
import googleapiclient.discovery

load_dotenv(verbose=True)

#print("[INFO] using glcoud to authenticate with GCP")
#os.system("gcloud auth application-default login")

compute = googleapiclient.discovery.build("compute", "v1")

image_response = compute.images().getFromFamily(project="ubuntu-os-cloud", family="ubuntu-1804-lts").execute()
source_disk_image = image_response["selfLink"]
zone = os.getenv("GCP_ZONE")
machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)

timestamp = str(int(time.time()))
instance_name = "sequential" + timestamp
bucket_name = os.getenv("GCP_BUCKET_NAME")
project_id = os.getenv("GCP_PROJECT_ID")
storage_account_service_email = os.getenv("GCP_STORAGE_SERVICE_ACCOUNT_EMAIL")

startup_script_path = os.path.join(os.path.dirname(__file__), 'startup-script.sh')
startup_script_vars = "export BUCKET_NAME=\"{}\"\n".format(bucket_name)
startup_script = startup_script_vars + open(startup_script_path, 'r').read()

config = {
    "name": instance_name,
    "machineType": machine_type,
    "disks": [{
        "boot": True,
        "autoDelete": True,
        "initializeParams": {
            "sourceImage": source_disk_image,
        }
    }],
    "networkInterfaces": [{
        "network": "global/networks/default",
        "accessConfigs": [
            {"type": "ONE_TO_ONE_NAT", "name": "External NAT"}
        ]
    }],
    "serviceAccounts": [
        {
            "email": storage_account_service_email,
            "scopes": [
                "https://www.googleapis.com/auth/devstorage.read_only",
                "https://www.googleapis.com/auth/devstorage.read_write"
            ]
        }
    ],
    'metadata': {
        'items': [{
            'key': 'startup-script',
            'value': startup_script
        }]
    }
}

print("[INFO] spinning up an instance")
compute.instances().insert(
        project=project_id,
        zone=zone,
        body=config).execute()

input("press any key to finish and shut down the instance")

print("[INFO] shutting down the instance")
compute.instances().delete(
        project=project_id,
        zone=zone,
        instance=instance_name).execute()

print("[INFO] complete")

