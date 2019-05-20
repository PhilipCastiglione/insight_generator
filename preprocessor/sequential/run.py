# TODO: create iam access role to access bucket
# TODO: create instance with IAM access to our storage bucket
import os
import time

from dotenv import load_dotenv
import googleapiclient.discovery

load_dotenv(verbose=True)

print("[INFO] using glcoud to authenticate with GCP")

os.system("gcloud auth application-default login")

compute = googleapiclient.discovery.build("compute", "v1")

image_response = compute.images().getFromFamily(project="ubuntu-os-cloud", family="ubuntu-1804-lts").execute()
source_disk_image = image_response["selfLink"]
zone = os.getenv("GCP_ZONE")
machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)

startup_script_path = os.path.join(os.path.dirname(__file__), 'startup-script.sh')
startup_script = open(startup_script_path, 'r').read()

timestamp = str(int(time.time()))
instance_name = "sequential" + timestamp
bucket_name = os.getenv("GCP_BUCKET_NAME")
project_id = os.getenv("GCP_PROJECT_ID")

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
    "serviceAccounts": [{
        "email": "default",
        "scopes": [
            "https://www.googleapis.com/auth/devstorage.read_write",
            "https://www.googleapis.com/auth/logging.write"
        ]
    }],
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
