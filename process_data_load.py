#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

mapping = { "St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.":"Road",
            "Cir": "Circle",
            "Pkwy":"Parkway",
            "Dr":"Drive",
            "Ct": "Court"}

def update_name(name, mapping):
    m = street_type_re.search(name)
    street_type = m.group()
    mapping[street_type]
    return name.replace(street_type, mapping[street_type])


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]




def shape_element(element):
    node = {}
    
    if element.tag == "node" or element.tag == "way":
        
        address_dic = {}
        nd_list = []
        
        for tag in element.iter("tag"):
            
            att = tag.attrib['k'] 
        
            if problemchars.search(att):
                continue
                
            elif tag.attrib['k'].startswith("addr:") and len(tag.attrib['k'].split(':')) < 3:
                
                if att.find('street')>-1:
                    address_dic['street']=update_name(tag.attrib['v'],mapping)
                    
                elif att.find('housenumber')>-1:
                    address_dic['housenumber']=tag.attrib['v']
                    
                elif att.find('postcode')>-1:
                    address_dic['postcode']=tag.attrib['v']
                    
            elif not tag.attrib['k'].startswith("addr:") and len(tag.attrib['k'].split(':')) < 3:
                node[tag.attrib['k']] = tag.attrib['v']
 
        if bool(address_dic):        
            node['address']  = address_dic    

        node['type'] = element.tag
        
        for tag in element.iter('nd'):
            nd_list.append(tag.attrib['ref'])
        
        if len(nd_list) > 0:
            node['node_refs'] = nd_list 
            
        created_dic = {}            
        pos_list = [None,None]
        
        for key,val in element.items():
            
            if key == 'lat':
                pos_list[0] = float(val)
            elif key == 'lon':
                pos_list[1] = float(val)
            elif key in CREATED:
                created_dic[key] = val
            else:
                node[key] = val
            
        node['created'] = created_dic
        node['pos'] = pos_list
        
        return node
    else:
        return None    


def process_map(file_in, pretty = False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data

if __name__ == '__main__':
    process_map(file_in,pretty = False)
    
    