#!/usr/bin/python
# -*- coding: UTF-8 -*-
import ConfigParser
import os
import sys
from ICCError import CfgFileNotFoundError
from ICCError import CfgNotDefaultError
from ICCError import CfgMissOptionError
from ICCError import MissTestFilePathError


class InitConfig:

    def run(self):
        self.cur_path = os.getcwd()
        self.cur_sep = os.sep
        self.init_file = '_setup.ini'
        self.cfg_file = 'base.cfg'
        self.init_path = self.cur_path + self.cur_sep + self.init_file
        self.cfg_path = self.cur_path + self.cur_sep + \
            'config' + self.cur_sep + self.cfg_file
        self.rpt_path = self.cur_path + self.cur_sep + 'reports'
        self.test_xml_path = self.cur_path + self.cur_sep + 'tests'
        self.checkIN()
        if(self.isCfg == False):
            raise CfgFileNotFoundError('\n>>>Can not find the config file,please create it!\n>>>Create base.cfg at below path:\n>>>' +
                                       self.cur_path + self.cur_sep + 'config')
        else:
            self.loadCfgFile()
        return self

    def checkIN(self):
        self.isInit = os.path.exists(self.init_path)
        self.isCfg = os.path.exists(self.cfg_path)
        if(os.path.exists(self.rpt_path) == False):
            os.mkdir(self.rpt_path)
        if(os.path.exists(self.test_xml_path) == False):
            raise MissTestFilePathError('\n>>>Can not find the tests folder,please create it!\n>>>Please create it at below path:\n>>>' +
                                        self.test_xml_path)
        if(self.isInit == False):
            f = open(self.init_path, 'w')
            f.write('setup icc test script.')
            f.close()
            print 'create init file...'
        return

    def loadCfgFile(self):
        config = ConfigParser.RawConfigParser()
        config.read(self.cfg_path)
        if(config.defaults() == None):
            raise CfgNotDefaultError(
                '\n>>>The base.cfg file needs [DEFAULT] section!')
        elif(config.has_option('DEFAULT', 'URL') == False):
            raise CfgMissOptionError(
                '\n>>>The DEFAULT section miss URL option')
        elif(config.has_option('DEFAULT', 'USER') == False):
            raise CfgMissOptionError(
                '\n>>>The DEFAULT section miss USER option')
        elif(config.has_option('DEFAULT', 'PASSWORD') == False):
            raise CfgMissOptionError(
                '\n>>>The DEFAULT section miss PASSWORD option')
        elif(config.has_option('DEFAULT', 'TestXML') == False):
            raise CfgMissOptionError(
                '\n>>>The DEFAULT section miss TestXML option')
        else:
            # print '>>>[Config file is OK]'
            pass
        self.cfg_file_info = config
        return
