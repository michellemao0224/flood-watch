from html.parser import HTMLParser
import urllib.request

class MultiStationHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.collect_data = False
        self.bound = 20
        self.des_tag = "div"
        self.des_attr = ("id", "content")
        self.stations_info = None

    def handle_starttag(self, tag, attrs):
        if tag == self.des_tag and self.des_attr in attrs:
            #print("Encountered a start tag:", tag)
            self.collect_data = True

    def handle_endtag(self, tag):
        if tag == self.des_tag and self.collect_data:
            #print("Encountered an end tag :", tag)
            self.collect_data = False

    def handle_data(self, data):
        if self.collect_data and len(data) > self.bound:
            self.stations_info = data
        #print("Encountered some data  :", data)

class RawStationsParser():
    def __init__(self, info):
        self.info = info
        self.index = 0
        self.bound = 5
        self.interest_indices = [8, 17, 48, 72, 93, 103,111]
        self.stations = dict()
    
    def process(self):
        for line in self.info.split('\\n'):
            if self.is_data(line):
                line = self.sanitise(line)
                num, _, name, river, basin, lat, long = self.extract(line)
                self.stations[num] = [name, river, basin, (lat, long)]               
    
    def extract(self, line):
        gauge_data = []
        prev = 0
        for index in self.interest_indices:
            if line[index] != ' ':
                #print("Misallignment (probably due to special character) when reading: {}".format(line))
                pass #should debug this.
            sub = line[prev:index].strip()
            if len(sub) <3:
                sub = None
            gauge_data.append(sub)
            prev = index
        return gauge_data
        
    
    def sanitise(self, line):
        return line.replace("\\", "")
    
    def is_data(self, line):
        if not isinstance(line, str):
            return False
        if len(line) < self.bound:
            return False
        if line[0] != " ":
            return False
        if line[2] == " ":
            return False
        return True
        
    
    def clip_page(self):
        pass
    
    def process_station(self):
        pass

def get_stations_raw(url):
    with urllib.request.urlopen(url) as response:
        html = str(response.read())
    parser = MultiStationHTMLParser()
    parser.feed(html)
    return parser.stations_info

def get_stations_dict(url):
    raw = get_stations_raw(url)
    sp = RawStationsParser(raw)
    sp.process()
    return sp.stations