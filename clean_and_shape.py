import csv
import sys, codecs
import re
import xml.etree.cElementTree as ET
import street
import phone
import postcode
import website

# url of page of kyrgyz post website, which contains the most of existing streets in Kyrgyzstan (but not all). Will be scraped for needs of data cleaning
kyrgyz_post_url = "http://kyrgyzpost.kg/ru/zipcodes-search.html?e%5B_itemcategory%5D%5B%5D=&e%5B6e61c763-659a-4bf2-8d0b-1fd1151b357f%5D=&limit=all&order=alpha&logic=and&send-form=%D0%98%D1%81%D0%BA%D0%B0%D1%82%D1%8C&controller=search&Itemid=356&option=com_zoo&task=filter&exact=0&type=otdelenie-svyazi&app_id=9"

OSM_PATH = "Bishkek.osm"

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS, problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements

    # handle tags
    for tag in element.iter("tag"):
        tag_attribs = {}
        k = tag.attrib['k']
        if problem_chars.match(k):
            pass
        if LOWER_COLON.match(k):
            colon_pos = k.find(':')
            tag_attribs['type'] = k[:colon_pos]
            tag_attribs['key'] = k[(colon_pos + 1):]
        else:
            tag_attribs['type'] = default_tag_type
            tag_attribs['key'] = k


        # perform the cleaning
        if k == "addr:street":
            fixed_street = street.fix_street(tag.attrib['v'], expected_streets)
            if fixed_street:
                tag_attribs['value'] = fixed_street
            else:
                pass
        elif k == "phone":
            fixed_phone = phone.fix_phone(tag.attrib['v'])
            if fixed_phone:
                tag_attribs['value'] = fixed_phone
            else:
                pass
        elif k == "addr:postcode":
            fixed_postcode = postcode.fix_postcode(tag.attrib['v'])
            if fixed_postcode:
                tag_attribs['value'] = fixed_postcode
            else:
                pass
        elif k == "website":
            fixed_website = website.fix_website(tag.attrib['v'])
            if fixed_website:
                tag_attribs['value'] = fixed_website
            else:
                pass
        else:
            tag_attribs['value'] = tag.attrib['v']

        tag_attribs['id'] = element.attrib['id']
        tags.append(tag_attribs)

    if element.tag == 'node':
        # handle node_attribs
        for attr in node_attr_fields:
            node_attribs[attr] = element.attrib[attr]
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        # handle way_attribs
        for attr in way_attr_fields:
            way_attribs[attr] = element.attrib[attr]
        # handle way_nodes
        for nd in element.iter("nd"):
            way_node = {}
            way_node['id'] = element.attrib['id']
            way_node['node_id'] = nd.attrib['ref']
            way_node['position'] = len(way_nodes)
            way_nodes.append(way_node)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}


def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
                                                    k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in
                                                    row.iteritems()
                                                    })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


def process_map(file_in):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)


        #nodes_writer.writeheader()
        #node_tags_writer.writeheader()
        #ways_writer.writeheader()
        #way_nodes_writer.writeheader()
        #way_tags_writer.writeheader()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    #scrape necessary for cleaning data
    expected_streets = street.get_expected_streets(kyrgyz_post_url)
    process_map(OSM_PATH)