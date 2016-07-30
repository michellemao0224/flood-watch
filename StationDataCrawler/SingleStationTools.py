from html.parser import HTMLParser
import urllib.request

class SingleStationHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.collect_time = False
        self.collect_height = False
        self.collect_station = False
        self.bound = 1
        self.station_tag = "p"
        self.station_attr = ("class","stationdetails")
        self.data_tag = "td"
        self.left_data = ("align", "left")
        self.right_data = ("align", "right")
        self.station_times = []
        self.station_heights = []
        self.station_raw = ""
        
    def handle_starttag(self, tag, attrs):
        if tag == self.station_tag and self.station_attr in attrs:
            self.collect_station = True
        elif tag == self.data_tag and self.left_data in attrs:
            #print("Encountered a start tag:", tag)
            self.collect_time = True
        elif tag == self.data_tag and self.right_data in attrs:
            #print("Encountered a start tag:", tag)
            self.collect_height = True
        else:
            self.collect_pause = True

    def handle_endtag(self, tag):
        if tag == self.station_tag and self.collect_station:
            self.collect_station = False
        elif tag == self.data_tag and self.collect_time:
            #print("Encountered a start tag:", tag)
            self.collect_time = False
        elif tag == self.data_tag and self.collect_height:
            #print("Encountered a start tag:", tag)
            self.collect_height = False
        else:
            self.collect_pause = False

    def handle_data(self, data):
        if self.collect_station and not self.collect_pause:
            self.station_raw += data
        elif self.collect_time:
            self.station_times.append(data)
        elif self.collect_height:
            self.station_heights.append(float(data))
        #print("Encountered some data  :", data)

def get_station_raw(url):
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
    parser = SingleStationHTMLParser()
    parser.feed(html)
    return parser.station_raw, parser.station_times, parser.station_heights

def get_station_info(url):
    raw, times, heights = get_station_raw(url)
    number = raw.split()[0].strip()
    data = list(zip(times,heights))
    height_info = raw.split("\\n")
    danger_heights = None
    if len(height_info) > 1:
        danger_heights = [float(x) for x in height_info[1].split()]
        if len(danger_heights) != 3:
            danger_heights = None
    return number, danger_heights, data