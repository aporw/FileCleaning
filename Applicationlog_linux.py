import os
from multiprocessing import Process

import mysql.connector
servername='localhost'
username= 'root'
passwd='coi_user@od'
dbname='uday'


def queryfunction(outfile,logfile,paths):

    conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
    conn.autocommit = True
    cursor = conn.cursor()    
    c = 0
    d = 0
    preline = ""
    secondpreline = ""
    issuetime = ""
    errors=["hibernate"]
    
    try:

        out = open(outfile, 'r')
        patharr=paths.split("\\")
        paths2=("\\\\").join(patharr)
        out2=outfile.split("//")[1]

        for line in out:
            for s in errors:

                if s in line:

                    c = c + 1
                    if "PDT" in line:
                        a = line.split(">")
                        issuetime = a[0]


                        break
                    if "PDT" in preline:
                        a = preline.split(">")
                        issuetime = a[0]

                        break
                    if "PDT" in secondpreline:
                        a = secondpreline.split(">")
                        issuetime = a[0]

                        break
                preline = line
                secondpreline = preline
            out.close()
            if (c > 0):
                b=issuetime.split("<")
                timing=b[1]
                if not (conn):


                    conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
                    conn.autocommit = True
                    cursor = conn.cursor()

                query = "insert into app_log (issue_time, filepath, error) VALUES ('" + timing + "','" + paths2+"\\\\"+out2  +"','"+s+"')"
                print query
                cursor.execute(query)


    except Exception,e:

        print e
        if(conn):
            conn.close()

    try:
        log = open(logfile, 'r')
        log2=logfile.split("//")[1]
        for line in log:
            if "java.lang.OutOfMemoryError" in line:
                d = d + 1

                if "PDT" in line:
                    a = line.split(">")
                    issuetime = a[0]


                    break
                if "PDT" in preline:
                    a = preline.split(">")
                    issuetime = a[0]

                    break
                if "PDT" in secondpreline:
                    a = secondpreline.split(">")
                    issuetime = a[0]

                    break
            preline = line
            secondpreline = preline

        log.close()
        if (d > 0):
            b = issuetime.split("<")
            timing = b[1]
            if not(conn):
	        
	    
                conn = mysql.connector.connect(user=username, password=passwd, host=servername, database=dbname)
                conn.autocommit = True
                cursor = conn.cursor()
            query = "insert into OOM (issue_time, filepath) VALUES ('" + timing + "','" +paths2+"\\\\"+ log2 +"')"
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
        
        print (paths)

        paths = paths.strip()

        array = paths.split("$")
        first = array[0] + "$"

        restpath = array[1]
        fullpaths=array[1]+"\\\logs"

        #[fullpaths.append(restpath+ser) for ser in serverpath]
        logpaths=[]
        #[logpaths.append(fullp + "\\\logs") for fullp in fullpaths]
        #print(logpaths)
        #diction = dict(zip(logpaths,serverarray))
        [logpaths.append(fullpaths + ser) for ser in serverarray]



        #print(diction)
        domain=paths.split("\\")
        
        dirr=pwd+"//"+domain[len(domain)-1]
        print(dirr)
        if not os.path.exists(dirr):
            os.mkdir(dirr)
    
        for key in diction:
            logfile=diction[key]+".log"
            outfile=diction[key]+".out"

            try:
                second = "lcd " + dirr + "; cd " + key + "; get " + logfile + "; get " + outfile
                command = "smbclient '" + first + "' -c '" + second + "' -U ondemand/appsrunner%SwAppsRun@$ / > /dev/null"
                print(command)
                os.system(command)
                log1=dirr+"//"+logfile
                out1=dirr+"//"+outfile
                print(log1)
                queryfunction(log1, out1,paths)
                
                os.remove(log1)
                os.remove(out1)

            except Exception, e:
                print(e)
        try:

            os.rmdir(dirr)
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
    print(allpaths)
    n = len(allpaths)
    mconn.close()
    #print(n)
    m = n/5
    paths1=allpaths[0:m]
    paths2=allpaths[m:2*m]
    paths3=allpaths[2*m:3*m]
    paths4=allpaths[3*m:4*m]
    paths5=allpaths[4*m:n]
    input=[paths1,paths2,paths3,paths4,paths5]
#    paths4=allpaths[(3*m):4*m]
#    paths5=allpaths[(4*m:n]

    #print(paths1)
    #print(paths2)
    pwd = os.getcwd()
    serverarray = ['efm_efmManagedServer', 'efm_efmManagedServer1', 'efm_efmManagedServer2', 'efm_efmManagedServer3','efm_efmManagedServer4']

    #serverpath = []
    #[serverpath.append("\\\servers\\" + arr) for arr in serverarray]
#    print(serverpath)
    
    if (n<10):
        s=allpaths[0]
        function(s)
#        p1.start()
#        p1.join()
# mconn.close()
    else:
    
        jobs = []       


        for i in range(0,5):
            #pth = 'paths' + str(i)
            #print ("token: " + pth)
            p = Process(target=function,args=(input[i],))
            jobs.append(p)
            print([i for i in jobs])
               
            p.start()
        
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


