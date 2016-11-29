import xml.etree.cElementTree as ET
import re
import requests

# Regex for website address in standard format
# (which follows best practices from https://wiki.openstreetmap.org/wiki/Key:website)
website_re = re.compile(r'https?://[a-z0-9\./]*')

def url_is_good(url):
    return website_re.match(url)

# Returns list of websites which are not in standard format
def audit_website(filename):
    unexpected_websites = []
    with open(filename, 'r') as file:
        for _, elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "website":
                        website = tag.attrib['v']
                        if not website_re.match(website):
                            unexpected_websites.append(website)
    return unexpected_websites

# Creates new osm xml file with websites in standard format
def clean_website(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if tag.attrib['k'] == "website":
                    website = tag.attrib['v']
                    if not url_is_good(website):
                        tag.attrib['v'] = "http://" + website

                        #possible validation of websites
                        """https_response = requests.get("https://" + website)
                        if https_response < 400:
                            tag.attrib['v'] = "https://" + website
                        else:
                            http_response = requests.get("http://" + website)
                            if http_response < 400:
                                tag.attrib['v'] = "http://" + website
                            else:
                                print(website + " is unreachable")"""

    tree.write("cleaned_website_" + filename, encoding='utf-8')
