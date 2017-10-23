# -*- coding: utf-8 -*-
import subprocess
import time
from icc_utils import create_download_directory
from icc_utils import remove_quotation
from icc_utils import get_filename_from_path


class DownloadS3:
    def __init__(self, case_id, key, cfg):
        # xudongz/enc/notfound.txt
        key = remove_quotation(key)
        self.file_name = str(case_id + '-' + get_filename_from_path(key))
        self.DOWNLOAD_PATH_S3 = cfg.get(
            'DEFAULT', 'tempdownloadpath') + self.file_name
        self.S3_ORIGINAL_PATH = 's3://' + \
            cfg.get('DEFAULT', 'awsbucket') + '/' + key
        create_download_directory(cfg.get('DEFAULT', 'tempdownloadpath'))
        pass

    def download(self):
        aws_cmd = ['aws', 's3', 'cp',
                   self.S3_ORIGINAL_PATH, self.DOWNLOAD_PATH_S3]
        start = time.time()
        pipe = subprocess.Popen(aws_cmd, stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        # pipe.wait()
        res = pipe.communicate()
        out = res[0]
        err = res[1]
        # out = pipe.stdout.read()
        end = time.time()
        # print 'error:' + err + '\n'
        status = 0
        if(err):
            pass
        else:
            # print 'execute successfully.'
            status = 1
            # print out
        cost = str(int(end - start))
        # print 'Cost ' + cost + ' seconds.'

        if(status == 1):
            return {'download_file_path': self.DOWNLOAD_PATH_S3, 'cost': cost}
            # return self.DOWNLOAD_PATH_S3
        else:
            return {'download_file_path': None, 'err': err}
