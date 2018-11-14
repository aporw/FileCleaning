import xlrd
import pymssql
import os
import shutil

arr=[[]]
diction={}
wb = xlrd.open_workbook('C:\Users\pankur\Downloads\Cleanup prod client list_test.xlsx')
sh = wb.sheet_by_index(0)

dst= '\\\\swodnas1\\appdomainbackups\\Outbound_Files_Backup'


for i in range(1,sh.nrows):

    cell_value_domain = sh.cell(i,0).value
    cell_value_db = sh.cell(i,2).value
    cell_value_retention=sh.cell(i,1).value
    cell_value_fileserver=sh.cell(i,3).value
    row=[cell_value_retention,str(cell_value_db),str(cell_value_fileserver)]
    arr.append(row)
    print cell_value_domain
    diction.update({str(cell_value_domain):row})

retention = []

db = []
for key in diction:

    #print domains

    Array=diction[key]
    dbserver=Array[1]
    Retention=Array[0]
    Fileserver=Array[2]

    DOC_PK = []
    server = dbserver
    username = 'user_read'
    password = 'steelwedge@123'
    dbname = key
    try:
        conn = pymssql.connect(server, username, password, dbname)
        cursor = conn.cursor()


        query = "select DOC_PK from REPORT_QUERY where JOB_ID  in (select job_id from JOB where JOB_TYPE='REPORT_QUERY_EXECUTION'  and DATEDIFF (DAY,START_DT,GETDATE())>%d) order by 1 desc" % (Retention)
        print query
        try:
            cursor.execute(query)
            for row in cursor:
                DOC_PK.append(str(row[0]))
            print DOC_PK
            conn.close()
            toMove = []

            path = Fileserver + "\\domains\\" + key + "\\applications\\steelwedge\\templates\\ambassador\\outbound"
            print path
            try:
                allfiles = os.listdir(path)
                for file in allfiles:
                    for DOC in DOC_PK:
                        if DOC in file:
                            toMove.append(file)

                destination = dst + "\\" + key
                if not os.path.exists(destination):
                    try:
                        os.mkdir(destination)
                        for f in toMove:
                            source = path + "\\" + f
                            try:
                                shutil.copy2(source, destination)
                            except:
                                print("not copied")

                    except:
                        print "%s folder could not be created" % (destination)
            except:
                print "%s File server path not accessible" % (path)

        except:
            print "Given sql query could not be executed: %s"%(query)
            conn.close()

        # row = cursor.fetchone()



    except Exception,e:
        print e
        print "no sql connection is established"

                
    
    
    

