#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ICCCaseStep:
    def __init__(self, case_id, execution, expected, cloud_type, step_type='normal'):
        self.id = case_id
        self.step_type = step_type
        self.execution = execution
        self.expected = expected
        self.command = ''
        self.cloud_type = cloud_type

    def parserCLI(self, opt, paramList):
        com = str(opt)
        for fun in paramList:
            com += ' ' + str(fun)
        self.command = com
        return com
