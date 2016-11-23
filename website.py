import xml.etree.cElementTree as ET
import re
import requests

website_re = re.compile(r'https?://[a-z0-9\./]*')

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

def clean_website(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if tag.attrib['k'] == "website":
                    website = tag.attrib['v']
                    if not website_re.match(website):
                        if len(website) < 3 or website[:3] != "www":
                            website = "www." + website
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
