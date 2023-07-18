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

Usage
First, import the necessary modules:

import csv
import hashlib
import json
import time
import requests
import boto3
