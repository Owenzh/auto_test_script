import xml.etree.ElementTree as ET
import ConfigParser
import re
from icc_test_case import ICCTestCase
from icc_case_step import ICCCaseStep
from ICCError import MissSpecificSectionError
from ICCError import MissSpecificOptionError
from ICCError import ParserVariableError


def getTestSuite(cfg):
    xml_list = str(cfg.cfg_file_info.defaults().get('testxml')).split(',')
    xml_folder = cfg.test_xml_path + cfg.cur_sep
    xml_file_count = len(xml_list)
    TestSuite = []
    for idx in range(xml_file_count):
        tree = ET.parse(xml_folder + xml_list[idx])
        suite = tree.getroot()
        for case in suite:
            caseinfo = case.attrib
            steps_list = list(case)
            steps_len = len(steps_list)
            prev_step = []
            targ_step = []
            last_step = []
            targetIdx = 0
            target_step = None
            for i in range(steps_len):
                tar_flag = steps_list[i].get('target', default=None)
                if (tar_flag is not None) or (steps_len == 1):
                    targ_step.append(steps_list[i])
                    target_step = steps_list[i]
                    targetIdx = i
                    break

            prev_step = steps_list[0:targetIdx]
            last_step = steps_list[(targetIdx + 1):steps_len]
            p = _parserStep(cfg, caseinfo, prev_step)
            t = _parserStep(cfg, caseinfo, targ_step, step_type='target')
            l = _parserStep(cfg, caseinfo, last_step)

            tc = ICCTestCase(caseinfo.get('id'), caseinfo.get('name'), p, t, l)
            TestSuite.append(tc)
    return TestSuite


def _findDefaultValue(_cfg, _key, _type, _option):
    if(_type == None):
        _type = ''
    _section = str(_key + _type)
    if(_cfg.has_section(_section) == False):
        raise MissSpecificSectionError('\n>>>Miss specific section  "' +
                                       _section + '" at base.cfg')
    else:
        try:
            default_value = _cfg.get(_section, _option)
        except ConfigParser.NoOptionError:
            raise MissSpecificOptionError('\n>>>Miss specific option  "' +
                                          _option + '" at "' + _section + '" section')

    return default_value


def _parserStep(cfg, caseinfo, step_list, step_type='normal'):
    step_new_list = []
    # print len(step_list)
    cloud_type = caseinfo.get('TYPE')
    case_id = caseinfo.get('id')
    for i in range(len(step_list)):
        step = step_list[i]
        stepinfo = step.attrib
        opt = stepinfo.get('OPTKEY')
        execution = None
        expected = None
        paramList = []
        for child in step:
            if(child.tag == 'params'):
                for param in child:
                    text = ''
                    tag = str(param.tag)
                    if(param.text):
                        text = str(param.text)
                    if(text == "?"):
                        text = _findDefaultValue(
                            cfg.cfg_file_info, opt, cloud_type, tag)
                    paramList.append(
                        tag + '(' + _parserVariable(cfg.cfg_file_info, text) + ')')
            elif(child.tag == 'execution_type'):
                execution = child.text
            elif(child.tag == 'expected_result'):
                expected = child.text
            else:
                pass
        step_obj = ICCCaseStep(case_id, execution, expected,
                               cloud_type, step_type)
        # print paramList
        step_obj.parserCLI(opt, paramList)
        step_new_list.append(step_obj)

    return step_new_list


def _parserVariable(cfg, txt):
    pattern = r'(\{\w+\})+'
    var_list = re.findall(pattern, txt)
    if len(var_list) > 0:
        for idx in range(len(var_list)):
            _var = var_list[idx]
            v = re.findall(r'\w+', _var)
            try:
                newVal = cfg.get('VARIABLE', v[0])
            except ConfigParser.NoOptionError:
                raise ParserVariableError(
                    '\n>>>Parser variable error: Can not find given "{0}" variable'.format(v[0]))
            txt = txt.replace(_var, newVal)
    return txt
