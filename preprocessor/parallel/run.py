import argparse
import os
import time

from dotenv import load_dotenv
import googleapiclient.discovery

load_dotenv(verbose=True)

parser = argparse.ArgumentParser()
parser.add_argument('scale', type=int, help='horizontal scaling - the number of vms to use')
args = parser.parse_args()

MAX_VMS_PER_ZONE = 8 # this is a GCP limit for aus AZs
if args.scale > 24:
    print("[ERROR] given max {} parallel instances per GCP AZ (eg for australia southeast), use a scale of 24 or less".format(
        MAX_VMS_PER_ZONE))
    exit(1)

print("[INFO] using glcoud to authenticate with GCP")
os.system("gcloud auth application-default login")
compute = googleapiclient.discovery.build("compute", "v1")

image_response = compute.images().getFromFamily(project="ubuntu-os-cloud", family="ubuntu-1804-lts").execute()
source_disk_image = image_response["selfLink"]
zone_1 = os.getenv("GCP_ZONE")
zone_2 = os.getenv("GCP_ZONE_TWO")
zone_3 = os.getenv("GCP_ZONE_THREE")

timestamp = str(int(time.time()))
bucket_name = os.getenv("GCP_BUCKET_NAME")
project_id = os.getenv("GCP_PROJECT_ID")
storage_account_service_email = os.getenv("GCP_STORAGE_SERVICE_ACCOUNT_EMAIL")

print("[INFO] {} instances to spin up".format(args.scale))

instance_names = []
for i in range(args.scale):
    if (i < MAX_VMS_PER_ZONE * 1):
        zone = zone_1
    elif (i < MAX_VMS_PER_ZONE * 2):
        zone = zone_2
    elif (i < MAX_VMS_PER_ZONE * 3):
        zone = zone_3

    machine_type = "zones/{}/machineTypes/n1-standard-1".format(zone)

    instance_name = "parallel{}{}".format(str(i), timestamp)
    instance_names.append(instance_name)
    startup_script_path = os.path.join(os.path.dirname(__file__), 'startup-script.sh')
    startup_script_vars = "export TIMESTAMP=\"{}\"\n".format(timestamp)
    startup_script_vars += "export BUCKET_NAME=\"{}\"\n".format(bucket_name)
    startup_script_vars += "export INSTANCE_NUMBER=\"{}\"\n".format(str(i))
    startup_script_vars += "export SCALE=\"{}\"\n".format(str(args.scale))
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

    print("[INFO] spinning up instance: {}".format(instance_name))
    compute.instances().insert(
            project=project_id,
            zone=zone,
            body=config).execute()

input("press any key to finish and shut down all instances")

for i, instance_name in enumerate(instance_names):
    if (i < MAX_VMS_PER_ZONE * 1):
        zone = zone_1
    elif (i < MAX_VMS_PER_ZONE * 2):
        zone = zone_2
    elif (i < MAX_VMS_PER_ZONE * 3):
        zone = zone_3

    print("[INFO] shutting down instance: {}".format(instance_name))
    compute.instances().delete(
            project=project_id,
            zone=zone,
            instance=instance_name).execute()

print("[INFO] complete")

