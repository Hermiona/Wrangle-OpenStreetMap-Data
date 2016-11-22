import xml.etree.cElementTree as ET

def is_valid_postcode(postcode):
    if len(postcode) != 6 or postcode[:2] != "72":
        return False
    return postcode.isdigit()

def audit_postcode(filename):
    unexpected_postcodes = {}
    with open(filename, 'r') as file:
        for _, elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:postcode":
                        postcode = tag.attrib['v']
                        if not is_valid_postcode(postcode):
                            if postcode not in unexpected_postcodes:
                                unexpected_postcodes[postcode] = 0
                            unexpected_postcodes[postcode] += 1
    return unexpected_postcodes