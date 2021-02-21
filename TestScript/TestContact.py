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
# 取出所有行，使用切片获取非第一行的所有行，因为第一行是标题，所以不用取
# 遍历每一行，然后使用读取这一行单元格的方法，将用户名和密码读取到两个
# 变量里面，然后传到login方法中，调用即可
pe = ParseExcel(test_data_excel_path)
pe.set_sheet_by_index(0)
print pe.get_default_name()
rows=pe.get_all_rows()[1:]
for id,row in enumerate(rows):
    if row[is_executed_col_no].value=='y':
        print "username:",row[username_col_no].value
        print "password:",row[password_col_no].value
        username=row[username_col_no].value
        password=row[password_col_no].value
        driver = webdriver.Chrome(executable_path="e:\\chromedriver")
        try:
            login(driver, username, password)
            visit_address_page(driver)
            time.sleep(3)
            pe.set_sheet_by_index(1)
            print pe.get_default_name()
            print "all rows:",pe.get_all_rows()
            test_data_result_flag = True
            for id2, row in enumerate(pe.get_all_rows()[1:]):
                if row[7].value == 'y':

                    try:
                        print "log:",row[1],row[1].value
                        print "log:",type(row[1])
                        add_contact(driver, row[1].value, row[2].value, row[3].value, row[4].value, row[5].value)
                        pe.write_cell_content(id2 + 2, 9,date_time() )
                        pe.write_cell_content(id + 2, 9, date_time())
                        pe.write_cell_content(id2+2,10,"pass")
                        #assert 1==2
                    except Exception, e:
                        u"异常信息：", e.message
                        pe.write_cell_content(id + 2, 9, date_time())
                        pe.write_cell_content(id2 + 2, 10, "fail")
                        test_data_result_flag=False
                else:
                    pe.write_cell_content(id2 + 2, 10, u"忽略")
                    continue
            if test_data_result_flag==True:
                pe.set_sheet_by_index(0)
                pe.write_cell_content(id + 2, test_result_col_no, u"成功")
            else:
                pe.set_sheet_by_index(0)
                pe.write_cell_content(id + 2, test_result_col_no, u"失败")

        except Exception,e:
            pe.set_sheet_by_index(0)
            print u"异常信息：",e.message
            pe.write_cell_content(id + 2, test_result_col_no, "fail")
            pe.write_cell_content(id + 2, exception_info_col_no, "fail")

        time.sleep(3)
        driver.quit()
    else:
        pe.set_sheet_by_index(0)
        pe.write_cell_content(id + 2, test_result_col_no, u"忽略")
        continue
