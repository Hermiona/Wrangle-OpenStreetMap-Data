# -*- coding: utf-8 -*-
import sys, codecs
from lxml import html
import requests
import xml.etree.cElementTree as ET
from collections import defaultdict
import re

#street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected_streets = [unicode("улица", 'utf8'), unicode("переулок", 'utf8'), unicode("проспект", 'utf8'), unicode("площадь", 'utf8'), unicode("микрорайон", 'utf8'), unicode("тупик", 'utf8'), unicode("бульвар", 'utf8')]

street_mapping = {
            unicode("ул", 'utf8'): unicode("улица", 'utf8'),
            unicode("ул.", 'utf8'): unicode("улица", 'utf8'),
            unicode("Str", 'utf8'): unicode("улица", 'utf8'),
            unicode("Str.", 'utf8'): unicode("улица", 'utf8'),
            unicode("St", 'utf8'): unicode("улица", 'utf8'),
            unicode("St.", 'utf8'): unicode("улица", 'utf8'),
            unicode("мкр", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("мкр.", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микра", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("Микрорайон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрарайон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микраройон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрорайно", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрораон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("пер", 'utf8'): unicode("переулок", 'utf8'),
            unicode("пер.", 'utf8'): unicode("переулок", 'utf8'),
            unicode("прe", 'utf8'): unicode("переулок", 'utf8'),
            unicode("пре.", 'utf8'): unicode("переулок", 'utf8'),
            unicode("перулок", 'utf8'): unicode("переулок", 'utf8'),
            unicode("Strasse", 'utf8'): unicode("проспект", 'utf8'),
            unicode("Avenue", 'utf8'): unicode("проспект", 'utf8'),
            unicode("blvrd.", 'utf8'): unicode("бульвар", 'utf8')
            }

def audit_street_type(street_types, street_name):
    #m = street_type_re.search(street_name)
    #if m:
    #   street_type = unicode(m.group())
    if True:
        #street_type = unicode(street_name)
        street_type = unicode(street_name.strip().split(" ")[-1])
        if street_type not in expected_streets and street_type not in street_mapping:
            street_type = unicode(street_name.strip().split(" ")[0])
            if street_type not in expected_streets and street_type not in street_mapping:
                street_type_prefix = unicode(street_name.strip().split(" ")[0][:4])
                if street_type_prefix not in expected_streets and street_type_prefix not in street_mapping:
                    street_types[street_type].add(unicode(street_name))

def audit_street(filename):
    street_types = defaultdict(set)
    with open(filename, 'r') as file:
        for _ , elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:street":
                        audit_street_type(street_types, tag.attrib['v'])
    return street_types

def get_expected_postcodes(url):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    postcodes_and_phones = tree.xpath('//span[@class="element element-text last"]/text()')
    postcodes_and_phones = [x.strip() for x in postcodes_and_phones]
    expected_postcodes = set()
    for i in range(0, len(postcodes_and_phones)):
        if i % 3 == 0:
            expected_postcodes.add(postcodes_and_phones[i])
    return expected_postcodes

def audit_postcode(filename):
    expected_postcodes = get_expected_postcodes("http://kyrgyzpost.kg/ru/zipcodes-search.html?e%5B_itemcategory%5D%5B%5D=35&e%5B_itemcategory%5D%5B%5D=&e%5B6e61c763-659a-4bf2-8d0b-1fd1151b357f%5D=&limit=all&order=alpha&logic=and&send-form=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&controller=search&Itemid=356&option=com_zoo&task=filter&exact=0&type=otdelenie-svyazi&app_id=9")
    unexpected_postcodes = {}
    with open(filename, 'r') as file:
        for _, elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:postcode":
                        postcode = tag.attrib['v']
                        if postcode not in expected_postcodes:
                            if postcode not in unexpected_postcodes:
                                unexpected_postcodes[postcode] = 0
                            unexpected_postcodes[postcode] += 1
    return unexpected_postcodes

def audit_phone(filename):
    return None

def audit_website(filename):
    return None

if __name__ == '__main__':
    audit_option = sys.argv[1]
    audit_filename = sys.argv[2]
    UTF8Writer = codecs.getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)
    if audit_option == "street":
        street_types = audit_street(audit_filename)
        for street_type in street_types.keys():
            print(street_type)
            for street_name in street_types[street_type]:
                print("\t" + street_name)
        #pprint.pprint(dict(street_types))
    elif audit_option == "postcode":
        post_codes = audit_postcode(audit_filename)
        for code, count in post_codes.items():
            print(code + " | " + str(count))
    elif audit_option == "phone":
        audit_phone(audit_filename)
    elif audit_option == "website":
        audit_website(audit_filename)
    else:
        print "Incorrect audit option. Choose from: street, postcode, phone, website."
