import os
import mysql.connector
#from subprocess import Popen, PIPE
from multiprocessing import Process
def WLSTfunction(userarr,passarr,URLarr,domainarr):
    num=len(userarr)
    for i in range(num):

        try:
            cmd='./wlst.sh WLST_multi.py \''+userarr[i]+'\' \''+passarr[i] +'\' \''+URLarr[i]+'\''
            #print cmd
            os.system(cmd)
            try:
                file="test_"+userarr[i]+".txt"
                if(os.path.exists(file)):
                    readfile(file,domainarr[i])
                    delfile(file)
            except Exception,e:
                print(e)
        except Exception,e:
            print("error")
            print(e)

def readfile(file,domainput):
    io=open(file)
    lines=io.readlines()
    dmar=domainput.split("\\")
    domain=("\\\\").join(dmar)
    for line in lines:
        try:
            line=line.strip()
            ln=line.split(":")
            #print line
            if (ln[1]=='RUNNING'):
                continue
            query2 = "insert into server_health (domain,servername,state) values ('"+domain+"','"+ln[0]+"','"+ln[1]+"')"
            #print query2

            #if not (conn):
            conn2 = mysql.connector.connect(user=uname, password=passwd, host=servername, database=dbname)
            conn2.autocommit = True
            cursor2 = conn2.cursor()
            cursor2.execute(query2)
            conn2.close()
        except Exception,e:
            print(e)
            conn2.close()

    io.close()
#os.system("connect('nvidiasteelwedge','Nu@v!u660r1','t3://swodap02.ondemand.steelwedge.com:8889')")
def delfile(file):
    try:
        rmcmd="rm "+file 
        os.system(rmcmd)
    except:
        try:
            os.system("rm "+file)
        except Exception,e:
            print "file not deleted"          
            print e

if __name__ == "__main__":
    servername = 'localhost'
    uname = 'root'
    passwd = 'coi_user@od'
    dbname = 'uday'
    mconn = mysql.connector.connect(user=uname, password=passwd, host=servername, database=dbname)
    mconn.autocommit = True
    cursor = mconn.cursor()
    query = "select * from weblogic_input"
    cursor.execute(query)
    userall=[]
    passall=[]
    urlall=[]
    domainall=[]
    for row in cursor:
        userall.append(row[0])
        passall.append(row[1])
        port = str(row[3])
        domainall.append(row[4])
        urlall.append('t3://' + row[2] + ":" + port)
    ntotal=len(userall)
    numOfTheads=2
    m=ntotal/numOfTheads
    userinput=[]
    pssinput=[]
    ulinput=[]
    dminput=[]
    
    for i in range(0,numOfTheads):
        if (ntotal-m*(i+1)>= m):
            p=m*(i+1)
        else:
            p=ntotal
        userinput.append(userall[m*i:p])
        pssinput.append(passall[m*i:p])
        ulinput.append(urlall[m*i:p])
        dminput.append(domainall[m*i:p])
    jobs=[]  
    #print userinput
    #print dminput  
    for i in range(0,numOfTheads):
            #pth = 'paths' + str(i)
            #print ("token: " + pth)
        p = Process(target=WLSTfunction,args=(userinput[i],pssinput[i],ulinput[i],dminput[i],))
        jobs.append(p)
        print([i for i in jobs])
               
        p.start()
            #p.join()
        #print(jobs)
    for p in jobs:
        p.join()
        print([p for p in jobs])
            #p.join() 
    #WLSTfunction(username,password,URL,domain)
        #readfile()
    mconn.close()

