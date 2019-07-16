from arcgis.gis import GIS
from arcgis.geocoding  import batch_geocode
import pandas as pd
import csv
from time import sleep

# login to ARCGIS
gis = GIS("http://www.arcgis.com", "fugrusha", "NiWhuBTtRrFqk3X")

#File location
input_file = input('Enter the name of the import csv file to geocode: ')
output_file = 'C://Users/andre/Anaconda3/Scripts/my_scripts/Script-geocoding/export.csv'

# Load data to Pandas Dataframe
data = pd.read_csv(input_file, encoding = 'utf8')
# Uncomment to check data
#data.head()

# Put data from column Address to list
addresses = data["Address"].tolist()

# Get coords from the list addresses
# return json-file
results = batch_geocode(addresses)

# Create two empty lists
latcoords = []
longcoords = []

time_to_sleep_when_captcha = 5

# put coords from json-file to list
for coordinates in results:
    try:
        longitude = "{:.4f}".format(float(coordinates[ 'location'][ 'x']))
        latitude = "{:.4f}".format(float(coordinates[ 'location'][ 'y']))
        longcoords.append(longitude)
        latcoords.append(latitude)
    except:
        sleep(time_to_sleep_when_captcha)
        time_to_sleep_when_captcha += 1

# Add columns to DataFrame
data['Lat'] = latcoords
data['Long'] = longcoords

# Create csv-file from DataFrame
pd.DataFrame(data).to_csv(output_file, encoding='utf-16')
len(results)