import os
from multiprocessing import Process

import mysql.connector
import re
servername='localhost'
username= 'root'
passwd='coi_user@od'
dbname='uday'


def queryfunction(logfile,paths):

    conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
    conn.autocommit = True
    cursor = conn.cursor()
    form =re.compile('.{4}-.{2}-.{2}')
    c = 0
    d = 0
    preline = ""
    secondpreline = ""
    issuetime = []
    errors = ["hibernate"]
    patharr=paths.split("\\")
    paths2=("\\\\").join(patharr)
    issues =[]
    


    try:
        filearr2=logfile.split("//")
        log2= filearr2[len(filearr2)-1]

        log = open(logfile, 'r')
        for line in log:
            for err in errors:

                if err in line:
                    d = d + 1
                    issues.append(err)
                    a=line.split(" ")
                    b=preline.split(" ")
                    c=secondpreline.split(" ")



                    if form.match(a[0]):
                        a = line.split(">")
                        issuetime.append(a[0])


                        break
                    if form.match(b[0]):
                        a = preline.split(">")
                        issuetime.append(b[0])

                        break
                    if form.match(c[0]):
                        a = secondpreline.split(">")
                        issuetime.append(c[0])


                        break
            preline = line
            secondpreline = preline

        log.close()
        if (d > 0):
            diction = dict(zip(issues, issuetime))

            if not(conn):
	        
                conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
                conn.autocommit = True
                cursor = conn.cursor()
            for key in diction:
                b = diction[key].split("<")
                timing = b[1]
                query = "insert into app_log (issue_time, filepath, error) VALUES ('" + timing + "','" +paths2 +"\\\\"+log2+"','"+key+"')"
                print query
                cursor.execute(query)
        
       


    except Exception,e:

        print e
        if(conn):
            conn.close()

    conn.close()



def function(ap):
    #conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
    #conn.autocommit = True
    #cursor = conn.cursor()
    for paths in ap:
        
        #print (paths)

        paths = paths.strip()

        array = paths.split("$")
        first = array[0] + "$"

        restpath = array[1]
        fullpaths = array[1] + "\\\logs"
        domain=paths.split("\\")
        
        
        


        #print(logpaths)

        #print(diction)
        domain=paths.split("\\")
        
        dirr=pwd+"//"+domain[len(domain)-1]
        #print(dirr)
        if not os.path.exists(dirr):
            os.mkdir(dirr)
    
        for arr in serverarray:
            logfile=arr+".log"
            logfile2=arr+".log.1"
            logfile3=arr+".log.2"


            try:
                second = "lcd " + dirr + "; cd " + fullpaths + "; get " + logfile + "; get " + logfile2+";get "+logfile3
                command = "smbclient '" + first + "' -c '" + second + "' -U ondemand/appsrunner%SwAppsRun@$ 2>/dev/null"
                #print(command)
                os.system(command)
                log1=dirr+"//"+logfile
                log2=dirr+"//"+logfile2
                log3=dirr+"//"+logfile3
                #print(log1)

#               queryfunction(log1, out1,paths)
                
                if(os.path.exists(log1)):
                    queryfunction(log1, paths)
                    try:
                        os.remove(log1)
                    except:
                        try:

                            os.remove(log1)
                        except Exception, e:
                            print e

                if(os.path.exists(log2)):
                    queryfunction(log2, paths)
                    try:
                        os.remove(log2)
                    except:
                        try:

                            os.remove(log2)
                        except Exception, e:
                            print e

                if (os.path.exists(log3)):
                    queryfunction(log3, paths)
                    try:
                        os.remove(log3)
                    except:
                        try:

                            os.remove(log3)
                        except Exception, e:
                            print e


                

            except Exception, e:
                print("no file in location")
        try:
            
            if(os.path.exists(dirr)):
                os.rmdir(dirr)
            #os.system(comm)
        except Exception,e:
            print e

if __name__ == "__main__":

    mconn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
    mconn.autocommit = True
    cursor = mconn.cursor()

    query = "select paths from allpaths where isactive='1'"
    cursor.execute(query)
    temp = []
    for row in cursor:
        temp.append(row[0])

    allpaths = temp
    #print(allpaths)
    n = len(allpaths)
    mconn.close()
    #print(n)
    m = n/6
    paths1=allpaths[0:m]
    paths2=allpaths[m:2*m]
    paths3=allpaths[2*m:3*m]
    paths4=allpaths[3*m:4*m]
    paths5=allpaths[4*m:5*m]
    paths6=allpaths[5*m:n]
    input=[paths1,paths2,paths3,paths4,paths5,paths6]
#    paths4=allpaths[(3*m):4*m]
#    paths5=allpaths[(4*m:n]

    #print(paths1)
    #print(paths2)
    pwd = os.getcwd()
    serverarray = ['efm_efmManagedServer', 'efm_efmManagedServer1', 'efm_efmManagedServer2', 'efm_efmManagedServer3',
                   'efm_efmManagedServer4']


#    print(serverpath)
    
    if (n<10):
        s=allpaths[0]
        function(s)
#        p1.start()
#        p1.join()
# mconn.close()
    else:
    
        jobs = []       


        for i in range(0,6):
            #pth = 'paths' + str(i)
            #print ("token: " + pth)
            p = Process(target=function,args=(input[i],))
            jobs.append(p)
            print([i for i in jobs])
               
            p.start()
            #p.join()
        #print(jobs)
        for p in jobs:
            p.join()
            print([p for p in jobs])
            #p.join()
                       
        
        ''' 
        p1 = Process(target=function,args=(paths1,))
        p2 = Process(target=function, args=(paths2,))
        p3 = Process(target=function, args=(paths3,))
        #p4 = Process(target=function, args=paths4)
        #p5 = Process(target=function, args=paths5)
        p1.start()
        p2.start()
        p3.start()
        #p4.start()
        #p5.start()

        #p4.join()
        #p5.join()
        '''
   

   # mconn.close()


