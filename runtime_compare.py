from ICCError import CfgExceptedValueInvaild
from ICCError import DownloadAWSFileError
from ICCError import DownloadSLRFileError
from ICCError import DownloadFTPFileError
from ICCError import GenerateMD5Error
from download_ftp import DownloadFTP
from download_s3 import DownloadS3
from download_sl import DownloadSL
from icc_utils import convertCLI
from icc_utils import getFileMd5
from icc_utils import remove_quotation
from icc_utils import get_filename_from_path
import time


class RuntimeCompare:
    def __init__(self, tc, cfg):
        self.tc = tc
        self.cfg = cfg
        self.destination_MD5 = None
        self.origin_MD5 = None
        self.compare_rule = None

    def compare(self):
        self.run_download_process()
        print '================================================================='
        print 'origin_MD5:      ' + str(self.origin_MD5)
        print 'destination_MD5: ' + str(self.destination_MD5)
        print '================================================================='
        if(self.origin_MD5):
            execute_value = (self.origin_MD5 == self.destination_MD5)
            if(execute_value == self.compare_rule):
                return True
            else:
                return False
        else:
            raise GenerateMD5Error(
                '\n>>>Generate MD5 hash coedes error: value is None.')

    def run_download_process(self):
        expected_value = self.tc.expected
        cloud_type = self.tc.cloud_type
        cmd_dict = convertCLI(self.tc.command)
        if (expected_value == 'CPT'):
            self.destination_MD5 = getFileMd5(self.downloadFromCloud(
                cloud_type, cmd_dict.get('CLOUDFILE'), self.cfg))

            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            self.compare_rule = True
            
        elif (expected_value == 'CPTENC'):
            self.destination_MD5 = getFileMd5(self.downloadFromCloud(
                cloud_type, cmd_dict.get('CLOUDFILE'), self.cfg))

            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            self.compare_rule = False

        elif (expected_value == 'CPF'):
            self.destination_MD5 = getFileMd5(self.downloadFromFTP(
            cmd_dict.get('LOCALFILE'), self.cfg))
            originpath = self.cfg.get('FTP', 'originpath')
            file_name = get_filename_from_path(cmd_dict.get('CLOUDFILE'))
            file_path = originpath + file_name
            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                file_path, self.cfg, prefix='ori_'))

            self.compare_rule = True
            
        elif (expected_value == 'CPFENC'):
            self.destination_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            originpath = self.cfg.get('FTP', 'originpath')
            file_name = get_filename_from_path(cmd_dict.get('CLOUDFILE'))
            file_path = originpath + file_name
            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                file_path, self.cfg, prefix='ori_'))

            self.compare_rule = True
            
        else:
            raise CfgExceptedValueInvaild(
                '\n>>>Invaild Excepted Value:\n>>>' + expected_value)

    def downloadFromCloud(self, cloud, cloud_file, cfg, callback=None):
        if(cloud == "S3"):
            cloud_obj = DownloadS3(cloud_file, cfg)
        elif (cloud == "SL"):
            cloud_obj = DownloadSL(cloud_file, cfg)
        else:
            pass

        download_result_dict = cloud_obj.download()
        download_file_path = download_result_dict.get('download_file_path')
        if(download_file_path == None):
            if(cloud == "S3"):
                raise DownloadAWSFileError(
                    '\n>>>Download AWS File Error:\n>>>' + download_result_dict.get('err'))
            else:
                raise DownloadSLRFileError(
                    '\n>>>Download SLR File Error:\n>>>' + download_result_dict.get('err'))
        return download_file_path

    def downloadFromFTP(self, local_file, cfg, callback=None, prefix=''):
        ftp_obj = DownloadFTP(local_file, cfg, prefix)
        download_result_dict = ftp_obj.download()
        download_file_path = download_result_dict.get('download_file_path')
        if(download_file_path == None):
            raise DownloadFTPFileError(
                '\n>>>Download FTP File Error:\n>>>' + download_result_dict.get('err'))
        return download_file_path
