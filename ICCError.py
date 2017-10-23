#!/usr/bin/python
# -*- coding: UTF-8 -*-


class DebugError(Exception):
    pass
    
class CfgFileNotFoundError(Exception):
    pass


class CfgNotDefaultError(Exception):
    pass


class CfgMissOptionError(Exception):
    pass


class MissTestFilePathError(Exception):
    pass


class MissSpecificSectionError(Exception):
    pass


class MissSpecificOptionError(Exception):
    pass


class CommandRunError(Exception):
    pass


class CfgExceptedValueInvaild(Exception):
    pass


class DownloadAWSFileError(Exception):
    pass


class DownloadSLRFileError(Exception):
    pass


class DownloadFTPFileError(Exception):
    pass


class GenerateMD5Error(Exception):
    pass

class GetFileListError(Exception):
    pass
