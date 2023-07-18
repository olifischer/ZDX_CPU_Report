# ZDX Device Monitor and CSV Reporter

This Python script fetches device information from ZDX, calculates the average CPU utilization for each device, and saves the data in a CSV file. The CSV file is then uploaded to an Amazon S3 bucket.

## Requirements

To use this script, you will need the following:

- Python 3.x
- Access to a ZDX account
- Access to an Amazon S3 bucket

Additionally, the following Python packages are required:

- csv
- hashlib
- json
- time
- requests
- boto3

## Installation

To install the necessary Python packages, run:

```shell
pip install csv hashlib json time requests boto3
```

Usage
First, import the necessary modules:

```
import csv
import hashlib
import json
import time
import requests
import boto3
```
Then, disable insecure request warnings:
```
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
```
Configuration
Several variables need to be set before running the script:

your_zdx_key_sec: Your ZDX key secret
your_zdx_key_id: Your ZDX key ID
your_aws_access_key_id: Your AWS access key ID
your_aws_secret_access_key: Your AWS secret access key
your_s3_bucket_name: The name of your S3 bucket
your_csv_file_name: The name of the CSV file you want to create
These variables should be set in the variables.py file.
