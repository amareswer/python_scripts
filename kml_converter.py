import csv,os

def kml_data(filename):
    """str -> list
        Return name,lat,lot
    """
    kml_details = []
    with open(filename, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            try:
                name = row[0]
                kml_details.append(name)
                long = float(row[1]) + (float(row[2]) / 60 )
                kml_details.append(long)
                lat = float(row[4]) + (float(row[5]) / 60 )
                kml_details.append(lat)
            except ValueError:
                print("Error with: "+row[0]+"")
    return kml_details

with open("kml_file.kml", 'w') as f:
    details=kml_data('config_params.csv')
    eof = int( len(details) / 3 )
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    for i in range(0,eof,3):
        f.write('\t<Placemark>\n')
        f.write("\t\t<name>"+str(details[i])+"</name>\n")
        f.write("\t\t<Point>\n")
        f.write("\t\t\t<coordinates>"+str(details[i+1])+","+str(details[i+2])+"</coordinates>\n")
        f.write("\t\t</Point>\n")
        f.write('\t</Placemark>\n')
    f.write('</Document>')
    f.write('</kml>\n')

