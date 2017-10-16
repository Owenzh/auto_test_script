#!/usr/bin/python
# -*- coding: UTF-8 -*-

from itoolkit import *
from itoolkit.rest.irestcall import *


class RunICC:
    def __init__(self, setting):
        url = str(setting.get('url'))
        user = str(setting.get('user'))
        password = str(setting.get('password'))
        self.itransport = iRestCall(url, user, password)

    def execCLI(self, cmdStr):
        itool = iToolKit(iparm=0, iret=0, ids=1, irow=0)
        defaultOpt = {'exec': 'system', 'error': 'fast'}
        itool.add(iCmd('iCMD', cmdStr, defaultOpt))
        itool.call(self.itransport)
        out_list = itool.list_out()
        exec_result = {}
        status_msg = str(out_list[0][0])
        hc_success = '+++ success'
        hc_error = '*** error'
        if(hc_success in status_msg):
            exec_result['key'] = 'S'
            exec_result['value'] = 'success'
        elif(hc_error in status_msg):
            exec_result['key'] = 'E'
            exec_result['value'] = str(out_list[0][1])
        itool = None
        return exec_result