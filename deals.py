#!/usr/bin/python

#-*- coding: utf-8 -*-

import xml.etree.ElementTree as xml
import MySQLdb
import time
import sys, getopt


g_shop_id_wanggou	= 1
g_city_id		= 2419
g_stored_count		= 0
g_missing_deal		= []


def parse_deals(conn, file_name):
    global g_missing_deal
    deal_shops_records = []
    deal_num = 0
    tree = xml.parse(file_name)
    root = tree.getroot()
    count = root.attrib['count']
    deals = root.findall("url")
    if deals != None:
        for deal in deals:
           deal_num += 1
           print "=====================================>>>>> [count " + str(deal_num) + "]:"
           data = deal.find("data")
           if data != None:
               display = data.find("display")
               cat_id = get_cat_id(display, conn)
               pic_id = get_pic_id(display, conn)
               title = get_child_content(display, "title")
               value = get_child_content(display, "value")
               price = get_child_content(display, "price")
               discount = get_child_content(display, "rebate")
               bought = get_child_content(display, "bought")
               deal_info = get_child_content(display, "detail")
               start_time = get_time_content(display, "startTime")
               end_time = get_time_content(display, "endTime")
               
               if (None == cat_id or None == pic_id or None == title or None == value or None == price or None == discount or None == bought or None == deal_info or None == start_time or None == end_time):
                   g_missing_deal.append(deal_num)
                   print "[PARSE]: The deal ID is: " + str(deal_num)
                   print "[PARSE]: Miss a Important Value!!! Go To Next Dirsctly! ============================================<<<>>><<<>>><<<>>><<<>>><<<>>>"
                   continue;
   
               deal_record = (cat_id, pic_id, title, value, price, discount, bought, deal_info, start_time, end_time) 
               check_deal_record = (str(cat_id), str(pic_id), title, str(value), str(price), str(discount), deal_info, start_time, end_time)
               if (True == is_exist(conn, check_deal_record)):
                   print "[WARNING]: This Deal has been stroed in database before!!! -=-=-=-=-=-=-=-=-=-=-=-=-=->>>>>"
                   continue;
   
               shops_record = get_shops(display)
               deal_shops_records = [deal_record, shops_record]
               if (store_deals_shops(conn, deal_shops_records)):
                   print "=================================================>>>>>  " + str(deal_num)  + " STORED OKOKOKOK!!!"
               else:
                   print "<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<  " + str(deal_num)  + " STORED  NONONONO!!!"
    else:
        print "There is no deals in the xml file."
    return True

def is_exist(conn, deal_record):
    sql = "select deal_id from deals where cat_id=%s and pic_id=%s and title=%s and value=%s and price=%s and discount=%s and deal_info=%s and start_time=%s and end_time=%s"
    param = deal_record
    cursor = conn.cursor()
    n = cursor.execute(sql, param)
    print "[DEAL_EXIST]: after select, n = " + str(n)
    if (0 == n):
        print "[DEAL_EXIST]: This is a new deal."
        cursor.close()
        return False
    elif (n > 0):
        print "[DEAL_EXIST]: This is an existing deal!"
        cursor.close()
        return True
    else:
        print "[DEAL_EXIST]: FAILED WHEN SELECT DB"
        cursor.close()
        conn.close()
        print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
        sys.exit(1)


def get_shops(display):
    shops_record = []
    shops = display.find("shops")
    shops_content = shops.findall("shop")
    if (shops_content != None):
        for shop in shops_content:
            print "---------------->>>>> SHOP --->>"
            name = get_child_content(shop, "name")
            tel = get_child_content(shop, "tel")
            addr = get_child_content(shop, "addr")
            longitude = get_child_content(shop, "longitude")
            latitude = get_child_content(shop, "latitude")
            shop_record = (name, name, longitude, latitude, g_city_id, addr, tel)
            shops_record.append(shop_record)
    else:
        print "[SHOPS]: There is no shop tag"
    return shops_record



def get_child_content(parent, child_tag):
    child = parent.find(child_tag)
    if (child != None):
        child_content = child.text
        if (child_content != None):
            print "[" + child_tag.upper() + "]: " + child_content
        else:
            print "[" + child_tag.upper() + "]: NO CONTENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
        return child_content
    else:
        print "[" + child_tag.upper() + "]: **<< GOT NOTHING >>**"
        return None


def get_time_content(parent, time_tag):
    t = parent.find(time_tag)
    if (t != None):
        if (t != None):
            t_content = time.strftime('%Y-%m-%d %X',time.localtime(int(t.text)))
            print "[" + time_tag.upper() + "]: " + t_content
            return t_content
        else:
            print "[" + time_tag.upper() + "]: NO CONTENT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
            return None
    else:
        print "[" + time_tag.upper() + "]: **<< GOT NOTHING  >>**" 
        return None


def get_pic_id(display, conn):
    pic = display.find("image")
    small_pic = display.find("small_image")
    if (None == pic or None == small_pic):
        print "[PIC]: **<< GOT NOTHING  >>**"
        return None 
    pic_content = pic.text
    small_pic_content = small_pic.text
    if (None == pic_content or None == small_pic_content):
        print "[PIC]: **<<< NO CONTNET  >>**"
        return None
    cursor = conn.cursor()
    sql = "select pic_id from pictures where pic_link = %s"
    param = (pic_content)
    n = cursor.execute(sql, param)
    print "[PIC]: after select, n = " + str(n)
    if (0 == n):
        print "[PIC]: This is a new pic."
        sql = "insert into pictures (pic_link, small_pic_link) values(%s, %s)"
        param = (pic_content, small_pic_content)
        n = cursor.execute(sql, param)
        if (1 == n):
            print "[PIC]: insert successfully, id = " + str(conn.insert_id())
            pic_id = conn.insert_id()
            conn.commit()
        else:
            print "[PIC]: FAILED insert into cate"
	    cursor.close()
            conn.close()
            print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
            sys.exit(1)
    else:
        row = cursor.fetchone()
        print row
        print "[PIC]: row[0] = " + str(row[0])
        pic_id = row[0]
    cursor.close()
    return pic_id



def get_cat_id(display, conn):
    cate = display.find("cate")
    if (None == cate):
        print "[CAT]: **<<GOT NOTHING>>**"
        return None
    cate_content = cate.text
    if (None == cate_content):
        print "[CAT]: **<<  NO CONTENT  >>**"
        return None
    cursor = conn.cursor()
    sql = "select cat_id from categories where cat_name = %s"
    param = (cate_content)
    n = cursor.execute(sql, param)
    print "[CAT]: after select, n = " + str(n)
    if (0 == n):
        print "[CAT]: This is a new category."
        sql = "insert into categories (cat_name, par_id) values(%s, %s)"
        param = (cate_content, 0)
        n = cursor.execute(sql, param)
        if (1 == n):
            print "[CAT]: insert successfully, id = " + str(conn.insert_id())
            cat_id = conn.insert_id()
            conn.commit()
        else:
            print "[CAT]: FAILED insert into cate"
            cursor.close()
            conn.close()
            print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
            sys.exit(1)
    else:
        row = cursor.fetchone()
        print row
        print "[CAT]: row[0] = " + str(row[0])
        cat_id = row[0]
    cursor.close()
    return cat_id




def store_deals_shops(conn, data):
    global g_stored_count
    shops_id = []
    cursor = conn.cursor()
    sql_deal = "insert into deals (cat_id, pic_id, title, value, price, discount, bought, deal_info, start_time, end_time) values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_shop = "insert into merchants (mer_name, mer_info, location_long, location_lat, city_id, address, tel) values(%s, %s, %s, %s, %s, %s, %s)"
    param_deal = data[0]
    #print "[STORE_DEAL]: param_deal = ", param_deal
    n = cursor.execute(sql_deal, param_deal)
    if (1 == n):
        print "[STORE_DEALS]: Store OK!"
        deal_id = conn.insert_id()
        print "[STORE_DEAL]: deal_id = " + str(deal_id)
        conn.commit()
        num_shops = len(data[1])
        print "[STORE_SHOP]: number of shops are: " + str(num_shops)
        if (num_shops > 0):
            for num in range(0, num_shops):
                param_shop = data[1][num]
                #print "[STORE_SHOP]: Current para_shop = ", param_shop
                n = cursor.execute(sql_shop, param_shop)
                if (1 == n):
                    print "[STORE_SHOP]: Store OK!"
                    shop_id = conn.insert_id()
                    conn.commit()
                    shops_id.append(shop_id)
                else:
                    print "[STORE_SHOP]: Store Error!"
                    cursor.close()
                    conn.close()
                    print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
                    sys.exit(1)
        elif (0 == num_shops): # wanggou
            print "[STROE_SHOP]: wanggou"
            shops_id.append(g_shop_id_wanggou)
    else:
        print "[STORE_DEALS]: Store Error!"
        cursor.close()
        conn.close()
        print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
        sys.exit(1)
    cursor.close()

    if (store_deal_shop_map(conn, deal_id, shops_id)):
        g_stored_count += 1
        print "[STORE_MAP]: OK!"
        return True
    else:
        print "[STORE_MAP]: Error!"      
        return False


def store_deal_shop_map(conn, deal_id, shops_id):
    dm_records = []
    cursor = conn.cursor()
    num_shops = len(shops_id)
    for num in range(0, num_shops):
        dm_records.append((deal_id, shops_id[num]))
    sql = "insert into deal_mers_map (deal_id, mer_id) values(%s, %s)"
    param = (dm_records)
    n = cursor.executemany(sql, param)
    if (n == num_shops):
        cursor.close()
        conn.commit()
        print "[STORE_DM_MAP]: OK!"
        return True
    else:
        cursor.close()
        print "[STORE_DM_MAP]: Error!"
        return False


def main():
    file_name = None
    try:
        opts,args = getopt.getopt(sys.argv[1:],"f:")
        for op,value in opts:
          if op == "-f":
            file_name = value
    except getopt.GetoptError:
        print("[ERROR]: Params are not defined well!")
        print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
        sys.exit(1)
    if (None == file_name):
        print "[ERROR]: Please give the parsed file name and path."
        print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
        sys.exit(1)
    conn = MySQLdb.connect(host="ec2-50-18-17-238.us-west-1.compute.amazonaws.com", user="root", passwd="RooT", db="CDC", charset="utf8")
    parse_deals(conn, file_name)
    conn.close()
    print "[INFO]: Stored " + str(g_stored_count) + " New Deals In Total!"
    print "[INFO]: Missing Value Deals are: "
    print g_missing_deal
    


if __name__ == "__main__":
    main()

