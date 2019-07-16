import csv
import os

#asks user the name of file
userFile = input('Enter the name of the csv file to convert it to geojson: ')

#reads in the data of file
f = open(userFile, encoding = 'utf-16')
csv_f = csv.reader(f)
next(csv_f, None)  # skip the headers

#reads it in again this time to count the rows in the file
with open(userFile, "r", encoding = 'utf-16') as l:
    reader = csv.reader(l,delimiter = ",")
    data = list(reader)
    tot_row_count = len(data)

#opening text of the geojson
test = "{ \n\t\"type\": \"FeatureCollection\",\n\t\"features\": [\n\t"
cords_list = []

row_count = 0

#iterates through all the rows of the file
for row in csv_f:
    #increments what row currently on 
    row_count = row_count + 1
    #the latitude data is stored on column 4 (5-1 = 4 =column F)
    latitude = row[4]
    longitude = row[5]
    Client = row[2]
    Address = row[3]
    ID_TT = row[1]  

    #if the row is not the last rown continue as normal
    if (row_count < tot_row_count - 1 ):
        cords_list.append("\t\t{\n\t\t\"type\": \"Feature\",\n\t\t\"geometry\": {\n\t\t\t\"type\": \"Point\",\n\t\t\t\"coordinates\": [\n\t\t\t"+str(longitude)+",\n\t\t\t"+str(latitude)+"\n\t\t\t]\n\t\t},\n\t\t\"properties\": {\n\t\t\t\"Client\": \""+str(Client)+"\",\n\t\t\t\"ID_TT\": \""+ID_TT+"\",\n\t\t\t\"Address\": \""+str(Address)+"\"\n\t\t}\n\t\t},\n")
    #if the row is the last row dont put a comma at the end
    else:
        cords_list.append("\t\t{\n\t\t\"type\": \"Feature\",\n\t\t\"geometry\": {\n\t\t\t\"type\": \"Point\",\n\t\t\t\"coordinates\": [\n\t\t\t"+str(longitude)+",\n\t\t\t"+str(latitude)+"\n\t\t\t]\n\t\t},\n\t\t\"properties\": {\n\t\t\t\"Client\": \""+str(Client)+"\",\n\t\t\t\"ID_TT\": \""+ID_TT+"\",\n\t\t\t\"Address\": \""+str(Address)+"\"\n\t\t}\n\t\t}\n")

#output geojson
#Output file location
#output_file = './html_map/geojson.geojson'

#deletes any geojson file first before recreating
try:
    os.remove("./html_map/geojson.geojson")
except OSError:
    pass
with open("./html_map/geojson.geojson", "a", encoding = "utf-8") as outputFile:
    outputFile.write(test) 
    for line in cords_list:
        outputFile.write(line)
    outputFile.write("\t]\n}")