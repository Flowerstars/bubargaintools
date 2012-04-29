#!/usr/bin/python

#-*- coding: utf-8 -*-

import xml.etree.ElementTree as xml
import MySQLdb

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
        #   print "name = " + name.text + "code = " + code.text
    else:
        print "There is no cities in the xml file."
    return city_infos




def storeDB(data):
   # conn = MySQLdb.connect(host="localhost", user="root", passwd="RooT", db="CDC")
    conn = MySQLdb.connect(host="ec2-50-18-17-238.us-west-1.compute.amazonaws.com", user="root", passwd="RooT", db="CDC", charset="utf8")
    cursor = conn.cursor()
    sql = "insert into citis (city_name, city_code) values(%s, %s)"
    param = (data)

    #print "db.charset = " + db.charset
    #print "conn.charset = " + conn.charset

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
    cities = parse_cities()
    print cities
    if (True == storeDB(cities)):
        print "[INFO]: STORE DB SUCCESSFULLY!"
    else:
        print "[INFO]: STORE FAILED!"


if __name__ == "__main__":
    main()

