# I will do step by step
# First, import what I need
import pandas as pd  # for data
import matplotlib.pyplot as plt  # for plots

# Load the data from the file
try:
    df = pd.read_excel('1730285881-Airbnb_Open_Data.xlsx') # In breaces it is the URL of the data file
    print("File loaded successfully!")
except FileNotFoundError:
    exit()  # Stop if file not found
except Exception as e:
    print("Other error:", e)
    exit()

# Show how many rows and columns
print("Number of rows:", len(df))
print("Number of columns:", len(df.columns))

# Clean the price column because it has $ and ,
for i in range(len(df)):
    if pd.notna(df['price'][i]):  # check if not empty
        price_str = str(df['price'][i])  # make string
        price_str = price_str.replace('$', '')  # remove $
        price_str = price_str.replace(',', '')  # remove ,
        try:
            df.at[i, 'price'] = float(price_str)  # make number, use .at for safety
        except ValueError:
            print("Bad price at row", i, ":", price_str)  # show error if bad data

# Same for service fee
for i in range(len(df)):
    if pd.notna(df['service fee'][i]):
        fee_str = str(df['service fee'][i])
        fee_str = fee_str.replace('$', '')
        fee_str = fee_str.replace(',', '')
        try:
            df.at[i, 'service fee'] = float(fee_str)
        except ValueError:
            print("Bad fee at row", i, ":", fee_str)

# Objective 1: Distribution of room types
# Count each type
room_types = {}  # use a dictionary like beginner
for room in df['room type']:
    if pd.notna(room):  # skip empty
        if room in room_types:
            room_types[room] += 1
        else:
            room_types[room] = 1

print("Room Type Distribution:")
for key, value in room_types.items():
    print(key, ":", value)

# Make a bar plot
rooms = list(room_types.keys())
counts = list(room_types.values())
plt.bar(rooms, counts)
plt.title('Room Type Distribution')
plt.xlabel('Room Type')
plt.ylabel('Count')
plt.show()

# Objective 2: Average price by neighbourhood group
# First, find unique groups
groups = []  
for group in df['neighbourhood group']:
    if pd.notna(group) and group not in groups:
        groups.append(group)

# Now, calculate average for each
avg_prices = {}
for group in groups:
    total_price = 0
    count = 0
    for i in range(len(df)):
        if df['neighbourhood group'][i] == group and pd.notna(df['price'][i]):
            total_price += df['price'][i]
            count += 1
    if count > 0:
        avg_prices[group] = total_price / count
    else:
        avg_prices[group] = 0

print("Average Price by Neighbourhood Group:")
for key, value in avg_prices.items():
    print(key, ":", value)

# Plot it
neighs = list(avg_prices.keys())
prices = list(avg_prices.values())
plt.bar(neighs, prices)
plt.title('Average Price by Neighbourhood Group')
plt.xlabel('Neighbourhood Group')
plt.ylabel('Average Price')
plt.show()

# Objective 3: Top 10 hosts by number of listings
hosts = {}
for host in df['host name']:
    if pd.notna(host):
        if host in hosts:
            hosts[host] += 1
        else:
            hosts[host] = 1

# Sort to get top 10
sorted_hosts = sorted(hosts.items(), key=lambda x: x[1], reverse=True)  # sort by count
top_10 = sorted_hosts[:10]

print("Top 10 Hosts by Listings:")
for host, count in top_10:
    print(host, ":", count)

# Objective 4: Correlation between price and review rate
# First, remove rows with nan in price or review rate
df_clean = df.dropna(subset=['price', 'review rate number'])

# Now correlation
if not df_clean.empty:
    correlation = df_clean['price'].corr(df_clean['review rate number'])
    print("Correlation between price and review rate:", correlation)
else:
    print("No data for correlation!")