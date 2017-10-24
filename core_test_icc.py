# -*- coding: utf-8 -*-
from _ParametrizedTestCase import ParametrizedTestCase
from ICCError import CommandRunError
from runtime_compare import RuntimeCompare
from icc_utils import clearDirectories
from read_cfg import InitConfig


class TestICC(ParametrizedTestCase):

    def setUp(self):
        print '\n>>>[previous steps running]'
        prev_steps_q = self.param['tc'].prev_steps
        ctx = self.param['ctx']
        previous = []
        for i in range(len(prev_steps_q)):
            step = prev_steps_q[i]
            exec_result = ctx.execCLI(step.command)
            step_exec = {}
            step_exec['name'] = '>>>Previous Step ' + str(i + 1)
            step_exec['msg'] = '\t>>>'+ str(step.command) + '\n\t>>>' + str(exec_result)
            exec_msg = exec_result.get('value')
            if(step.execution == 'S'):
                step_exec['value'] = (exec_msg == step.expected)
            elif(step.execution == 'E'):
                step_exec['value'] = (exec_msg == step.expected)
            elif (step.execution == 'R'):
                print 'Runtime compare!'
                cfg = self.param['cfg']
                step_exec['value'] = self.deal_with_runtime_compare(
                    exec_msg, step, cfg)
            else:
                step_exec['value'] = True
            previous.append(step_exec)
        self.previous_steps = previous

    def tearDown(self):
        last_steps_q = self.param['tc'].last_steps
        ctx = self.param['ctx']
        for i in range(len(last_steps_q)):
            step = last_steps_q[i]
            exec_result = ctx.execCLI(step.command)
            exec_msg = exec_result.get('value')
            if(step.execution == 'S'):
                pass
            elif(step.execution == 'E'):
                pass
            elif (step.execution == 'R'):
                print 'Runtime compare!'
                cfg = self.param['cfg']
                self.deal_with_runtime_compare(exec_msg, step, cfg)
            else:
                pass
        pass

    @classmethod
    def setUpClass(cls):
        print '>>>[clean directories]'
        config = InitConfig().run().cfg_file_info
        clearDirectories(config)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_cli(self):
        print '\n>>>[target step running]'
        # previous step fail will stop case
        pre = self.get_previous_steps_result()
        if (pre is None):
            pass
        elif (len(pre) == 0):
            pass
        else:
            for p in pre:
                print p
            self.assertEqual(True, False)

        testcase = self.param['tc'].targ_steps[0]
        # print testcase.step_type
        ctx = self.param['ctx']
        exec_result = ctx.execCLI(testcase.command)
        exec_msg = exec_result.get('value')
        if(testcase.execution == 'S'):
            print 'execute result =>' + str(exec_result)
            self.assertEqual(exec_msg, testcase.expected)
        elif(testcase.execution == 'E'):
            print 'execute result =>' + str(exec_result)
            self.assertEqual(exec_msg, testcase.expected)
        elif (testcase.execution == 'R'):
            print 'Runtime compare!'
            cfg = self.param['cfg']
            self.deal_with_runtime_compare(exec_msg, testcase, cfg)
        else:
            pass

    def shortDescription(self):
        caseDesc = self.param['tc']
        return '[' + str(caseDesc.id) + '] ' + str(caseDesc.name)

    def deal_with_runtime_compare(self, exec_val, tc, cfg):
        if(exec_val == 'success'):
            RTC = RuntimeCompare(tc, cfg)
            run_val = RTC.compare()
            self.assertEqual(run_val, True)
            return run_val == True
        else:
            raise CommandRunError(
                '\n>>>The command run fail.\n>>>' + tc.command + '>>>\n Error code: ' + exec_val)

    def get_previous_steps_result(self):
        pres_len = len(self.previous_steps)
        res = []
        if(pres_len == 0):
            return None
        else:
            for idx in range(pres_len):
                step_res = self.previous_steps[idx]
                if(step_res['value'] == False):
                    res.append(step_res['name'] +
                               ' run fails.\n' + step_res['msg'])
            return res
