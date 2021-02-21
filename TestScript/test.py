#encoding=utf-8
from selenium import webdriver
from Util.log import *
from Util.FormatTime import *
import time
from Action.visit_address_page import *
from Action.add_contact import *
from Action.login import *
from ProjectVar.var import *
import sys
reload(sys)
sys.setdefaultencoding("utf8")

pe2 = ParseExcel(test_data_excel_path)
pe2.set_sheet_by_index(1)
print pe2.get_default_name()
print  pe2.get_all_rows()
