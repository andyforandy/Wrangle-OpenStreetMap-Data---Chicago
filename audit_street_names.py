import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

OSMFILE = "chicago_illinois.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons",'Terrace','Broadway','Highway','Circle','Park','Plaza','Way','West']

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.":"Road",
            "Cir": "Circle",
            "Pkwy":"Parkway",
            "Dr":"Drive",
            "Ct": "Court"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected and street_type in mapping:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types


def update_name(name, mapping):
    m = street_type_re.search(name)
    street_type = m.group()
    mapping[street_type]
    return name.replace(street_type, mapping[street_type])


def test():
    st_types = audit(OSMFILE)

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name

if __name__=='__main__':
    test()