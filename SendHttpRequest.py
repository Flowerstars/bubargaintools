#!/usr/bin/python

import httplib, urllib, json, getopt, sys



g_server = {}



def http_GET():
    global g_server
    conn = g_server.get("conn")
    url = g_server.get("url")
    http_headers = {"Content-type":"application/json"}
    http_body = ("")
    print "[INFO]: Start sending HTTP GET request to url: " + url
    conn.request("GET", url, http_body, http_headers)
    response = conn.getresponse()
    data = response.read()
    print "[INFO]: " + str(response.status), response.reason
    if (response.status >= 200 and response.status <= 299):
        print "[INFO]: Reply from server: " + data
        print "[INFO]: HTTP GET request Successfully!"
        return True
    else:
        print "[ERROR]: Error Info: " + data  
        print "[INFO]: HTTP GET request Failed!"
        return False


def http_POST(body):
    global g_server
    conn = g_server.get("conn")
    url = g_server.get("url")
    http_headers = {"Content-type":"application/json"}
    http_body = urllib.urlencode(body)
    print "[INFO]: Start sending HTTP POST request to url: " + url + "with the body: " + body
    conn.request("POST", url, http_body, http_headers)
    response = conn.getresponse()
    data = response.read()
    print "[INFO]: " + str(response.status), response.reason
    if (response.status >= 200 and response.status <= 299):
        print "[INFO]: Reply from server: " + data
        print "[INFO]: HTTP POST request Successfully!"
        return True
    else:
        print "[ERROR]: Error Info: " + data  
        print "[INFO]: HTTP POST request Failed!"
        return False



def main():
    global g_server
    host = "localhost:8888"
    try:  
        opts,args = getopt.getopt(sys.argv[1:],"h:m:u:b:s:")  
        for op,value in opts:  
            if op == "-h":  
                host = value  
            elif op == "-m":
                method  = value
            elif op == "-u":
                url = value
            elif op == "-b":  
                body = value 
        #print(opts)  
        #print(args)  
    except getopt.GetoptError:  
        print("[ERROR]: Params are not defined well!")
        sys.exit(1) 
    
    if (('method' not in dir() or 'url' not in dir()) or (0 == cmp(method.upper(), "POST") and 'body' not in dir())):
        print "[INFO]: Please give params: method, url and the content.\n"
        sys.exit(1) 
    elif (cmp(host, "localhost") != 0):
        print "[INFO]: Use default host: localhost."
    else:
        print "[INFO]: Use Host: " + host  
    
    conn = httplib.HTTPConnection(host)
    g_server = {"conn":conn, "url":url}

    if (0 == cmp(method.upper(), "GET")):
        http_GET()
    elif (0 == cmp(method.upper(), "POST")):
        http_POST(body)
    else:
        print "[ERROR]: Other methods has not implemented yet, except GET and POST."
    conn.close()


#if __name__ =="__main__":
print "\n"
main()
print "\n"


