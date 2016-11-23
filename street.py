# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from bs4 import BeautifulSoup
import requests
import urllib2

# url of page of kyrgyz post website, which contains the most of existing streets in Kyrgyzstan (but not all)
kyrgyz_post_url = "http://kyrgyzpost.kg/ru/zipcodes-search.html?e%5B_itemcategory%5D%5B%5D=&e%5B6e61c763-659a-4bf2-8d0b-1fd1151b357f%5D=&limit=all&order=alpha&logic=and&send-form=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&controller=search&Itemid=356&option=com_zoo&task=filter&exact=0&type=otdelenie-svyazi&app_id=9"

# list of possible full street types
expected_street_types = [unicode("улица", 'utf8'), unicode("переулок", 'utf8'), unicode("проспект", 'utf8'), unicode("площадь", 'utf8'), unicode("микрорайон", 'utf8'), unicode("тупик", 'utf8'), unicode("бульвар", 'utf8'), unicode("село", 'utf8')]

# map from abbreviations and misspellings of street types to the full street types
street_type_mapping = {
            unicode("ул", 'utf8'): unicode("улица", 'utf8'),
            unicode("ул.", 'utf8'): unicode("улица", 'utf8'),
            unicode("Str", 'utf8'): unicode("улица", 'utf8'),
            unicode("Str.", 'utf8'): unicode("улица", 'utf8'),
            unicode("St", 'utf8'): unicode("улица", 'utf8'),
            unicode("St.", 'utf8'): unicode("улица", 'utf8'),
            unicode("Улица", 'utf8'): unicode("улица", 'utf8'),
            unicode("улица", 'utf8'): unicode("улица", 'utf8'),
            unicode("с.", 'utf8'): unicode("село", 'utf8'),
            unicode("мкр", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("мкр.", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("м/р-н", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микра", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("Микрорайон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрарайон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрорайон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микраройон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрорайно", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("микрораон", 'utf8'): unicode("микрорайон", 'utf8'),
            unicode("пер", 'utf8'): unicode("переулок", 'utf8'),
            unicode("пер.", 'utf8'): unicode("переулок", 'utf8'),
            unicode("прe", 'utf8'): unicode("переулок", 'utf8'),
            unicode("пре.", 'utf8'): unicode("переулок", 'utf8'),
            unicode("перулок", 'utf8'): unicode("переулок", 'utf8'),
            unicode("переулок", 'utf8'): unicode("переулок", 'utf8'),
            unicode("проспект", 'utf8'): unicode("проспект", 'utf8'),
            unicode("Strasse", 'utf8'): unicode("проспект", 'utf8'),
            unicode("Avenue", 'utf8'): unicode("проспект", 'utf8'),
            unicode("blvrd.", 'utf8'): unicode("бульвар", 'utf8')
            }

# manually prepared map from some street names (which exist, but not presented on kyrgyz post site) to the street names with street types
manual_street_name_mapping = {
    unicode("Джал-15 (Джал Артис)", 'utf8'): unicode("Джал Арча микрорайон", 'utf8'),
    unicode("Озёрная", 'utf8'): unicode("Oзерная улица", 'utf8'),
    unicode("Верхний Кокжар", 'utf8'): unicode("Верхний Кокжар село", 'utf8'),
    unicode("dreevesnaja", 'utf8'): unicode("Древесная улица", 'utf8'),
    unicode("Абаканская - Баетово", 'utf8'): unicode("Абаканская улица", 'utf8'),
    unicode("Молодая Гвардия", 'utf8'): unicode("Молодая Гвардия проспект", 'utf8'),
    unicode("Верхний Джал", 'utf8'): unicode("Верхний Джал микрорайон", 'utf8'),
    unicode("Мирная", 'utf8'): unicode("Мирная улица", 'utf8'),
    unicode("Ленина", 'utf8'): unicode("Чуй проспект", 'utf8'),
    unicode("Тыналиева", 'utf8'): unicode("Тыналиева улица", 'utf8'),
    unicode("он-арча", 'utf8'): unicode("Он Арча улица", 'utf8'),
    unicode("Карла Маркса", 'utf8'): unicode("Юнусалиева проспект", 'utf8'),
    unicode("Летняя", 'utf8'): unicode("Летняя улица", 'utf8'),
    unicode("Белинского", 'utf8'): unicode("Манаса проспект", 'utf8'),
    unicode("Горький - Матросов", 'utf8'): unicode("Горького улица", 'utf8'),
    unicode("Жилгородок совмина", 'utf8'): unicode("Совмина микрорайон", 'utf8'),
    unicode("Сатке", 'utf8'): unicode("Сатку улица", 'utf8'),
    unicode("Т-Молдо", 'utf8'): unicode("Т. Молдо улица", 'utf8'),
    unicode("Спортивная", 'utf8'): unicode("Спортивная улица", 'utf8'),
    unicode("Горький", 'utf8'): unicode("Горького улица", 'utf8'),
    unicode("Жилой комплекс \"Юг-7\"", 'utf8'): unicode("Юг-7 микрорайон", 'utf8'),
    unicode("Ореховая", 'utf8'): unicode("Ореховая улица", 'utf8'),
    unicode("Скобелевская", 'utf8'): unicode("Скобелевская улица", 'utf8'),
    unicode("Мадиева", 'utf8'): unicode("Мадиева улица", 'utf8'),
    unicode("Сухэ-Батора", 'utf8'): unicode("Сухэ-Батора улица", 'utf8'),
    unicode("Восток-5 д. 1/2 Апам", 'utf8'): unicode("Восток-5 микрорайон", 'utf8'),
    unicode("Совхозная", 'utf8'): unicode("Совхозная улица", 'utf8'),
    unicode("Юлиуса Фучика", 'utf8'): unicode("Ю. Фучика улица", 'utf8'),
    unicode("Жылга-Сай", 'utf8'): unicode("Жылга-Сай улица", 'utf8'),
    unicode("Дабан", 'utf8'): unicode("Дабан улица", 'utf8')
}

# Returns list of streets from osm xml, which doesn't have an expected street type in the end
def audit_street(filename):
    unexpected_streets = set()
    with open(filename, 'r') as file:
        for _ , elem in ET.iterparse(file, events=("start",)):
            if elem.tag == "node" or elem.tag == "way":
                for tag in elem.iter("tag"):
                    if tag.attrib['k'] == "addr:street":
                        raw_street = tag.attrib['v']
                        if unicode(raw_street.strip().split(" ")[-1]) not in expected_street_types:
                            unexpected_streets.add(raw_street)
    return unexpected_streets

# Takes url (hardcoded url of kyrgyz post website) and returns set of existing street names with street types
def get_expected_streets(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "lxml")
    tds = []
    for table in soup.find_all("table"):
        for td in table.find_all("td"):
            tds.append(td.get_text().strip())
    expected_streets = set()
    for street in tds[::3]:
        expected_streets.add(street)
    return expected_streets

# Takes a string of raw street and returns it with street type in standard format if possible. Otherwise returns None.
def fix_street_type(raw_street):
    if raw_street == None:
        return None
    # check if the street type in the end of raw street
    street_type = unicode(raw_street.strip().split(" ")[-1])
    street_without_type = " ".join(unicode(raw_street.strip().split(" ")[:-1])) + " "
    if street_type not in street_type_mapping:
        # check if the street type in the beginning of raw street
        street_type = unicode(raw_street.strip().split(" ")[0])
        street_without_type = " ".join(unicode(raw_street.strip().split(" ")[1:])) + " "
        if street_type not in street_type_mapping:
            # check if the street type is the abbreviation in the end of raw street
            street_type = unicode(raw_street.strip()[:4])
            street_without_type = unicode(raw_street.strip()[4:]) + " "
            if street_type not in street_type_mapping:
                # check if the street type is the abbreviation in the beginning of raw street
                street_type = unicode(raw_street.strip()[-3:])
                street_without_type = unicode(raw_street.strip()[:-3]) + " "
                if street_type not in street_type_mapping:
                    return None
    return street_without_type + street_type_mapping[street_type]


# Takes a string of raw street and returns it in standard format. Manually prepared fixing is performing for existing raw streets.
# However, for non existing streets function returns None.
def fix_street(raw_street, expected_streets):
    # Check manually prepared map of existing raw streets
    if raw_street in manual_street_name_mapping:
        return manual_street_name_mapping[raw_street]
    # Try to fix street type to standard format
    fixed_street = fix_street_type(raw_street)
    if fixed_street == None:
        # Try to get street type from expected streets (from kyrgyz post website)
        expected_street = None
        for street in expected_streets:
            if street.find(raw_street.strip()) != -1:
                expected_street = street
                break
        fixed_street = fix_street_type(expected_street)
        if fixed_street == None:
            return None
    return fixed_street


# Creates new osm xml file, which contains all streets in standard format: <street name> <full street type>
def clean_street(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    expected_streets = get_expected_streets(kyrgyz_post_url)
    for child in root:
        if child.tag == "node" or child.tag == "way":
            for tag in child.iter("tag"):
                if tag.attrib['k'] == "addr:street":
                    raw_street = tag.attrib['v']
                    if unicode(raw_street.strip().split(" ")[-1]) not in expected_street_types:
                        fixed_street = fix_street(raw_street, expected_streets)
                        if fixed_street == None:
                            #print(raw_street + " is not a street")
                            child.remove(tag)
                        else:
                            tag.attrib['v'] = fixed_street
    tree.write("cleaned_street_" + filename, encoding='utf-8')



