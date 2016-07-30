from StationCrawler import get_station_urls
from SingleStationTools import get_station_info
from MultiStationTools import get_stations_dict
import csv
import os

output_file = "QldStationData.cvs"
data_folder = "data"
stations_folder_name = "stations"
stations_folder = os.path.join(data_folder, stations_folder_name)
output_suffix = ".cvs"
base_domain = "http://www.bom.gov.au"
seed_url = "http://www.bom.gov.au/cgi-bin/wrap_fwo.pl?IDQ60005.html"
station_coords_url = "http://www.bom.gov.au/qld/flood/networks/section3.shtml"

def setup_data_folders():
    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
    if not os.path.exists(stations_folder):
        os.makedirs(stations_folder)

def update_station_data():
    #QLD station lookup
    index = 0
    station_lookup = get_stations_dict(station_coords_url)
    urls = get_station_urls(seed_url, base_domain)
    output_file_path = os.path.join(data_folder, output_file)
    with open(output_file_path, 'w') as csv_parent:
        fieldnames = ['station id', 'station name', 'river', 'basin', 'low danger level', 'mid danger level', 'high danger level', 'latitude', 'longatude', 'csv file location']    
        writer = csv.DictWriter(csv_parent, fieldnames=fieldnames)
        writer.writeheader()
        print("Found {} urls during crawl.\nTime to collect data from each (will report for each 10 stations collected).".format(len(urls)))
        for url in urls:
            index += 1
            if index%10 == 0:
                print("{} of {}".format(index, len(urls)))
            num, danger_heights, height_info = get_station_info(url)
            if danger_heights is None:
                continue
            try:
                name, river, basin, coords = station_lookup[num]
            except KeyError:
                print("Could not find cordinates for station: {}".format(num))
                continue
            station_file_name = num + output_suffix
            station_file_path = os.path.join(stations_folder, station_file_name) 
            writer.writerow({'station id':num, 
                 'station name':name,
                 'river':river,
                 'basin':basin,
                 'low danger level':danger_heights[0],
                 'mid danger level':danger_heights[1],
                 'high danger level':danger_heights[2],
                 'latitude':coords[0],
                 'longatude':coords[1],
                 'csv file location':station_file_path})
            with open(station_file_path, 'w') as csv_child:
                fieldnames = ['time', 'height']    
                child_writer = csv.DictWriter(csv_child, fieldnames=fieldnames)
                child_writer.writeheader()
                for time, height in height_info:
                    child_writer.writerow({"time":time, "height":height})       
 
if __name__ == "__main__":                   
    setup_data_folders()
    update_station_data()
