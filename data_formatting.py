import json
import pandas as pd

# Load the data from the file
with open('stock_data.json', 'r') as file:
    data = json.load(file)

# Extract relevant data from the JSON
formatted_data = []
for record in data['data']:
    formatted_data.append({
        'symbol': record['symbol'],
        'companyName': record['meta']['companyName'] if 'meta' in record else None,
        'industry': record['meta']['industry'] if 'meta' in record else None,
        'open': record['open'],
        'dayHigh': record['dayHigh'],
        'dayLow': record['dayLow'],
        'lastPrice': record['lastPrice'],
        'previousClose': record['previousClose'],
        'change': record['change'],
        'pChange': record['pChange'],
        'yearHigh': record['yearHigh'],
        'yearLow': record['yearLow'],
        'totalTradedVolume': record['totalTradedVolume'],
        'totalTradedValue': record['totalTradedValue'],
        'perChange365d': record['perChange365d'],
        'perChange30d': record['perChange30d']
    })

# Create a pandas DataFrame
df = pd.DataFrame(formatted_data)

# Display the first 5 rows
print(df.head())

# Save to a CSV file (optional)
df.to_csv('stock_data.csv', index=False)
