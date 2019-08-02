import pandas as pd
import numpy as np
import geocoder
import requests
import time
import os
from PyQt5 import QtCore # Use for updating GUI after each iteration to display active log


def main_geo_func(params):
    '''
    The function tries to geocode address
    - input: list of parametrs [input_file_path, start_index, write_data_rate, attempts_to_geocode]
    - output: creates file on your desktop with longs and lats

    input_file_path - type (str), Set the input file
    start_index - type (int), instances of the program starting at different spots in the input file
    write_data_rate - type (int), How often the program saves a backup file
    attempts_to_geocode - type (int), How many times the program tries to geocode an address before it gives up
    '''
    # Set args from params
    input_file_path = str(params[0])      # Set the input file
    start_index = int(params[1])          # instances of the program starting at different spots in the input file
    write_data_rate = int(params[2])      # How often the program saves a backup file
    attempts_to_geocode = int(params[3])  # How many times the program tries to geocode an address before it gives up
    output_file_name = str(params[4])

    # How often the program prints the status of the running program
    status_rate = 10

    # Time it delays each time it does not find an address
    # Note that this is added to itself each time it fails so it should not be set to a large number
    wait_time = 3

    # Set the output files
    # Find Desktop path for saving output file
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') 
    output_file_path = desktop + '\\' + output_file_name

    data = pd.read_excel(input_file_path)

    # Set the name of the column indexes here so that pandas can read the Excel file
    id_column_name = "ID_TT"
    client_column_name = "Client"
    region_column_name = "Region"
    city_column_name = "City"
    street_column_name = "Street"
    house_column_name = "NoHouse"
    address_column_name = "Address"

    if address_column_name in data.columns:
        addresses = data[address_column_name]
    else:
        # Raise errors if the provided column names could not be found in the input file
        # ID_TT column
        if id_column_name not in data.columns:
            #raise ValueError("Can't find the ID_TT column in the input file.")
            return print("Упс... Не найден столбец 'ID_TT' в файле импорта.")
        # Client column
        if client_column_name not in data.columns:
            #raise ValueError("Can't find the Client column in the input file.")
            return print("Упс... Не найден столбец 'Client' в файле импорта.")
        # Region column
        if region_column_name not in data.columns:
            #raise ValueError("Can't find the Region column in the input file.")
            return print("Упс... Не найден столбец 'Region' в файле импорта.")
        # City column
        if city_column_name not in data.columns:
            #raise ValueError("Can't find the City column in the input file.")
            return print("Упс... Не найден столбец 'City' в файле импорта.")
        # Street column
        if street_column_name not in data.columns:
            #raise ValueError("Can't find the Street column in the input file.")
            return print("Упс... Не найден столбец 'Street' в файле импорта.")
        # NoHouse column
        if house_column_name not in data.columns:
            #raise ValueError("Can't find the NoHouse column in the input file.")
            return print("Упс... Не найден столбец 'NoHouse' в файле импорта.")

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
        # Create Nan lists to fill empty rows
        nan_list = [np.nan for x in range(start_index)]
        second_nan_list = [np.nan for x in range(progress - len(search_address))]
        # Add columns to DataFrame
        data['Search Address'] = nan_list + search_address + second_nan_list
        data['Lat'] = nan_list + latcoords + second_nan_list
        data['Long'] = nan_list + longcoords + second_nan_list
        
        file_name = (output_file_path + str(index)+ ".xlsx")
        print("Создан файл: " + file_name)
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
                "Завершено {} из {}. Не найдено {} в этой группе и {} в общем.".format(i + start_index, progress, failed,
                                                                                        total_failed))
            failed = 0
        
        # Try geocoding the addresses
        try:
            g = try_address(address, s, attempts_to_geocode, wait_time)
            if (g.ok == False):
                search_address.append(address)
                latcoords.append(["not"])
                longcoords.append(["found"])
                print("Строка {} - координаты не определены: {} ".format(i + start_index, address))
                failed += 1
            else:
                search_address.append(address)
                latcoords.append(g.latlng[0])
                longcoords.append(g.latlng[1])
        
        # If we failed with an error like a timeout we will try the address again after we wait 5 secs
        except Exception as error:
            print("Строка {} - координаты не определены с ошибкой {} по адресу {}. Попробуем еще раз.".format(i + start_index, error, address))
            try:
                time.sleep(5)
                s = create_sessions()
                g = geocode_address(address, s)
                if (g.ok == False):
                    print("Координаты не определены.")
                    search_address.append(address)
                    latcoords.append(["not"])
                    longcoords.append(["found"])
                    failed += 1
                else:
                    print("Координаты успешно определены.")
                    search_address.append(address)
                    latcoords.append(g.latlng[0])
                    longcoords.append(g.latlng[1])
            except Exception as error:
                print("Строка {} - координаты не определены с ошибкой {} по адресу {} опять.".format(i + start_index, error, address))
                failed += 1
                search_address.append(address)
                latcoords.append(error)
                longcoords.append(["ERROR"])

        # Writing what has been processed so far to an output file
        if (i%write_data_rate == 0 and i != 0):
            write_data(search_address, latcoords, longcoords, i + start_index)
        QtCore.QCoreApplication.processEvents()  # Use for updating GUI after each iteration to display active log

    # Finished
    write_data(search_address, latcoords, longcoords, i + start_index + 1)
    print('''=*=*=*=*=*=* Готово! *=*=*=*=*=*=''')
    return 