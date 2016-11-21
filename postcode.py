from lxml import html
import requests
import xml.etree.cElementTree as ET

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