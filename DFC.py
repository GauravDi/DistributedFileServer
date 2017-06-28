import socket
import os
import hashlib
import time
import threading
import re
import sys

name={}
z=0
conf=sys.argv[1]
file=open(conf)
i=0
for line in file:                                                      #Parsing dfc.conf file
    if line:
        a=line.split(':')
        if i==0:
            port=a[1][:-1]
            print("port:",port)
            ip=a[0].split(' ')
            IP=ip[2]
            print("IP:",IP)
            i=i+1
        elif i==1:
            port1=a[1][:-1]
            print("port1:",port1)
            i=i+1
        elif i==2:
            port2=a[1][:-1]
            print("port2:",port2)
            i=i+1
        elif i==3:
            port3=a[1][:-1]
            print("port3:",port3)
            i=i+1
        elif i==4:
            Uname=a[1][:-1]
            print("USERNAME:",Uname)
            i=i+1
        elif i==5:
            Pword=a[1]
            print("PASSWORD:",Pword)


sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          #Create sockets for each server     
sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  

DFS1=(IP, int(port))
DFS2=(IP, int(port1))
DFS3=(IP, int(port2))
DFS4=(IP, int(port3))
try:
    sock1.connect(DFS1)
except:
    print("COULD NOT CONNECT")
try:
    sock2.connect(DFS2)
except:
    print("COULD NOT CONNECT")
try:
    sock3.connect(DFS3)
except:
    print("COULD NOT CONNECT")
try:
    sock4.connect(DFS4)
except:
    print("COULD NOT CONNECT")

def cmd():                                                  #Function for continuous looping
    filen=raw_input("Enter File Name:")
    hash=hashlib.md5()
    with open(filen,'rb') as fh:
        buffer=fh.read()
        hash.update(buffer)
        digest=hash.hexdigest()
        number=int(digest,16)
        x=int(number%4)
        print("X=",x)
    
    size=os.path.getsize(filen)
    size=int(size)
    print("FILESIZE:",size)
    siz=size/4
    print("PACKET SIZE:",siz)
    
    fh=open(filen,"rb")                                             #Dividing a file into pieces
    m=0
    while m<4:
        if m==0:
            fh.seek(0)
            with open("1"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==1:
            fh.seek(siz)
            with open("2"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==2:
            fh.seek(2*siz)
            with open("3"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==3:
            fh.seek(3*siz)
            with open("4"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1 
    answer=raw_input("ENTER COMMAND: ")
    if answer=="PUT"+filen:            
        PUT(filen,x)
    elif answer=="LIST":
        LIST(filen,x)
    elif answer=="GET"+filen:
        GET(filen,x) 
    elif answer=="TO":
        GET1(filen,x)    
            
def PUT(filen,x):                                                                        #PUT FUNCTION
    filen=filen
    x=x
    def putit(sock1,sock2,sock3,sock4):
        '''
        sock1.sendto("PUT",(IP,int(port)))
        sock2.sendto("PUT",(IP,int(port1)))
        sock3.sendto("PUT",(IP,int(port2)))
        sock4.sendto("PUT",(IP,int(port3)))
        '''
        if x==0:
            try:
                sock1.sendto(filen,(IP,int(port)))
                print("FILENAME:",filen)
                dat=sock1.recv(1024)
                if dat:
                    print(dat)
            except:
                print("COULD NOT SEND/RECEIVE")
            try:
                sock2.sendto(filen,(IP,int(port1)))
                print("FILENAME:",filen)
                dat1=sock2.recv(1024)
                if dat1:
                    print(dat1)
            except:
                print("COULD NOT SEND/RECEIVE")
            try:          
                sock3.sendto(filen,(IP,int(port2)))
                print("FILENAME:",filen)
                dat2=sock3.recv(1024)
                if dat2:
                    print(dat2)
            except:
                print("COULD NOT SEND/RECEIVE")
            try:               
                sock4.sendto(filen,(IP,int(port3)))
                print("FILENAME:",filen)
                dat3=sock4.recv(1024)
                if dat3:
                    print(dat3)
            except:
                print("COULD NOT SEND/RECEIVE")
                    
            #time.sleep(10)
            time.sleep(1)
            
            fh=open("4"+filen)                                               #TO DFS1
            fh=fh.read()
            try:
                sock1.sendto(fh+"BGBVm"+"4"+filen,(IP,int(port)))
                print
                print("FILE PACKET 1 IS SENT")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK1 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:  
                sock4.sendto(fh+"BGBVm"+"4"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 1 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
           
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK2 FROM DFS4 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
                     
            fh1=open("1"+filen)
            fh1=fh1.read()
            try:
                sock1.sendto(fh1+"BGBVm"+"1"+filen,(IP,int(port)))
                print
                print("FILE PACKET 2 IS SENT to DFS1")
            except:
                print("COULD NOT SEND")
           
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(fh1+"BGBVm"+"1"+filen,(IP,int(port1)))
                print
                print("FILE PACKET 2 IS SENT TO DFS2")
            except:
                print("COULD NOT SEND")                                   # TO imgc                            
            
            try:
                data1=sock2.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS2 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
            fh=open("2"+filen)
            fh=fh.read()
            try:
                sock2.sendto(fh+"BGBVm"+"2"+filen,(IP,int(port1)))
                print
                print("FILE PACKET 3 IS SENT TO DFS2")
            except:
                print("COULD NOT SEND") 
            try:
                data=sock2.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            try:
                sock3.sendto(fh+"BGBVm"+"2"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 3 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
            try:
                data1=sock3.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS3 IS RECEIVED")   
            except:
                print("COULD NOT RECEIVE")
             
            fh1=open("3"+filen)
            fh1=fh1.read()
            try:
                sock3.sendto(fh1+"BGBVm"+"3"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 4 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock3.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS3 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            try:
                sock4.sendto(fh1+"BGBVm"+"3"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 4 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK1 FROM DFS4 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
                
        elif x==1:
            try:
                sock1.sendto(filen,(IP,int(port)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            
            try:
                dat=sock1.recv(1024)
                if dat:
                    print(dat)
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(filen,(IP,int(port1)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            
            try:
                dat1=sock2.recv(1024)
                if dat1:
                    print(dat1)
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock3.sendto(filen,(IP,int(port2)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            
            try:
                dat2=sock3.recv(1024)
                if dat2:
                    print(dat2)
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock4.sendto(filen,(IP,int(port3)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat3=sock4.recv(1024)
                if dat3:
                    print(dat3)
            except:
                print("COULD NOT RECEIVE")
            
                    
            #time.sleep(10)
            time.sleep(1)
            print("FILENAME:",filen[:-4])
            fh=open("1"+filen[:-4]+".txt","rb")                                               #TO DFS1
            fh=fh.read()
            try:
                sock1.sendto(fh+"BGBVm"+"1"+filen,(IP,int(port)))
                print
                print("FILE PACKET 1 IS SENT")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK1 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
           
            try:  
                sock4.sendto(fh+"BGBVm"+"1"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 1 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK2 FROM DFS4 IS RECEIVED")  
            except:
                print("COULD NOT RECEIVE")
            
            fh1=open("2"+filen[:-4]+".txt","rb")
            fh1=fh1.read()
            try:
                sock1.sendto(fh1+"BGBVm"+"2"+filen,(IP,int(port)))
                print
                print("FILE PACKET 2 IS SENT to DFS1")
            except:
                print("COULD NOT SEND")
           
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(fh1+"BGBVm"+"2"+filen,(IP,int(port1)))  
                print
                print("FILE PACKET 2 IS SENT TO DFS2")           
            except:
                print("COULD NOT SEND")                      # TO imgc                            
            
            try:
                data1=sock2.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
                 
            fh=open("3"+filen[:-4]+".txt","rb")
            fh=fh.read()
            try:
                sock2.sendto(fh+"BGBVm"+"3"+filen,(IP,int(port1)))
                print
                print("FILE PACKET 3 IS SENT TO DFS2")
            except:
                print("COULD NOT SEND")
            try:
                data=sock2.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock3.sendto(fh+"BGBVm"+"3"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 3 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock3.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS3 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
                   
            fh1=open("4"+filen[:-4]+".txt","rb")
            fh1=fh1.read()
            try:
                sock3.sendto(fh1+"BGBVm"+"4"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 4 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
        
            try:
                data=sock3.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS3 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock4.sendto(fh1+"BGBVm"+"4"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 4 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK1 FROM DFS4 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
        
        elif x==2:
            try:
                sock1.sendto(filen,(IP,int(port)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat=sock1.recv(1024)
                if dat:
                    print(dat)
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(filen,(IP,int(port1)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat1=sock2.recv(1024)
                if dat1:
                    print(dat1)
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock3.sendto(filen,(IP,int(port2)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat2=sock3.recv(1024)
                if dat2:
                    print(dat2)
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock4.sendto(filen,(IP,int(port3)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat3=sock4.recv(1024)
                if dat3:
                    print(dat3)
            except:
                print("COULD NOT RECEIVE")
            
                    
            #time.sleep(10)
            time.sleep(1)
            
            fh=open("3"+filen)                                               #TO DFS1
            fh=fh.read()
            try:
                sock1.sendto(fh+"BGBVm"+"3"+filen,(IP,int(port)))
                print
                print("FILE PACKET 1 IS SENT")
            except:
                print("COULD NOT SEND")
           
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK1 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:  
                sock4.sendto(fh+"BGBVm"+"3"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 1 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK2 FROM DFS4 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
                     
            fh1=open("4"+filen)
            fh1=fh1.read()
            try:
                sock1.sendto(fh1+"BGBVm"+"4"+filen,(IP,int(port)))
                print
                print("FILE PACKET 2 IS SENT to DFS1")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(fh1+"BGBVm"+"4"+filen,(IP,int(port1)))   
                print
                print("FILE PACKET 2 IS SENT TO DFS2")                         
            except:
                print("COULD NOT SEND")       # TO imgc                            
            
            try:
                data1=sock2.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            fh=open("1"+filen)
            fh=fh.read()
            try:
                sock2.sendto(fh+"BGBVm"+"1"+filen,(IP,int(port1)))
                print
                print("FILE PACKET 3 IS SENT TO DFS2")
            except:
                print("COULD NOT SEND")
            try:
                data=sock2.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock3.sendto(fh+"BGBVm"+"1"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 3 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock3.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS3 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
               
            fh1=open("2"+filen)
            fh1=fh1.read()
            try:
                sock3.sendto(fh1+"BGBVm"+"2"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 4 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
           
            try:
                data=sock3.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS3 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock4.sendto(fh1+"BGBVm"+"2"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 4 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK1 FROM DFS4 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            
        elif x==3:
            try:
                sock1.sendto(filen,(IP,int(port)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat=sock1.recv(1024)
                if dat:
                    print(dat)
            except:
                print("COULD NOT RECEIVE")
            
            try:    
                sock2.sendto(filen,(IP,int(port1)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat1=sock2.recv(1024)
                if dat1:
                    print(dat1)
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock3.sendto(filen,(IP,int(port2)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat2=sock3.recv(1024)
                if dat2:
                    print(dat2)
            except:
                print("COUL NOT RECEIVE")
            
            try:
                sock4.sendto(filen,(IP,int(port3)))
            except:
                print("COULD NOT SEND")
            print("FILENAME:",filen)
            try:
                dat3=sock4.recv(1024)
                if dat3:
                    print(dat3)
            except:
                print("COULD NOT RECEIVE")
            
                    
            #time.sleep(10)
            time.sleep(1)
            print("FILENAME:",filen[:-4])
            fh=open("2"+filen[:-4]+".txt","rb")                                               #TO DFS1
            fh=fh.read()
            try:
                sock1.sendto(fh+"BGBVm"+"2"+filen,(IP,int(port)))
                print
                print("FILE PACKET 1 IS SENT")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK1 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:  
                sock4.sendto(fh+"BGBVm"+"2"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 1 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK2 FROM DFS4 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
                     
            fh1=open("3"+filen[:-4]+".txt","rb")
            fh1=fh1.read()
            try:
                sock1.sendto(fh1+"BGBVm"+"3"+filen,(IP,int(port)))
                print
                print("FILE PACKET 2 IS SENT to DFS1")
            except:
                print("COULD NOT SEND")
            
            try:
                data=sock1.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS1 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock2.sendto(fh1+"BGBVm"+"3"+filen,(IP,int(port1)))   
                print
                print("FILE PACKET 2 IS SENT TO DFS2")                          
            except:
                print("COULD NOT SEND")                                 
            
            try:
                data1=sock2.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS2 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
                 
            fh=open("4"+filen[:-4]+".txt","rb")
            fh=fh.read()
            try:
                sock2.sendto(fh+"BGBVm"+"4"+filen,(IP,int(port1)))
                print
                print("FILE PACKET 3 IS SENT TO DFS2")
            except:
                print("COULD NOT SEND")
           
            try:
                data=sock2.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS2 IS RECEIVED")
            except:
                print("COULd NOT RECEIVE")
            
            try:
                sock3.sendto(fh+"BGBVm"+"4"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 3 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock3.recv(1024)
                if data1:
                    print
                    print(data1)
                    print("ACK1 FROM DFS3 IS RECEIVED") 
            except:
                print("COULD NOT RECEIVE")
            
                   
            fh1=open("1"+filen[:-4]+".txt","rb")
            fh1=fh1.read()
            try:
                sock3.sendto(fh1+"BGBVm"+"1"+filen,(IP,int(port2)))
                print
                print("FILE PACKET 4 IS SENT TO DFS3")
            except:
                print("COULD NOT SEND")
    
            
            try:
                data=sock3.recv(1024)
                if data:
                    print
                    print(data)
                    print
                    print("ACK2 FROM DFS3 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
            try:
                sock4.sendto(fh1+"BGBVm"+"1"+filen,(IP,int(port3)))
                print
                print("FILE PACKET 4 IS SENT TO DFS4")
            except:
                print("COULD NOT SEND")
            
            try:
                data1=sock4.recv(1024)
                if data1:
                    print
                    print(data1)
                    print
                    print("ACK1 FROM DFS4 IS RECEIVED")
            except:
                print("COULD NOT RECEIVE")
            
                
    threading.Thread(target=putit,args=(sock1,sock2,sock3,sock4)).start()                   #THREADING            
            
    print
    #time.sleep(11)
    time.sleep(2)
    answer=raw_input("ENTER COMMAND: ")
    if answer=="LIST":    
        LIST(filen,x)      
    
def LIST(filen,x):                                                              #FUNCTION FOR LIST
    filen=filen
    x=x
    try:
        sock1.sendto("LIST",(IP,int(port)))
    except:
        print("COULD NOT SEND")
    try:
        sock2.sendto("LIST",(IP,int(port1)))
    except:
        print("COULD NOT SEND")
    try:
        sock3.sendto("LIST",(IP,int(port2)))
    except:
        print("COULD NOT SEND")
    try:
        sock4.sendto("LIST",(IP,int(port3)))
    except:
        print("COULD NOT SEND")
    
     
    def sock(sock1,sock2,sock3,sock4):
        p=0
        q=0
        r=0
        s=0 
        try:
            sock1.sendto(filen,(IP,int(port)))
        except:
            print("COULD NOT SEND")
        try:
            sock2.sendto(filen,(IP,int(port1)))
        except:
            print("COULD NOT SEND")
        try:
            sock3.sendto(filen,(IP,int(port2)))
        except:
            print("COULD NOT SEND")
        try:
            sock4.sendto(filen,(IP,int(port3)))
        except:
            print("COULD NOT SEND")
        try:
            dat=sock1.recv(1024)
            if dat:
                dat1=dat.split("+")
                dat2=dat1[0].split(",")
                #print("FILES:",dat2)
            v=0
            print
            print("LIST:")
            print
            while v<dat1[1]:
                print(dat2[v])
                v=v+1
        except:
            print
        time.sleep(1)
        try:            
            data=sock1.recv(1024)
            if data:
                #print(data)
                fname=data.split('+')  
                comp=re.search(r'\b-OK\b',data)
                p=p+1    
        except:
            print("COULD NOT RECEIVE:SERVER 1 IS OFFLINE")
        try:
            data1=sock2.recv(1024)
            if data1:
                fname=data1.split('+')
                #print(data1)
                comp1=re.search(r'\b-OK\b',data1)
                q=q+1
        except:
            print("COULD NOT RECEIVE:SERVER 2 IS OFFLINE")
        try:                
            data2=sock3.recv(1024)
            if data2:
                fname=data2.split('+')
                #print(data2)
                comp2=re.search(r'\b-OK\b',data2)
                r=r+1
        except:
            print("COULD NOT RECEIVE:SERVER 3 IS OFFLINE")
        try: 
            data3=sock4.recv(1024)
            if data3:       
                fname=data3.split('+')
                #print(data3)
                comp3=re.search(r'\b-OK\b',data3)
                s=s+1
        except:
            print("COULD NOT RECEIVE:SERVER 4 IS OFFLINE")
        
        
        w=0
               
        if p!=0:
            hasattr(comp,'group')
            print
            print("DFS1-OK")
        else:
            print
            print("DFS1-NOT OK")
            w=w+1
        if q!=0:
            hasattr(comp1,'group')
            print
            print("DFS2-OK")
        else:
            print
            print("DFS2-NOT OK")
            w=w+1
        if r!=0:
            hasattr(comp2,'group')
            print
            print("DFS3-OK")
        else:
            print
            print("DFS3-NOT OK")
            w=w+1
        if s!=0:
            hasattr(comp3,'group')
            print
            print("DFS4-OK")
            s=s+1
        else:
            print
            print("DFS4-NOT OK")
            w=w+1
        print("W:",w)
        if w>2:
            print
            print("FILE CAN NOT BE RECONSTRUCTED")
            print    
            fnam=filen+"[INCOMPLETE]"
            name[filen]=fnam
            print
            print("LIST")
            print
            if filen in name.keys():
                print(name[filen])
        
        elif w<=1:
            name[fname[0]]=filen
            print("FILE CAN BE RECONSTRUCTED")
            print
            print("LIST")
            print
            if fname[0] in name.keys():
                print(name[fname[0]])      
        elif w==2:
            print
            print("SUM:",(p+q+r+s))   
            if p==0 and q==0:
                print
                print("FILE CANNOT BE RE-CONSTRUCTED")
                fnam=filen+"[INCOMPLETE]"
                name[filen]=fnam
                print
                print("LIST")
                print
                if filen in name.keys():
                    print(name[filen])
            
            elif r==0 and s==0:
                print
                print("FILE CANNOT BE RE-CONSTRUCTED")
                fnam=filen+"[INCOMPLETE]"
                name[filen]=fnam
                print
                print("LIST")
                print
                if filen in name.keys():
                    print(name[filen])
                
            elif p==0 and r==0:
                print
                print("FILE CAN BE RE-CONSTRUCTED")
                name[fname[0]]=filen
                print
                print("LIST")
                print
                if fname[0] in name.keys():
                    print(name[fname[0]])
                    
            elif q==0 and s==0:
                print
                print("FILE CAN BE RE-CONSTRUCTED")
                name[fname[0]]=filen
                print
                print("LIST")
                print
                if fname[0] in name.keys():
                    print(name[fname[0]])            
                
    threading.Thread(target=sock,args=(sock1,sock2,sock3,sock4)).start()                #THREADING
    print
    time.sleep(2)
    #z=z+1
    answer=raw_input("ENTER COMMAND: ")
    if answer=="GET"+filen:
        print
        print("GET")
        print
        GET(filen,x)
    elif answer=="LIST":
        LIST(filen,x)
    elif answer=="PUT"+filen:
        PUT(filen,x)
    elif answer=="TO":
        GET1(filen,x)

def GET(filen,x):                                                                  #GET FUNCTION
    filen=filen
    x=x
    print
    print("X:",x)
    print
    try:
        sock1.sendto("GET",(IP,int(port)))
    except:
        print("COULD NOT SEND")
    try:
        sock2.sendto("GET",(IP,int(port1)))
    except:
        print("COULD NOT SEND")
    try:
        sock3.sendto("GET",(IP,int(port2)))
    except:
        print("COULD NOT SEND")
    try:
        sock4.sendto("GET",(IP,int(port3)))
    except:
        print("COULD NOT SEND")
    
    def get1(sock1,):                                               
        try:
            data1=sock1.recv(999999)
            if data1:
                file=open("RE1.txt","wb")
                file.write(data1)
                file.close()
                time.sleep(2)
        except:
            print("COULD NOT RECEIVE")
        try:
            data2=sock1.recv(999999)
            if data2:
                file=open("RE2.txt","wb")
                file.write(data2)
                file.close()
        except:
            print("COULD NOT RECEIVE")
               
    def get2(sock2,):
        try:
            data3=sock2.recv(999999)
            if data3:
                file=open("RE3.txt","wb")
                file.write(data3)
                file.close()
                time.sleep(2)
        except:
            print("COULD NOT RECEIVE")
        try:
            data4=sock2.recv(999999)
            if data4:
                file=open("RE4.txt","wb")
                file.write(data4)
                file.close()
        except:
            print("COULD NOT RECEIVE")
          
    def get3(sock3,):
        try:
            data5=sock3.recv(999999)
            if data5:
                file=open("RE5.txt","wb")
                file.write(data5)
                file.close()
                time.sleep(2)
        except:
            print("COULD NOT RECEIVE")
        try:  
            data6=sock3.recv(999999)
            if data6:
                file=open("RE6.txt","wb")
                file.write(data6)
                file.close()
        except:
            print("COULD NOT RECEIVE")
        
    def get4(sock4,):
        try:
            data7=sock4.recv(999999)
            if data7:
                file=open("RE7.txt","wb")
                file.write(data7)
                file.close()
                time.sleep(2)
        except:
            print("COULD NOT RECEIVE")
        try:
            data8=sock4.recv(999999)
            if data8:
                file=open("RE8.txt","wb")
                file.write(data8)
                file.close()
        except:
            print("COULD NOT RECEIVE")
        
        
    threading.Thread(target=get1,args=(sock1,)).start()
    threading.Thread(target=get2,args=(sock2,)).start()
    threading.Thread(target=get3,args=(sock3,)).start()
    threading.Thread(target=get4,args=(sock4,)).start()
    
    time.sleep(10)
    if x==0:
        try:  
            fh1=open("RE2.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        except:
            fh1=open("RE3.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        try:
            fh2=open("RE4.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        except:
            fh2=open("RE5.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        try:    
            fh3=open("RE6.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        except:
            fh3=open("RE8.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        try:
            fh4=open("RE7.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
        except:
            fh4=open("RE1.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
            
        with open("R-PC.txt","wb") as fil:
            fil.write(fh1+fh2+fh3+fh4)
        cmd()
    elif x==1:
        try:  
            fh1=open("RE1.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        except:
            fh1=open("RE8.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        try:
            fh2=open("RE3.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        except:
            fh2=open("RE2.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        try:    
            fh3=open("RE5.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        except:
            fh3=open("RE4.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        try:
            fh4=open("RE8.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
        except:
            fh4=open("RE6.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
            
        with open("R-ice.png","wb") as fil:
            fil.write(fh1+fh2+fh3+fh4)
        cmd()
    elif x==2:
        try:  
            fh1=open("RE4.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        except:
            fh1=open("RE5.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        try:
            fh2=open("RE6.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        except:
            fh2=open("RE7.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        try:    
            fh3=open("RE8.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        except:
            fh3=open("RE1.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        try:
            fh4=open("RE2.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
        except:
            fh4=open("RE3.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
            
        with open("R-test.txt","wb") as fil:
            fil.write(fh1+fh2+fh3+fh4)
        cmd()
    elif x==3:
        try:  
            fh1=open("RE6.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        except:
            fh1=open("RE8.txt","rb")
            fh1=fh1.read()
            fh1=fh1.split('BGBVm')
            fh1=fh1[0]
        try:
            fh2=open("RE7.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        except:
            fh2=open("RE1.txt","rb")
            fh2=fh2.read()
            fh2=fh2.split('BGBVm')
            fh2=fh2[0]
        try:    
            fh3=open("RE2.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        except:
            fh3=open("RE3.txt","rb")
            fh3=fh3.read()
            fh3=fh3.split('BGBVm')
            fh3=fh3[0]
        try:
            fh4=open("RE4.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
        except:
            fh4=open("RE5.txt","rb")
            fh4=fh4.read()
            fh4=fh4.split('BGBVm')
            fh4=fh4[0]
        with open("R-para.jpg","wb") as fil:
            fil.write(fh1+fh2+fh3+fh4)
        cmd()  
        
def GET1(filen,x):                                                           #FUNCTION FOR TRAFFIC OPTIMIZATION
    
    filen=filen
    x=x
    print
    print("X:",x)
    print
    
    try:
        sock2.sendto("GET1",(IP,int(port1)))
    except:
        print("COULD NOT SEND")
    try:
        sock4.sendto("GET1",(IP,int(port3)))
    except:
        print("COULD NOT SEND")
    
    
    if x==0:           
        def get2(sock2,):
            try:
                data1=sock2.recv(999999)
                if data1:
                    print("FILE 1 RECEIVING FROM SERVER 2")
                    #print(data1)
                    file=open("TO1.txt","wb")
                    file.write(data1)
                    file.close()
                    time.sleep(2)
            except:
                print("COULD NOT RECEIVE")
            try:
                data2=sock2.recv(999999)
                if data2:
                    print("FILE 2 RECEIVING FROM SERVER 2")
                    file=open("TO2.txt","wb")
                    file.write(data2)
                    file.close()
            except:
                print("COULD NOT RECEIVE")
            
        def get4(sock4,):
            try:
                data3=sock4.recv(999999)
                if data3:
                    print("FILE 1 RECEIVING FROM SERVER 4")
                    file=open("TO3.txt","wb")
                    file.write(data3)
                    file.close()
                    time.sleep(2)
            except:
                print("COULD NOT RECEIVE")
            try:
                data4=sock4.recv(999999)
                if data4:
                    print("FILE 1 RECEIVING FROM SERVER 4")
                    file=open("TO4.txt","wb")
                    file.write(data4)
                    file.close()
            except:
                print("COULD NOT RECEIVE")
            
        threading.Thread(target=get2,args=(sock2,)).start()
        threading.Thread(target=get4,args=(sock4,)).start()
        time.sleep(6)
        fh1=open("TO1.txt","rb")
        fh1=fh1.read()
        fh1=fh1.split('BGBVm')
        fh1=fh1[0]
        fh2=open("TO2.txt","rb")
        fh2=fh2.read()
        fh2=fh2.split('BGBVm')
        fh2=fh2[0]
        fh3=open("TO3.txt","rb")
        fh3=fh3.read()
        fh3=fh3.split('BGBVm')
        fh3=fh3[0]
        fh4=open("TO4.txt","rb")
        fh4=fh4.read()
        fh4=fh4.split('BGBVm')
        fh4=fh4[0]
        
        with open("TO-PC.txt","wb") as fil:
            fil.write(fh1+fh2+fh4+fh3)
        cmd()
    else:
        cmd()
        
while True:
    
    try:
        sock1.sendto(Uname+"+"+Pword,(IP,int(port)))
        data=sock1.recv(1024)
        if data:
            print
            print(data)
            if data=="INVALID USERNAME/PASSWORD. PLEASE TRY AGAIN.":
                break
    except:
        print("COULD NOT SEND")
        
    try:
        sock2.sendto(Uname+"+"+Pword,(IP,int(port1)))
        data1=sock2.recv(1024)
        if data1:
            print
            print(data1)
            if data1=="INVALID USERNAME/PASSWORD. PLEASE TRY AGAIN.":
                break
    except:
        print("COULD NOT SEND")
        
    try:
        sock3.sendto(Uname+"+"+Pword,(IP,int(port2)))
        data2=sock3.recv(1024)
        if data2:
            print
            print(data2)
            if data2=="INVALID USERNAME/PASSWORD. PLEASE TRY AGAIN.":
                break
    except:
        print("COULD NOT SEND")
        
    try:
        sock4.sendto(Uname+"+"+Pword,(IP,int(port3)))
        data3=sock4.recv(1024)
        if data3:
            print
            print(data3)
            if data3=="INVALID USERNAME/PASSWORD. PLEASE TRY AGAIN.":
                break
    except:
        print("COULD NOT SEND")
        
    time.sleep(1)
    filen=raw_input("Enter File Name:")
    hash=hashlib.md5()
    with open(filen,'rb') as fh:
        buffer=fh.read()
        hash.update(buffer)
        digest=hash.hexdigest()
        number=int(digest,16)
        x=int(number%4)
        print("X=",x)
    
    size=os.path.getsize(filen)
    size=int(size)
    print("FILESIZE:",size)
    siz=size/4
    print("PACKET SIZE:",siz)
    
    fh=open(filen,"rb")    
    m=0
    while m<4:
        if m==0:
            fh.seek(0)
            with open("1"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==1:
            fh.seek(siz)
            with open("2"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==2:
            fh.seek(2*siz)
            with open("3"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1
        elif m==3:
            fh.seek(3*siz)
            with open("4"+filen[:-4]+".txt","wb") as fil:
                data=fh.read(siz)
                fil.write(data)
                m=m+1 
    print
    time.sleep(1)
    answer=raw_input("ENTER COMMAND:")
    if answer=="PUT"+filen:
        PUT(filen,x)
       
        