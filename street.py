# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict

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