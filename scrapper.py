import requests
import json

# URL for NIFTY 50 data
url = 'https://www.nseindia.com/api/equity-stockIndices?index=NIFTY%2050'
headers = {
    'User-Agent': 'Mozilla/5.0'
}

# Start session and load data
session = requests.Session()
session.get('https://www.nseindia.com', headers=headers)
response = session.get(url, headers=headers)
data = response.json()

# Save to JSON file
with open('stock_data.json', 'w') as json_file:
    json.dump(data, json_file, indent=4)

print("Data saved to 'stock_data'")