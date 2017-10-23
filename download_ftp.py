# -*- coding: utf-8 -*-
import os
import ftplib
import time
from icc_utils import create_download_directory
from icc_utils import remove_quotation
from icc_utils import get_filename_from_path


class DownloadFTP:
    def __init__(self, case_id, local_file, cfg, prefix='', default='DEFAULT'):
        host = cfg.get(default, 'HOSTNAME')
        user = cfg.get(default, 'USER')
        pwd = cfg.get(default, 'PASSWORD')
        download_dir = cfg.get('DEFAULT', 'tempdownloadpath')
        create_download_directory(download_dir)
        # '/home/xudong_test/origin/1Kfile.txt'
        local_file = remove_quotation(local_file)
        _f = get_filename_from_path(local_file)
        # self.file_name = str(case_id + _f)
        self.file_name = _f
        ftp = ftplib.FTP(host)
        ftp.login(user, pwd)
        # print ftp.getwelcome()
        if (default == 'DEFAULT'):
            cwd_path = local_file.replace(_f, "")
        else:
            # /home/xudong
            root_dir = cfg.get(default, 'ROOTDIR')
            cwd_path = root_dir + '/' + local_file.replace(_f, "")
        # print cwd_path
        ftp.cwd(cwd_path)
        self.ftp_obj = ftp
        self.download_path = download_dir + case_id + '-' + prefix + self.file_name
        pass

    def download(self):
        file = open(self.download_path, 'wb')
        self.ftp_obj.retrbinary('RETR %s' % self.file_name, file.write)
        file.close()
        if(os.path.exists(self.download_path)):
            return {'download_file_path': self.download_path}
        else:
            return {'download_file_path': None, 'err': 'FTP download fails.'}
    # def
