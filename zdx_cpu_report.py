# Import necessary modules
import csv
import hashlib
import json
import time
import requests
import boto3
from urllib3.exceptions import InsecureRequestWarning
from variables import your_zdx_key_sec, your_zdx_key_id, your_aws_access_key_id, your_aws_secret_access_key, your_s3_bucket_name, your_csv_file_name

# Suppressing insecure request warnings for cleaner log output
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

# ZDX API requires hashed key for authentication
key_sec = your_zdx_key_sec

# Setting headers for ZDX API Access
headers = {'Content-Type': 'application/json', 'accept': 'application/json'}

# Current time needed for API authentication
timestamp = int(time.time())

# Constructing the API key info payload
payload = {
    'key_id': your_zdx_key_id,
    'key_secret': hashlib.sha256((key_sec + str(timestamp)).encode()).hexdigest(),
    'timestamp': timestamp
}

# Authenticate with ZDX API
response = requests.post('https://api.zdxcloud.net/v1/oauth/token', verify=False, headers=headers, data=json.dumps(payload))

# Access token is stored if response is successful, error message printed otherwise
if response.status_code == 200:
    accessToken = response.json()['token']
else:
    print("Failed with status code: {}".format(response.status_code))

# Update headers with the acquired access token
headers = {'Content-Type': 'application/json', 'accept': 'application/json', 'Authorization': "Bearer " + accessToken}

# Fetching the device list from ZDX
device_list_from_zdx = 'https://api.zdxcloud.net/v1/devices'
device_list_response = requests.get(device_list_from_zdx, verify=False, headers=headers)

# Initialize the CSV file with headers
csv_data = [['Hostname', 'DeviceID', 'CPU_Spec', 'CPU_Util_1', 'CPU_Util_2', 'CPU_Util_3', 'CPU_Util_4', 'CPU_Util_5', 'Avg_CPU_Util']]  # Added 'Avg_CPU_Util' in CSV headers

# Loop over the devices, only process the first 10 devices (to keep the list short)
for i, device in enumerate(device_list_response.json()['devices']):
    if i >= 10:  # Stop after processing 4 devices
        break

    # Fetching device details
    device_id = device['id']
    api_endpoint = 'https://api.zdxcloud.net/v1/devices/'
    api_url = api_endpoint + str(device_id)
    individual_device_details = requests.get(api_url, verify=False, headers=headers)
    hostname = individual_device_details.json()['software']['hostname']
    cpu_model = individual_device_details.json()['hardware']['cpu_model']

    # Fetching device health metrics
    health_metrics_url = api_url + "/health-metrics"
    health_metrics_details = requests.get(health_metrics_url, verify=False, headers=headers)
    
    # Fetching CPU utilization metrics from health metrics
    cpu_utilization_and_timestamp = [["NA", "NA"]] * 5  # Default value in case the CPU metric is not found
    for category in health_metrics_details.json():
        if category['category'] == 'cpu':
            for instance in category['instances']:
                for metric in instance['metrics']:
                    if metric['metric'] == 'total':
                        datapoints = metric['datapoints'][-10:]  # Getting the most recent 5 datapoints
                        for j in range(min(5, len(datapoints))):
                            cpu_utilization_and_timestamp[j] = [datapoints[j]['value']]
                        break
                if cpu_utilization_and_timestamp[0][0] != "NA":
                    break
        if cpu_utilization_and_timestamp[0][0] != "NA":
            break
    
    # Parse Hostname and Device ID from the ZDX Output
    print("ZDX Device ID: " + str(device_id) + ", hostname: " + hostname + ", CPU Utilizations: " + ", ".join([str(x) for x in cpu_utilization_and_timestamp]))

    # Calculate the average CPU usage
    avg_cpu_util = round(sum([float(x[0]) for x in cpu_utilization_and_timestamp if x[0] != "NA"]) / max(1, sum([x[0] != "NA" for x in cpu_utilization_and_timestamp])), 2)
    
    # Add data to CSV
    csv_data.append([hostname, str(device_id), str(cpu_model)] + [item for sublist in cpu_utilization_and_timestamp for item in sublist] + [avg_cpu_util])  # Added 'avg_cpu_util' in CSV data

# Write the CSV data structure to a file
csv_file_name = your_csv_file_name
with open(csv_file_name, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(csv_data)

# Initialize the S3 client
s3 = boto3.client('s3', region_name='eu-central-1', aws_access_key_id=your_aws_access_key_id,
                  aws_secret_access_key=your_aws_secret_access_key)

# Upload the CSV file to S3
with open(csv_file_name, "rb") as data:
    s3.upload_fileobj(data, your_s3_bucket_name, csv_file_name)

print(f"CSV uploaded to S3: {csv_file_name}")
