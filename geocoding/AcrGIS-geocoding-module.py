import pandas as pd
import geocoder
import requests
import time
import os

# Set the input and output files
#input_file_path = "C:\\Users\\andre\Anaconda3\Scripts\my_scripts\Script-geocoding\Eimport.xlsx"
#output_file_path = "C:\\Users\\andre\Anaconda3\Scripts\my_scripts\Script-geocoding\Toutput"  # appends "####.xlsx" to the file name when it writes the file.

input_file_path = input('Enter the name of the import Excel-file: ')
# Find Desktop path for savint output file
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
output_file_path = desktop + '\output'   # appends "####.xlsx" to the file name when it writes the file

data = pd.read_excel(input_file_path)

# Set the name of the column indexes here so that pandas can read the Excel file
id_column_name = "ID_TT"
client_column_name = "Client"
region_column_name = "Region"
city_column_name = "City"
street_column_name = "Street"
house_column_name = "NoHouse"

# Raise errors if the provided column names could not be found in the input file
# ID_TT column
if id_column_name not in data.columns:
    raise ValueError("Can't find the ID_TT column in the input file.")
# Client column
if client_column_name not in data.columns:
    raise ValueError("Can't find the Client column in the input file.")
# Region column
if region_column_name not in data.columns:
    raise ValueError("Can't find the Region column in the input file.")
# City column
if city_column_name not in data.columns:
    raise ValueError("Can't find the City column in the input file.")
# Street column
if street_column_name not in data.columns:
    raise ValueError("Can't find the Street column in the input file.")
# NoHouse column
if house_column_name not in data.columns:
    raise ValueError("Can't find the NoHouse column in the input file.")


# Where the program starts processing the addresses in the input file
# This is useful in case the computer crashes so you can resume the program where it left off or so you can run multiple
# instances of the program starting at different spots in the input file
start_index = 0

# How often the program prints the status of the running program
status_rate = 100

# How often the program saves a backup file
write_data_rate = 1000

# How many times the program tries to geocode an address before it gives up
attempts_to_geocode = 3

# Time it delays each time it does not find an address
# Note that this is added to itself each time it fails so it should not be set to a large number
wait_time = 3

# concatenate Region, City, Street, NoHouse fields into one string excluding NaNs
cols = ['Region', 'City', 'Street', 'NoHouse']
addresses = data[cols].apply(lambda x: ','.join(x.dropna().astype(str)), axis=1).tolist()


# ----------------------------- Function Definitions -----------------------------#

# Creates request sessions for geocoding
class GeoSessions:
    def __init__(self):
        self.Arcgis = requests.Session()
        self.Komoot = requests.Session()

# Class that is used to return 3 new sessions for each geocoding source
def create_sessions():
    return GeoSessions()

# Main geocoding function that uses the geocoding package to covert addresses into lat, longs
def geocode_address(address, s):
    g = geocoder.arcgis(address, session=s.Arcgis)
    if (g.ok == False):
        g = geocoder.komoot(address, session=s.Komoot)
    return g

def try_address(address, s, attempts_remaining, wait_time):
    g = geocode_address(address, s)
    if (g.ok == False):
        time.sleep(wait_time)
        s = create_sessions()  # It is not very likely that we can't find an address so we create new sessions and wait
        if (attempts_remaining > 0):
            try_address(address, s, attempts_remaining-1, wait_time+wait_time)
    return g

# Creat two emty lists
latcoords = []
longcoords = []
search_address = []

# Function used to write data to the output file
def write_data(search_address, latcoords, longcoords, index):
    # Add columns to DataFrame
    data['Search Address'] = search_address
    data['Lat'] = latcoords
    data['Long'] = longcoords
    
    file_name = (output_file_path + str(index)+ ".xlsx")
    print("Created the file: " + file_name)
    pd.DataFrame(data).to_excel(file_name)

# ----------------------------- Main Loop -----------------------------#

# Variables used in the main for loop that do not need to be modified by the user
s = create_sessions()
failed = 0
total_failed = 0
progress = len(addresses) - start_index

for i, address in enumerate(addresses[start_index:]):
    # Print the status of how many addresses have be processed so far and how many of the failed.
    if ((start_index + i) % status_rate == 0):
        total_failed += failed
        print(
            "Completed {} of {}. Failed {} for this section and {} in total.".format(i + start_index, progress, failed,
                                                                                     total_failed))
        failed = 0
    
    # Try geocoding the addresses
    try:
        g = try_address(address, s, attempts_to_geocode, wait_time)
        if (g.ok == False):
            search_address.append(address)
            latcoords.append(["not"])
            longcoords.append(["found"])
            print("Gave up on address: " + address)
            failed += 1
        else:
            search_address.append(address)
            latcoords.append(g.latlng[0])
            longcoords.append(g.latlng[1])
    
    # If we failed with an error like a timeout we will try the address again after we wait 5 secs
    except Exception as error:
        print("Failed with error {} on address {}. Will try again.".format(error, address))
        try:
            time.sleep(5)
            s = create_sessions()
            g = geocode_address(address, s)
            if (g.ok == False):
                print("Did not fine it.")
                search_address.append(address)
                latcoords.append(["not"])
                longcoords.append(["found"])
                failed += 1
            else:
                print("Successfully found it.")
                search_address.append(address)
                latcoords.append(g.latlng[0])
                longcoords.append(g.latlng[1])
        except Exception as error:
            print("Failed with error {} on address {} again.".format(error, address))
            failed += 1
            search_address.append(address)
            latcoords.append(error)
            longcoords.append(["ERROR"])

# Writing what has been processed so far to an output file
if (i%write_data_rate == 0 and i != 0):
    write_data(search_address, latcoords, longcoords, i + start_index)

# Finished
write_data(search_address, latcoords, longcoords, i + start_index + 1)
print("Finished! :)")
input("Press Enter to exit...")