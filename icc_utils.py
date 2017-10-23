import os
import hashlib
import ftplib
import re
import shutil
from ICCError import GetFileListError


def convertCLI(cmd):
    # CPYTOCLD RESOURCE(XDAWSENC) ASYNC(*NO) LOCALFILE('/home/xudong_test/notfound.txt') CLOUDFILE('xudongz/enc/notfound.txt')
    cmd_dict = {}
    pattern = r'\w+\([^\)]*\)'
    cmd_list = re.findall(pattern, cmd)
    for cmd_part in cmd_list:
        _list = re.sub(r'\)', '', cmd_part).split('(')
        cmd_dict.update({_list[0]: str(_list[1])})
    return cmd_dict


def remove_quotation(_str):
    pattern1 = r'^[\'|\"]'
    pattern2 = r'[\'|\"]$'
    new_str = re.sub(pattern1, '', _str)
    return re.sub(pattern2, '', new_str)


def get_filename_from_path(_path):
    _f = _path.split('/')
    _f.reverse()
    return _f[0]


def create_download_directory(file_dir):
    if (os.path.exists(file_dir) == False):
        os.mkdir(file_dir)


def getFileMd5(filename):
    if not os.path.isfile(filename):
        print 'not file ' + filename
        return None
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.flush()
    f.close()
    return myhash.hexdigest()


def delete_directory(file_dir):
    if (os.path.exists(file_dir) == True):
        shutil.rmtree(file_dir)
        # os.rmdir(file_dir)


def delete_ftp_directory(cfg):
    host = cfg.get('DEFAULT', 'HOSTNAME')
    user = cfg.get('DEFAULT', 'USER')
    pwd = cfg.get('DEFAULT', 'PASSWORD')
    cwd_path = cfg.get('DEFAULT', 'downloadpath')
    ftp = ftplib.FTP(host)
    ftp.login(user, pwd)
    file_obj = []
    # print cwd_path
    try:
        ftp.retrbinary('NLST %s' % cwd_path, file_obj.append)
    except:
        print '\n>>>[GetFileListError] Please check the paths: ' + cwd_path
        raise GetFileListError(
            '\n>>>Please check the paths:\n>>>' + cwd_path)
    # ftp.retrbinary('NLST %s' % cwd_path, file_obj.append)
    # print file_obj
    if(len(file_obj) >= 1):
        file_list = file_obj[0].split('\r\n')
        # print file_list
        for fn in file_list:
            if(fn != ''):
                ftp.delete(fn)
                # print 'Delete file: ' + fn


def clearDirectories(config):
    delete_ftp_directory(config)
    delete_directory(config.get('DEFAULT', 'tempdownloadpath'))
