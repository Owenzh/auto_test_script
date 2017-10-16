#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ICCTestCase:
    def __init__(self, id, name, execution, expected, cloud_type):
        self.id = id
        self.name = name
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
