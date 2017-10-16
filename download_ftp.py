# -*- coding: utf-8 -*-
import os
import ftplib
import time
from icc_utils import create_download_directory
from icc_utils import remove_quotation
from icc_utils import get_filename_from_path


class DownloadFTP:
    def __init__(self, local_file, cfg, prefix=''):
        host = cfg.get('FTP', 'HOSTNAME')
        user = cfg.get('FTP', 'USER')
        pwd = cfg.get('FTP', 'PASSWORD')
        download_dir = cfg.get('FTP', 'downloadpath')
        create_download_directory(download_dir)
        # '/home/xudong_test/origin/1Kfile.txt'
        local_file = remove_quotation(local_file)
        _f = get_filename_from_path(local_file)
        self.file_name = _f
        ftp = ftplib.FTP(host)
        ftp.login(user, pwd)
        # print ftp.getwelcome()
        cwd_path = local_file.replace(_f, "")
        # print cwd_path
        ftp.cwd(cwd_path)
        self.ftp_obj = ftp
        self.download_path = download_dir + prefix + self.file_name
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