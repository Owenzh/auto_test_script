# -*- coding: utf-8 -*-
from _ParametrizedTestCase import ParametrizedTestCase
from ICCError import CommandRunError
from runtime_compare import RuntimeCompare
from icc_utils import clearDirectories
from read_cfg import InitConfig


class TestICC(ParametrizedTestCase):

    def setUp(self):
        # clearDirectories(self.param['cfg'])
        pass

    def tearDown(self):
        # clearDirectories(self.param['cfg'])
        pass

    @classmethod
    def setUpClass(cls):
        print '>>>clean directories...'
        config = InitConfig().run().cfg_file_info
        clearDirectories(config)
        pass

    @classmethod
    def tearDownClass(cls):
        # config = InitConfig().run().cfg_file_info
        # clearDirectories(config)
        pass

    def test_cli(self):
        testcase = self.param['tc']
        ctx = self.param['ctx']
        exec_result = ctx.execCLI(testcase.command)
        executionDict = {'key': testcase.execution, 'value': testcase.expected}
        print 'execute result =>' + str(exec_result)

        exec_msg = exec_result.get('value')
        if(testcase.execution != 'R'):
            self.assertEqual(exec_msg, testcase.expected)
        else:
            print 'Runtime compare!'
            cfg = self.param['cfg']
            self.deal_with_runtime_compare(exec_msg, testcase, cfg)

    def shortDescription(self):
        caseDesc = self.param['tc']
        return '[' + str(caseDesc.id) + ']'

    def deal_with_runtime_compare(self, exec_val, tc, cfg):
        if(exec_val == 'success'):
            RTC = RuntimeCompare(tc, cfg)
            run_val = RTC.compare()
            self.assertEqual(run_val, True)
        else:
            raise CommandRunError(
                '\n>>>The command run fail.\n>>>' + tc.command)
