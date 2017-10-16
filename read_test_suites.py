import xml.etree.ElementTree as ET
import ConfigParser
from icc_test_case import ICCTestCase
from ICCError import MissSpecificSectionError
from ICCError import MissSpecificOptionError


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
            for child in case:
                if(child.tag == 'params'):
                    paramList = []
                    for param in child:
                        text = ''
                        tag = str(param.tag)
                        if(param.text):
                            text = str(param.text)
                        if(text == "?"):
                            text = _findDefaultValue(cfg.cfg_file_info, caseinfo.get(
                                'OPTKEY'), caseinfo.get('TYPE'), tag)
                        paramList.append(tag + '(' + text + ')')
                elif(child.tag == 'execution_type'):
                    execution = child.text
                else:
                    expected = child.text
            tc = ICCTestCase(caseinfo.get('id'), caseinfo.get(
                'name'), execution, expected, caseinfo.get('TYPE'))
            tc.parserCLI(caseinfo.get('OPTKEY'), paramList)
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
