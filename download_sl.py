# -*- coding: utf-8 -*-
import subprocess
import time
from icc_utils import create_download_directory
from icc_utils import remove_quotation
from icc_utils import get_filename_from_path


class DownloadSL:
    def __init__(self, case_id, file_path, cfg):
        file_path = remove_quotation(file_path)
        self.file_name = str(case_id + '-' + get_filename_from_path(file_path))
        self.connector = cfg.get('DEFAULT', 'slrconnector')
        self.SL_ORIGINAL_PATH = file_path
        self.DOWNLOAD_PATH_SL = cfg.get(
            'DEFAULT', 'tempdownloadpath') + self.file_name
        create_download_directory(cfg.get('DEFAULT', 'tempdownloadpath'))
        pass

    def download(self):
        swift_cmd = ['swift', 'download', self.connector,
                     self.SL_ORIGINAL_PATH, '--output', self.DOWNLOAD_PATH_SL]
        start = time.time()
        pipe = subprocess.Popen(swift_cmd, stdin=subprocess.PIPE,
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
            return {'download_file_path': self.DOWNLOAD_PATH_SL, 'cost': cost}
            # return self.DOWNLOAD_PATH_S3
        else:
            return {'download_file_path': None, 'err': err}
