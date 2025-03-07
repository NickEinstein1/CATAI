import os
os.system("pip install pandas")
os.system("pip install requests")
os.system("pip install numpy")
os.system("pip install schedule")


import pandas as pd
import requests
import numpy as np

import time
from datetime import datetime, timedelta

# Replace with your NOAA CDO access token
access_token = "YourAccessTokenHere"

# Track daily usage
daily_requests = 0
daily_limit = 10000
last_request_time = None

# Function to fetch data from NOAA CDO API with rate limiting
def fetch_noaa_data(endpoint, params=None):
    global daily_requests, last_request_time

    # Check daily request limit
    if daily_requests >= daily_limit:
        print("Daily request limit reached. Please try again tomorrow.")
        return None

    # Throttle requests to 5 per second
    if last_request_time is not None:
        elapsed_time = time.time() - last_request_time
        if elapsed_time < 0.2:  # 5 requests per second (1/5 = 0.2 seconds)
            time.sleep(0.2 - elapsed_time)

    # Make the request
    base_url = "https://www.ncdc.noaa.gov/cdo-web/api/v2"
    url = f"{base_url}{endpoint}"
    headers = {"token": access_token}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an error for bad status codes

        # Update request tracking
        daily_requests += 1
        last_request_time = time.time()

        return response.json()  # Return the JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# Function to reset daily request count
def reset_daily_requests():
    global daily_requests
    daily_requests = 0

# Example usage
params = {
    "datasetid": "GHCND",  # Global Historical Climatology Network Daily
    "locationid": "ZIP:10001",  # New York, NY
    "startdate": "2023-01-01",
    "enddate": "2023-12-31"
}

# Fetch data multiple times (for testing rate limiting)
for i in range(10)s:
    data = fetch_noaa_data("/data", params=params)
    if data:
        print(f"Request {i + 1}: Data fetched successfully!")
    else:
        break

# Reset daily requests at the start of each day
# (This can be automated using a scheduler like cron or a background task)
reset_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
print(f"Daily requests will reset at: {reset_time}")
