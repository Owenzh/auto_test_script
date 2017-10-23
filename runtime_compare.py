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
        msg = 'different'
        if self.compare_rule is True:
            msg = 'same'
        print '================================================================='
        print '***Tester expects these two MD5 values are ' + msg
        print 'origin_MD5:      ' + str(self.origin_MD5)
        print 'destination_MD5: ' + str(self.destination_MD5)
        print '================================================================='
        if((self.origin_MD5 is not None) and (self.destination_MD5 is not None)):
            execute_value = (self.origin_MD5 == self.destination_MD5)
            if(execute_value == self.compare_rule):
                return True
            else:
                return False
        else:
            raise GenerateMD5Error(
                '\n>>>Generate MD5 hash coedes error: value is None.')

    # CPYTOCLD RESOURCE(XDAWSENC) ASYNC(*NO) LOCALFILE('/home/xudong_test/notfound.txt') CLOUDFILE('xudongz/enc/notfound.txt')
    def run_download_process(self):
        expected_list = str(self.tc.expected).split('-')
        expected_value = expected_list[0]
        rule = None
        if(len(expected_list) == 2):
            if(expected_list[1] == 'T'):
                rule = True
            else:
                rule = False

        cloud_type = self.tc.cloud_type
        cmd_dict = convertCLI(self.tc.command)
        self.cmd = cmd_dict
        if (expected_value == 'CPT'):
            self.destination_MD5 = getFileMd5(self.downloadFromCloud(
                cloud_type, cmd_dict.get('CLOUDFILE'), self.cfg))

            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            self.compare_rule = self.cal_rule(True, rule)

        elif (expected_value == 'CPTENC'):
            self.destination_MD5 = getFileMd5(self.downloadFromCloud(
                cloud_type, cmd_dict.get('CLOUDFILE'), self.cfg))

            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            self.compare_rule = self.cal_rule(False, rule)

        elif (expected_value == 'CPF'):
            self.destination_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            originpath = self.cfg.get('DEFAULT', 'originpath')
            file_name = get_filename_from_path(cmd_dict.get('CLOUDFILE'))
            file_path = originpath + remove_quotation(file_name)
            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                file_path, self.cfg, prefix='ori_'))

            self.compare_rule = self.cal_rule(True, rule)

        elif (expected_value == 'CPFENC'):
            self.destination_MD5 = getFileMd5(self.downloadFromFTP(
                cmd_dict.get('LOCALFILE'), self.cfg))
            originpath = self.cfg.get('DEFAULT', 'originpath')
            file_name = get_filename_from_path(cmd_dict.get('CLOUDFILE'))
            file_path = originpath + remove_quotation(file_name)
            self.origin_MD5 = getFileMd5(self.downloadFromFTP(
                file_path, self.cfg, prefix='ori_'))

            self.compare_rule = self.cal_rule(True, rule)

        else:
            raise CfgExceptedValueInvaild(
                '\n>>>Invaild Excepted Value:\n>>>' + expected_value)

    def downloadFromCloud(self, cloud, cloud_file, cfg, callback=None):
        case_id = self.tc.id
        if(cloud == "S3"):
            cloud_obj = DownloadS3(case_id, cloud_file, cfg)
        elif (cloud == "SL"):
            cloud_obj = DownloadSL(case_id, cloud_file, cfg)
        elif (cloud == "FTP"):
            res_name = str('Target_' + self.cmd.get('RESOURCE'))
            cloud_obj = DownloadFTP(case_id, cloud_file, cfg, default=res_name)
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
        case_id = self.tc.id
        ftp_obj = DownloadFTP(case_id, local_file, cfg, prefix)
        download_result_dict = ftp_obj.download()
        download_file_path = download_result_dict.get('download_file_path')
        if(download_file_path == None):
            raise DownloadFTPFileError(
                '\n>>>Download FTP File Error:\n>>>' + download_result_dict.get('err'))
        return download_file_path

    def cal_rule(self, default_rule, set_rule=None):
        if set_rule is None:
            return default_rule
        else:
            return set_rule
