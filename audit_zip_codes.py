#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

zipcode_re = re.compile(r'^\d{5}(?:[-\s]?\d{4})?$', re.IGNORECASE)


def audit_zip_code(zip_code_types, zip_code):
    m = zipcode_re.search(zip_code)
    if not m:
        #zip_code_type = m.group()
        zip_code_types[zip_code].add(zip_code)


def is_zip_code(elem):
    return (elem.attrib['k'] == "addr:postcode")


def audit_zip(osmfile):
    osm_file = open(osmfile, "r")
    zip_code_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zip_code(tag):
                    audit_zip_code(zip_code_types, tag.attrib['v'])
    osm_file.close()
    return zip_code_types

if __name__ = '__main__':
    
    audit_zip(osmfile)