


import os,shutil
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






def copyfolder(src, dst):
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
                # print(src_dir)
                dst_dir = src_dir.replace(src, dst, 1)
                # print(dst_dir)
                if not os.path.exists(dst_dir):
                    os.makedirs(dst_dir)
                    logger.info(dst_dir + " folder has been created")
                for file_ in files:
                    src_file = os.path.join(src_dir, file_)
                    # print(src_file)
                    dst_file = os.path.join(dst_dir, file_)
                    # print(dst_file)
                    if os.path.exists(dst_file):
                        os.remove(dst_file)
                    try:
                        shutil.copy2(src_file, dst_dir)
                        logger.info("%s file is copied\n" % (src_file))
                    except:
                        logger.error("%s file could not be copied, please place this file manually\n" % (src_file))

            logger.info("%s folder is successfullly copied\n" % (folder))
            # c+=1

        except Exception, e:
            logger.error("%s folder could not be copied from %s\n" % (dst, src))
            logger.error(e, exc_info=True)


def copyfile(src, dst):
    logger = logging.getLogger(__name__)
    filearray = src.split("\\")
    file = filearray[len(filearray) - 1]
    if not os.path.isfile(src):
        logger.error("file %s does not exist in source\n" % (file))
    else:
        if os.path.exists(dst):
            os.remove(dst)
        try:

            shutil.copy2(src, dst)

            logger.info("%s file is successfullly copied\n" % (file))
            # d+=1


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
                listoffolders.append(os.path.join(src_dir, dir_))
        listoffolders.sort()
        # print(listoffolders)

        for i in range(len(listoffolders) - 1, -1, -1):

            try:
                if (os.listdir(listoffolders[i]) == []):
                    os.rmdir(listoffolders[i])
                    logger.info("%s folder is deleted\n " % listoffolders[i])
                    TIME_.sleep(1)
            except Exception, e:
                logger.error("%s folder could not be deleted\n " % listoffolders[i])
                logger.error(e)



    except:
        print("%s folder could not be deleted, please delete manually\n" % folder)

def impalamove(impalabcp,dstdomain):
    # for impalabcp files
    if os.path.exists(impalabcp):

        ago = now - dt.timedelta(days=timeforImpalaBCP)
        src = impalabcp
        dst = dstdomain + "\\" + "impalabcp"
        if not os.path.exists(dst):
            os.mkdir(dst)
            logger.info(dst + "folder has been created")
            dirs = os.listdir(impalabcp)
            for fname in dirs:
                path = impalabcp + "\\" + fname
                fold = dst + "\\" + fname
                if os.path.exists(path):
                    st = os.stat(path)

                mtime = dt.datetime.fromtimestamp(st.st_mtime)

                if mtime < ago:
                    try:
                        copyfolder(path, fold)
                        logger.info(path + " folder is successfully copied")
                        try:
                            rmtree(path)
                            logger.info(path + " folder is successfully deleted")
                        except Exception, e:
                            logger.error(path + "folder could not be deleted")
                            logger.error(e, exc_info=True)

                    except Exception, e:
                        logger.error(
                            "folder is not copied completely, please copy remaining files and delete from source")
                        logger.error(e, exc_info=True)

def rmmove(rmproposal, dstdomain):
    # for RMproposal
    if os.path.exists(rmproposal):
        now = dt.datetime.now()
        dst = dstdomain + "\\RMproposal"
        if not os.path.exists(dst):
            os.mkdir(dst)
            logger.info(dst + " folder is successfully created")
        ago = now - dt.timedelta(days=timeforRmproposal)
        src = rmproposal
        files = os.listdir(rmproposal)
        for fname in files:
            path = rmproposal + "\\" + fname
            fl = dst + "\\" + fname
            if os.path.exists(path):
                st = os.stat(path)

                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime < ago:
                    try:
                        copyfile(path, fl)
                        logger.info(path + " file is successfully copied")
                        try:
                            os.remove(path)
                            logger.info(path + " file is successfully deleted")

                        except:
                            logger.error(path + "file is not deleted")
                            logger.error(e, exc_info=True)
                    except:
                        logger.error(path + "file is not copied, please copy to backup location and delete")
                        logger.error(e, exc_info=True)

def rpdelete(reportbatch):
    # for ReportBatch
    now = dt.datetime.now()
    if not (reportbatch == ''):
        ago = now - dt.timedelta(days=timeforReportbatch)
        src = reportbatch
        files = os.listdir(reportbatch)
        for fname in files:

            path = reportbatch + "\\" + fname
            if os.path.exists(path):
                st = os.stat(path)

            mtime = dt.datetime.fromtimestamp(st.st_mtime)
            if mtime < ago:
                try:
                    rmtree(path)
                    logger.info(path + " file is successfully deleted")
                except:
                    logger.error(path + "folder could not be deleted")
                    logger.error(e, exc_info=True)





def CSVmove(csvpath,dstdomain):
    # csv files
    if os.path.exists(csvpath):
        now = dt.datetime.now()

        ago = now - dt.timedelta(days=timeforCSV)
        src = csvpath
        dst = dstdomain + "\\CSVfiles"
        if not os.path.exists(dst):
            os.mkdir(dst)
            logger.info(dst + " file is successfully created")
        files = os.listdir(csvpath)
        for fname in files:
            if fname.endswith(".csv"):
                path = csvpath + "\\" + fname
                fl = dst + "\\" + fname
                if os.path.exists(path):
                    st = os.stat(path)

                mtime = dt.datetime.fromtimestamp(st.st_mtime)
                if mtime < ago:
                    try:
                        copyfile(path, fl)
                        logger.info(path + " file is successfully copied")
                        try:
                            os.remove(path)
                            logger.info(path + " file is successfully deleted")
                        except Exception, e:
                            logger.error(path + "file is not deleted")
                            logger.error(e, exc_info=True)

                    except Exception, e:
                        logger.error(path + "file is not copied")
                        logger.error(e, exc_info=True)





if __name__ == "__main__":
    setup_logging()
    logger = logging.getLogger(__name__)

    now = dt.datetime.now()
    strdate = str(now)
    date = strdate.split(' ')[0].strip()
    time = strdate.split(' ')[1].strip()
    time2 = time.split(":")
    hr = time.split(':')[0]
    min = time.split(':')[1]
    # sec = time.split(':')[2]
    time2 = hr + "-" + min
    # time2 = "-".join(time2)
    neslocation = '\\\\swtestvirt01\\RegBackUp\\FileServerCleanUp'

    timeforCSV = 7
    timeforImpalaBCP = 4
    timeforRmproposal = 4
    timeforReportbatch = 2
    dstfolder=neslocation +"\\"+ date + "_" + time2
    if not os.path.exists(dstfolder):
        os.mkdir(dstfolder)
        logger.info(dstfolder + "folder has been created")
    #dstradisys = neslocation + "\\radisys_prod_issue_" + date + "_" + time2
    #dstnokia = neslocation + "\\nokia_prod_issue_" + date + "_" + time2

    io=open("inputpath.txt")
    alllines =io.readlines()
    for line in alllines:
        line =line.strip()
        if "nokia" in line or "lear" in line or "radisys" in line:
            arr=line.split("\\")
            dstdomain=dstfolder+"\\"+arr[len(arr)-1]
            if not os.path.exists(dstdomain):
                os.mkdir(dstdomain)
                logger.info(dstdomain + "folder has been created")



            CSVpath = line + "\\etl\\inbound"
            try:

                CSVmove(CSVpath,dstdomain)
            except Exception,e:
                logger.error(e,exc_info=True)

            impalabcp = CSVpath + "\\" + "ImpalaBCPFiles"
            try:
                impalamove(impalabcp,dstdomain)
            except Exception,e:
                logger.error(e,exc_info=True)
            reportbatch = line + "\\applications\steelwedge\\templates\\ambassador\\outbound\\reportbatch"
            try:
                rpdelete(reportbatch)
            except Exception,e:
                logger.error(e,exc_info=True)
            if "radisys" in line:
                 rmproposal=CSVpath+"\\rm_proposal"
                 try:
                     rmmove(rmproposal,dstdomain)
                 except Exception, e:
                     logger.error(e, exc_info=True)




        else:
            reportbatch = line + "\\applications\steelwedge\\templates\\ambassador\\outbound\\reportbatch"
            try:
                rpdelete(reportbatch)
            except Exception,e:
                logger.error(e,exc_info=True)























