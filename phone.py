import xml.etree.cElementTree as ET
import re

phone_re = re.compile(r'\+?996[\-\(]?[0-9]{3}[\-\)]?[0-9]{2}\-?[0-9]{2}\-?[0-9]{2}')
phone_re1 = re.compile(r'0[0-9]{3}\-?[0-9]{2}\-?[0-9]{2}\-?[0-9]{2}')

def match_phone(phone):
    return phone_re.match(phone) or phone_re1.match(phone)

def audit_phone(filename):
    unexpected_phones = []
    with open(filename, 'r') as file:
        for _, elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "phone":
                        phone = tag.attrib['v'].replace(" ", "")
                        if not match_phone(phone):
                            unexpected_phones.append(phone)
    return unexpected_phones