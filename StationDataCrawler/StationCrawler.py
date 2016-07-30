from html.parser import HTMLParser
import urllib.request

class MultiURLHTMLParser(HTMLParser):
    def __init__(self, base_domain):
        HTMLParser.__init__(self)
        self.des_tag = "a"
        self.des_attr = "href"
        self.des_prefix = "/fwo/IDQ"
        self.des_suffix = ".tbl.shtml"
        self.stations_info = None
        self.base_domain = base_domain
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == self.des_tag and len(self.des_attr) > 0:
            if self.des_attr == attrs[0][0] and attrs[0][1].startswith(self.des_prefix) and attrs[0][1].endswith(self.des_suffix):
                self.urls.append(self.base_domain + attrs[0][1])
            #print("Encountered a start tag:", tag)
            #self.collect_data = True

    def handle_endtag(self, tag):
        pass
        #if tag == self.des_tag and self.collect_data:
            #print("Encountered an end tag :", tag)
            #self.collect_data = False

    def handle_data(self, data):
        pass
        #if self.collect_data and len(data) > self.bound:
            #self.stations_info = data
        #print("Encountered some data  :", data)

def get_station_urls(seed_url, domain):
    parser = MultiURLHTMLParser(domain)
    with urllib.request.urlopen(seed_url) as response:
        html = str(response.read())    
    parser.feed(html)
    return parser.urls