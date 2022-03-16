"""
Veeeery simplistic webserver which serves all files from a specific directory
TODO:
- handle file names and directories more generic
- Maybe HTML output as well?
- Test, test, test
- timeout if nobody is connected after n seconds
"""


import usocket as socket
import os
import ujson as json
import gc
gc.collect()
import network
#import time

n = 1

class SimpleWebserver(object):

    def serve_index_1(self, conn):
        

        html1 = """<html><head> <title>Navel Project: Mark-1</title> <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
        border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
        .button2{background-color: #4286f4;}</style></head><body> <h1>Navel Project: Mark-1</h1>
        </strong></p><p><a href="/?sds"><button class="button">Shut down server</button></a></p>
        <p><a href="/?po"><button class="button">Show data</button></a></p></body></html>"""
                        
        conn.send(html1)
    
    def data_page(self, conn):
        global n
        files = os.listdir('/sd')
        response1 = str()
        html2 = str()
        ls = files[(n*4-4):(4*n)]
        file_len = str(len(files))
        for f in ls:
            response1 = response1 + """<p><a href= """ + '/'+ f + """><button class="button"> """ + f + """</button></a></p>"""
        print(ls)
        html2 = """<html> <head> <title>Data Files:</title> <meta name="viewport" content="width=device-width, height=100%, initial-scale=1">
        <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
        h1{color: #0F3376; padding: 2vh;}p{font-size: 0.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
        border-radius: 2px; color: white; padding: 8px 20px; text-decoration: none; font-size: 15px; margin: 1px; cursor: pointer;}
        </style></head><body><h1>Data Files</h1></strong></p>""" + response1 + """<p><a href="/?nxt"><button class="button">Next page</button></a></p>
        <p><a href="/"><button class="button">Home page</button></a></p><p>Number of Data files =""" +file_len+ """</p> </body></html>"""
        conn.send(html2)
    

    def serve_file(self, conn, file):
        files = os.listdir('/sd')
        if file in files:
            conn.sendall('HTTP/1.0 200 OK\r\nContent-type: application/json\r\n\r\n')
            conn.sendall('[')
            with open('/sd/'+file, "r") as infile:
                isfirst = True
                for line in infile:
                    if not isfirst:
                        conn.send(",")
                    else:
                        isfirst = False
                    conn.sendall(line)
            conn.sendall(']')



    def serve(self):
        
        global n
        
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(password="navel2021")
        while ap.active() == False:
            pass
        print(ap.ifconfig())

        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        s = socket.socket()
        s.bind(addr)
        s.listen(1)

        print('listening on', addr)

        while True:
            cl, addr = s.accept()
            cl.setblocking(True)
            print('client connected from', addr)
            cl_file = cl.makefile('rwb', 0)
            url = ""
            while True:
                line = cl_file.readline()
                #print(line.decode("utf-8"))
                if line.decode("utf-8").startswith("GET "):
                    get_params = line.decode("utf-8").split(" ")
                    if len(get_params) > 2:
                        url = get_params[1]
                if not line or line == b'\r\n':
                    break

            if url[1:] in os.listdir('/sd'):
                self.serve_file(cl, url[1:])
            elif url[1:] == '?po':
                n = 1
                self.data_page(cl)
            elif url[1:] == '?nxt':
                n = n+1
                self.data_page(cl)
            elif url[1:] == '?sds':
                ap.active(False)
                break            
            else:
                self.serve_index_1(cl)
            cl.close()