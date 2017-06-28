import socket
import os
import sys 
import time
import threading

port=int(sys.argv[2])
print(port)
Uname=[]
Pw=[]
path=sys.argv[1].split('/')
paths=path[1]
print(paths)

file=open('dfs.conf')                                                #parsing dfs file for username and passwords
for line in file:
    a=line.split(' ')
    Uname.append(a[0])
    Pw.append(a[1])
print
print("USERNAME:",Uname)
print
print("PASSWORD:",Pw)
    
if not os.path.isdir(paths):
    os.makedirs(paths)

    
sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
s_addre=('', port)
sock1.bind(s_addre)
sock1.listen(10)



def putit(Uname,):
    #Uname=Uname
    
    try:      
        data=client1.recv(1024)
        if data:
            filen=data
            print
            print("FILENAME:",data)
            print
            ACK="FILENAME RECEIVED"
            try:
                client1.sendto(ACK,s_addre)
            except:
                print("COULD NOT SEND")
    except:
        print("COULD NOT RECEIVE")
    
    
   
    time.sleep(1)
    try:
        data1=client1.recv(999999)
        if data1:
            #print("DATA:",data1)
            print
            print
            index=data1.split('BGBVm')
            #print("INDEX:",index)
            indexx=index[1]
            n1=indexx
            #print("PATH:",paths+"/"+Uname+"/"+"."+indexx[1:]+".1")
            with open(paths+"/"+Uname+"/"+"."+indexx[1:]+".1","wb") as fil:            #storing data in a file under username
                fil.write(data1)
            ACK=paths+"ACK1"
            try:
                client1.sendto(ACK,s_addre)
            except:
                print("COULD NOT SEND")
            print
            print("ACK1 FROM"+paths+"IS SENT")
    except:
        print("COULD NOT RECEIVE")
    
    try:    
        data2=client1.recv(999999)
        if data2:
            index=data2.split('BGBVm')
            indexx=index[1]
            n2=indexx
            #print("PATH:",paths+"/"+Uname+"/"+indexx[1:]+".2")
            with open(paths+"/"+Uname+"/"+"."+indexx[1:]+".2","wb") as fil:
                fil.write(data2)
            ACK1=paths+"ACK2"
            try:
                client1.sendto(ACK1,s_addre)
                print("ACK2 FROM"+paths+"IS SENT")
            except:
                print("COULD NOT SEND")
            print
    except:
        print("COULD NOT RECEIVE")
    
        
    try:
        data3=client1.recv(1024)
        if data3:
            if data3=="LIST":
                listit(n1,n2,indexx,Uname)
                #threading.Thread(target=listit,args=(n1,n2,indexx,Uname)).start()        
            elif data3=="GET"+filen:
                getit(n1,n2,Uname)
                #threading.Thread(target=getit,args=(n1,n2,Uname)).start()  
    except:
        print("COULD NOT RECEIVE")
          
       
                
def listit(n1,n2,indexx,Uname):
    n1=n1
    n2=n2
    indexx=indexx
    Uname=Uname
    try:
        data=client1.recv(1024)
        if data:
            print 
            print("FILENAME:",data)
            filen=data
    except:
        print
        print("COULD NOT RECEIVE")
        
    t=n1.split('.')
    list=[]
    list1=[]
    for file in os.listdir(paths+"/"+Uname):                             #search of required file
        if file.endswith(filen+".1") or file.endswith(filen+".2"):
            list.append(file)
        if file.endswith(".1"):
            list1.append(file[1:-2])
    u=len(list1)
    set=",".join(list1)+"+"+str(u)
    print
    print("set:",set)
    try:
        client1.sendto(set,s_addre)
    except:
        print("COULD NOT SEND")
    print
    print(list)
    fname=list[0].split('.')
    fnam=fname[0]
    print(fnam)
    #P=indexx[1:]
    #P=fnam+"."+fname[1]
    #print("FULL FILENAME:",P)
    print(len(list))
    if len(list)==2:
        msg=paths+"-"+"OK"+"+"+filen 
        try:
            client1.sendto(msg,s_addre)
        except:
            print("COULD NOT SEND")
    elif len(list)==1 or len(list)==0:
        msg=paths+"-"+"NOTOK"+"+"+filen
        try:
            client1.sendto(msg,s_addre)
        except:
            print("COULD NOT SEND")
    
    try:
        data4=client1.recv(1024)
        if data4:
            if data4=="GET":
                getit(n1,n2,Uname)
                #threading.Thread(target=getit,args=(n1,n2,Uname)).start()        
            elif data4=="LIST":
                listit(n1,n2,indexx,Uname)
                #threading.Thread(target=listit,args=(n1,n2,indexx,Uname)).start()        
            elif data4=="GET1":
                get1(n1,n2,Uname)
                #threading.Thread(target=get1,args=(n1,n2,Uname)).start()        
    except:
        print("COULD NOT RECEIVE")

            
def getit(n1,n2,Uname):
    n1=n1
    n2=n2
    Uname=Uname
    
    print("ULALALALAL")
    print(n1)
    print(n2)
    print(paths+"/"+Uname+"/")
    if os.path.exists(paths+"/"+Uname+"/"):                          #search for required file pieces
        fh1=open(paths+"/"+Uname+"/"+"."+n1[1:]+".1","rb")
        fh1=fh1.read()
        try:
            client1.sendto(fh1,s_addre)
        except:
            print("COULD NOT SEND")
        print("FILE1 SENT")
        fh2=open(paths+"/"+Uname+"/"+"."+n2[1:]+".2","rb")
        fh2=fh2.read()
        time.sleep(1)
        try:
            client1.sendto(fh2,s_addre)
        except:
            print("COULD NOT SEND")
        print("FILE2 SENT")
    putit(Uname)
    #threading.Thread(target=putit,args=(Uname,)).start()                

def get1(n1,n2,Uname):                                           #FUNCTION FOR TRAFFIC OPTIMIZATION
    n1=n1
    n2=n2
    Uname=Uname

    print(n1)
    print(n2)
    if os.path.exists(paths+"/"+Uname+"/"):            
        fh1=open(paths+"/"+Uname+"/"+"."+n1[1:]+".1","rb")
        fh1=fh1.read()
        try:
            client1.sendto(fh1,s_addre)
        except:
            print("COULD NOT SEND")
        print("FILE1 SENT")
        fh2=open(paths+"/"+Uname+"/"+"."+n2[1:]+".2","rb")
        fh2=fh2.read()
        time.sleep(1)
        try:
            client1.sendto(fh2,s_addre)
        except:
            print("COULD NOT SEND")
        print("FILE2 SENT")
    putit(Uname)
            
         
while True:    
    try:
        client1, address=sock1.accept()
    except:
        print("COULD NOT ACCEPT")
        
    def multi(Uname,Pw):
        Uname=Uname
        Pw=Pw
        try:
            dat=client1.recv(1024)
        except:
            print("COULD NOT RECEIVE")
        if dat:
            A=dat.split('+')
            user=A[0]
            psw=A[1]
            
        if user in Uname and psw in Pw:
            print("FIRST")
            #Uname=Uname[0]
            Uname=user
            ACK="USERNAME PASSWORD MATCH"
            
            if not os.path.isdir(paths+'/'+Uname):
                os.mkdir(os.path.join(paths,Uname))
            try:
                client1.sendto(ACK,s_addre)
            except:
                print("COULD NOT SEND")
            #print("UNAME:",Uname[0])
            print("UNAME:",Uname)
            putit(Uname)    
            #threading.Thread(target=putit,args=(Uname,)).start()                       
        
        else:
            ACK="INVALID USERNAME/PASSWORD. PLEASE TRY AGAIN."
            try:
                client1.sendto(ACK,s_addre)        
            except:
                print("COULD NOT SEND")
                
    threading.Thread(target=multi,args=(Uname,Pw)).start()                              #MULTITHREADING