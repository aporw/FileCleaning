import os
import shutil
import errno
import xlrd
import fileinput
import subprocess
import datetime as dt
import logging.config
import datetime
import yaml
import time as TIME_

def setup_logging(default_path=os.getcwd()+"//logging.yaml",default_level=logging.INFO):

    path = default_path

    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = yaml.safe_load(f.read())
            log_filename_i = config['handlers']['info_file_handler']['filename']
            log_filename_e = config['handlers']['error_file_handler']['filename']
            log_filename_w = config['handlers']['warning_file_handler']['filename']

            base_i, extension = os.path.splitext(log_filename_i)
            base_e, extension = os.path.splitext(log_filename_e)
            base_w, extension = os.path.splitext(log_filename_w)

            today = datetime.datetime.today()
            log_filename_i = '{}{}{}'.format(base_i, today.strftime('_%Y%m%d__%H%M%S'), extension)
            log_filename_e = '{}{}{}'.format(base_e, today.strftime('_%Y%m%d__%H%M%S'), extension)
            log_filename_w = '{}{}{}'.format(base_w, today.strftime('_%Y%m%d__%H%M%S'), extension)

            config['handlers']['info_file_handler']['filename'] = log_filename_i
            config['handlers']['error_file_handler']['filename'] = log_filename_e
            config['handlers']['warning_file_handler']['filename'] = log_filename_w

        logging.config.dictConfig(config)
    else:
        print("Place the yaml file at given location")



def copyfolder(src,dst):
    logger = logging.getLogger(__name__)
    folderarray = src.split("\\")
    folder = folderarray[len(folderarray) - 1]

    if not os.path.exists(src):
        logger.error("%s folder does not exist in source/n" % (folder))
    else:
        if os.path.exists(dst):
            rmtree(dst)
        try:
            for src_dir, dirs, files in os.walk(src):
               #print(src_dir)
               dst_dir = src_dir.replace(src, dst, 1)
               #print(dst_dir)
               if not os.path.exists(dst_dir):
                   os.makedirs(dst_dir)
                   logger.info(dst_dir + " folder has been created")
               for file_ in files:
                   src_file = os.path.join(src_dir, file_)
            #print(src_file)
                   dst_file = os.path.join(dst_dir, file_)
            #print(dst_file)
                   if os.path.exists(dst_file):
                      os.remove(dst_file)
                   try:   
                       shutil.copy2(src_file, dst_dir)
                       logger.info("%s file is copied\n" % (src_file))
                   except:
                       logger.error("%s file could not be copied, please place this file manually\n" % (src_file))

            logger.info ("%s folder is successfullly copied\n" % (folder))
            # c+=1
            increment()
        except Exception,e:
             logger.error("%s folder could not be copied from %s\n" % (dst, src))
             logger.error(e, exc_info=True)




def copyfile(src, dst):
    logger = logging.getLogger(__name__)
    filearray = src.split("\\")
    file = filearray[len(filearray) - 1]
    if not os.path.isfile(src):
        logger.error("file %s does not exist in source\n"%(file))
    else:
        if os.path.exists(dst):
            os.remove(dst)
        try:
            
            shutil.copy2(src, dst)
            
            logger.info("%s file is successfullly copied\n" % (file))
            #d+=1
            increment()

        except Exception, e:
            logger.error("%s file could not be copied from %s\n" % (dst, src))
            logger.error(e, exc_info=True)


def rmtree(path):
    logger = logging.getLogger(__name__)	
    listoffolders = [path]
    folderarray = path.split("\\")
    folder = folderarray[len(folderarray) - 1]
    if not os.path.exists(path):
        logger.error("%s folder does not exist in source/n" % (folder))
        return 1
    try:
        for src_dir, dirs, files in os.walk(path):
            for file_ in files:
                 src_file = os.path.join(src_dir, file_)
                 try:
                      
                     os.remove(src_file)
                     logger.info("%s file is deleted\n" % (src_file))

                 except:
                    logger.error("%s file could not be deleted, please delete manually\n" % (src_file))
            for dir_ in dirs:

                listoffolders.append(os.path.join(src_dir,dir_))
        listoffolders.sort()
        #print(listoffolders)

        for i in range(len(listoffolders)-1,-1,-1):

            try:
                if(os.listdir(listoffolders[i])==[]):
                    os.rmdir(listoffolders[i])
                    logger.info("%s folder is deleted\n "%listoffolders[i])
                    TIME_.sleep(1)
            except Exception,e:
                logger.error("%s folder could not be deleted\n "%listoffolders[i])
                logger.error(e)



    except:
        print("%s folder could not be deleted, please delete manually\n" % folder)  


def t3change(file, newurl):
    logger = logging.getLogger(__name__)
    try:

        lines = fileinput.input(file, inplace=True)
        for line in lines:
            line = line.strip()
            
            if("property" in line):
	        line="    "+line
	    if("mapping" in line):
	        line="    "+line
	    if("session" in line):
        	line="  "+line
            if ("t3:" in line):
                url = line.split("=")[1]

                line = line.replace(url, newurl)
                print line

            else:
                print line
        lines.close
        logger.info("t3 url change is done for %s\n" % file)
    except Exception,e:

        logger.error("t3 url could not changed for %s\n" % file)
        logger.error(e, exc_info=True)

logger = logging.getLogger(__name__)
setup_logging()
io = open("cloninginput.txt")

backup_required = io.readline().strip().split("=")[1]
CSR = io.readline().strip().split("=")[1]
deletedate = io.readline().strip().split("=")[1]
source_location = io.readline().strip().split("=")[1]
domainname = io.readline().strip().split("=")[1]
fileserver = io.readline().strip().split("=")[1]

wb = xlrd.open_workbook("Client_Env_Details.xls")
st = wb.sheet_by_index(1)

c=0
d=0
def increment():
    global c
    global d
    c+=1
    d+=1
    
j = 0
for rw in range(st.nrows):
    temp = str(st.cell_value(rw, 10).encode("utf-8")).lower()
    domainname = domainname.lower();

    if (domainname == temp):
        i = rw
        j = 1
        # getting values from clientenv
        primary = st.cell_value(i, 1).encode("utf-8").lower().strip()
        secondary = st.cell_value(i, 2).encode("utf-8").lower().strip()
        # dbserver = st.cell_value(i, 9).encode("utf-8").lower()
        adminport = st.cell_value(i, 23)
        managedport = st.cell_value(i, 24)
        domainpath = st.cell_value(i, 6).encode("utf-8").lower().strip()

if (j == 0):
    logger.error("please check domain name")
    exit()


primarypath = domainpath.split("\n")[0].strip()
if not((len(secondary) <3) or (secondary == "n/a") or (secondary == "na")):
  secondarypath = domainpath.split("\n")[1].strip()

backuplocation = "\\\swtestvirt01\RegBackUp\AppBackups\\" + primary + "\\" + "CSR_" + CSR + "_delon" + deletedate
logger.info("setting backup path as "+backuplocation)

if not os.path.exists(backuplocation):
    os.mkdir(backuplocation)

else:
    logger.error("the folder already exists, please give new folder name")
    exit()

if (backup_required == "yes"):
    logger.info("taking backup")
    
    src = primarypath + "\\applications"
    dst = backuplocation + "\\applications"

    copyfolder(src, dst)

    src = primarypath + "\\lib"
    dst = backuplocation + "\\lib"
    copyfolder(src, dst)

    src = primarypath + "\\hibernate_mapping"
    dst = backuplocation + "\\hibernate_mapping"
    copyfolder(src, dst)

    src = primarypath + "\\etl\\formats"
    dst = backuplocation + "\\etl\\formats"
    copyfolder(src, dst)

    src = primarypath + "\\config"
    dst = backuplocation + "\\config"
    copyfolder(src, dst)

    src = primarypath + "\\conf"
    dst = backuplocation + "\\conf"
    copyfolder(src, dst)

    src = primarypath + "\\bin"
    dst = backuplocation + "\\bin"
    copyfolder(src, dst)

    src = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\excel"
    dst = backuplocation + "\\excel"

    copyfolder(src, dst)
    
    if(c==8):
        logger.info("backup is complete")
    else:
    	logger.error("please place the uncopied folder manually,stopping the process")
    	exit()
            
    
    

else:
    print("backing axis2 and licencetango only")
    #d=0

    os.mkdir(backuplocation + "\\applications")
    os.mkdir(backuplocation + "\\applications\steelwedge")
    os.mkdir(backuplocation + "\\applications\steelwedge\\ambassador")
    os.mkdir(backuplocation + "\\applications\steelwedge\WEB-INF")
    os.mkdir(backuplocation + "\\applications\steelwedge\WEB-INF\conf")
     
    src = str(primarypath).strip() + "\\applications\\steelwedge\\ambassador\\license_tango.xml"
    print(src)
    dst = str(backuplocation) + "\\applications\\steelwedge\\ambassador\\license_tango.xml"
    #print(src)
    
    copyfile(src, dst)
    
    

    src = primarypath + "\\applications\steelwedge\WEB-INF\conf\\axis2.xml"
    dst = backuplocation + "\\applications\steelwedge\WEB-INF\conf\\axis2.xml"
    print(src+"\n")
    copyfile(src, dst)
    
    
    if(d==2):
    	logger.info("backup is completed")
    else:
    	logger.error("please place the upcopied file into backup, stopping the process now")
    	exit()
   

logger.info("moving for cloning")

src = source_location + "\\applications"
dst = primarypath + "\\applications"

copyfolder(src, dst)

src = source_location + "\\lib"
dst = primarypath + "\\lib"
copyfolder(src, dst)

src = source_location + "\\hibernate_mapping"
dst = primarypath + "\\hibernate_mapping"
copyfolder(src, dst)

src = source_location + "\\etl\\formats"
dst = primarypath + "\\etl\\formats"
copyfolder(src, dst)

src = source_location + "\\config\jms"
dst = primarypath + "\\config\jms"
copyfolder(src, dst)

src = source_location + "\\excel"
dst = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\excel"

copyfolder(src, dst)

oldFoldDel = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador"
files=os.listdir(oldFoldDel)
for file in files:
    if(file.startswith ("inbound_")):
        todel=oldFoldDel+"\\"+file
        try:
            rmtree(todel)
            logger.info("old inbound folder is deleted")
	except:
            logger.error("old inbound folder could not be deleted")

    if (file.startswith("outbound_")):
        todel=oldFoldDel+"\\"+file
        try:
	    rmtree(todel)
	    logger.info("old outbound folder is deleted")
	except:
            logger.error("old outbound folder could not be deleted")
            
src = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\inbound"
dst = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\inbound_"+ CSR
try:
    os.rename(src,dst)
    logger.info("inbound folder has been renamed by inbound_"+CSR)
    try:
        os.mkdir(src)
        logger.info("New inbound folder is created")
    except Exception,e:
        logger.error("New inbound folder could not be created")
        logger.error(e, exc_info=True)

except Exception,e:
    logger.error("inbound folder could not be renamed")
    logger.error(e,exc_info=True)

src = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound"
dst = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound_" + CSR
try:
    os.rename(src, dst)
    logger.info("inbound folder has been renamed by outbound_" + CSR)
    try:
        os.mkdir(src)
        logger.info("New inbound folder is created")
        src1= fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound_" + CSR+"\\masterdata"
        dst1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound"+"\\masterdata"
        copyfolder(src1,dst1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound_" + CSR + "\\solver"
        dst1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound" + "\\solver"
        copyfolder(src1, dst1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound_" + CSR + "\\deleterelations"
        dst1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound" + "\\deleterelations"
        copyfolder(src1, dst1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound\wkscsv"
        os.mkdir(src1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound\\reportbatch"
        os.mkdir(src1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound\\reportresponse"
        os.mkdir(src1)
        src1 = fileserver + ":\domains\\" + domainname + "\\applications\steelwedge\\templates\\ambassador\outbound\\response"
        os.mkdir(src1)

    except Exception, e:
        logger.error("New outbound folder could not be created")
        logger.error(e, exc_info=True)

except Exception, e:
    logger.error("outbound folder could not be renamed")
    logger.error(e, exc_info=True)


src = backuplocation + "\\applications\steelwedge\WEB-INF\conf\\axis2.xml"
dst = primarypath + "\\applications\steelwedge\WEB-INF\conf\\axis2.xml"

copyfile(src, dst)

src = backuplocation + "\\applications\steelwedge\\ambassador\license_tango.xml"
dst = primarypath + "\\applications\steelwedge\\ambassador\license_tango.xml"

copyfile(src, dst)

src = source_location + "\\conf\message-bundle.properties"
dst = primarypath + "\\conf\message-bundle.properties"

copyfile(src, dst)

src = source_location + "\\conf\message-bundle_de_DE.properties"
dst = primarypath + "\\conf\message-bundle_de_DE.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_es_ES.properties"
dst = primarypath + "\\conf\message-bundle_es_ES.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_fr_FR.properties"
dst = primarypath + "\\conf\message-bundle_fr_FR.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_it_IT.properties"
dst = primarypath + "\\conf\message-bundle_it_IT.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_ja_JP.properties"
dst = primarypath + "\\conf\message-bundle_ja_JP.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_pt_BR.properties"
dst = primarypath + "\\conf\message-bundle_pt_BR.properties"
copyfile(src, dst)

src = source_location + "\\conf\message-bundle_zh_CN.properties"
dst = primarypath + "\\conf\message-bundle_zh_CN.properties"
copyfile(src, dst)

src = source_location + "\\conf\hibernate.properties"
dst = primarypath + "\\conf\hibernate.properties"
copyfile(src, dst)

if not((len(secondary) <3) or (secondary == "n/a") or (secondary == "na")):
  newurl = "t3://%s.test.steelwedge.com:%d,%s.test.steelwedge.com:%d" % (primary, managedport, secondary, managedport)
else:
    newurl = "t3://%s.test.steelwedge.com:%d"%(primary, managedport)

t3change(dst, newurl)

src = source_location + "\\conf\\filter.hibernate.cfg.xml"
dst = primarypath + "\\conf\\filter.hibernate.cfg.xml"
copyfile(src, dst)

if not((len(secondary) <3) or (secondary == "n/a") or (secondary == "na")):
  newurl = '"hibernate.jndi.url"'+">t3://%s.test.steelwedge.com:%d,%s.test.steelwedge.com:%d" % (primary, managedport, secondary, managedport)+ "</property>"
else:
    newurl = '"hibernate.jndi.url"' + ">t3://%s.test.steelwedge.com:%d"% (primary, managedport)+ "</property>"
t3change(dst, newurl)

src = source_location + "\\conf\\filterautomation.hibernate.cfg.xml"
dst = primarypath + "\\conf\\filterautomation.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\\footer.hibernate.cfg.xml"
dst = primarypath + "\\conf\\footer.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\\forecastengine.hibernate.cfg.xml"
dst = primarypath + "\\conf\\forecastengine.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\hibernate.cfg.xml"
dst = primarypath + "\\conf\hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\mybatis-config.xml"
dst = primarypath + "\\conf\mybatis-config.xml"
copyfile(src, dst)

src = source_location + "\\conf\planningsets.hibernate.cfg.xml"
dst = primarypath + "\\conf\planningsets.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\solver.hibernate.cfg.xml"
dst = primarypath + "\\conf\solver.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\\template.hibernate.cfg.xml"
dst = primarypath + "\\conf\\template.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\user.hibernate.cfg.xml"
dst = primarypath + "\\conf\user.hibernate.cfg.xml"
copyfile(src, dst)
t3change(dst, newurl)

src = source_location + "\\conf\CatalogPublicFilters.xml"
dst = primarypath + "\\conf\CatalogPublicFilters.xml"
copyfile(src, dst)

src = source_location + "\\conf\CatalogPrivateFilters.xml"
dst = primarypath + "\\conf\CatalogPrivateFilters.xml"
copyfile(src, dst)

src = source_location + "\\conf\CatalogFilters.xml"
dst = primarypath + "\\conf\CatalogFilters.xml"
copyfile(src, dst)

src = source_location + "\\conf\ForecastPublicFilters.xml"
dst = primarypath + "\\conf\ForecastPublicFilters.xml"
copyfile(src, dst)

src = source_location + "\\conf\ForecastPrivateFilters.xml"
dst = primarypath + "\\conf\ForecastPrivateFilters.xml"
copyfile(src, dst)

src = source_location + "\\conf\ForecastFilters.xml"
dst = primarypath + "\\conf\ForecastFilters.xml"
copyfile(src, dst)

src = source_location +"\\conf\config.properties"
dst = os.getcwd()+"\config_prod.properties"
copyfile(src,dst)

src = primarypath +"\\conf\config.properties"
dst = os.getcwd()+"\config_test.properties"
copyfile(src,dst)

subprocess.call(['java','-jar','PropertyUtility.jar','config_prod.properties', 'config_test.properties', 'conf_diff_file'])
file = open("conf_diff_file\\Diffdata.txt")
entry = open("conf_diff_file\\DiffFileEntryIgnored.txt","w")
lines = file.readlines()
for line in lines:
    if not (line.startswith("wl.")):
        if not (line.startswith("db.")):
            if not ("@steelwedge.com" in line):
                entry.write(line)
entry.close()

src = primarypath + "\compiledjsps"
try:
    if os.path.exists(src):
        rmtree(src)
        logger.info(src + " has been successfully deleted\n")
    else:
        logger.info(src +" does not exist")
except Exception, e:
    logger.error("please delete" + src)
    logger.error(e, exc_info=True)
src = primarypath + "\servers\efmManagedServer\cache"
try:
    if os.path.exists(src):
        rmtree(src)
        logger.info(src + " has been successfully deleted\n")
    else:
        logger.info(src +" does not exist")
except Exception, e:
    logger.error("please delete" + src)
    logger.error(e, exc_info=True)
src = primarypath + "\servers\efmManagedServer\\tmp"
try:
    if os.path.exists(src):
        rmtree(src)
        logger.info(src + " has been successfully deleted\n")
    else:
        logger.info(src +" does not exist")
except Exception, e:
    logger.error("please delete" + src)
    logger.error(e, exc_info=True)

src = primarypath + "\servers\efmserver\cache"
try:
    if os.path.exists(src):
        rmtree(src)
        logger.info(src + " has been successfully deleted\n")
    else:
        logger.info(src +" does not exist")
except Exception, e:
    logger.error("please delete" + src)
    logger.error(e, exc_info=True)
src = primarypath + "\servers\efmserver\\tmp"
try:
    if os.path.exists(src):
        rmtree(src)
        logger.info(src + " has been successfully deleted\n")
    else:
        logger.info(src +" does not exist")
except Exception, e:
    logger.error("please delete" + src)
    logger.error(e, exc_info=True)

if not ((len(secondary) <3) or (secondary == "n/a") or (secondary == "na")):
    src = secondarypath + "\compiledjsps"
    try:
        if os.path.exists(src):
            rmtree(src)
            logger.info(src + " has been successfully deleted\n")
        else:
            logger.info(src + " does not exist")
    except Exception, e:
        logger.error("please delete" + src)
        logger.error(e, exc_info=True)

    src = secondarypath + "\servers\efmManagedServer1\cache"
    try:
        if os.path.exists(src):
            rmtree(src)
            logger.info(src + " has been successfully deleted\n")
        else:
            logger.info(src + " does not exist")
    except Exception, e:
        logger.error("please delete" + src)
        logger.error(e, exc_info=True)

    src = secondarypath + "\servers\efmManagedServer1\\tmp"
    try:
        if os.path.exists(src):
            rmtree(src)
            logger.info(src + " has been successfully deleted\n")
        else:
            logger.info(src + " does not exist")
    except Exception, e:
        logger.error("please delete" + src)
        logger.error(e, exc_info=True)




logger.info("app cloning is completed, please check the conf_diff_file and setdomain_diff_file for comparison")