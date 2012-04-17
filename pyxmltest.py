#!/usr/bin/python
# -*- coding: utf-8 -*-


import xml.etree.ElementTree as xml
import MySQLdb


def write_xml():
    root = xml.Element('root')
    child = xml.Element('child')
    root.append(child)

    child.attrib['name'] = "Charlie"

    file  = open("writexml.xml", "w")
    xml.ElementTree(root).write(file)

    file.close()


def read_xml():
    tree = xml.parse("deals.xml")
    root = tree.getroot()
    count = root.attrib['count']
    print "count = " + count   
   
    url_list = root.findall("url")
    if url_list != None:
        for url in url_list:
            data = url.find("data")
            if data != None:
                cate = data.find("display").find("cate")
                if cate != None:
                    cate_name = cate.text
                    print "cate_name = " + cate_name
                else:
                    print "NO cate tag"
            else:
                print "no data"
    else:
        print "no urls"


   # if childlist != None:
    #    for child in childlist:
     #       print child.attrib['name']




def parse_cities():
    city_infos = []
    tree = xml.parse("cities.xml")
    root = tree.getroot()
    cities = root.findall("city")
    if cities != None:
        for city in cities:
           name = city.find("name")
           code = city.find("id")
           city_info = (name.text, code.text)
           city_infos.append(city_info)
           print "name = " + name.text + "code = " + code.text
    else:
        print "There is no cities in the xml file."
    return city_infos




def storeDB(data):
   # conn = MySQLdb.connect(host="localhost", user="root", passwd="RooT", db="CDC")
    conn = MySQLdb.connect(host="ec2-50-18-17-238.us-west-1.compute.amazonaws.com", user="root", passwd="RooT", db="CDC")
    cursor = conn.cursor()
    sql = "insert into citis (city_name, city_code) values(%s, %s)"
    param = (data)
    n = cursor.executemany(sql, param)
    print "Doing " + str(n) + "Records."
    conn.commit()
    cursor.close()
    conn.close()
    if (0 != n):
        return True
    else:
        return False


def main():
    #write_xml()
    #read_xml()
    cities = parse_cities()
    print cities
#    cities = [("shanghai", "4444"), ("beijing", "1111"), ("tianjin", "2222")]
    if (True == storeDB(cities)):
        print "[INFO]: STORE DB SUCCESSFULLY!"
    else:
        print "[INFO]: STORE FAILED!"


if __name__ == "__main__":
    main()

