#!/usr/bin/python
# -*- coding: UTF-8 -*-


class ICCTestCase:
    def __init__(self, id, name, prev, targ, last):
        self.id = id
        self.name = name
        self.prev_steps = prev
        self.targ_steps = targ
        self.last_steps = last
