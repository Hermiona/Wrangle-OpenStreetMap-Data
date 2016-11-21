import xml.etree.cElementTree as ET
import re

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
