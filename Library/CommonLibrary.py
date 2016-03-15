from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import datetime
import re
import os
import random
from operator import contains
from itertools import imap, repeat
import calendar
import csv
import win32clipboard
from pytz import timezone
import pytz
import time
import calendar
from datetime import datetime, time, date
from datetime import datetime
from datetime import date
from dateutil.parser import parse
import time
import datetime
import os
import socket
import string
import collections
from selenium import webdriver
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities 
from sys import exit

class CommonLibrary:
                
                def __init__(self):
                        pass
    
                def get_unique_id(self):
                    """Returns Unique Value by adding Time Stamp
                    """
                    return 'Test'+str(time.localtime().tm_year)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                def get_time_stamp(self,timezoneName='EST5EDT'):
                    """Returns the Current Date and Time
                    """
                    return datetime.datetime.now(timezone(str(timezoneName))).strftime('%a %m/%d/%Y %I:%M %p')
                
                def close_alert_message(self):
                    """Returns 'True'if any alert message displayed returns 'False' if not"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        selenium.get_alert_message()
                        return True
                    except:
                        return False


                def click_element_using_javascript(self,locator,n=1):
                    """Returns 'True' if the element clciking by Java Script with the 'locator' in the corresponding page else returns 'False' """

                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        elements = selenium._element_find(locator,False,True)
                        selenium._current_browser().execute_script("arguments[0].click();", elements[n-1])
                        return True
                    except Exception as exp:
                        print "not clcikable by JS, "+ str(exp)
                        return False
                
                    
                def table_verify_matching_row_values(self, table_locator, uniqueColDts,rowValuesValidation, expected):
                    """Takes the arguments 'table_locator','unique value','rowValuesValidation-accepts one or more column names','expected-expected error message'
                        Returns the matching rows with the unique value. If there are no matching rows returns expected error message. 
                        """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    uniColDts = uniqueColDts.split('|')
                    iUnColNo = self._table_get_column_no(table_locator,uniColDts[0])
                       
                    if iUnColNo == 0:
                        raise AssertionError("Unique Column Name:" + uniColDts[0] + " not found")
                    iRowNo = self.table_get_row_no(table_locator,iUnColNo,uniColDts[1])
                    print 'step2'
                    if iRowNo == 0:
                        raise AssertionError("UniqueValue :" + uniColDts[1] + " not found")
                    #Get the number of rows with the unique value
                    #rows = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr/td/div/div[contains(text(),"'+uniColDts[1]+'")]'))
                        
                    #iRowCount = rows                      
                    iRowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr/..//span[contains(text(),"'+uniColDts[1]+'")]'))
                    rowCounter = 0
                    values={}
                    for liCounter in range(len(rowValuesValidation)):
                            
                        colDts = rowValuesValidation[liCounter].split('|')
                        iColNo = self._table_get_column_no(table_locator,colDts[0])
                        print 'step4'
                        if iColNo == 0:
                            raise AssertionError("Column Name:" + colDts[0] + " not found")
                        values.setdefault(iColNo,colDts[1])
                    while rowCounter<iRowCount:
                        bStatus = True    
                        #Get the row that matches the unique value
                           
                        print "Matching row "+str(iRowNo)
                        #Loop through each value in the row set that should match
                        for valueIter in values.keys():
                            print 'step5'
                            try:
                                selenium.wait_until_element_is_visible(table_locator+'/tbody/tr/td['+str(valueIter)+']/div/div['+str(iRowNo)+']',"30s")
                            except:
                                print "print table cell data not displayed"
                            curValue = selenium._get_text(table_locator+'/tbody/tr/td['+str(valueIter)+']/div/div['+str(iRowNo)+']')
                            print "Actual "+curValue
                            print "Expected "+values.get(valueIter)
                            #Check if the cell value matches, if not break the loop to check for the next matching row. If the cell value matches break the loop
                            if curValue != values.get(valueIter):
                                bStatus = False
                                rowCounter +=1
                                break
                        iRowNo = self.table_get_row_no(table_locator,iUnColNo,uniColDts[1],rowCounter)
                            
                        if bStatus:
                            break
                                
                        #If no matching row has found matching row set report a failure
                        if not bStatus:
                            raise AssertionError("Values "+str(rowValuesValidation)+" do not match with values in any row of the table")
                        else:
                            return True

                def verify_element_present(self,locator):
                    """Returns 'True' if the element found with the 'locator' in the corresponding page else returns 'False'
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        bStatus = selenium._is_element_present(locator)
                        if(str(bStatus) != str(True)) and (str(BuiltIn().get_variable_value("${BROWSER}"))!="ie"):
                            selenium.capture_page_screenshot()
                        return bStatus
                    except:
                        print "Got Exception"
                        return True

                def wait_for_element_present(self,locator,timeout=None):
                    """Returns 'True' if the element present with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            return True
                        except:
                            print "ValueError: Element locator "+str(locator) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locator)
                    return False

                def wait_for_element_not_present(self,locator,timeout=None):
                    """Returns 'True' if the element not present with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "5s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,10):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_for_element_invisible(locator,"5s")
                            
                        except:
                            print "exception : element is not present"
                            return True
                    return False

               

                def verify_element_visible(self,locator):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False'
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        try:
                            bStatus = selenium._is_visible(locator)
                            if(str(bStatus) != str(True)) and (str(BuiltIn().get_variable_value("${BROWSER}"))!="ie"):
                                selenium.capture_page_screenshot()
                            return bStatus
                        except:
                            print "Got exception"
                    return False
                
                def wait_for_element_visible(self,locator,timeout=None,messgae=''):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            selenium.wait_until_element_is_visible(locator,timeout)
                            return True
                        except:
                            if(len(messgae)>0):
                                print "Error Message:" +str(messgae)
                            print "ValueError: Element locator "+str(locator) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locator)
                    return False

                def wait_for_element_invisible(self,locator,timeout=None):
                    """Returns 'True' if the element visible with the 'locator' in the corresponding page else returns 'False' base timeout
                    """
                    if(timeout == None):
                        timeout = "3s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,20):
                        print "iCounter: "+str(iCounter)
                        try:
                            time.sleep(3)
                            selenium.wait_until_page_contains_element(locator,timeout)
                            selenium.wait_until_element_is_visible(locator,timeout)
                        except:
                            print "exception : element is not visible"
                            return True
                    return False

                def get_text(self,locator,timeout=None):
                    """Returns the element visible text values other wise keyword will fail with proper reason """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    textVal = ""
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    for iCounter in range(1,10):
                        print "get_text iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            textVal = selenium.get_text(locator)
                            print "textVal="+str(textVal)
                            return textVal
                        except:
                            print "Unable get text"
                    raise AssertionError("Unable to get text from specified locator locator= "+str(locator))

                def mouse_scrolling(self,locator,timeout=None):
                    """Returns the element visible text values other wise keyword will fail with proper reason """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    if bStatus==False:
                        return False
                    for iCounter in range(1,5):
                        print "mouse_scrolling iCounter: "+str(iCounter)
                        try:
                            textVal = selenium.mouse_scroll(locator)
                            return True
                        except:
                            print "Unable do scrolling"
                    raise AssertionError("Unable perform mouse scroll on specified locator locator= "+str(locator))


                def enter_text(self,locator,inputValue,timeout=None):
                    """It will enter the specified value into the specifies text field  """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    textVal = ""
                    bStatus = self.wait_for_element_visible(locator,timeout)
                    for iCounter in range(1,10):
                        print "enter text: iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            textVal = selenium.input_text(locator,inputValue)
                            print "textVal="+str(textVal)
                            return textVal
                        except:
                            print "Unable get text"
                            time.sleep(1)
                    raise AssertionError("Unable to enter text into the specified field vased locator ,locator= "+str(locator))


                def get_element_attribute_value(self,locator,timeout=None):
                    """Returns the element attribute values """
                    if(timeout == None):
                        timeout = "30s"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    attVal = None
                    locator = str(locator)
                    print "locator="+str(locator)
                    elementlocator = locator[0:int(locator.rfind("@"))]
                    try:
                        selenium.wait_until_page_contains_element(elementlocator,timeout)
                        bStatus = True
                    except:
                        print "element not present"
                        bStatus = False
                    for iCounter in range(1,6):
                        print "get_element_attribute iCounter: "+str(iCounter)
                        if bStatus==False:
                            break
                        try:
                            attVal = selenium.get_element_attribute(locator)
                            print "attVal="+str(attVal)
                            return attVal
                        except:
                            print "Unable get text"
                    raise AssertionError("Unable get element attribute value ,locator= "+str(locator))


                def wait_for_dropdown_selection(self,locatorxpath,listVal,timeout=None):
                    """This keyword will wait upto selection was done  and return the True or False"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if(timeout == None):
                        timeout = "20s"
                    for iCounter in range(1,3):
                        print "wait_for_dropdown_selection iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath+"/option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            selenium.wait_until_element_is_visible(locatorxpath+"/option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            return True
                        except:
                            print "drop down option was not selected within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                        
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            selenium.wait_until_element_is_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            return True
                        except:
                            print "drop down option was not selected within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                    return False
                
                def _table_get_column_no(self, table_locator, columnName):
                    """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
                    #try:
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        selenium.wait_for_element_visible(table_locator+'/tbody/tr/td',"30s")
                    except:
                        print "Table was Not Displayed within time,Please check above screesnshot" 
                    colCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr/td'))
                    print "colCount: "+str(colCount)
                    for iCounter in range(1,colCount+1):
                        print "iCounter: "+ str(iCounter)
                        curColName = self.get_text(table_locator+'/tbody/tr/td['+str(iCounter)+']/div/div[1]')
                        print "curColName: "+ str(curColName)
                        if (curColName.strip()==columnName.strip()):
                            print "column name match"
                            #print iCounter
                            return iCounter
                        
                    return 0

                def table_get_column_no(self, table_locator, columnName):
                    """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
                    #try:
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td')
                    colCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr/td'))
                    print "colCount: "+str(colCount)
                    for iCounter in range(1,colCount+1):
                        print "iCounter: "+str(iCounter)
                        curColName = self.get_text(table_locator+'/tbody/tr/td['+str(iCounter)+']/div/div[1]')
                        print "curColName: "+ str(curColName)
                        if (curColName.strip()==columnName.strip()):
                            print "column name match"
                            #print iCounter
                            return iCounter
                        
                    return 0


                def table_get_row_no(self, table_locator, columnNo,Value,index=0):
                    """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
                    #try:
                    index = int(index)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div',"10s")
                    iPrevRowNo = self._get_element_index(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div',Value)
                    print "iPrevRowNo="+str(iPrevRowNo)
                    if index==0:
                        return iPrevRowNo
                    else:
                        myval = selenium._element_find(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iPrevRowNo+index)+']/div/span',True,True).text
                        #myval = self.get_text(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iPrevRowNo+index)+']/div/span',True,True).text
                        if myval!=Value:
                            iRowNo=0
                        else:
                            iRowNo=iPrevRowNo
                        if iRowNo==0:
                            return 0
                        else:
                            return iPrevRowNo+index
                        #except:
                        return 0

                def get_table_row_no(self, table_locator, columnNo,Value,index=0):
                    """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
                    #try:
                    index = int(index)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div',"10s")
                    iPrevRowNo = self._get_element_index(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div',Value)
                    print "iPrevRowNo="+str(iPrevRowNo)
                    if index==0:
                        return (iPrevRowNo-1)
                    else:
                        myval = selenium._element_find(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iPrevRowNo+index)+']/div/span',True,True).text
                        #myval = self.get_text(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iPrevRowNo+int(index))+']/div/span',True,True).text
                        if myval!=Value:
                            iRowNo=0
                        else:
                            iRowNo=iPrevRowNo
                        if iRowNo==0:
                            return 0
                        else:
                            retVal = int(iPrevRowNo)+int(index)-1
                            print "retVal: "+str(retVal)
                            return True
                            
                        #except:
                        return 0

                def table_get_row_selection_status(self, table_locator, rowNo):
                    """Returns the specified row selection status from the table located at 'table_locator'."""
                    #try:
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rowNo = int(rowNo)+1
                    rowNo = str(rowNo)
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td[1]/div/div')
                    for iIndex in range(1,5):
                        try:
                            attVal = self.get_element_attribute_value(table_locator+'/tbody/tr/td[1]/div/div['+ str(rowNo)+']@class')
                            print "attVal: " + str(attVal)
                            if attVal.lower().find("selected")>=0:
                                return True
                            else:
                                time.sleep(2)
                        except:
                            print "attribute value is not reading correctlly"
                    return False


                def table_get_row_highlighted_status(self, table_locator, rowNo):
                    """Returns the specified row highlighted status from the table located at 'table_locator'."""
                    #try:
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rowNo = int(rowNo)+1
                    rowNo = str(rowNo)
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td[1]/div/div')
                    for iIndex in range(1,5):
                        try:
                            attVal = self.get_element_attribute_value(table_locator+'/tbody/tr/td[1]/div/div['+ str(rowNo)+']@class')
                            print "attVal: " + str(attVal)
                            if attVal.lower().find("highlighted")>=0:
                                return True
                            else:
                                time.sleep(2)
                        except:
                            print "attribute value is not reading correctlly"
                    return False

                
                def table_get_headers(self, table_locator, headerName, sessionNum):
                    """Takes the Arguments as 'table_locator','headername','sessionNum' and Returns the activities headers from the Activities table from the
                    Account Detail page"""
                    
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    AccountDetails = BuiltIn().get_library_instance('AccountDetails')
                    rfHeatMapdts = AccountDetails.get_timeline_headers_color(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}"),headerName,sessionNum)
                    return rfHeatMapdts.keys()
                
                def is_digit(self,string):
                    return string.isdigit()
                
                def get_index_val(self,locator,expected):
                    """ Returns index value for the exact match with the expected value"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rowCount = int(selenium.get_matching_xpath_count(locator))
                    for iCounter in range(1,rowCount+1):
                        actualVal = selenium.get_text(locator+'['+str(iCounter)+']/td[2]')
                        print "actualVal:"+str(actualVal)
                        if actualVal==expected:
                            return iCounter

                def list_comparison(self, li_actual, li_expected,message=''):
                    """ Takes Two lists as Arguments and Pass if the two lists are equal else Fails"""
                    print 'Expected: %s\n' % str(li_expected)
                    print 'Actual: %s' % str(li_actual)
                    if li_actual == []:
                        raise AssertionError('Actual is empty')                    
                    for index in range(0,len(li_expected)):
                        if li_expected[index] in li_actual:
                            continue
                        for actualIndex in range(0,len(li_actual)):
                            if li_expected[index][:14] in li_actual[actualIndex]:
                                break
                        else:
                            raise AssertionError('Actual does not match expected'+str(message))
                
                def list_difference(self, li_actual, li_expected):
                    """Takes Two lists as arguments and returns a list containing the difference of the two lists"""
                    return list(set(li_expected).difference(set(li_actual)))    
                             
                def list_comparison_partially(self,li_actual, li_expected):
                    """ Takes Two lists as Arguments and Pass if the two lists are equal else Fails"""
                    print 'Expected: %s\n' % str(li_expected)
                    print 'Actual: %s' % str(li_actual)
                    if li_actual == []:
                        raise AssertionError('Actual is empty')                    
                    
                    if len(li_actual)==len(li_expected):
                        for index in range(0,len(li_actual)):
                            element1=li_actual[index].lower()
                            element2=li_expected[index].lower()
                            if not (element2.find(element1)>=0 or element1.find(element2))>=0:
                                print "error "
                                return False
                    else:
                        print "len vals not same"
                        return False
                    return True

                def partial_value_count_in_list(self,list_actual, item):
                    """ It will return count of value in the specified values"""
                    print 'Expected val ' +str(item)
                    print 'Actual: %s' % str(list_actual)
                    intCount = 0
                    for index in range(0,len(list_actual)):
                        element1=list_actual[index].lower()
                        if element1.find(item)>=0:
                            intCount = intCount +1
                    return intCount


                def get_element_index(self, table_locator,value):
                    """Returns the index of the value located by the table locator 'table_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    index = self._get_element_index(table_locator,value)
                    return index

                def verify_item_in_context_menu_disabled(self, element):
                    """Returns True if the 'element' disabled in the Context Menu else returns False """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    elementStyle = selenium.get_element_attribute("//span[contains(text(),'"+element+"')]@style")
                    if ("color:#bbbbbb" in elementStyle) or ("color: rgb(187, 187, 187)" in elementStyle):
                        return True
                    else:
                        return False

                def click_column_to_sort(self, table_locator, columnName):
                    """Clicks on the column with the 'columnName' from the table located at 'table_locator' having the"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    iColNo = self._table_get_column_no(table_locator, columnName)
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td['+str(iColNo)+']/div/div[1]')
                    selenium.click_element(table_locator+'/tbody/tr/td['+str(iColNo)+']/div/div[1]')
                    time.sleep(3)
                    return True
                #def get_cell_value(self, table_locator, columnNo, iRowNo):
                    "Returns the text located in the table 'table_locator' with in the Column 'columnNo' and matching Row 'iRowNo'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if int(columnNo)<1 or int(iRowNo)<1:
                        raise AssertionError('Please send RowNo and Column No arguments as non zero value, columnNo= ' +str(columnNo)+ 'iRowNo='+str(iRowNo))
                        
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(int(iRowNo)+1)+']/div/span')
                    return selenium._element_find(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(int(iRowNo)+1)+']/div/span',True,True).text

                def get_cell_value(self, table_locator, columnNo, iRowNo):
                    "Returns the text located in the table 'table_locator' with in the Column 'columnNo' and matching Row 'iRowNo'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if int(columnNo)<1 or int(iRowNo)<1:
                        raise AssertionError('Please send RowNo and Column No arguments as non zero value, columnNo= ' +str(columnNo)+ 'iRowNo='+str(iRowNo))
                        
                    return self.get_text(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(int(iRowNo)+1)+']/div/span')

                def double_click_table_row(self, table_locator, columnNo, Value='',iRowNo=0):
                    """Double Clicks on the table row of the table 'table_locator' and in the column 'columnNo'  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, columnNo, Value)
                    else:
                        iRowNo=iRowNo+1
                    selenium.double_click_element(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div/span')

                def right_click_on_table_row(self, table_locator, columnNo, Value='',iRowNo=0):
                    """Performs the Action Right Mouse Click on the column of the table located at 'table_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, columnNo, Value)
                    else:
                        iRowNo=iRowNo+1
                    print "iRowNo:"+str(iRowNo)
                    try:
                        self.wait_and_click_element(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div')
                        self.wait_for_element_based_on_attribute_value(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']','class','Selected')
                        selenium.open_context_menu(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div')
                    except:
                        raise AssertionError('Open context menu not working on table')                        

                def left_click_on_table_row(self, table_locator, columnNo, Value='',iRowNo=0):
                    """Performs the Action Left Mouse Click on the column of the table located at 'table_locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print Value
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, columnNo, Value)
                        print "iRowNo-> " +str(iRowNo)
                    else:
                        iRowNo=iRowNo+1
                    if iRowNo==0:
                        raise AssertionError('No row matching the expected value')
                    print "iRowNo: "+str(iRowNo)
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div')
                            selenium.click_element(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div')
                            self.wait_for_element_based_on_attribute_value(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']','class','Selected')                            
                            return True
                        except:
                            print "Exception: left_click_on_table_row keyword"
                    raise AssertionError('Left clicking on table row keyword got failed')
                
                def select_item_in_table_row(self, table_locator, Value='',iRowNo=0):
                    """Clicks on the Row at which the 'value' on the table 'table_locator' founds """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, 4, Value)
                    else:
                        iRowNo=iRowNo+1
                    self.wait_for_element_visible(table_locator+'/tbody/tr/td[1]/div/div['+str(iRowNo)+']/div/div/input')
                    selenium.click_element(table_locator+'/tbody/tr/td[1]/div/div['+str(iRowNo)+']/div/div/input')
                    #selenium._selenium.fire_event(table_locator+'/tbody/tr/td[1]/div/div['+str(iRowNo)+']/div/div/input','click')
                def unselect_item_in_table_row(self, table_locator, Value='',iRowNo=0):
                    """Unselects the table row at which the 'value' found on the table 'table_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, 4, Value)
                    else:
                        iRowNo=iRowNo+1
                    selenium.click_element(table_locator+'/tbody/tr/td[1]/div/div['+str(iRowNo)+']/div/div/input')

                def check_status_for_table_row_item(self, table_locator, expected_value, Value='',iRowNo=0):
                    """Finds the status of a row of the table 'table_locator' and returns true if it is equal to the expected status 'expected_value' false if not """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print Value
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, 4, Value)
                    else:
                        iRowNo=iRowNo+1
                    src = selenium.get_element_attribute(table_locator+"/tbody/tr/td[2]/div/div["+str(iRowNo)+"]/div/img@src")
                    print src
                    src = src[55:].replace('.png','').replace('_',' ').replace('V','Viewed').replace('D','Dismissed').replace('N','Not ').replace('CO','Open Case Owned')
                    print "replacedsrc:"+str(src)
                    if src==expected_value:
                        return True
                    raise AssertionError('Values do not match '+src+' and '+expected_value)
                    
                    
                def check_session_status(self, expected_value):
                    """Returns True if the sesssion status matches with 'expected_value' fails if not"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icount in range(0,5):
                        status=self.wait_for_element_visible("//div[contains(@id,'dismissButton') and contains(@class,'disabled')]")
                        if status==True:
                            try:
                                if selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.sessionPaneHeader}") + "/tbody/tr/td/img@title")==expected_value:
                                    return True
                            except:
                                print "dismiss button was not disabled"
                        else:
                            self.wait_for_element_visible("//div[contains(@id,'dismissButton')]")
                            selenium.click_image("//div[contains(@id,'dismissButton')]//img")
                    raise AssertionError('The values do not match')

                def select_icon(self, icon_locator):
                    """selects the icon located by the locator 'icon_locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print selenium._is_visible('//a[@title="'+icon_locator+'"]')
                    if not self.check_icon_selected(icon_locator):
                        selenium.click_link('//a[@title="'+icon_locator+'"]')
                    #if not selenium._selenium.get_attribute('//a[@title="'+icon_locator+'"]'+'@class')=='selected':
                     #   raise AssertionError("The icon "+icon_locator+" is not selected")
                    return True
                def check_icon_selected(self, icon_locator):
                    """Checks the icon located at 'icon_locator' if it is already selected"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if not selenium.get_element_attribute('//a[@title="'+icon_locator+'"]'+'@class')=='selected':
                        return False
                    return True
                def select_item_from_list(self, select_locator, itemValue):
                    """Selects the item with the 'itemValue' from the list appreared after clicking 'select_locator'  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.click_element(select_locator)
                    selenium._is_visible('//div[@class="'+itemValue+'"]/img')
                    #selenium.mouse_over('//div[@class="'+itemValue+'"]/img')
                    selenium.simulate('//div[@class="'+itemValue+'"]/img','click')
                def type_keys_into_textbox(self, text_locator,value):
                    """Enters text 'value' into 'text_locator' after checking the presence of the locator"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCnt in range(0,4):
                        try:
                            selenium.wait_until_page_contains_element(text_locator)
##                            try:
##                                selenium.click_element(text_locator)
##                            except:
##                                print "got exception while clicking on text field"
##                                continue
                            selenium._element_find(text_locator,True,True).send_keys(value)
                            return True
                        except:
                            time.sleep(3)
                            print "got exception"
                    return False
                def mouse_move(self, locator):
                    """Moves the Mouse to the 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.mouse_over(locator)
                def scroll_table_to_item(self, table_locator, Value, columnNo):
                    """Scrolls to the item found by the 'Value' in the column 'columnNo' on the table 'table_locator'  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #print "'"+BuiltIn().get_variable_value("${table.viewHistory.scrollToTableItem}")+"@style"+"'"
                    prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.viewHistory.scrollToTableItem}")+"@style")[18:]
                    iRowNo = 0
                    uniColDts = Value.split('|')
                    iRowNo = self.table_get_row_no(table_locator, 1, uniColDts[1])
                    print 'here the row number is something'+str(iRowNo)
                    if iRowNo==0:
                        selenium.mouse_down(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                        selenium.mouse_up(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                        #prevvalue = selenium._selenium.get_attribute('ajs_T_RiskAppUserTable_tData_F_RiskAppUserTable_tData_bar_knob@style')[18:]
                        while(not (prevvalue==selenium.get_element_attribute(BuiltIn().get_variable_value("${table.viewHistory.scrollToTableItem}")+"@style")[18:])):
                            prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.viewHistory.scrollToTableItem}")+"@style")[18:]
                            iRowNo = self.table_get_row_no(table_locator, 1, uniColDts[1])
                            if not(iRowNo==0):
                                return iRowNo
                            selenium.mouse_down(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                            selenium.mouse_up(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                        selenium.mouse_down(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                        selenium.mouse_up(BuiltIn().get_variable_value("${table.mouseUp.scrollToTableItem}"))
                        iRowNo = self.table_get_row_no(table_locator, 1, uniColDts[1])
                        if not(iRowNo==0):
                            return iRowNo
                        raise AssertionError('The value not found')
                def wait_for_ajax(self,time_out=5):
                    """ Wailt for given time"""
                    '''selenium = BuiltIn().get_library_instance('Selenium2Library')
                    status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
                    print status'''
                    timeout = 0
                    while(timeout<time_out):
                        '''status = selenium._selenium.get_eval('(window.jQuery || { active : 0 }).active')
                        if(status):
                            return True'''
                        time.sleep(1)
                        timeout=timeout+1
                    return True
                def _get_element_index(self,locator,expected):
                    """Returns index of the element at which the 'expected' value found """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator,"5s")
                    elements = selenium.get_matching_xpath_count(locator)
                    print "elements : "+str(elements)
                    for ele in range(int(elements)):
                        newelements = selenium._element_find(locator,False,False)
                        print "newelements:"+str(newelements)
                        actual = newelements[ele].text
                        print "actual : "+str(actual)
                        if expected in actual:
                            print "header:"+str(newelements[ele].text)
                            print 'matched at'+str(ele+1)
                            return ele+1
                    else:
                        return 0
                def select_my_window(self,windowname=''):
                    """Selects the window by the window name """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    browser = selenium._current_browser()
                    #print browser.get_current_window_info()
                    x=browser.get_window_handles()
                    print x
                    '''if windowname=='':
                        browser.switch_to_window(x[0])'''
                    browser.switch_to_window(x[1])
                    print 'done'
                    '''for handle in range(len(x)):
                        browser.switch_to_window(x[handle])
                        print selenium.get_title()'''
                    return True
                
                def press_down_key(self,locator):
                    """ Presses the down Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_DOWN)
                            return True
                        except:
                            print "Exception in press_down_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_down_key")
                
                def press_up_key(self,locator):
                    """ Presses the up Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_UP)
                            return True
                        except:
                            print "Exception in press_up_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_up_key")

                def modifyFraudExportedFile(self,strFile,newFilePath):
                    """Modifies the exported file and returns new file path """
                    #newFilePath = re.sub(".csv","_new.csv",strFile)

                    linestring = open(strFile,'r').read()
                    listLines = linestring.split('\n')
                    #Get Owner name column numer
                    colList = listLines[0].split(',')
                    print len(listLines)
                    for i in range(1,len(listLines)):                         
                        print "getline:"+str(i)+":"+str(listLines[i])
                    colOwnerNo = 0
                    colDescNo = 0
                    for i in range(len(colList)):
                        if colList[i] == '"Description"':
                            colDescNo=i
                        if colList[i] == '"Owner"':
                            colOwnerNo = i
                            break

                        

                    #get the owner name and description from first row
                    colList = listLines[1].split(',')
                    currentOwner = colList[colOwnerNo]
                    currentDesc = colList[colDescNo]

                    #Search and Replace the owner name and description of first row
                    listLines[1] = re.sub(currentDesc,'"modified descrption"' ,listLines[1],count=1)
                    listLines[1] = re.sub(currentOwner,'"dummyOwner"',listLines[1],count=1)


                    #Replace data and write to new file
                    count = 0
                    newfile = open(newFilePath,'w')
                    oldfile = open(strFile)
                    for line in oldfile:
                        #Modify the owner and description data
                        if count == 1:                            
                            newfile.write(listLines[1]+'\n')
                        else:
                            newfile.write(line)
                        count = count + 1

                    newfile.close()
                    oldfile.close()
                    return len(listLines)-2
                    #os.remove(strFile)
                    #os.rename(newFilePath,strFile)
                

                def get_items_in_context_menu(self, locator):
                    """Returns the text from the context menu located by 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    return selenium.execute_javascript("return document.getElementById('dashMenu_4').getElementsByTagName'div')[1].getElementsByClassName('rich-menu-item rich-menu-item-enabled')["+str(locator)+"].getElementsByTagName('span')[1].textContent")

                def get_element_text(self,element,child):
                    """Returns the text found at the 'child' of the 'element' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    id = selenium.get_element_attribute(element+'@id')
                    print "id:"+str(id)
                    return selenium.execute_javascript('return document.getElementById("'+id+'").childNodes['+str(child)+'].textContent')
                    #return selenium.execute_javascript("return document.getElementById('"+id+"').childNodes['"+str(child)+"'][2].getElementsByTagName('td').textContent")

                def input_file_name(self,locator,value):
                    """Enters the 'value' into the field located by 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    selenium._element_find(locator,True,True).send_keys(value)
                    return True

                def get_custom_dropdown_commands(self, locator):
                    """Returns a list of commands under Custom Dropdown """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${list.reports.dateFilter}"))
                    listCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.dateFilter}")))
                    list = []
                    for item in range(1,listCnt+1):
                        currentVal = selenium.get_text(locator+'['+str(item)+']')
                        list.append(currentVal)
                    return list
                def match_table_values(self, table_locator, uniqueColDts,rowValuesValidation, expected):
                    """Takes 'table_locator' and column that has unique values 'uniqueColDts' and values to be searched 'rowValuesValidation' and returns the Matching rows from the table.
                        if the Values to be matched not found in the table it will return a 'expected' Error message"""
                    uniColDts = uniqueColDts.split('|')
                    timestamp = datetime.datetime.strptime(uniColDts[1],'%a %m/%d/%Y %I:%M %p')
                    timestamps = [ timestamp.strftime('%a %m/%d/%Y %I:%M %p'), (timestamp-datetime.timedelta(minutes=1)).strftime('%a %m/%d/%Y %I:%M %p'),(timestamp-datetime.timedelta(minutes=-1)).strftime('%a %m/%d/%Y %I:%M %p')]
                    for time in timestamps:
                        try:
                            if self.table_verify_matching_row_values(table_locator,uniColDts[0]+'|'+time,rowValuesValidation,expected):
                                print 'success'
                                break
                        except:
                            print time+' did not match'
                def get_current_date(self,timezoneName="EST5EDT"):
                    """ Returns the current date in the format month date year"""
                    if timezoneName==None:
                        cdate = datetime.datetime.now()
                        cdate = cdate.strftime("%m/%d/%Y")
                    else:
                        cdate = datetime.datetime.now(timezone(str(timezoneName))).strftime('%m/%d/%Y')
                    return cdate

                def get_from_date(self, fromDate,timezoneName='EST5EDT'):
                    """Substracts the days from the current date to get the From date"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    fromdate = cdate - datetime.timedelta(days=int(fromDate))
                    return fromdate.strftime("%m/%d/%Y")

                def get_last_week_last_date(self,timezoneName="EST5EDT"):
                    """Returns the Last week last date to compare with the To date after selecting the Date dropdown item 'Previous Week'"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    print "cdate: "+str(cdate)
                    lastweeklastday = datetime.datetime.now(timezone(str(timezoneName))).weekday()
                    if int(lastweeklastday)==6:
                        lastweeklastday = 1
                    else:
                        lastweeklastday = lastweeklastday + 2
                    lastday = cdate - datetime.timedelta(days=int(lastweeklastday))
                    return lastday.strftime("%m/%d/%Y")
                    
                def get_last_week_first_date(self,timezoneName="EST5EDT"):
                    """Returns the Last week first date to compare with the From date after selecting the Date dropdown item 'Previous Week'"""
                    cdate = datetime.datetime.now(timezone(str(timezoneName)))
                    lastweeklastday = datetime.datetime.now(timezone(str(timezoneName))).weekday()
                    if int(lastweeklastday)==6:
                        lastweeklastday = 7
                    else:
                        lastweeklastday = lastweeklastday + 8
                    firstday = cdate - datetime.timedelta(days=int(lastweeklastday))
                    return firstday.strftime("%m/%d/%Y")

                def get_last_month_last_date(self,timezoneName="EST5EDT"):
                    """Returns the Last month last date to compare with the To date after selecting the Date dropdown item 'Previous Month'"""
                    first_day_of_current_month = datetime.datetime.now(timezone(str(timezoneName))).today().replace(day=1)
                    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
                    return last_day_of_previous_month.strftime("%m/%d/%Y")

                def get_last_month_first_date(self,timezoneName="EST5EDT"):
                    """Returns the Last Month first date to compare with the From date after selecting the Date dropdown item 'Previous Month'"""
                    first_day_of_current_month = datetime.datetime.now(timezone(str(timezoneName))).today().replace(day=1)
                    last_day_of_previous_month = first_day_of_current_month - datetime.timedelta(days=1)
                    first_day_of_last_month = datetime.date(day=1, month= last_day_of_previous_month.month, year= last_day_of_previous_month.year)
                    return first_day_of_last_month.strftime("%m/%d/%Y")

                def get_timezone_from_date(self,timezone):
                    """Returns the Time zone from the 'timezone'"""
                    words = timezone.split()
                    splitleft = words[1].split("(")
                    splitright = splitleft[1].split(")")
                    return splitright[0]

                def get_graph_chart_color_in_reports_page(self, colorIndex):
                    """Returns a list containing Graph chart colors found at the index 'colorIndex'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    colorList= []
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${label.reports.graphChart.color}"))
                    cnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.reports.graphChart.color}")))
                    cnt = int(cnt/2)
                    print cnt
                    for iCounter in range(1,cnt+1):
                        for iCount in range(int(colorIndex)):
                            bStatus = self.verify_element_present(BuiltIn().get_variable_value("${label.reports.graphChart.color}")+str(colorIndex)+"_0')]")
                            print bStatus
                            if bStatus:
                                sessionColor = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.reports.graphChart.color}")+str(colorIndex)+"_0')]/div@style")
                                print sessionColor
                                if sessionColor.find('#AD2021') > 0:
                                    colorList.append('red')
                                elif sessionColor.find('#E7CF18') > 0:
                                     colorList.append('yellow')
                                elif sessionColor.find('#9BE29E') > 0:
                                    colorList.append('blue')
                                elif sessionColor.find('#07B70C') > 0:
                                    colorList.append('green')       
                    return colorList

                def get_risk_dropdown_items(self):
                    """Returns a list of risk items found under Risk dropdown """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${list.reports.riskdropdownitems}"))
                    cnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.riskdropdownitems}")))
                    risklist = []
                    for iCounter in range(1,cnt+1):
                        riskcol = selenium.get_element_attribute(BuiltIn().get_variable_value("${list.reports.riskdropdownitems}")+"["+str(iCounter)+"]@class")
                        risklist.append(riskcol)
                    return risklist

                def delete_space(self,word):
                    """deletes an undesired spce from the 'word' and returns the word """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    words = str(word)
                    deletespace = words.replace(' ','')
                    return deletespace
                    

                def get_custom_hover_over_dropdown_commands(self, locator):
                    """Returns a list containing items displayed after hovering on Custom Dropdown """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    listCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.customIconItems}")))
                    list = [] 
                    for item in range(1,listCnt+1):
                        currentVal = selenium.get_text(locator+"["+str(item)+"]/span[2]")
                        #print "locator is: "+locator+"["+str(item)+"]"/span[2]"
                        list.append(currentVal)
                    return list

                def get_sorted_sessionNumbers_in_reports_page(self, locator):
                    """ Returns the sorted list of session numbers from a table """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    sessionNumCnt = int(selenium.get_matching_xpath_count(locator))
                    list = []
                    for iCounter in range(1,sessionNumCnt+1):
                        sessionNum = selenium.get_text(locator+'['+str(iCounter)+']/div/span')
                        list.append(sessionNum)
                    return list
                        
                def get_table_columns_into_list(self,locator):
                    """ Returns a list of column names from a table"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        selenium.wait_until_element_is_visible(locator+'/tbody/tr/td')
                    except:
                        print "columns names are not displayed"
                    colCount = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                    print "colCount: "+str(colCount)
                    colNames=[]
                    for iCounter in range(1,colCount+1):
                        print "columns iCounter = "+str(iCounter)
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iCounter)+']/div/div')
                            colVal = self.get_text(locator+'/tbody/tr/td['+str(iCounter)+']/div/div')
                            print "iCounter: "+str(iCounter)+" ,colVal : "+str(colVal)
                            colNames.append(colVal)
                            if colVal == " " or colVal == "":
                                colNames.remove(colVal)
                        except:
                            print "got exception"
                    if len(colNames)==0:
                        raise AssertionError("The column names could not be fetched")
                    return colNames

                

                def get_values_for_multiple_columns_in_a_table(self,locator,*columnNames):
                    """Returns values of multiple columns in a table """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rowValues = []
                    valuesOfAllCols = []
                    for iColNme in range(0,len(columnNames)):
                        rowValues=[]
                        print columnNames[iColNme]
                        keyColNum = self._table_get_column_no(locator,columnNames[iColNme])
                        prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:]
                        colValues = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                        print "colValues:"+str(colValues)
                        for ele in range(1,int(colValues)):
                            colValues = selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div',False,False)
                            rowValues.append(colValues[ele].text)
                            if ((colValues[ele].text == " ") or (colValues[ele].text == "")):
                                print "removed"
                                rowValues.remove(colValues[ele].text)
                        print rowValues
                        valuesOfAllCols.append(rowValues)
                    #Scroll down
                    selenium.mouse_down(BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"))
                    selenium.mouse_up(BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"))
                    #Get the values from all rows by scrolling down
                    while(not (prevvalue==selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:])):
                        prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:]
                        for iColNme in range(0,len(columnNames)):
                            rowValues=[]
                            print columnNames[iColNme]
                            keyColNum = self._table_get_column_no(locator,columnNames[iColNme])
                            prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:]
                            colValues = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                            print "colValues:"+str(colValues)
                            for ele in range(1,int(colValues)):
                                colValues = selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div',False,False)
                                rowValues.append(colValues[ele].text)
                                if ((colValues[ele].text == " ") or (colValues[ele].text == "")):
                                    print "removed"
                                    rowValues.remove(colValues[ele].text)
                                print rowValues
                                valuesOfAllCols[iColNme].append(colValues[ele].text)
                        selenium.mouse_down(BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"))
                        selenium.mouse_up(BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"))
                    #Scroll back to the top
                    self.scroll_to_top()
                    return valuesOfAllCols                                          
                   
                def change_date_format(Self, date):
                    """ Returns a date after changing its format from 'month/date/year' to 'Year month date'"""
                    #date = date.replace('/',",")
                    return datetime.datetime.strptime(date, '%m/%d/%Y').strftime('%Y,%m,%d')
                
                def compare_dates_for_given_range(self, date1, date2):
                    """ Returns True if the 'date1' is less than 'date2' else fails"""
                    date1 = self.change_date_format(str(date1))
                    date2 = self.change_date_format(str(date2))
                    return datetime.date(date1)<datetime.date(date2)
                def list_comp_by_sequence(self, actualList,expectedList):
                    """Takes lists 'actualList' and 'expectedList'as arguments and compares them in the sequence """
                    if cmp(actualList,expectedList)!=0:
                        return False
                    return True
                def get_length_of_list(self, actuallist):
                    """Takes the list 'actuallist' as argument and finds the length of the list. Fails if the length of the list equal to Zero""" 
                    if len(actuallist)==0:
                        raise AssertionError('Actual is empty')
                    return len(actuallist)
                
                def get_countries_matching_enteredcriteria(self):
                    """Returns a list of countries displayed after entering a letter into country field of advance search"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    cnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.countriesmatchingcriteria}")))
                    countries = []
                    for iCounter in range(1,cnt):
                        cntrycol = selenium.get_text(BuiltIn().get_variable_value("${list.reports.countriesmatchingcriteria}")+"["+str(iCounter)+"]/td[2]")
                        countries.append(cntrycol)
                    return countries
                
                def get_sum_of_values_in_list(self, actuallist):
                    """Takes a list 'actualList' containing float values as argument and returns the sum of the list items"""
                    sum = 0
                    for index in range(0,len(actuallist)):
                        val = actuallist[int(index)]
                        print val
                        if val=="":
                            continue
                        sum = sum + int(val)
                    return sum
                def get_sum_of_float_values_in_list(self, actuallist):
                    """Takes a list 'actualList' containing float values as argument and returns the sum of the list items"""
                    sum = 0
                    for index in range(0,len(actuallist)):
                        val = actuallist[int(index)]
                        if val=="":
                            continue
                        sum = sum +float(val)
                    return round(sum, 2)
    
                def get_session_numbers_by_hovering_on_risk_level(self):
                    """Returns session numbers by hovereing over each risk level in the graph chart of reports page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    risklvlCnt = int(selenium.get_matching_xpath_count("//div[contains(@id,'chartPlacement_acb_0_')]"))
                    print "risklvlCnt:"+str(risklvlCnt)
                    sessionCnt = 0
                    list = []
                    for iCounter in range(risklvlCnt):
                        for index in range(int(4)):
                            print index
                            print "//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]" 
                            bStatus = selenium._is_visible("//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]")
                            print bStatus
                            print "//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]:"+str(bStatus)
                            if bStatus:
                                selenium.mouse_down("//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]")
                                selenium.mouse_up("//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]")
                                print "//div[contains(@id,'chartPlacement_acb_"+str(index)+"_"+str(iCounter)+"')]"
                                print "//div[contains(@id,'chartPlacement_dv_"+str(index)+"')]/div[@id='chartPlacement_dv_"+str(index)+"_span']"
                                sessionNum = selenium.get_text("//div[contains(@id,'chartPlacement_dv_"+str(index)+"')]/div[@id='chartPlacement_dv_"+str(index)+"_span']")
                                print "sessionNum:"+sessionNum
                                list.append(sessionNum)
                    return list

                def get_value_without_delimiters(self, value):
                    """Takes a string as argument and returns its value without delimiter"""
                    return value.replace(",", "")

                def get_activities_matching_enteredcriteria(self):
                    """Returns a list of activities displayed after entering a letter into activity field of advance search"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    cnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.activitiesmatchingcriteria}")))
                    activities = []
                    for iCounter in range(1,cnt):
                        activitycol = selenium.get_text(BuiltIn().get_variable_value("${list.reports.activitiesmatchingcriteria}")+"["+str(iCounter)+"]/td[2]")
                        activities.append(activitycol)
                    return activities

                def click_desiredresult_by_the_text(self,locator,text):
                    """Clicks on item by the 'text' from the dropwdown items displayed after entering a character into advance search fields """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    cnt = int(selenium.get_matching_xpath_count("//table[@id='"+locator+"']/tbody/tr"))
                    activities = []
                    for iCounter in range(1,cnt):
                        activitycol = selenium.get_text("//table[@id='"+locator+"']/tbody/tr["+str(iCounter)+"]/td[2]")
                        activities.append(activitycol)
                        print "activitycol:"+str(activitycol)
                        if activitycol==text:
                            print "if conditon satisfied"
                            selenium.click_element("//table[@id='"+locator+"']/tbody/tr["+str(iCounter)+"]/td[2]")
                            break
                        

                def get_session_by_account_in_table(self,num1,num2):
                    """Returns Rounded value of session by account """
                    num1 = float(num1)
                    num2 = float(num2)
                    cnt = num1/num2
                    return round(cnt, 2)

                def compare_first_letter_of_countries_in_list(self,startingletter):
                    """Returns 'True' if the list of countries displayed are starting with the 'startingletter' 'False' if not """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    cnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.countriesmatchingcriteria}")))
                    countries = []
                    for iCounter in range(1,cnt):
                        cntrycol = selenium.get_text(BuiltIn().get_variable_value("${list.reports.countriesmatchingcriteria}")+"["+str(iCounter)+"]/td[2]")
                        if not cntrycol.startswith(startingletter.lower()):
                            return False
                    return True 
           
                def match_result_values_to_pattern(self,listofresults,pattern):
                    """Returns the True if all the list values matching with specified pattern else False"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rstList = []
                    pattern = pattern.replace('*','')
                    rstList = listofresults
                    print " The Number of Search Results are "+str(len(rstList))
                    print " The Number of Search Results matching the search pattern are "+str(len([rst for rst in rstList if pattern or pattern.lower() in rst]))
                    if not len(rstList)== len([rst for rst in rstList if pattern or pattern.lower() in rst]):
                        print " The Number of Search Results are "+str(len(rstList))
                        print " The Number of Search Results matching the search pattern are "+str(len([rst for rst in rstList if pattern or pattern.lower() in rst]))
                        return False
                    else:
                        return True

                def validate_the_graph_type_on_dashboard(self,tableName,graphtype):
                    """Returns the graph type selected in the graph chart in dashboard page"""
                    dctexpectedList={'alertspastweek':['7px','18px','30px','10px'],'alertsPastYear':['2px','4px','7px','10px'],'sessionsVsAccountsPastYear':['15px','4px','7px','10px']}
                    if dctexpectedList.has_key(tableName):
                       comp=dctexpectedList[tableName]
                    time.sleep(10)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".primaryColorNode}"))
                    dispdgraphtype = ""
                    if bstatus==False:
                        bpresent=selenium._is_element_present(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNode}"))
                        if bpresent:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNode}"))
                        if bstatus==False or bpresent==False:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".siblingColorNode}"))
                           if bstatus==True:
                              style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".siblingColorNodeStyle}"))
                              print style
                              
                        if bstatus==True and bpresent==True:
                            style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNodeStyle}"))
                            print style
                            
                    else:
                        style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".primaryColorNodeStyle}"))
                        print style
                        
                    if 'width: 0px' in style:
                        return False
                                                    
                    if 'width: '+comp[0] in style:
                        dispdgraphtype = 'Line Scatter'
                    if 'width: '+comp[1] in style:
                        dispdgraphtype = 'Clustered Column'
                    if 'width: '+comp[2] in style:
                        dispdgraphtype = 'StackedColumn'
                    if 'width: '+comp[3] in style:
                        dispdgraphtype = 'Stacked Area'
                    if dispdgraphtype==graphtype:
                        return True
                def validate_the_graph_type_on_dashboard_new(self,tableName,graphtype):
                    """Returns the graph type selected in the graph chart in dashboard page"""
                    dctexpectedList={'alertspastweek':['7px','17px','29px','10px'],'alertsPastYear':['15px','4px','7px','10px'],'sessionsVsAccountsPastYear':['15px','4px','7px','10px']}
                    if dctexpectedList.has_key(tableName):
                       comp=dctexpectedList[tableName]
                    time.sleep(10)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".primaryColorNode}"))
                    dispdgraphtype = ""
                    if bstatus==False:
                        bpresent=selenium._is_element_present(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNode}"))
                        if bpresent:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNode}"))
                        if bstatus==False or bpresent==False:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard."+tableName+".siblingColorNode}"))
                           if bstatus==True:
                              style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".siblingColorNodeStyle}"))
                              
                        if bstatus==True and bpresent==True:
                            style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".secondaryColorNodeStyle}"))
                           
                    else:
                        style=selenium.get_element_attribute(BuiltIn().get_variable_value("${label.dashboard."+tableName+".primaryColorNodeStyle}"))

                    print "style:"+str(style)    
                    if 'width: 0px' in style:
                        return False
                                                    
                    if 'width: '+comp[0] in style:
                        dispdgraphtype = 'Line Scatter'
                    if 'width: '+comp[1] in style:
                        dispdgraphtype = 'Clustered Column'
                    if 'width: '+comp[2] in style:
                        dispdgraphtype = 'StackedColumn'
                    if 'width: '+comp[3] in style:
                        dispdgraphtype = 'Stacked Area'
                    if dispdgraphtype==graphtype:
                        return True


                def select_item_context_menu(self,item):
                    """clicks on an item from the context menu matched by the text 'item'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus=self.verify_item_in_context_menu_disabled(item)
                    if not bstatus:
                        selenium.click_element("//span[contains(text(),'"+item+"')]")
                    else:
                        return "The menu is already selected"
                
                def verify_advnce_search_after_search(self):
                    """Returns the list of values from Advance search fields labels which Checkboxs status is checked  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    getEleAttr = []
                    getXpathCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.reports.advanceSearchItemsCount}")))
                    for icnt in range(1,getXpathCnt+1):
                        getEleAttribute = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.reports.advanceSearchItemsCount}")+"["+str(icnt)+"]/div[@class='fadvChkAndTitleCell']/input[@checked='checked']/../following-sibling::div//input@value")
                        print "getEleAttribute:"+str(getEleAttribute)
                        #iCounter = getEleIndex + 2
                        #getEleAttribute = selenium.get_element_attribute("//div[@class='fadvContainer']/div["+str(cnt)+"]/div["+str(iCounter)+"]//input@value")
                        getEleAttr.append(getEleAttribute)
                    return getEleAttr


                def test_validate_previous_search(self, search, action=''):
                    """Returns previous search data if previous search dropdown is enabled else returns False"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = selenium._is_visible("//div[@class='doralPulldown']")
                    list = []
                    if not bStatus:
                        return False
                    selenium.click_element(BuiltIn().get_variable_value("${list.reports.riskdropdown}"))
                    previousSrchCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${list.reports.previoussearches}")))
                    print "previousSrchCnt:"+str(previousSrchCnt)
                    for iCounter in range(1,previousSrchCnt+1):
                        selenium.mouse_over(BuiltIn().get_variable_value("${list.reports.previoussearches}")+"["+str(iCounter)+"]")
                        rwCnt = int(selenium.get_matching_xpath_count("//div[@id='queries']/div[contains(@id,'pqsDetail_')]["+str(iCounter)+"]/table/tbody/tr"))
                        print "rwCnt:"+str(rwCnt)
                        for iRow in range(1,rwCnt+1):
                            #selenium.mouse_over("//div[@id='queries']/div[contains(@id,'pqsDetail_')]["+str(iCounter)+"]/table")
                            locator = "//div[@id='queries']/div[contains(@id,'pqsDetail_')]["+str(iCounter)+"]/table/tbody/tr["+str(iRow)+"]"
                            srchVal = selenium._element_find(locator,True,True).text
                            #srchVal = selenium.get_text("//div[@id='queries']/div[contains(@id,'pqsDetail_')]["+str(iCounter)+"]/table/tbody/tr["+str(iRow)+"]/td")
                            print "srchVal:"+str(srchVal)
                            list.append(srchVal)    
                    print list
                    for i in range(4,len(list)-1):
                        if list[i] in search:
                            print list[i]
                            selenium.click_element(BuiltIn().get_variable_value("${list.reports.previoussearches}")+"["+str(iCounter)+"]")
                            print "clicked"
                            break
                        else:
                            continue
                    return True
                            
                def verify_previous_search_result(self):
                    """If previous search dropdown is enabled it verifies previous search results for non matching search criteria
                       and returns the search criteria or else it returns false"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    getEleAttr = []
                    getSrchVals = [] 
                    for iCnt in range(2,5):
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${list.reports.riskdropdown}"))
                        selenium.click_element(BuiltIn().get_variable_value("${list.reports.riskdropdown}"))  
                        selenium.mouse_over(BuiltIn().get_variable_value("${list.reports.previoussearches}")+"["+str(iCnt)+"]")
                        cmpltdCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.reports.previousSearch.count}")))
                        for cnt in range(1,cmpltdCnt+1):
                            rwCnt = int(selenium.get_matching_xpath_count("//div[@id='queries']/div["+str(cnt)+"]/table/tbody/tr"))
                            for row in range(2,rwCnt+1):
                                getSrchVal = selenium.get_text("//div[@id='queries']/div["+str(cnt)+"]/table/tbody/tr["+str(row)+"]/td")
                                print "getSrchVal:"+str(getSrchVal)
                                getSrchVals.append(getSrchVal)
                        selenium.click_element(BuiltIn().get_variable_value("${list.reports.previoussearches}")+"["+str(iCnt)+"]")
                        self.verify_advnce_search_after_previous_search()
                    return getSrchVals
                
                def new_search_name(self,defaultsearchname,userdesiredsearchname):
                    """Returns search name by appending timestamp to userdesired search name or default search name """
                    if userdesiredsearchname=='':
                        return defaultsearchname+datetime.datetime.now().strftime("%B%d%Y%I:%M%p")
                    else:
                        return userdesiredsearchname+datetime.datetime.now().strftime("%B%d%Y%I:%M%p")
                    
                def clear_text(self,locator):
                    """Clears Text From the field located by 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium._element_find(locator,True,True).clear()
                    
                def select_custom_item(self,menuitem):
                    """Clicks on the customized column header menu options by the text 'menuitem'"""
                    selenium.mouse_down(BuiltIn().get_variable_value("${image.reports.customIcon}"))
                    selenium.simulate("//span[contains(text(),'"+menuitem+"')]",'click')


                def select_custom_item_menu(self,menuitem):
                    """Clicks on the customized column header menu options by the text 'menuitem'"""
                    for iCounter in range(0,5):
                        try:
                            print "C" +str(iCounter)
                            #self.wait_for_element_visible("//td[@class='searchCmdsIcon']"),"5s")
                            #selenium.click_element(BuiltIn().get_variable_value("${image.reports.customIcon}"))
                            self.mouse_over_on_element("//td[@class='searchCmdsIcon']")
                            bstatu = self.wait_for_element_visible("//span[contains(text(),'Save Search As')]","5s")
                            print "bstatu is: "+str(bstatu)
                            bstatus = self.wait_for_element_present("//span[contains(text(),'Save Search As')]","5s")
                            print "bstatus is: "+str(bstatus)
                            self.mouse_over_on_element("//span[contains(text(),'Save Search As')]")
                            #selenium.execute_javascript('document.getElementByXpath("//span[contains(text(),"Save Search As..")]")'.click())
                            #selenium.simulate("//span[contains(text(),'Save Search As')]",'click')
                            selenium.double_click_element("//span[@id='mainForm:j_id74:anchor']")
                            time.sleep(10)
                            return True
                        except:
                            print "select_custom_item_menu is not selected C" +str(iCounter)
                    return False
                            
                def compare_from_and_to_dates_of_reports_page(self,lastsession,daysdiff):
                    """Compares the dates displayed on the reports page with the date displayed at last session processed on dashboard page after clicking
                       on View Full Report under Pulldown menu"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    daysdifference = int(daysdiff)
                    lastsessiondate = lastsession.split('(')[1].replace(')','')                  
                    newdt = datetime.datetime.strptime(lastsessiondate,'%m/%d/%y')
                    lastsessiondate = newdt.strftime('%m/%d/%Y')
                    print 'last session date after splitting:'+lastsessiondate
                    enddate = datetime.datetime.strptime(lastsessiondate,'%m/%d/%Y')
                    bstatus = calendar.isleap(enddate.year)
                    if daysdiff>7 and bstatus==True:
                        daysdifference = daysdifference+1
                    startdate = enddate.date() - datetime.timedelta(days= daysdifference)
                    startdatemodified = datetime.datetime.strftime(startdate,'%m/%d/%Y')
                    print "startdatemodified: " + str(startdatemodified)
                    try:
                       alertsFromDate = selenium.get_element_attribute(BuiltIn().get_variable_value("${text.reports.fromDatevalue}"))
                       alertsToDate = selenium.get_element_attribute(BuiltIn().get_variable_value("${text.reports.toDatevalue}"))
                       bstatus = (lastsessiondate == alertsToDate)
                       if not bstatus == True:
                           return False
                       bstatus = (startdatemodified == alertsFromDate)
                       if not bstatus == True:
                           return False
                       return True
                    except:
                       print "Got exception"
                       return False

                def get_column_header_menu_options(self,locator):
                    """Returns list of items displayed on table header of a table after right mouse click on it"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    menuOptionscnt = int(selenium.get_matching_xpath_count(locator))
                    menuOptions = []
                    for iCounter in range(0,menuOptionscnt):
                        menuItem =  selenium.get_text("//td[@id='ArdentEdge_widgetPopUpMenu_R"+str(iCounter)+"C2']/span")
                        menuOptions.append(menuItem)
                    return menuOptions

                def get_customized_columns_column_names(self,locator):
                    """Returns the list of items displayed under 'Column' on the 'customized columns' table""" 
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    customizecolscnt = int(selenium.get_matching_xpath_count(locator))
                    print "customizecolscnt:"+str(customizecolscnt)
                    customizecolitems = []
                    for iCounter in range(0,customizecolscnt):
                        if iCounter>5:
                            selenium.mouse_over("//div[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_cell_R"+str(iCounter)+"C0']")
                            selenium.mouse_scroll("//div[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_cell_R"+str(iCounter)+"C0']")
                        customizecolitem = selenium.get_text("//div[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_cell_R"+str(iCounter)+"C0']/div/span")
                        customizecolitems.append(customizecolitem)
    
                    return customizecolitems

                def get_items_from_end_of_list(self,listofitems,cnt=0):
                    """Returns the number of items from end of the list matching the argument 'cnt'""" 
                    if int(cnt)!=0:
                        return listofitems[-int(cnt):]
                def select_window_by_title(self,windowtitle):
                    """Select a window by window title"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #browser = selenium._current_browser()
                    windows=selenium.get_window_titles()
                    for window in windows:
                        if window==windowtitle:
                            selenium.select_window(window)
                            
                def get_the_type_of_quick_search_results(self):
                    """Returns the type of the results displayed in Quick Search Results Popup"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #browser = selenium._current_browser()
                    windows=selenium.get_window_titles()
                    windowscnt=len(windows)
                    if windowscnt>1:
                        bstatus= windows[1]
                        print bstatus
                        if 'Account' in bstatus:
                            return "exactSingleQuickSearchResult"
                    bstatus=selenium._is_visible(BuiltIn().get_variable_value("${table.common.noQuickSearchResult}"))
                    if bstatus:
                        return "noQuickSearchResult"
                    else:
                        bstatus=selenium._is_visible(BuiltIn().get_variable_value("${table.common.multipleQuickSearchResult}"))
                        if bstatus:
                            return "multipleQuickSearchResult"

                def get_colum_data_from_quick_search_popup(self,columnname):
                    """Returns the values displayed under column 'columnname' from the Quick Search Popup """
                    colData=[]
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    colCount = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.quicksearch.popupWindow.columnCount}")))
                    for iCounter in range(1,colCount+1):
                        crntColName=selenium.get_text(BuiltIn().get_variable_value("${label.quicksearch.popupWindow.columnCount}")+"["+str(iCounter)+"]")
                        if crntColName in columnname:
                            colNumber=iCounter
                    matchedRecCnt=int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.quicksearch.popupWindow.matchedRecordCount}")))
                    for iCounter in range(1,matchedRecCnt+1):
                        crtColData=selenium.get_text(BuiltIn().get_variable_value("${label.quicksearch.popupWindow.matchedRecordCount}")+"["+str(iCounter)+"]/td["+str(colNumber)+"]/div")
                        if crtColData!=" " and crtColData!="":
                            colData.append(crtColData)
                    return colData
             
                def validate_timestamp_on_header(self,tStamp):
                    """Returns True if the 'tStamp' matches the pattern else Fails"""
                    pat='[0-1][0-9]:[0-5][0-9][A,P]M [E,P,M,C]T [(][0,1][0-9][/][0-3][0-9][/][1-9][0-9][)]'
                    if tStamp==(re.match(pat,tStamp)).group():
                        return True
                    raise AssertionError("Time Stamp does not match the expected Pattern")
                
                def validate_isnumber_ignore_special_characters(self,strn):
                    """Replaces delimiter ',' with nothing and returns True if 'strn' is a number False if not""" 
                    return strn.replace(',','').isdigit()
                
                def search_item(self, *searchItem):
                    """To input data for multiple fields in advance search"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    dict = {}           
                    print "length of list:"+str(len(searchItem))
                    for iVal in searchItem:
                    #keySearch = searchItem.split("|")
                        print "valinlist:"+str(iVal)
                        keySearch = str(iVal)
                        print "listitem:"+str(keySearch)
                        key = keySearch.split(":")
                        dict[key[0]] = key[1]
                        if key[0] == 'activity':
                            key[0] = BuiltIn().get_variable_value("${text.advanceSearch.activity}")
                            selenium.input_text(key[0],key[1])
                            selenium.input_text(key[0],key[1])
                            selenium.click_element("//div[@id='activityFieldList']")
                        if key[0] == 'country':
                            key[0] = BuiltIn().get_variable_value("${text.advanceSearch.country}")
                            selenium.input_text(key[0],key[1])
                            selenium.input_text(key[0],key[1])
                            selenium.click_element("//div[@id='activityFieldList']")
                        if key[0] == 'ipaddress':
                            key[0] = BuiltIn().get_variable_value("${text.advanceSearch.ipAddress}")
                        if key[0] == 'state':
                            key[0] = BuiltIn().get_variable_value("${text.reports.advancesearchStatefield}")
                            selenium.input_text(key[0],key[1])
                            selenium.input_text(key[0],key[1])
                            selenium.click_element("//div[@id='activityFieldList']")
                        if key[0] == 'city':
                            key[0] = BuiltIn().get_variable_value("${text.reports.advancesearchCityfield}")
                            selenium.input_text(key[0],key[1])
                            selenium.input_text(key[0],key[1])
                            selenium.click_element("//div[@id='activityFieldList']")
                        if key[0] == 'provider':
                            key[0] = BuiltIn().get_variable_value("${text.reports.advnceSearchprovider}")
                            selenium.input_text(key[0],key[1])
                            selenium.input_text(key[0],key[1])
                            selenium.click_element("//div[@id='activityFieldList']")
                            
                        
              
                def get_sorted_list(self, actualList):
                    """Returns the sorted list by taking a list 'actualList' as argument"""
                    for iCounter in range(0,len(actualList)-1):
                        print "forloop"
                        if (int(actualList[iCounter]) > int(actualList[iCounter+1])):
                            print "ifloop"
                            print "actualList[iCounter]:"+str(actualList[iCounter])
                            print "actualList[iCounter+1]:"+str(actualList[iCounter+1])
                            temp = actualList[iCounter]
                            actualList[iCounter] = actualList[iCounter+1]
                            actualList[iCounter+1] = temp
                        print actualList
                    return actualList
                
                def sort_list_for_strings(self, actualList):
                    """Returns String values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList)

                def sort_list_for_integers(self, actualList):
                    """Returns String values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,key=int)
                
                def reverse_list_for_integers(self, actualList):
                    """Returns String values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,key=int,reverse=True)

                def reverse_list_for_strings(self, actualList):
                    """Returns String values into a list in sorted order"""
                    if len(actualList)==0:
                        return 0
                    return sorted(actualList,reverse=True)
                
                def get_float_values_in_sorted_list(self, actualList):
                    """Returns float values into a list in sorted order"""
                    return sorted(actualList,key=float)

                def get_float_values_in_reverse_sorted_list(self, actualList):
                    """Returns float values into a list in Reverse sorted order"""
                    print actualList
                    print ".................."
                    print sorted(actualList,key=float,reverse=True)
                    return sorted(actualList,key=float,reverse=True)


                def get_table_values_by_pressing_down_key(self, locator,imageLocator,order,columnName='', optionalTag=''):

                    """Returns values in a table into a list of specified columns by performing click action on 'Down Arrow' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #Get Column Num
                    rwCnt = 0
                    iColNo = self._table_get_column_no(locator,columnName)
                    rowValues = []
                    colValues = []
                    counter = 0
                    self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell') and contains(@class,'Selected')]")
                    newelements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell') and contains(@class,'Selected')]")
                    print "1"
                    valLocator = locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell') and contains(@class,'Selected')]"
                    selenium.simulate(locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell')]",'mouseover')
                    self.wait_for_element_visible(valLocator+'/div')
                    val = selenium.get_text(valLocator+'/div')
                    if (val in rowValues):
                        rowValues.remove(val)
                    rowValues.append(val)
                    if ((val == " ") or (val == "")):
                        rowValues.remove(val)
                    rwCnt = self.get_table_rows_count_by_scrolling(BuiltIn().get_variable_value("${table.dashboard.highRiskAlertsTodayTable.barKnob}"),BuiltIn().get_variable_value("${table.dashboard.highRiskAlertsTodayTable.barContainer}"))
                    print "2"
                    for iCounter in range(int(rwCnt)):
                        self.press_down_key(locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell')]")
                        valLocator = locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell') and contains(@class,'Selected')]"
                        selenium.simulate(locator+'/tbody/tr/td['+str(iColNo)+"]/div//div[contains(@id,'HighRiskToday_cell')]",'mouseover')
                        self.wait_for_element_visible(valLocator+'/div')
                        val = selenium.get_text(valLocator+'/div')
                        print "val:"+val
                        if (val in rowValues):
                            rowValues.remove(val)
                        rowValues.append(val)
                        if ((val == " ") or (val == "")):
                            rowValues.remove(val)
                    return rowValues
                    
                def get_table_values_into_list_for_given_row(self,locator,rowNum=0):
                    """Returns values into a list for given row number """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    colCount = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                    colNames=[]
                    for iCounter in range(1,colCount+1):
                        self.wait_for_element_visible(locator+"/tbody/tr/td["+str(iCounter)+"]/div//div[contains(@id,'HighRiskToday_cell')and contains(@class,'Selected')]")
                        colVal = selenium.get_text(locator+"/tbody/tr/td["+str(iCounter)+"]/div//div[contains(@id,'HighRiskToday_cell')and contains(@class,'Selected')]")
                        colNames.append(colVal)
                        if colVal == " ":
                            colNames.remove(colVal)
                    if len(colNames)==0:
                        raise AssertionError("The values for given row could not be fetched")
                    return colNames

                def get_table_values_into_list_by_mouse_scroll(self, locator,imageLocator,order='',columnName='all',parentLocator='',scrollDownButtonLocator='',):
                    """Returns values in a table into a list for specified columns by performing 'mouse scroll'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #Get the column number
                    if columnName!='all':
                        iColNo = self._table_get_column_no(locator,columnName)
                        print "columnNum:"+str(iColNo)
                    #Add code to loop through all the columns here
                    #Get the initial cursor position
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(iColNo)+']/div/div')
                    print "elements:"+str(elements)
                    rowValues = []
                    recordsCnt = 0
                    iCounter = 0
                    #Get the values from current rows
                    #Scroll down
                    rwCnt = self.get_table_rows_count_by_scrolling(parentLocator,"//div[contains(@id,'"+scrollDownButtonLocator+"')]")
                    self._click_ascending_or_descending_icon(locator,imageLocator,columnName,order)
                    while(iCounter <= int(rwCnt) and int(recordsCnt) != int(rwCnt)):
                    #Get the values from all rows by mouse scroll
                        print "iCounter:"+str(iCounter)
                        print "elements in loop:"+str(elements)
                        for ele in range(1,int(elements)):
                            print "counter ele:"+str(ele)
                            try:
                                session = selenium._element_find(locator+'/tbody/tr/td['+str(iColNo)+']/div/div',False,False)
                                val = str(session[ele].text)
                                print "val:"+str(val)
                            except:
                                print "Reading the session val failed" 
                            
                            if val in rowValues:
                                rowValues.remove(val)
                            rowValues.append(val)
                            if ((val == " ") or (val == "")):
                                rowValues.remove(val)
                        try:
                            selenium.mouse_scroll(parentLocator)
                        except:
                            print "selenium.mouse_scroll keyword failed"
                        try:
                            selenium.simulate(parentLocator,'mouseover')
                        except:
                            print "selenium.simulate keyword failed"
                        recordsCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                        print "recordsCnt: " + str(recordsCnt)
                        recordsCnt = recordsCnt.split("-")
                        recordsCnt = recordsCnt[1].replace(" ","")
                        iCounter = iCounter + 1
                    return rowValues

                def get_table_values_into_list_by_mouse_scroll_in_alerts(self, locator,columnName='all',parentLocator='',scrollDownButtonLocator='',imageLocator=None,order=''):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #Get the column number
                    rwCnt = self.get_table_rows_count_by_scrolling(parentLocator,"//div[contains(@id,'"+scrollDownButtonLocator+"')]")
                    if imageLocator!=None:
                        self._click_ascending_or_descending_icon(locator,imageLocator,columnName,order)
                    rowValues = self.get_table_values_into_list_by_down_arrow(locator,parentLocator,scrollDownButtonLocator,columnName,True,rwCnt)
                    return rowValues
                    

                def click_ascending_or_descending_icon(self,tableLocator,imageLocator,columnName,order):
                    """ clicks the column name accoring to given order in  a table """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_please_wait_option()
                    self.wait_for_element_visible("//div[contains(@id,'"+imageLocator+"') and contains(text(),'"+columnName+"')]")
                    selenium.click_element("//div[contains(@id,'"+imageLocator+"') and contains(text(),'"+columnName+"')]")
                    time.sleep(4)
                    #selenium.simulate("//div[contains(@id,'"+imageLocator+"') and contains(text(),'"+columnName+"')]",'click')
                    imageVal = selenium.get_element_attribute("//div[contains(@id,'"+imageLocator+"')]//div[2]@style")
                    print "imageValinOrder:"+str(imageVal)
                    print "order:"+str(order)
                    if order=='ascending':
                        if 'a2' in imageVal:
                            selenium.click_element("//div[contains(@id,'"+imageLocator+"')]//div[2]")
                            time.sleep(4)
                            imageValue = selenium.get_element_attribute("//div[contains(@id,'"+imageLocator+"')]//div[2]@style")

                            if 'a1' in imageValue:
                                return
                            else:
                                selenium.click_element("//div[contains(@id,'"+imageLocator+"')]//div[2]")
                                time.sleep(4)
                                return
                        if 'a1' in imageVal:
                            return
                    if order=='descending':
                        if 'a1' in imageVal:
                            print "a1 clicked"
                            selenium.click_element("//div[contains(@id,'"+imageLocator+"')]//div[2]")
                            time.sleep(4)
                            imageValue = selenium.get_element_attribute("//div[contains(@id,'"+imageLocator+"')]//div[2]@style")

                            if 'a2' in imageValue:
                                return
                            else:
                                selenium.click_element("//div[contains(@id,'"+imageLocator+"')]//div[2]")
                                time.sleep(4)
                                return
                        if 'a2' in imageVal:
                            return                         
               
                def scroll_to_top(self, parentLocator='', parentscroll=''):
                    """ Scrolls up to the top in a table"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:]
                    #Scroll up
                    selenium.mouse_down(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                    selenium.mouse_up(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                    while(not (prevvalue==selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:])):
                        prevvalue = selenium.get_element_attribute(BuiltIn().get_variable_value("${label.tableScrollBar.style}"))[18:]
                        selenium.mouse_down(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                        selenium.mouse_up(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                    selenium.mouse_down(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                    selenium.mouse_up(parentLocator+'//div[@class="ajs_tb_bar_up"]')
                    return True

                def get_values_in_reverse_sort(self, actualList):
                    """Takes a list 'actualList' as an argument and returns the list in reverse sort"""
                    for iCounter in range(len(actualList)-1,0):
                        if (int(actualList[iCounter]) > int(actualList[iCounter+1])):
                            print "actualList[iCounter]:"+str(actualList[iCounter])
                            print "actualList[iCounter+1]:"+str(actualList[iCounter+1])
                            temp = actualList[iCounter]
                            actualList[iCounter] = actualList[iCounter+1]
                            actualList[iCounter+1] = temp
                    print actualList
                    return actualList
                
                def get_float_values_in_reverse_sort(self, actualList):
                    """Returns float values into a list in sorted order"""
                    return sorted(actualList,key=float,reverse=True)

                def string_should_contain(self,string,substring):
                    """Returns True if The string contains substring else False' """
                    ind=string.find(substring)
                    if ind>=0:
                        return True
                    return False

                def string_should_contain_any_of_elements_in_the_list(self,mainString,elementsOfList):
                    """returns true if any one element in the list is the substring of the string"""
                    for i in elementsOfList:
                        if i in mainString:
                            print str(i)
                            return True
                    return False
                
                def mouse_over_on_table_row(self, table_locator, columnNo, Value='',iRowNo=0):
                    """Performs the Action Left Mouse Click on the column of the table located at 'table_locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print Value
                    if not Value=='':
                        iRowNo = self.table_get_row_no(table_locator, columnNo, Value)
                    else:
                        iRowNo=iRowNo+1
                    if iRowNo==0:
                        raise AssertionError('No row matching the expected value')
                    print iRowNo
                    selenium.mouse_over(table_locator+'/tbody/tr/td['+str(columnNo)+']/div/div['+str(iRowNo)+']/div')                
                def press_down_key(self,locator):
                    """ Presses the down Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium._element_find(locator,True,True).send_keys(Keys.ARROW_DOWN)
                    
                def press_control_and_key(self,locator,key):
                    """Presses the control Key and Specified key 'key' at element located by the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    loc = selenium._element_find(locator,True,True)
                    loc.send_keys(Keys.CONTROL, 'a')
                    time.sleep(1)
                    loc.send_keys(Keys.CONTROL,key)
                    time.sleep(1)
                    
                def press_up_key(self,locator):
                    """Presses the Up Key at element located by the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.ARROW_UP)
                            return True
                        except:
                            print "Exception in press_up_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_up_key")

                def press_page_down_key(self,locator):
                    """Presses the page down Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_DOWN)
                            return True
                        except:
                            print "Exception in press_page_down_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_page_down_key")


                def press_page_up_key(self,locator):
                    """Presses the page up Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.PAGE_UP)
                            return True
                        except:
                            print "Exception in press_page_up_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_page_up_key")

                def press_home_key(self,locator):
                    """Presses the Home Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.HOME)
                            return True
                        except:
                            print "Exception in press_home_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_home_key")

                def press_end_key(self,locator):
                    """Presses the End Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.END)
                            return True
                        except:
                            print "Exception in press_end_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_end_key")

                def press_tab_key(self,locator):
                    """Presses the End Key starting from the 'locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for i in range(1,3):
                        try:
                            self.wait_for_element_visible(locator)
                            selenium._element_find(locator,True,True).send_keys(Keys.TAB)
                            return True
                        except:
                            print "Exception in press_tab_key keyword"
                    raise AssertionError("Exception: Unable to perform the press_tab_key")

                def get_table_values_into_list_by_down_arrow(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows='',useJavaScript=False):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' and scrollbar located at 'scrollbar_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    keyColNum = self._table_get_column_no(locator,columnName)
                    time.sleep(2)
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    rowValues=[]
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        print "iValue: "+str(iValue)
                        if (iValue==2):
                            try:
                                self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                            except:
                                print "click elemet keyword got failed at table row"
                                selenium.capture_page_screenshot()
                        else:
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            except:
                                print "mouse over keyword got failed at table row"
                                selenium.capture_page_screenshot()
                            try:
                                selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                                self.wait_for_please_wait_option()
                            except:
                                print "Arrow down failed at table row"
                                selenium.capture_page_screenshot()

                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValue=self.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            print "got exception while reading row values"
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "Counter:"+str(Counter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            self.wait_for_please_wait_option()
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValue=self.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "duplicate counter:"+str(Counter)
                                print "duplicate val:"+str(iCounter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    self.verify_table_read_all_rows(rowsCount,scrollbar_locator)
                    return rowValues

                def get_table_values_into_list_by_down_arrow_for_session_history(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows='',useJavaScript=False):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' and scrollbar located at 'scrollbar_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    keyColNum = self._table_get_column_no(locator,columnName)
                    time.sleep(2)
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    rowValues=[]
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        print "iValue: "+str(iValue)
                        if (iValue==2):
                            try:
                                self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                            except:
                                print "click elemet keyword got failed at table row"
                                selenium.capture_page_screenshot()
                        else:
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            except:
                                print "mouse over keyword got failed at table row"
                                selenium.capture_page_screenshot()
                            try:
                                selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                                self.wait_for_please_wait_option()
                            except:
                                print "Arrow down failed at table row"
                                selenium.capture_page_screenshot()

                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValue=self.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            print "got exception while reading row values"
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "Counter:"+str(Counter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            self.wait_for_please_wait_option()
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValue=self.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "duplicate counter:"+str(Counter)
                                print "duplicate val:"+str(iCounter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    #self.verify_table_read_all_rows(rowsCount,scrollbar_locator,)
                    return rowValues
                
                def get_table_values_into_list_by_down_arrow1(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows=''):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' and scrollbar located at 'scrollbar_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    keyColNum = self._table_get_column_no(locator,columnName)
                    time.sleep(2)
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    rowValues=[]
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        if (iValue==2):
                            selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                        else:
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            
                        rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "Counter:"+str(Counter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        print "iCounter "+str(iCounter)
                    iValue=int(elements)-1
                    print "done first while loop"
                    while(iCounter<=rowsCount):
                        selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                        rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        #if(len(rowValue)==0):
                            #selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                        rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "duplicate counter:"+str(Counter)
                                print "duplicate val:"+str(iCounter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    return rowValues


                def get_csv_file_row_values_into_list(self,path,rowNo):
                    """Returns the list of specified row values from cvs file in Specified File by 'path' """
                    file_Reader = csv.reader(open(path))
                    rowNumber=0
                    lines=[]
                    for row in file_Reader:
                        rowNumber=rowNumber+1
                        if rowNumber==int(rowNo):
                            lines=row
                            break

                    return lines

                def get_csv_file_column_no(self,path,columnname):
                    """Returns the column of specified column by  columnname from cvs file in Specified File by 'path' """
                    file_Reader = csv.reader(open(path))
                    linevalues=[]
                    print "text01"
                    for row in file_Reader:
                        linevalues=row
                        break
                    for index in range(0,len(linevalues)):
                        print "index="+str(index)
                        if len(linevalues)>0:
                            if linevalues[index]==columnname:
                                return index+1
                    return 0

                def get_csv_file_column_values_into_list(self,path,columnname):
                    """Returns the list of specified columns values from cvs file in Specified File by 'path' """
                    print "kw01"
                    keyColno=self.get_csv_file_column_no(path,columnname)
                    keyColno=int(keyColno)-1
                    file_Reader = csv.reader(open(path))
                    rowNumber=0
                    lines=[]
                    columnValues=[]
                    for row in file_Reader:
                        rowNumber=rowNumber+1
                        if rowNumber>1:
                            lines=row
                            try:
                                val= lines[keyColno]
                                print val
                                val = str(val).strip()
                                columnValues.append()
                            except:
                                print "Empty row found"
                                #columnValues.append("")
                    return columnValues


                def validate_csv_file_and_table_record_values(self,locator,path):
                    """Validates exported CSV file values with alerts page table values"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    time.sleep(2)
                    rowsCount=self.get_csv_file_rows_count(path)
                    rowsCount=int(rowsCount)
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td[3]/div/div')
                    for rowNo in range(2,rowsCount):
                        if rowNo==2:
                            time.sleep(2)
                            selenium.simulate(locator+'/tbody/tr/td[3]/div/div[2]','click')
                            time.sleep(2)
                            self.press_page_down_key(locator+'/tbody/tr/td[3]/div/div[2]')
                        csvRowValues=self.get_csv_file_row_values_into_list(path,rowNo)
                        if rowNo<int(elements):
                            tableRowValues=self.get_table_row_values_into_list(locator,rowNo)
                        else:
                            rowNo=int(elements)-1
                            selenium._element_find(locator+'/tbody/tr/td[3]/div/div'+'['+str(rowNo)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            time.sleep(1)
                            tableRowValues=self.get_table_row_values_into_list(locator,rowNo)

                        self.list_comparison(csvRowValues,tableRowValues)

                def get_csv_file_rows_count(self,path):
                    """Return The Total No Rows In Csv File Using The Specified File Path"""
                    file_Reader = csv.reader(open(path))
                    rowsCount=sum(1 for row in file_Reader)
                    return  rowsCount
                
                def get_table_rows_count_by_scrolling(self, parentLocator,parentScroll=''):
                    """Returns the total no of rows in a table by scrolling specifying scrolling knob locator"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #selenium.reload_page()
                    bStatus = True
                    while bStatus:
                        try:
                            self.wait_for_element_visible(parentLocator)
                            selenium.mouse_down(parentLocator)
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentLocator)
                            selenium.mouse_down(parentLocator)
                        try:
                            selenium.mouse_up(parentLocator)
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentLocator)
                            selenium.mouse_up(parentLocator)
                        try:
                            prevvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        except:
                            selenium.capture_page_screenshot()
                            print "selenium getattribute failed at: "+str(parentLocator+'@style')
                            prevvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        
                        print "Prev value: "+str(prevvalue)
                        #selenium.mouse_up(parentLocator)
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')

                        try:
                            postvvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        except:
                            selenium.capture_page_screenshot()
                            print "selenium getattribute failed at: "+str(parentLocator+'@style')
                            postvvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        
                        print "Post value: "+str(postvvalue)
                        if(prevvalue!=postvvalue):
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        else:
                            bStatus = False
                            break
                    print 'selenium.mouse_down'
                    #selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    print 'selenium.mouse_up'
                    for iIndex in range(1,5):
                        self.wait_for_element_visible(parentLocator)
                        try:
                            selenium.mouse_over(BuiltIn().get_variable_value("${button.alerts.export}"))
                        except:
                            print "mouser over on export button"
                        selenium.mouse_over(parentLocator)
                        selenium.mouse_over(parentLocator)
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                        rwCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                        if len(rwCnt)>1 and (str(rwCnt).find("-"))>0:
                            break
                    print "tooltip text - rwCnt:"+str(rwCnt)
                    rwCnt = rwCnt.split("-")
                    rwCnt = rwCnt[1].replace(" ","")
                    print "rwCnt:"+str(rwCnt)
                    time.sleep(5)
                    selenium.reload_page()
                    self.wait_for_please_wait_option()
                    time.sleep(5)
                    #self.scroll_to_top()
                    return str(rwCnt)

                def get_activities_from_selected_record (self,column,tablename=None):
                    """Return The All Activies of Selected Record in Table using column name by 'column'  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if tablename == None:
                        tablename = "tAlerts_cell_R"
                    bStatus = self.wait_for_element_visible("//div[contains(@class,'Selected')][1]")
                    try:
                        recordid=self.get_element_attribute_value(BuiltIn().get_variable_value("${label.alerts.searchResults.selectedRecordActivity}"))
                        print "recordid: "+ str(recordid)
                        recordid=recordid.split(tablename)
                        recordrow=recordid[1].split("C0")
                    except:
                        print "split keyword failed due list index out of range"
                        time.sleep(2)
                        recordid=self.get_element_attribute_value(BuiltIn().get_variable_value("${label.alerts.searchResults.selectedRecordActivity}"))
                        print "recordid: "+ str(recordid)
                        recordid=recordid.split(tablename)
                        recordrow=recordid[1].split("C0")
                        
                    columnno=self._table_get_column_no(BuiltIn().get_variable_value("${table.alerts.searchResultsTable}"),column)
                    columnno=columnno-1
                    return selenium.execute_javascript("return document.getElementById('ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_R"+str(recordrow[0])+"C"+str(columnno)+"').getElementsByTagName('div')[0].textContent")

                def validate_the_activities_of_the_selected_record(self,searchcriteria,activities):
                     """Returns The True If the Activites List contains the Activity Values matching with SearchCriteria by 'searchcriteria' if not return False """
                     #searchcriteria='Info & -Adp , xyz'
                     #activities=["hes","Info","xyz"]
                     nospacesearchcriteria=searchcriteria.replace(' ','')
                     replacedsearchcriteria=nospacesearchcriteria.replace('&',',')
                     splitsearchcriteria=replacedsearchcriteria.split(',')
                     print splitsearchcriteria
                     for element in splitsearchcriteria:
                         print "The current search is :"+element
                         print "The search criteria is :"+searchcriteria
                         if element.find('-')!=-1:
                             print "- is found"
                             currelement=element.replace('-','')
                             try:
                                 eleindex=activities.index(currelement)
                             except:
                                 eleindex=-1
                             print "the element index is "+str(eleindex)
                             if eleindex!=-1:
                                 searchcriteria=searchcriteria.replace(element, 'False')
                                 print element+" :False"
                                 print "The updated search is "+searchcriteria
                             else:
                                 searchcriteria=searchcriteria.replace(element, 'True')
                                 print element+" :True"
                                 print searchcriteria
                         if element.find('-')==-1:
                             print "- is not found in the element"
                             try:
                                 eleindex=activities.index(element)
                             except:
                                  eleindex=-1
                             print eleindex
                             if eleindex!=-1:
                                 searchcriteria=searchcriteria.replace(element, 'True')
                                 print element+" :True"
                                 print searchcriteria
                             else:
                                 searchcriteria=searchcriteria.replace(element, 'False')
                                 print element+" :False"
                                 print searchcriteria

                     searchcriteria=searchcriteria.replace('&','and')
                     searchcriteria=searchcriteria.replace(',',' or ')
                     print searchcriteria
                     print eval(searchcriteria)
                     return eval(searchcriteria)

                def clear_clipboard_content(self):
                    """ clears the clipboard content """
                    win32clipboard.OpenClipboard()
                    win32clipboard.EmptyClipboard()
                    
                def get_clipboard_content(self):
                    """ Returns the clipboard content """
                    win32clipboard.OpenClipboard()
                    print "clipboard content:"
                    return win32clipboard.GetClipboardData()

                def get_status_column_no(self,locator):
                    """ Returns column of column names from a table"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    colCount = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                    colNames=[]
                    for iCounter in range(1,colCount+1):
                        colVal = selenium.get_text(locator+'/tbody/tr/td['+str(iCounter)+']/div/div')
                        print iCounter
                        print colVal
                        colNames.append(colVal)
                        if colVal == " ":
                            if iCounter==1:
                                continue
                            return iCounter
                    if len(colNames)==0:
                        raise AssertionError("The column names could not be fetched")                

                def get_status_values_into_list(self, locator,parentLocator='',parentScroll=''):
                    """Reads all the Status values into a list by hovering on the  Status icon of each Record from the Alerts Search Results table. """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    columnNum = self.get_status_column_no(locator)
                    print "columnNum:"+str(columnNum)
                    keyelements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]")
                    print "keyelements:"+str(keyelements)
                    rowValues = []
                    iCounter = 1
                    recordsCnt = 1
                    #Get the values from current rows
                        #keys = selenium._element_find(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]["+str(ele)"]/div/img",False,False)
                        #print len(newelements)
                    for ele in range(2,int(keyelements)+1):
                        for counter in range(1,7):
                            bStatus = selenium._is_visible(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]["+str(ele)+"]//img")
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]["+str(ele)+"]//img")
                    toolTipVal = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                    rowValues.append(toolTipVal)
                    #Scroll down
                    rwCnt = self.get_table_rows_count_by_scrolling(parentLocator,parentScroll)                               
                    while(iCounter<=rwCnt and recordsCnt!=rwCnt ):
                    #Get the values from all rows by mouse scroll
                        print "iCounter:"+str(iCounter)
                        keyelements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]")
                            #keys = selenium._element_find(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]",False,False)
                        for ele in range(2,int(keyelements)+1):
                            for counter in range(1,7):
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@id,'tAlerts_cell_')]["+str(ele)+"]//img")
                            toolTipVal = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            rowValues.append(toolTipVal)
                            #selenium.mouse_scroll(locator+'/tbody/tr/td['+str(columnNum)+"]/div/div[contains(@class,'Selected')]")
                        selenium.mouse_scroll(parentLocator)
                        selenium.simulate(parentLocator,'mouseover')
                        recordsCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                        recordsCnt = recordsCnt.split("-")
                        recordsCnt = recordsCnt[1].replace(" ","")
                        iCounter = iCounter + 1
                    return rowValues

                def is_list_contains_value(self,statuslist,value):
                    """ checks the given value in the list """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    statuslistvalues = []
                    statuslistvalues = statuslist
                    return value in statuslistvalues

                def validate_table_account_and_risk_values(self,accountlist,risklist):
                    """ Validate the accountlist and risklist """
                    accountslistlen=len(accountlist)
                    riskvalueslen=len(risklist)
                    print "accountslistlen" +str(accountslistlen)
                    print "riskvalueslen" +str(riskvalueslen)
                    if not(accountslistlen==riskvalueslen):
                        raise AssertionError("The Accounts List Length And Risk List Length not Same")
                        print '1'
                    else:
                        index=0
                        print '2'
                        while(index<accountslistlen):
                            print 'k'
                            accountValue=accountlist[index]
                            print "accountValue" +str(accountValue)
                            riskValue=risklist[index]
                            print "riskValue" +str(riskValue)
                            if str(accountValue) == "":
                                print "empty account value condition satisfied"
                                index=index+1
                                continue
                            val1=accountValue.index("(")+1
                            print "val1" +str(val1)
                            val2=accountValue.index(")")
                            print "val2" +str(val2)
                            rCount=accountValue[val1:val2]
                            rCount=int(rCount)
                            print "rCount" +str(rCount)
                            if rCount>1:
                                print '3'
                                for i in range(1,rCount):
                                    print '4'
                                    index=index+1
                                    print "index" +str(index)
                                    if not(accountlist[index]==" " or accountlist[index]==""):
                                        print '5'
                                        raise AssertionError("account values is not empty")
                                    if not(float(risklist[index-1])>=float(risklist[index])):
                                        print float(risklist[index-1])
                                        print float(risklist[index])
                                        print '6'
                                        raise AssertionError("Risk values not in correct Order")
                            index=index+1

                def get_csv_file_column_no(self,path,columnname):
                    """Returns the column of specified column by  columnname from cvs file in Specified File by 'path' """
                    file_Reader = csv.reader(open(path))
                    linevalues=[]
                    for row in file_Reader:
                        linevalues=row
                        break
                    for index in range(0,len(linevalues)):
                        if linevalues[index]==columnname:
                            return index+1
                    return 0

                def get_csv_file_column_values_into_list(self,path,columnname):
                    """Returns the list of specified columns values from cvs file in Specified File by 'path' """
                    keyColno=self.get_csv_file_column_no(path,columnname)
                    keyColno=int(keyColno)-1
                    file_Reader = csv.reader(open(path))
                    rowNumber=0
                    lines=[]
                    columnValues=[]
                    for row in file_Reader:
                        rowNumber=rowNumber+1
                        if rowNumber>1:
                            lines=row
                            try:
                                columnValues.append(str(lines[keyColno]).strip())
                            except:
                                print "Empty Row Found"
                                columnValues.append("")
                    return columnValues

                def get_random_number_in_given_range(self,start,stop):
                    """ Returns the random from given range"""
                    return random.randint(int(start),int(stop))

                
                def get_unique_string(self,name =None):
                    """ Returns the random from given size"""
                    if name == None:
                        return  'Test'+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_year)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                    else:
                        return  str(name)+str(time.localtime().tm_mon)+str(time.localtime().tm_mday)+str(time.localtime().tm_year)+str(time.localtime().tm_hour)+str(time.localtime().tm_min)+str(time.localtime().tm_sec)
                        

                def convert_string_case(self,string,case=''):
                    """Converts the Case of the string to Upper if specified else to lower """
                    if case=="upper":
                        return string.upper()
                    else:
                        return string.lower()

                def combine_list_of_activities_or_riskfactors_with_and_symbol(self,activitieslist):
                    """joins a list with " & " symbol"""
                    return " & ".join(activitieslist)
                
                def get_fraud_match_source_table_values_into_list(self,locator,rowNum=0):
                    """Returns values into a list for given row number """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator+'/tbody/tr/td')
                    colCount = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                    print "colCount:"+str(colCount)
                    colNames=[]
                    for iCounter in range(1,colCount+1):
                        colVal = self.get_text(locator+"/tbody/tr/td["+str(iCounter)+"]//div/div[contains(@id,'cell') and contains(@class,'Selected')]")
                        colNames.append(colVal)
                        if colVal == " ":
                            colNames.remove(colVal)
                    if len(colNames)==0:
                        raise AssertionError("The values for given row could not be fetched")
                    return colNames
                
                def verify_list_sortorder(self,list_items):
                    """ Returns stauts for the given list is sorted or not """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for item in list_items:
                        if item=='XXXXXXXXX':
                            return True
                    status = self._isSorted(list_items)
                    return status
                
                def _isSorted(self, list_items):
                    """  checks the given list is sorted or not """
                    expectedListItems = sorted(list_items)
                    if expectedListItems==list_items:
                        return True

                def get_activities_from_selected_record_on_fraudmatch_page(self,columnNumber=''):
                    """Return The All Activies of Selected Record in Table using column name by 'column'  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    recordid = ''
                    
                    if columnNumber == '':
                        recordid=self.get_element_attribute_value("//div[contains(@id,'C8') and contains(@class,'Selected') and contains(@id,'AlertsTable_tAlerts')]@id")
                    else:
                        recordid=self.get_element_attribute_value("//div[contains(@id,'C"+str(columnNumber)+"') and contains(@class,'Selected') and contains(@id,'AlertsTable_tAlerts')]@id")
                    print recordid
                    recordid=recordid.split("tAlerts_cell_R")
                    recordrowandcolumn=recordid[1].split("C")
                    recordrow=recordrowandcolumn[0]
                    #columnno=self._table_get_column_no(BuiltIn().get_variable_value("${table.alerts.searchResultsTable}"),column)
                    columnno=recordrowandcolumn[1]
                    return selenium.execute_javascript("return document.getElementById('ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_R"+str(recordrow)+"C"+str(columnno)+"').getElementsByTagName('div')[0].textContent")


                def convert_localtime_to_GMT_time(self,dateandtime,bstatusofpm):
                    dateandtime = dateandtime
                    date = dateandtime.split(' ')
                    time = date[1].split(':')
                    timehours = time[0]
                    monthyeardate = date[0]
                    month,date,year  = (int(x) for x in monthyeardate.split('/'))
                    bstatusofPMtime = bstatusofpm
                    dateconverted = datetime.datetime.strftime(pytz.timezone('EST').localize(datetime.datetime.strptime(dateandtime, '%m/%d/%Y %H:%M')).astimezone(pytz.utc),'%Y/%m/%d %H:%M')
                    li1 = dateconverted.split('/')
                    li2 = li1[2].split(' ')
                    li3 = li2[1].split(':')
                    d1 = datetime.date(year, month, date)
                    d2 = datetime.date(2013, 03, 10)
                    d3 = datetime.date(2013, 11, 03)
                    if (d2 <= d1 <= d3) and (8 <= int(timehours)<=11) and (bstatusofPMtime==True):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) + datetime.timedelta(hours=23)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (d2 <= d1 <= d3) and (int(timehours)==12) and (bstatusofPMtime==True):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) - datetime.timedelta(hours=1)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (d2 <= d1 <= d3) and (int(timehours)==12) and (bstatusofPMtime==False):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) - datetime.timedelta(hours=1)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (d2 <= d1 <= d3) and (8 <= int(timehours)<=11) and (bstatusofPMtime==False):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) - datetime.timedelta(hours=1)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (d2 <= d1 <= d3) and (int(timehours)<8) and (bstatusofPMtime==False):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) - datetime.timedelta(hours=1)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (d2 <= d1 <= d3) and (int(timehours)<8) and (bstatusofPMtime==True):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) - datetime.timedelta(hours=1)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    elif (int(timehours)>=8) and (bstatusofPMtime==True):
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1])) + datetime.timedelta(hours=24)
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")
                    else:
                        convertedtogmt = datetime.datetime(int(li1[0]),int(li1[1]),int(li2[0]),int(li3[0]),int(li3[1]))
                        return convertedtogmt.strftime("%m/%d/%Y %I:%M")                

                def header_comparison(self,listItm1,listItm2):
                    """ Returns a list of column names from a table"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    list1 =[]
                    list2 =[]
                    list1=listItm1
                    list2=listItm2
                    len1= len(list1)
                    len2= len(list2)
                    print "len"+str(len1);
                    #if len1 !=len2:
                    #raise AssertionError ("Lenths are not equal")
                    for val in list2:
                        if val in list1:
                            return True 
                        else:
                            raise AssertionError("values are not equal")

                def days_between(self,d1,d2):
                    d1 = datetime.datetime.strptime(d1, "%m/%d/%Y")
                    d2 = datetime.datetime.strptime(d2, "%m/%d/%Y")
                    return abs((d2 - d1).days)

                def get_elements_after_split(self,activity):
                    list1=[]
                    list1=activity.split(' ')
                    return list1

                def verify_activity_data_displayed_in_risk_order_or_not(self,imagelist):
                    """Returns true if the activity data displyed in descending order , Other wise returns false"""
                    list1=[]
                    list1=imagelist
                    for i in xrange(len(list1) - 1):
                        if list1[i]<list1[i+1]:
                            return False

                    return True
                
                def get_current_time(self):
                    """Returns current time with date"""
                    ts = time.time()
                    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                    return timestamp

                def check_format_of_date(self,date):
                    """Returns True if the given date is in desired formate , Other wise returns False"""
                    try:
                        datetime.datetime.strptime(date,'%m/%d/%Y')
                        return True
                    except ValueError:
                        return False
    
                def date_sorting(self,actuallist):
                    datelist=[]
                    datelist1=[]
                    for index in range(len(actuallist)):
                        date=datetime.datetime.strptime(actuallist[index], '%m/%d/%Y').strftime('%Y-%m-%d')
                        datelist.append(date)
                    datesort=sorted(datelist)
                    for index in range(len(datesort)):
                        date1=datetime.datetime.strptime(datesort[index], '%Y-%m-%d').strftime('%m/%d/%Y')
                        datelist1.append(date1)
                    return datelist1

                def reverse_date_sorting(self,actuallist):
                    datelist=[]
                    datelist1=[]
                    for index in range(len(actuallist)):
                        date=datetime.datetime.strptime(actuallist[index], '%m/%d/%Y').strftime('%Y-%m-%d')
                        datelist.append(date)
                    datesort=sorted(datelist,reverse=True)
                    for index in range(len(datesort)):
                        date1=datetime.datetime.strptime(datesort[index], '%Y-%m-%d').strftime('%m/%d/%Y')
                        datelist1.append(date1)
                    return datelist1

                def is_list_contains_value(self,listofvals,value):
                    '''Returns True if the "value" found from the list "listofvals" else False'''
                    listofvals = []
                    listofvals = listofvals
                    if value in listofvals:
                        return True
                    else:
                        return False
                
                def get_table_rows_count_by_scroll(self,locator,parentLocator='',parentScroll=''):
                    """Returns the total no of rows in a table by scrolling specifying scrolling knob locator"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible(locator)
                    prevvalue = selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:]                    
                    print "First scrool value:" + str(prevvalue)
                    #Scroll down
                    self.wait_for_element_visible(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    #Get the values from all rows by scrolling down
                    while(not (prevvalue==selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:])):
                        prevvalue = selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:]
                        selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    selenium.mouse_over(locator)
                    rwCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                    rwCnt = rwCnt.split("-")
                    rwCnt = rwCnt[1].replace(" ","")
                    print "rwCnt:"+str(rwCnt)
                    #Scroll back to the top
                    self.scroll_to_top()
                    return str(rwCnt)

                def is_Octet_Format(self,address):
                    try:
                        socket.inet_aton(address)
                        ip = True
                    except socket.error:
                        ip = False
                    return ip
                def get_EST_current_time(self):
                    Est = timezone('US/Eastern')
                    est = datetime.datetime.now(Est)
                    return str(est.strftime('%m/%d/%Y %I:%M %p'))
                
                def match_the_string_pattern(self,x,y):
                    lenOfFirst = len(x)
                    lenOfSec = len(y)
                    x=x.lower()
                    y=y.lower()
                    if(y[lenOfSec-1] == '*'):
                        y=y.replace('*','')
                        if(x[:len(y)] == y):
                            return True
                        else:
                             return False
                    else:
                        if(x[:len(y)] == y):
                            return True
                        else:
                            return False

                def any_one_element_should_be_visible(self, locator1 , locator2 , message=''):
                    """Verifies that the element identified by `locator` is visible.

                    Herein, visible means that the element is logically visible, not optically
                    visible in the current browser viewport. For example, an element that carries
                    display:none is not logically visible, so using this keyword on that element
                    would fail.

                    `message` can be used to override the default error message.

                    Key attributes for arbitrary elements are `id` and `name`. See
                    `introduction` for details about locating elements.
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    visible1 = self.wait_for_element_visible(locator1)
                    print "visible1 "+str(visible1)
                    visible2 = self.wait_for_element_visible(locator2,"7s")
                    print "visible2 "+str(visible2)
                    if visible1 != True and visible2 != True  :
                        if not message:
                            message = "any one of elements should ot be visible"
                        raise AssertionError(message)
                    time.sleep(4)

                def get_table_each_rows_values_into_list_by_down_arrow(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows=''):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' and scrollbar located at 'scrollbar_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    keyColNum = self._table_get_column_no(locator,columnName)
                    time.sleep(2)
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    rowValues=[]
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    allTableValues =[]
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        if (iValue==2):
                            selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                        else:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                        colCount2 = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                        dctVals = {}
                        for iCounter2 in range(1,colCount2+1):
                            curColName2 = selenium._get_text(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div[1]')
                            if(len((str(curColName2).strip()))==0):
                                continue
                            rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div'+'['+str(iValue)+']')
                            dctVals[curColName2] = rowValue
                            print "curColName2:"+ str(rowValue) +" & rowValue:"+str(rowValue)
                            allTableValues.append(dctVals)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "Counter:"+str(Counter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                        try:
                            selenium.wait_until_element_is_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',"10s")
                        except:
                            print "column values is not displayed"                     
                        rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "duplicate counter:"+str(Counter)
                                print "duplicate val:"+str(iCounter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        colCount2 = int(selenium.get_matching_xpath_count(locator+'/tbody/tr/td'))
                        dctVals = {}
                        for iCounter2 in range(1,colCount2+1):
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div[1]')
                            curColName2 = selenium._get_text(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div[1]')
                            if(len((str(curColName2).strip()))==0):
                                continue
                            try:
                                selenium.wait_until_element_is_visible(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div'+'['+str(iValue)+']')
                            except:
                                print "columns names are not displayed"
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div'+'['+str(iValue)+']')
                            rowValue=selenium.get_text(locator+'/tbody/tr/td['+str(iCounter2)+']/div/div'+'['+str(iValue)+']')
                            dctVals[curColName2] = rowValue
                            print "curColName2:"+ str(rowValue) +" & rowValue:"+str(rowValue)
                        allTableValues.append(dctVals)
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    return allTableValues

                def validate_results_table_details_with_search_field_values(self,tablevalues,searchDeatisl):
                    for tableRowValues in tablevalues:
                        tableHeaders = tableRowValues.keys()
                        searchFiledNames = searchDeatisl.keys()
                        for tableHeader in tableHeaders:
                            tablerowval = tableRowValues[tableHeader]
                            print "tablerow "+str(tableHeader) +" val : "+ str(tablerowval)
                            for searchFiledName in searchFiledNames:
                                searchFiledValue = searchDeatisl[searchFiledName]
                                print "searchFiledValue: "+str(searchFiledValue)
                                if (tableHeader == searchFiledName):
                                    if(searchFiledValue.lower() != tablerowval.lower()):
                                        return False
                                    if ((str(tableHeader)=="Session" or str(tableHeader)== "Total #") and int(tablerowval)==0):
                                            return False
                                else:
                                    print "Not in Search Deatils"
                                    if(len(tablerowval) == 0):
                                        return False
                                    if ((str(tableHeader)=="Session" or str(tableHeader)== "Total #") and  int(tablerowval)==0):
                                        return False
                    return True
                        
                def Get_Previous_search_text_status(self,buttonName,expectedText):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    buttonLocator = BuiltIn().get_variable_value("${button.fraudMatch.showResults."+str(buttonName)+"}")
                    bStatus = False
                    for iCounter in range(1,6):
                        print "iCounter="+ str(iCounter)+ " and button name "+ str(buttonName)
                        try:
                            btnStatus = self.wait_for_element_visible(buttonLocator,"10s")
                            print "btnStatus= "+str(btnStatus)
                            if btnStatus==False:
                                selenium.wait_until_element_is_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                print "showResults"
                            selenium.wait_until_element_is_visible(buttonLocator,"10s")
                            selenium.click_element(buttonLocator)
                            print "clicked "+str(buttonName) +"button"
                            for iIndex in range(1,7):
                                print "riskdropdown iIndex: "+ str(iIndex)
                                try:
                                    self.wait_for_element_visible("//div[@class='doralPulldown']/div[text()='Previous Searches']","5s")
                                    selenium.mouse_over("//div[@class='doralPulldown']")
                                    selenium.click_element("//div[@class='doralPulldown']")
                                    #txtStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${list.accounts.previoussearches.dropdownitem}")+"/div","10s")
                                    #print "txtStatus= "+str(txtStatus)
                                    #selenium.mouse_over(BuiltIn().get_variable_value("${list.accounts.previoussearches.dropdownitem}")+"/div")
                                    #print "dropdownitem mouse over"
                                    #self.wait_for_element_visible("//div[@id='pqsHoverDetailObj']/div","5s")
                                    #previoussearchtext = selenium._get_text("//div[@id='pqsHoverDetailObj']/div")
                                    previoussearchtext = selenium.execute_javascript("return document.getElementById('pqsHoverDetailObj').getElementsByTagName('div')[0].textContent")
                                    print "previoussearchtext: "+str(previoussearchtext)
                                    break
                                except:
                                    print "reading previoussearchtext failed"
                            bStatus = self.string_should_contain(previoussearchtext,expectedText)
                            print "bStatus: "+str(bStatus)
                            if bStatus==True:
                                return bStatus                               
                        except:
                            print "Iteration was "+str(iCounter) +" failed"
                    return bStatus
                    
                def enter_and_validate_advanced_search_fields(self,dictVar,hideFilters=True,expectedLocator=None,reset=True):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    print "resetStatus: "+str(resetStatus)
                    if reset==True:
                        self.wait_and_click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "ipaddress":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "sessionrange":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "channel":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "country":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace("/","") == "osbrowser":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "iptype":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "state":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "useragent":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"))
                                    if fieldStatus == True:
                                        print "${textbox.advanceSearch.useragent}: "+str(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"))
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "riskfactor":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "provider":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "city":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "activity":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "recipientname":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "amount":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "tracenumber":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "recipientaccountnumber":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "seccode":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.SECCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.SECCode}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.SECCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "odfiid":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transactioncode":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyid":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyname":
                                    print "enter in to recipientname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "user":
                                    print "enter in to User field"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.advanceSearch.user}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${text.advanceSearch.user}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${text.advanceSearch.user}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                        
                                        
                        except:
                            print "entering search details failed"
                        showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "showResultsStatus: " +str(showResultsStatus)
                        if showResultsStatus == True:
                            selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            time.sleep(5)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                        else:
                            print "check expectedLocator "+ str(expectedLocator)
                            self.wait_for_element_visible(expectedLocator)
                        searchStatus = self.check_search_checkbox(dictVar)
                        print "searchStatus: "+str(searchStatus)
                        if searchStatus == True:
                            showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            print "showResultsStatus: " +str(showResultsStatus)
                            if showResultsStatus == True:
                                time.sleep(2)
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                if expectedLocator==None:
                                    for iCnt in range(1,1000):
                                        searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                        print "searchingStatus: "+str(searchingStatus)
                                        if searchingStatus == False:
                                            break
                                    self.wait_for_search_is_running_in_background_alert_message()
                                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                                else:
                                    print "check expectedLocator "+ str(expectedLocator)
                                    self.wait_for_element_visible(expectedLocator)
                        else:
                            break;
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']","5s") == True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                            print "hiding Filters section done"
                        except:
                            print "hiding Filters failed"
                    return True


                def enter_and_validate_advanced_search_fields_in_alertsbw(self,dictVar,hideFilters=True,expectedLocator=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","10s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    if resetStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "riskfactor":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "direction":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "paymentmethod":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transferrange":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "activity":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "businesscode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "type":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "subtype":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "amount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "originatorcountry":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "beneficiarycountry":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "creditaccount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "debitaccount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transferstatus":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                        except:
                            print "entering search details failed"
                        showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "showResultsStatus: " +str(showResultsStatus)
                        if showResultsStatus == True:
                            selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            time.sleep(5)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                        else:
                            print "check expectedLocator "+ str(expectedLocator)
                            self.wait_for_element_visible(expectedLocator)
                        searchStatus = self.check_search_checkbox_in_alertsbw(dictVar)
                        print "searchStatus: "+str(searchStatus)
                        if searchStatus == True:
                            showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            print "showResultsStatus: " +str(showResultsStatus)
                            if showResultsStatus == True:
                                time.sleep(2)
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                if expectedLocator==None:
                                    for iCnt in range(1,1000):
                                        searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                        print "searchingStatus: "+str(searchingStatus)
                                        if searchingStatus == False:
                                            break
                                    self.wait_for_search_is_running_in_background_alert_message()
                                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                                else:
                                    print "check expectedLocator "+ str(expectedLocator)
                                    self.wait_for_element_visible(expectedLocator)
                        else:
                            break;
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']") == True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                        except:
                            print "hiding Filters failed"
                    return True


                def enter_and_validate_wire_trasfer_details_in_alertsbw(self,dictVar,hideFilters=True,expectedLocator=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","10s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    if resetStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.advanceSearch.edit}"),"10s")
                    if editButtonStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.advanceSearch.edit}"))
                        time.sleep(5)
                        
                    for iCounter in range(1,2):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "originatorname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "originatorcode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorCode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorCode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "originatorid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "beneficiaryname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "beneficiarycode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryCode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryCode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "beneficiaryid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "sendingfiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "sendingficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "sendingfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "receivingfiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "receivingficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SendingFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "receivingfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ReceivingFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "originatorfiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "originatorficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "originatorfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatorFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","")== "beneficiaryfiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "beneficiaryficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "beneficiaryfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.BeneficiaryFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "instructingfiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "instructingficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "instructingfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructingFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","")== "intermediatefiname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","")== "intermediateficode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFICode}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFICode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFICode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                
                                elif keyVal.lower().replace(" ","") == "intermediatefiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.IntermediateFIID}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "senderreference":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SenderReference}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SenderReference}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.SenderReference}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "source":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.Source}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.Source}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.Source}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "instructedamount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructedAmount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructedAmount}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.InstructedAmount}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "originatortobeneficiaryinstructions":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatortoBeneficiaryInstructions}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatortoBeneficiaryInstructions}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.OriginatortoBeneficiaryInstructions}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "currencycode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.CurrencyCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.CurrencyCode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.CurrencyCode}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "exchangerate":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ExchangeRate}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ExchangeRate}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.wireTransferDetails.ExchangeRate}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)
                                
                        except:
                            print "entering search details failed"
                    okButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                    if okButtonStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                        time.sleep(5)
                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.advanceSearch.edit}"),"10s")
                    if editButtonStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.advanceSearch.edit}"))
                        time.sleep(5)
                    checkStatus = self.check_search_checkbox_in_wire_transfer_details(dictVar)
                    print "checkStatus : "+str(checkStatus)

                    details = selenium.get_text("//div[@id='activityFieldList']")
                    bStatus = self.string_should_contain(details,dictVals[0])
                    if bStatus != True:
                        print "details not contain entered values of wire details: "+str(bStatus)
                        
                    showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                    print "showResultsStatus: " +str(showResultsStatus)
                    if showResultsStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        time.sleep(5)
                    if expectedLocator==None:
                        for iCnt in range(1,1000):
                            searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                            print "searchingStatus: "+str(searchingStatus)
                            if searchingStatus == False:
                                break
                        self.wait_for_search_is_running_in_background_alert_message()
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                    else:
                        print "check expectedLocator "+ str(expectedLocator)
                        self.wait_for_element_visible(expectedLocator)
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")==True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","10s")
                        except:
                            print "hiding Filters failed"
                    return True
                

                def enter_and_validate_single_advanced_search_field(self,dictVar,hideFilters=True,expectedLocator=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","10s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    if resetStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "riskfactor":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "direction":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Direction}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "paymentmethod":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.PaymentMethod}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transferrange":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferRange}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "activity":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Activity}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "businesscode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.BusinessCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "type":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Type}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "subtype":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Subtype}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "amount":
                                    print "Enter into amount conidtion block"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"))
                                    print "fieldStatus:"+str(fieldStatus)
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "originatorcountry":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.OriginatorCountry}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "beneficiarycountry":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.BeneficiaryCountry}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "creditaccount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CreditAccount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "debitaccount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.DebitAccount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transferstatus":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransferStatus}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                        except:
                            "Enter value to advance search failed ,again trying"
                        searchStatus = self.check_search_checkbox_in_alertsbw(dictVar)
                        if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")==True:
                            try:
                                selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                                self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","10s")
                            except:
                                print "hiding Filters failed"
                    return True

                def check_search_checkbox_in_alertsbw(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "check : "+str(keyVal) + " checkbox"
                        try:
                            if keyVal.lower().replace(" ","")== "riskfactor":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.RiskFactor}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[contains(text(),'Risk Factor')]")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                    
                            elif keyVal.lower().replace(" ","") == "direction":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Direction}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Direction']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "paymentmethod":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.PaymentMethod}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Payment Method']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                    
                            elif keyVal.lower().replace(" ","") == "transferrange":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TransferRange}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Transfer Range']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "activity":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Activity}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Activity']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "businesscode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.BusinessCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Business Code']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "type":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Type}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Type']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "subtype":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Subtype}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Subtype']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "amount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Amount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Amount']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "originatorcountry":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.OriginatorCountry}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Originator Country']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "beneficiarycountry":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.BeneficiaryCountry}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Beneficiary Country']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "creditaccount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.CreditAccount}"))
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Credit Account']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "debitaccount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.DebitAccount}"))
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='DebitAccount']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "transferstatus":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TransferStatus}"))
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Transfer Status']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "recipientname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.RecipientName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Recipient Name']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                    
                            print "fieldStatus: "+str(fieldStatus)
                        except:
                            print "all checkboxes are not selected" + str(keyVal) + " check box not checked"
                       
                    return bStatus

                def check_search_checkbox_in_wire_transfer_details(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
             
                    for keyVal in dictKeys:
                        print "check : "+str(keyVal) + " checkbox"
                        try:
                            if keyVal.lower().replace(" ","")== "originatorname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")
                                    
                            elif keyVal.lower().replace(" ","")== "originatorcode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "originatorid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiaryname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiarycode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiaryid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "sendingfiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Sending FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Sending FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "sendingficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Sending FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Sending FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "sendingfiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Sending FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Sending FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "receivingfiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Receiving FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Receiving FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "receivingficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Receiving FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Receiving FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "receivingfiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Receiving FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Receiving FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "originatorfiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "originatorficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "originatorfiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiaryfiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiaryficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "beneficiaryfiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Beneficiary FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Beneficiary FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "instructingfiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Instructing FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Instructing FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "instructingficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Instructing FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Instructing FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "instructingfiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Instructing FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Instructing FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "intermediatefiname":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Intermediate FI Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Intermediate FI Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "intermediateficode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Intermediate FI Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Intermediate FI Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "intermediatefiid":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Intermediate FI ID')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Intermediate FI ID')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "senderreference":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Sender Reference')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Sender Reference')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "source":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Source')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Source')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "instructedamount":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Instructed Amount')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Instructed Amount')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "originatortobeneficiaryinstructions":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Originator to Beneficiary Instructions')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Originator to Beneficiary Instructions')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "exchangerate":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Exchange Rate')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Exchange Rate')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "currencycode":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Currency Code')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Currency Code')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","")== "templatename":
                                fieldStatus = selenium.get_element_attribute("//label[contains(text(),'Template Name')]//preceding-sibling::input@checked")
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)    
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//label[contains(text(),'Template Name')]")
                                    editButtonStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"),"10s")
                                    if editButtonStatus == True:
                                        selenium.click_element(BuiltIn().get_variable_value("${button.alerts.activityDetailsDialogOk}"))
                                        time.sleep(5)
                                        bStatus = True
                                        print str(keyVal) + str(" checkbox was selected using click element keyword")
                                        
                            print "fieldStatus: "+str(fieldStatus)
                        except:
                            print "all checkboxes are not selected" + str(keyVal) + " check box not checked"
                       
                    return bStatus

                


                def check_search_checkbox(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "check : "+str(keyVal) + " checkbox"
                        try:
                            if keyVal.lower().replace(" ","")== "ipaddress":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.IPAddress}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected / checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='IP Address']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                            elif keyVal.lower().replace(" ","") == "sessionrange":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.SessionRange}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Session Range']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "country":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.country}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Country']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                            elif keyVal.lower().replace(" ","") == "channel":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.accessmode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Channel']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace("/","") == "osbrowser":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.osbrowser}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='OS/Browser']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "iptype":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.iptype}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='IPType']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "state":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.state}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='State']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "useragent":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.useragent}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='User Agent']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "riskfactor":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.riskfactor}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Risk Factor']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "provider":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.provider}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Provider']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "city":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.city}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='City']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "activity":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.activity}"))
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Activity']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "recipientname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.RecipientName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Recipient Name']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "tracenumber":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TraceNumber}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Trace Number']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "recipientaccountnumber":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.RecipientAccountNumber}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Recipient Account Number']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "amount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.Amount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Amount']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "seccode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.SECCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='SEC Code']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "odfiid":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.ODFIID}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='ODFI ID']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "transactioncode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TransactionCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Transaction Code']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companyid":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.CompanyID}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company ID']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companyname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.CompanyName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company Name']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                            print "fieldStatus: "+str(fieldStatus)
                        except:
                            print "all checkboxes are not selected" + str(keyVal) + " check box not checked"
                       
                    return bStatus

                def click_element_and_check_expected_element(self,element_locator1,element_locator2=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "element_locator1: "+ str(element_locator1)
                    print "element_locator2: "+ str(element_locator2)
                    for iCounter in range(1,5):
                        try:
                            self.wait_for_element_visible(element_locator1)
                            selenium.click_element(element_locator1)
                            time.sleep(2)
                            if element_locator2==None:
                                return True
                        except:
                            print "element exception"
                        bStatus = self.wait_for_element_visible(element_locator2)
                        if bStatus == True:
                            print "expected element was visible"
                            return bStatus
                        else:
                            print "expected element was not visible"
                    return bStatus

                def wait_and_click_element(self,element_locator1,timeOut=None):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    if timeOut == None:
                        timeOut = "5s"
                    print "element_locator: "+ str(element_locator1)
                    for iCounter in range(1,5):
                        try:
                            bStatus = self.wait_for_element_visible(element_locator1,timeOut)
                            if bStatus==True:
                                selenium.click_element(element_locator1)
                                return True
                            else:
                                continue
                        except:
                            print "element exception"
                    return bStatus

                def select_date_in_basic_search(self,dateVal):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icount in range(10):
                        try:
                            print "date filed status "+ str(self.wait_for_element_visible(BuiltIn().get_variable_value("${list.alerts.date}")))
                            selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.alerts.date}"),dateVal)
                            for i in range(1,10):
                                bStatus = self.wait_for_element_visible("//select[@id='mainForm:dateFilter']/option[@selected='selected' and text()='"+str(dateVal) +"']","5s")
                                if bStatus==True:
                                    time.sleep(2)
                                    break
                            time.sleep(5)
                        except:
                            print "date was not selected"
                            return False
                        return True

                def rest_default_columns(self,headerlocator=None):
                    """Restore the default column"""
                    if headerlocator == None:
                        headerlocator = "//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_th_R0C8']/div/div[1]"
                    headerlocator = str(headerlocator)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        for iCounter in range(1,5):
                            mStatus = self.wait_for_element_visible(headerlocator)
                            if mStatus ==True:
                                selenium.mouse_over(headerlocator)
                                selenium.open_context_menu(headerlocator)
                                self.wait_for_element_visible("//span[contains(text(),'Restore default columns')]")
                                selenium.mouse_over("//span[contains(text(),'Restore default columns')]")
                                selenium.click_element("//span[contains(text(),'Restore default columns')]")
                                break
                            else:
                                time.sleep(4)

                    except:
                        print "drestore default coloumn not succeded"
                        return False
                    return True

                def select_risk_in_basic_search(self,riskcolor):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "riskcolor: "+ str(riskcolor)
                    try:
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${image.basicsearch.riskdownarrow}"))
                        selenium.click_element(BuiltIn().get_variable_value("${image.basicsearch.riskdownarrow}"))
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${link.common.risk"+str(riskcolor)+"}"))
                        selenium.click_element(BuiltIn().get_variable_value("${link.common.risk"+str(riskcolor)+"}"))
                    except:
                        print "risk color selection was failed"


                def select_status_in_basic_search(self,StatusValues):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    StatusValuesList = StatusValues.split(",")
                    print "StatusValuesList"
                    print StatusValuesList
                    try:
                        self.wait_for_element_visible("//div[@class='buttonList']/div/a")
                        iCount = selenium.get_matching_xpath_count("//div[@class='buttonList']/div/a")
                        print "iCount: "+str(iCount)
                        for iIndex in range(1,int(iCount)+1):
                            sbtnClassAttrVal = selenium.get_element_attribute("//div[@class='buttonList']/div/a["+str(iIndex)+"]@class")
                            print "sbtnClassAttrVal: " +str(sbtnClassAttrVal)
                            if sbtnClassAttrVal.lower().find("selected")>=0:                                
                                selenium.click_element("//div[@class='buttonList']/div/a["+str(iIndex)+"]")
                                time.sleep(2)
                        for statusVal in StatusValuesList:
                            print "statusVal: " +str(statusVal)
                            self.wait_for_element_visible("//div[@class='buttonList']//a[@title='"+str(statusVal)+"']")
                            selenium.click_element("//div[@class='buttonList']//a[@title='"+str(statusVal)+"']")
                            time.sleep(2)
                    except:
                        print "status button selection was failed"
                        return False
                    return True

                def do_basic_search(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "Basic Search - dctkey : "+str(keyVal) + " dctval: " + str(dictVar[keyVal])
                        try:
                            if keyVal.lower().replace(" ","")== "date":
                                fieldStatus = self.select_date_in_basic_search(str(dictVar[keyVal]))
                                if fieldStatus == True:
                                    print str(keyVal) + str(" date was selected")
                                else:
                                    print str(keyVal) + str(" date was not selected")
                            elif keyVal.lower().replace(" ","") == "from" and len(str(dictVar[keyVal]))>0:
                                fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.alerts.fromDate}"))
                                if fieldStatus == True:
                                    selenium.input_text(BuiltIn().get_variable_value("${text.alerts.fromDate}"),dictVar[keyVal])
                                    print str(keyVal) + str(" values was enterted")
                                else:
                                    print str(keyVal) + str(" values was not enterted")

                            elif keyVal.lower().replace(" ","") == "type" and len(str(dictVar[keyVal]))>0:
                                print "tempVals"
                                tempVals = str(dictVar[keyVal]).split(",")
                                print tempVals
                                tempValsCount = len(tempVals)
                                print "tempValsCount: "+str(tempValsCount)
                                dropDown1Val = tempVals[0]
                                fieldStatus01 = self.wait_for_element_visible(BuiltIn().get_variable_value("${list.reports.typeDropDwn}"))
                                if fieldStatus01 == True:
                                    selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.reports.typeDropDwn}"),dropDown1Val)
                                    print str(keyVal) + str(" values was selected")
                                    time.sleep(2)
                                else:
                                    print str(keyVal) + str(" values was not selected")
                                    return False
                                if int(tempValsCount)==2:
                                    dropDown2Val = tempVals[1]
                                    fieldStatus02 = self.wait_for_element_visible(BuiltIn().get_variable_value("${list.reports.volumeCountbySelectVal}"))
                                    if fieldStatus02 == True:
                                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.reports.volumeCountbySelectVal}"),dropDown2Val)
                                        print str(keyVal) + str(" values was selected")
                                    else:
                                        print str(keyVal) + str(" values was not selected")
                                        return False

                            elif keyVal.lower().replace(" ","") == "to" and len(str(dictVar[keyVal]))>0:
                                fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.alerts.todate}"))
                                if fieldStatus == True:
                                    selenium.input_text(BuiltIn().get_variable_value("${text.alerts.todate}"),dictVar[keyVal])
                                    print str(keyVal) + str(" values was enterted")
                                else:
                                    print str(keyVal) + str(" values was not enterted")

                            elif keyVal.lower().replace(" ","") == "risk":
                                fieldStatus = self.select_risk_in_basic_search(dictVar[keyVal])
                            elif keyVal.lower().replace(" ","") == "status":
                                fieldStatus = self.select_status_in_basic_search(dictVar[keyVal])
                                if fieldStatus == True:
                                    print str(keyVal) + str(" status buttons were selected ")
                                else:
                                    print str(keyVal) + str(" status buttons were notselected ")

                            elif keyVal.lower().replace(" ","") == "from(ct)" and len(str(dictVar[keyVal]))>0:
                                fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.alerts.fromDate}"))
                                if fieldStatus == True:
                                    selenium.input_text(BuiltIn().get_variable_value("${text.alerts.fromDate}"),dictVar[keyVal])
                                    print str(keyVal) + str(" values was enterted")
                                else:
                                    print str(keyVal) + str(" values was not enterted")

                            elif keyVal.lower().replace(" ","") == "to(ct)" and len(str(dictVar[keyVal]))>0:
                                fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.alerts.todate}"))
                                if fieldStatus == True:
                                    selenium.input_text(BuiltIn().get_variable_value("${text.alerts.todate}"),dictVar[keyVal])
                                    print str(keyVal) + str(" values was enterted")
                                else:
                                    print str(keyVal) + str(" values was not enterted")

                        except:
                            print "basic search was not done"

                def do_cases_basic_search(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "Cases Basic Search - dctkey : "+str(keyVal) + " dctval: " + str(dictVar[keyVal])
                        try:
                            
                            if keyVal.lower().replace(" ","")== "by":
                                fieldStatus = self.select_by_in_cases_basic_search(str(dictVar[keyVal]))
                                if fieldStatus == True:
                                    print str(keyVal) + str(" By was selected")
                                else:
                                    print str(keyVal) + str(" By was not selected")

                            
                                    
                            elif keyVal.lower().replace(" ","") == "category":
                                 fieldStatus = self.select_category_in_cases_basic_search(dictVar[keyVal])
                                 if fieldStatus == True:
                                     print str(keyVal) + str(" Categy was selected")
                                 else:
                                     print str(keyVal) + str(" Categy was not selected")
                                
                            elif keyVal.lower().replace(" ","") == "owner":
                                 fieldStatus = self.select_owner_in_cases_basic_search(dictVar[keyVal])
                                 if fieldStatus == True:
                                     print str(keyVal) + str(" Owner buttons were selected ")
                                 else:
                                     print str(keyVal) + str(" Owner buttons were notselected ")
                                        
                            elif keyVal.lower().replace(" ","") == "resolution":
                                 fieldStatus = self.select_resolution_in_cases_basic_search(dictVar[keyVal])
                                 if fieldStatus == True:
                                    print str(keyVal) + str(" Resolution buttons were selected ")
                                 else:
                                    print str(keyVal) + str(" Resolution buttons were notselected ")

                            elif keyVal.lower().replace(" ","") == "status":
                                 fieldStatus = self.select_status_in_cases_basic_search(dictVar[keyVal])
                                 if fieldStatus == True:
                                    print str(keyVal) + str(" status buttons were selected ")
                                 else:
                                    print str(keyVal) + str(" status buttons were notselected ")


                        except:
                            print "Caess basic search was not done"


                def select_owner_in_cases_basic_search(self,ownerVal):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        print "Owner filed status "+ str(self.wait_for_element_visible(BuiltIn().get_variable_value("${list.cases.owner}")))
                        #selenium.input_text(BuiltIn().get_variable_value("${list.cases.owner}"),ownerVal)
                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.cases.owner}"),ownerVal)
                        for i in range(1,10):
                            bValue = selenium.get_selected_list_label(BuiltIn().get_variable_value("${list.cases.owner}"))
                            if bValue==ownerVal:
                                break
                            else:
                                time.sleep(2)
                    except:
                        print "date was not selected"
                        return False
                    return True

                def select_category_in_cases_basic_search(self,categVal):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        print "date filed status "+ str(self.wait_for_element_visible(BuiltIn().get_variable_value("${list.cases.category}")))
                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.cases.category}"),categVal)
                        for i in range(1,10):
                            bValue = selenium.get_selected_list_label(BuiltIn().get_variable_value("${list.cases.category}"))
                            if bValue==categVal:
                                break
                            else:
                                time.sleep(2)
                    except:
                        print "Cateegory was not selected"
                        return False
                    return True

                def select_resolution_in_cases_basic_search(self,resVal):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        print "date filed status "+ str(self.wait_for_element_visible(BuiltIn().get_variable_value("${list.cases.resolution}")))
                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.cases.resolution}"),resVal)
                        for i in range(1,10):
                            bValue = selenium.get_selected_list_label(BuiltIn().get_variable_value("${list.cases.resolution}"))
                            if bValue==resVal:
                                break
                            else:
                                time.sleep(2)
                    except:
                        print "Resolution was not selected"
                        return False
                    return True
                
                def select_by_in_cases_basic_search(self,byVal):
                    """It will select the date values in basic search functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        print "By filed status "+ str(self.wait_for_element_visible(BuiltIn().get_variable_value("${list.cases.by}")))
                        selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.cases.by}"),byVal)
                        for i in range(1,10):
                            bValue = selenium.get_selected_list_label(BuiltIn().get_variable_value("${list.cases.by}"))
                            if bValue==byVal:
                                break
                            else:
                                time.sleep(2)
                    except:
                        print "By was not selected"
                        return False
                    return True


                def open_context_menu_and_select_menu_item(self,headerlocator,itemName):
                    """Restore the default column"""
                    headerlocator = str(headerlocator)
                    itemlocator = str("//span[contains(text(),'"+str(itemName)+"')]")
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,3):
                        try:
                            headerStatus = self.wait_for_element_visible(headerlocator)
                            if headerStatus ==True:
                                selenium.mouse_over(headerlocator)
                                selenium.open_context_menu(headerlocator)
                                self.wait_for_element_visible(itemlocator)
                                #selenium.capture_page_screenshot()
                                selenium.mouse_over(itemlocator)
                                selenium.simulate(itemlocator,'click')
                                time.sleep(2)
                                return True
                            else:
                                time.sleep(4)
                        except:
                            print "context menu selection not succeded"
                    return False

                def wait_for_search_is_running_in_background_alert_message(self):
                    """This keyword will wait for wait for alert message in advanced search functionality"""
                    alerttextlocator = str("//div[@id='cmdHiddenWarnDialogContentDiv']//div[@class='clearfix' and contains(text(),'The search is continuing to run in the background')]")
                    print "check background alert message:"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,10):
                        print "iCounter: "+ str(iCounter)
                        try:
                            bstatus = self.wait_for_element_invisible("//div[@id='cmdHiddenWarnDialogContentDiv']//div[@class='uniButton']/a[@class='uniText' and text()='Ok']","5s")
                            print "search is running background dialog is not present after clicking show results"
                            if bstatus==True:
                                return bstatus
                            else:
                                continue
                        except:
                            print "search is continuing dialog is present after clicking show results"
                        alertStatus = self.wait_for_element_visible(alerttextlocator,"5s")
                        print "alertStatus: " + str(alertStatus)
                        if alertStatus == True:
                            time.sleep(5)
                            print "The search is continuing to run in the background"
                            try:
                                selenium.click_element("//div[@id='cmdHiddenWarnDialogContentDiv']//div[@class='uniButton']/a[@class='uniText' and text()='Ok']")
                                selenium.simulate("//div[@id='cmdHiddenWarnDialogContentDiv']//div[@class='uniButton']/a[@class='uniText' and text()='Ok']","click")
                            except:
                                print "click on Ok btn failed"
                            self.wait_for_spinning_icon_search_in_background()
                            break
                        else:
                            print "The search is continuing to run in the background not visible"
                            break
                def get_table_current_tooltip_row_count(self,parentLocator,expEndRow=True):
                    """ It will return the table rows count using tool tip text"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iIndex in range(1,5):
                        self.wait_for_element_visible(parentLocator)
                        try:
                            selenium.mouse_over(BuiltIn().get_variable_value("${button.alerts.export}"))
                        except:
                            print "Export button not displayed"
                        time.sleep(02)
                        selenium.mouse_over(parentLocator)
                        selenium.mouse_over(parentLocator)
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                        rwCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                        if len(rwCnt)>1 and (str(rwCnt).find("-"))>0:
                            break
                    print "rwCnt:"+str(rwCnt)
                    rwCnt = rwCnt.split("-")
                    if expEndRow==False:
                        startrwCnt = rwCnt[0].replace(" ","")
                        print "startrwCnt: "+str(startrwCnt)
                        return startrwCnt
                    rwCnt = rwCnt[1].replace(" ","")
                    print "rwCnt:"+str(rwCnt)
                    return rwCnt
                def verify_table_read_all_rows(self,totalRows,parentLocator):
                    """It will verify the total records are reading properly ot not"""
                    print "verify_table_read_all_rows keyword"
                    currentTooltipRowsCount= self.get_table_current_tooltip_row_count(parentLocator)
                    print "totalRows: "+ str(totalRows) +" currentTooltipRowsCount: "+ str(currentTooltipRowsCount)
                    if int(totalRows) == int(currentTooltipRowsCount):
                        print "Reading data from table was success"
                    else:
                        print ("Reading data from table was failed.Total rows count  is "+str(totalRows) +" but keyword reading only "+ str(currentTooltipRowsCount) +" records")
                        

                def wait_for_please_wait_option(self):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iIndex in range(1,10):
                        try:
                            attval = selenium.get_element_attribute("//div[@id='loadingMsg' and text()='Please wait...']@style")
                            print "attval: "+ str(attval)
                            if attval.find("visibility: hidden")>=0:
                                break
                            else:
                                time.sleep(1)
                        except:
                            print "exception in wait_for_please_wait_option keyword"
                            
                def wait_for_spinning_icon_search_in_background(self):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iIndex in range(1,10):
                        attval = selenium.get_element_attribute("//div[@id='queries']/img[contains(@src,'activityIndicator')]@style")
                        print "attval: "+ str(attval)
                        if attval.find("visibility: hidden")>=0:
                            break
                        else:
                            time.sleep(1)

                def wait_for_ajax_call(self):
                    """ Wailt for given time  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')

                    jscript = "return jQuery.active"
                    print jscript
                    
                    for iIndex in range(1,6):
                        try:
                            print int(selenium.execute_javascript(jscript))
                        except:
                            print "exception while reading jQuery.active"
                        try:
                            print int(selenium.execute_javascript("Ajax.activeRequestCount"))
                        except:
                            print "exception while reading Ajax.activeRequestCount"


                def count_of_checked_checkboxes_on_alerts_page(self,rowsCount):
                    """ This keyword will retunr the count of chcked checkboxes on alert table """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    locator = "//table[@class='ajs_tb_table']"
                    keyColNum = int(10)
                    time.sleep(2)
                    Counter = 0
                    rowsCount=int(rowsCount)                  
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        return 0
                    iCounter=0
                    iValue=1
                    time.sleep(2)
                    cbcount = 0
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        print "iValue: "+str(iValue)
                        if (iValue==2):
                            try:
                                self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                            except:
                                print "click elemet keyword got failed at table row"
                        else:
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            except:
                                print "mouse over keyword got failed at table row"
                            try:
                                if int(iValue)<int(int(elements)-2):
                                    selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                                time.sleep(1)
                            except:
                                print "Arrow down failed at table row"
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td[1]/div/div'+'['+str(iValue)+']//input[contains(@id,"AlertsTable") and @type="checkbox"]')
                            print "Account name:" +str(selenium.get_text(locator+'/tbody/tr/td[4]/div/div'+'['+str(iValue)+']'))
                            attValue = selenium.get_element_attribute(locator+'/tbody/tr/td[1]/div/div'+'['+str(iValue)+']//input[contains(@id,"AlertsTable") and @type="checkbox"]@checked')
                            if attValue=='true' or attValue=='checked':
                                cbcount = cbcount+1
                        except:
                            selenium.capture_page_screenshot()
                        print "attValue:"+str(attValue)
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            time.sleep(1)
                            self.wait_for_please_wait_option()
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td[1]/div/div'+'['+str(iValue)+']//input[contains(@id,"AlertsTable") and @type="checkbox"]')
                            print "Account name:" +str(selenium.get_text(locator+'/tbody/tr/td[4]/div/div'+'['+str(iValue)+']'))
                            attValue = selenium.get_element_attribute(locator+'/tbody/tr/td[1]/div/div'+'['+str(iValue)+']//input[contains(@id,"AlertsTable") and @type="checkbox"]@checked')
                            if attValue=='true' or attValue=='checked':
                                cbcount = cbcount+1
                        except:
                            selenium.capture_page_screenshot()
                        print "attValue:"+str(attValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    self.verify_table_read_all_rows(rowsCount,"//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob_top']")
                    time.sleep(5)
                    self.set_knob_position_at_top_of_the_table()
                    print "cbcount: "+ str(cbcount)
                    return cbcount

                def validate_checkbox_selection_and_count(self,rowsCount,checkboxCount):
                    """ """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    kStatus = True
                    checkboxCount = int(checkboxCount)
                    for iIndex in range(1,checkboxCount+1):
                        childWindowStatus = self.wait_for_element_visible("//td[@id='ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_body']/table[@class='ajs_tb_table']","5s")
                        if childWindowStatus==False:
                            self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']/div[1]")
                            selenium.click_element("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']/div[1]")
                        selenium.click_element("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                        statusoption = selenium.get_text("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                        print "statusoption:" + str(statusoption)
                        dropdowncount = (str(statusoption).split("(")[1]).replace(")","")
                        print "dropdowncount: "+str(dropdowncount)
                        selenium.click_element("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]//input")
                        checkedCount = self.count_of_checked_checkboxes_on_alerts_page(rowsCount)
                        print "counts comparison :dropdowncount "+ str(dropdowncount) +" and checkedCount "+str(checkedCount)
                        if int(checkedCount) != int(dropdowncount):
                            kStatus = False
                        for iCnt in range(1,5):
                            checkboxAttVal = selenium.get_element_attribute("//table[@class='ajs_tb_table']/tbody/tr/td//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']//input[@type='checkbox' and contains(@id,'tAlerts')]@checked")
                            if checkboxAttVal == 'checked' or checkboxAttVal == 'true':
                                selenium.click_element("//table[@class='ajs_tb_table']/tbody/tr/td//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']//input[@type='checkbox' and contains(@id,'tAlerts')]")
                            else:
                                break
                        childWindowStatus = self.wait_for_element_visible("//td[@id='ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_body']/table[@class='ajs_tb_table']","5s")
                        if childWindowStatus==False:
                            self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']/div[1]")
                            selenium.click_element("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_title_R0C0']/div[1]")
                            for iVal in range(1,100):
                                selenium.click_element("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                                statusoption2 = selenium.get_text("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                                if statusoption == statusoption2:
                                    break
                                else:
                                    self.press_down_key("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                        else:
                            selenium.click_element("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]//input")
                        statusoptiontext1 = selenium.get_text("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                        self.press_down_key("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                        for ival2 in range(1,5):
                            time.sleep(2)
                            statusoptiontext2 = selenium.get_text("//div[contains(@id,'ajs_T_AA_CheckBoxGroup_F_AA_CheckBoxGroup_cell') and contains(@class,'Selected')]/div/span")
                            if statusoptiontext1 != statusoptiontext2:
                                break
                    return kStatus 
                  
                def set_knob_position_at_top_of_the_table(self,locator=None,knobLocator=None):
                    """ This keyword will retunr the count of chcked checkboxes on alert table """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if locator==None:
                        locator = "//table[@class='ajs_tb_table']"
                    if knobLocator==None:
                        knobLocator = "//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']/div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob_top']"
                    else:
                        knobLocator = str(knobLocator)+"/div[contains(@id,'bar_knob_top')]"
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td[4]/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        return 0
                    cbcount = 0
                    for iIndex in range(0,5):
                        self.wait_for_element_visible(locator+'/tbody/tr/td[4]/div/div[2]')
                        selenium.click_element(locator+'/tbody/tr/td[4]/div/div[2]')
                        self.press_home_key(locator+'/tbody/tr/td[4]/div/div[2]')
                        time.sleep(2)
                        startrowNo = self.get_table_current_tooltip_row_count(knobLocator,False)
                        if int(startrowNo) == 1:
                            break

                def close_no_longer_available_alert_message(self):
                    """ This keyword will close FraudMAP is no longer available dialog"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iIndex in arnge(1,10):
                        alerStatus = self.wait_for_element_visible("//div[@id='serviceUnavailableDialogHeader' and contains(text(),'FraudMAP is no longer available')]","3s")
                        print "alerStatus="+str(alerStatus)
                        if alerStatus==False:
                            break
                        else:
                            self.wait_for_element_visible("//div[@id='serviceUnavailableDialogContentDiv']//a[@class='uniText' and text()='Close']")
                            selenium.click_element("//div[@id='serviceUnavailableDialogContentDiv']//a[@class='uniText' and text()='Close']")

                def get_column_no_from_table(self, table_locator, columnName,headerlocator=None):
                    """Returns the column number of the column matching 'columnName' from the table located at 'table_locator'."""
                    #try:
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    colmNo = self.table_get_column_no(table_locator,columnName)
                    if int(colmNo)==0:
                        self.rest_default_columns(headerlocator)
                        colmNo = self.table_get_column_no(table_locator,columnName)
                    if int(colmNo)==0:
                        raise AssertionError(columnName+" column name was not displayed in table heares ")
                    return colmNo

                def replace_item_in_list(self, listvar, oldstring,newstring,substring=None):
                    """replace the liste item with new string"""
                    for iIndex in range(0,len(listvar)):
                        if substring==None and str(listvar[iIndex])==str(oldstring):
                            listvar[iIndex]=str(newstring)
                        elif substring!=None:
                            print "substring"
                            listvar[iIndex]=str(str(listvar[iIndex]).replace(str(oldstring),str(newstring)))
                        else:
                            print "normal list"
                    return listvar


                def get_table_stausvalues_into_list_by_down_arrow(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows='',page=''):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' and scrollbar located at 'scrollbar_locator' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')

                    if(page.lower()=='research'):
                        keyColNum = 1
                    else:
                        keyColNum = 2
                    #keyColNum = 1
                    time.sleep(2)
                    rowValue = ""
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    rowValues=[]
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        print "iValue: "+str(iValue)
                        if (iValue==2):
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                                #self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                                rowValue=selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                                print "rowValue=" +str(rowValue)

                            except:
                                print "click elemet keyword got failed at table row"
                                selenium.capture_page_screenshot()
                        else:
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                                #self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                                rowValue=selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                                print "rowValue=" +str(rowValue)
                            except:
                                print "mouse over keyword got failed at table row"
                                selenium.capture_page_screenshot()
                            try:
                                if int(iValue)<int(int(elements)-2):
                                    selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                                self.wait_for_please_wait_option()
                            
                            except:
                                print "Arrow down failed at table row"
                                selenium.capture_page_screenshot()

                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                            self.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']//div')
                            #self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                            rowValue=selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            print "rowValue=" +str(rowValue)
                            time.sleep(2)
                        except:
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "Counter:"+str(Counter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']/div')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']/div')
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            self.wait_for_please_wait_option()
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']/div')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']/div')
                            #self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                            rowValue=selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            time.sleep(2)
                        except:
                            selenium.capture_page_screenshot()
                        print "rowValue:"+str(rowValue)
                        if (rowValue in rowValues) and (unique=="True"):
                            Counter= Counter+1
                            if Counter > 1:
                                print "duplicate counter:"+str(Counter)
                                print "duplicate val:"+str(iCounter)
                                raise AssertionError(rowValue+"  duplicate value is exist")
                        rowValues.append(rowValue)
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    #self.scroll_to_top()
                    self.verify_table_read_all_rows(rowsCount,scrollbar_locator)
                    return rowValues

                def mouse_over_on_element(self,actlocator,explocator=None):
                    """Hovering mouse on the actlocator and verify the explocator visiblity"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus=(explocator==None)
                    kwstatus = False
                    for counter1 in range(1,10):
                        try:
                            self.wait_for_element_visible(actlocator)
                            selenium.mouse_over(actlocator)
                            time.sleep(1)
                            if bstatus==True:
                                return True
                            if bstatus==False:
                                expelestatus=self.verify_element_visible(explocator)
                            if expelestatus==True:
                                return True
                        except:
                            print "mouse_over_on_element keyword failed"
                    return kwstatus

                def click_on_showresults_button_and_wait_for_desired_element(self,showresultsLoator,desiredLocator):
                    """Click on show results::"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    showResultsStatus = self.wait_for_element_visible(showresultsLoator)
                    print "showResultsStatus: " +str(showResultsStatus)
                    if showResultsStatus == True:
                        time.sleep(2)
                        selenium.click_element(showresultsLoator)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(desiredLocator)
                        else:
                            print "check expectedLocator "+ str(desiredLocator)
                            self.wait_for_element_visible(desiredLocator)


                def click_on_desired_watch_list(self,fieldName,dialogHeaderName,clickOnResetStatusInWatchlist=''):
                    """Mouse Over on selcted addvance Search Field and Click on WatchList Icon."""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    wStatus = False
                    for iCont in range(0,5):
                        print "iCont: "+str(iCont)
                        try:
                            advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='showAdvancedFilters' and @id='mainForm:advancedButton']","5s")
                            if advancedFilterStatus == True:
                                selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                            resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                            if resetStatus == True:
                                if ((clickOnResetStatusInWatchlist == "") or (clickOnResetStatusInWatchlist == True)):
                                    bStatus = self.wait_and_click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                                    print "bStatus : " +str(bStatus)
                                    if bStatus == False:
                                        continue
                                time.sleep(5)
                                for iCounter in range(0,2):
                                    print "iCounter: "+str(iCounter)
                                    if fieldName== "Account":
                                        print "Account Field"
                                        print "advance search field status: "+ str(self.wait_for_element_present("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input"))
                                        selenium.click_element("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                                        try:
                                            selenium.mouse_over("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                            print "Mouse hvering done"
                                        except:
                                            print "Mouse hvering not done"
                                        try:
                                            selenium.click_element("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                            print "clicked icon"
                                            break
                                        except:
                                            print "not clicked"
                                    else:
                                        print "Reaming Field"
                                        print "advance search field status: "+ str(self.wait_for_element_present("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input"))
                                        selenium.click_element("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                                        try:
                                            selenium.mouse_over("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                            print "Mouse hvering done"
                                        except:
                                            print "Mouse hvering not done"
                                        try:
                                            selenium.click_element("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                            print "clicked icon"
                                            break
                                        except:
                                            print "not clicked"
                            #wStatus = self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            wStatus =  self.verify_watchlist_status("5s")
                            print "Watch List opened successfully : " +str(wStatus)
                            if wStatus == True:
                                listStatus = self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                                print "listStatus:"+str(listStatus)
                                return True
                        except:
                            print "Watch List not opened" +str(wStatus)
                            continue
                    return False

                def delete_watch_list_which_is_associated_with_saved_search(self,fieldName,dialogHeaderName,watchlistName):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible("//table[@id='applWarningDialogContentTable']//span")
                    warningText = selenium.get_text("//table[@id='applWarningDialogContentTable']//span")
                    print str(warningText)
                    print "A1"
                    try:
                        selenium.click_element("//table[@id='applWarningDialogContentTable']//input[@id='warnForm:applWarningClose']")
                        print "A2"
                        self.wait_for_element_invisible("//table[@id='applWarningDialogContentTable']//input[@id='warnForm:applWarningClose']","15s")
                        print "A3"
                        time.sleep(4)
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Close')]")
                        print "A5"
                        selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Close')]")
                        print "A6"
                        self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Close')]","15s")
                        print "A7"
                        #Get Watch List NAme From Warning Message

                        print "Original Text"
                        originalText = warningText.replace("\n\n","BREAK1")
                        print "Original Text after Break1 replcce"
                        print originalText
                        originalText = originalText.replace("\n","BREAK2")
                        print "Original Text after Break2 replace in break1 second element "
                        print originalText
                        originalTextBraek1 = originalText.split("BREAK1")
                        print "Original Text after split break1"
                        print originalTextBraek1[1]
                        originalTextBraek2 = originalTextBraek1[1].split("BREAK2")
                        print "Original Text after split break2"

                        print originalTextBraek2
                        listOfNames = []
                        for i in range(0,len(originalTextBraek2)):
                            text = originalTextBraek2[i].split('(')
                            print len(text)
                            acctualText = str(text[0])
                            print len(acctualText)
                            acctualText = str(acctualText)
                            print acctualText
                            lstripText = acctualText.lstrip()
                            print str(lstripText)
                            rstripText = lstripText.rstrip()
                            print str(rstripText)
                            listOfNames.append(rstripText)
                        print "list of names after break2"
                        print listOfNames
                        for iCounterValue in listOfNames:
                            print iCounterValue
                            iCounterValue = str(iCounterValue)
                            print "A7 - L1"
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${list.common.searchFilterTab}"))
                            print "A7 - L2"
                            print "iCounterValue : " +str(iCounterValue)
                            self.select_list_option("//select[@id='saveSearchSelect']",iCounterValue)
                            #selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.common.searchFilterTab}",i))
                            print "A7 - L3"
                            self.select_custom_item_menu("Delete Search");
                            print "A7 - L4"
                            confmStatus = self.wait_for_element_visible("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]","15s")
                            print "A7 - L5"
                            if confmStatus == True:
                                print "A7 - C1"
                                selenium.click_element("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                print "A7 - C2"
                                self.wait_for_element_invisible("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]","15s")
                                print "Watch List deleted successfully"
                            else:
                                self.wait_for_element_present("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                selenium.click_element("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                print "Watch List deleted successfully"
                    except: 
                        print "Watch List which is associated with saved search is not Deleted"
                        return False
                    return True
                
                def select_list_option(self,locatorxpath,listVal,timeout=None):
                    """This keyword will select the dropdown value and check the selection status also but locator shoud be xpath"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #locatorxpath = "//select[@id='saveSearchSelect']"
                    if(timeout == None):
                        timeout = "30s"
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath,timeout)
                            selenium.select_from_list_by_label(locatorxpath,listVal)
                            bStatus = self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            print "bStatus using list_by_label "+str(bStatus)
                            time.sleep(4)
                            return True
                        except:
                            print "ValueError: Element locator "+str(locatorxpath) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                            try:
                                selenium.click_element(locatorxpath)
                                self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"']")
                                selenium.click_element(locatorxpath+"//option[text()='"+str(listVal)+"']")
                                bStatus = self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                                print "bStatus using click element "+str(bStatus)
                                time.sleep(4)
                                return bStatus
                            except:
                                print "selection of list item was failed"
                    return False

                             
                def create_watch_list(self,fieldName,dialogHeaderName,watchlistName,actualListOfValues,negationSymbol=''):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "CWL1"
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    print "CWL2"
                    for iCounter in range(0,3):
                        try:
                            list1=[]
                            print "CWL3"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            print "CWL4"
                            list1 = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            print "CWL5"
                            print str(list1)
                            print watchlistName in list1
                            if(watchlistName in list1):
                                print "CWL6 - DWL1"
                                desiredStatus = "False"
                                self.delete_watch_list(fieldName,dialogHeaderName,watchlistName,desiredStatus)
                            print "Select New.. from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            print "CWL7"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            print "CWL8"
                            dropdownSlectionStatus = self.wait_for_dropdown_selection("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            print "dropdownSlectionStatus: "+str(dropdownSlectionStatus)
                            if dropdownSlectionStatus==False:
                                selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            fieldStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div[contains(@id,'watchListDialogForm')]//input")
                            if fieldStatus == True:
                                print "CWL9 - Enter Watch List Name"
                                selenium.input_text("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div[contains(@id,'watchListDialogForm')]//input",watchlistName)
                                time.sleep(2)
                                try:
                                    selenium.capture_page_screenshot()
                                    print "screen captured"
                                except:
                                    print "Exception while capturing screenshot"
                                if negationSymbol=="-":
                                    print "CWL10 - Acct Text"
                                    negationValue = "-"+str(actualListOfValues)
                                    self.type_keys_into_textbox("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div[contains(@id,'watchListDialogForm')]//textarea",negationValue)
                                else:
                                    print "CWL10 - Rem Text"
                                    print "else part"
                                    self.type_keys_into_textbox("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div[contains(@id,'watchListDialogForm')]//textarea",actualListOfValues)
                                self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                saveButtonInvisibleStatus = self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "saveButtonInvisibleStatus: " +str(saveButtonInvisibleStatus)
                                if saveButtonInvisibleStatus == False:
                                    saveButtonInvisibleStatus = self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                    print "saveButtonInvisibleStatus: " +str(saveButtonInvisibleStatus)
                                print "Watch List Created success fully"
                                return True
                            else:
                                continue
                        except: 
                            print "Watch List creation failed"
                            continue
                    return False

                def create_watch_list_for_country_field(self,fieldName,dialogHeaderName,watchlistName,actualListOfValues,columnName):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "CWL1"
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    print "CWL2"
                    try:
                        list1=[]
                        print "CWL3"
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "CWL4"
                        list1 = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "CWL5"
                        print str(list1)
                        print watchlistName in list1
                        if(watchlistName in list1):
                            print "CWL6 - DWL1"
                            self.delete_watch_list(fieldName,dialogHeaderName,watchlistName)

                        print "Select New.. from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                        print "CWL7"
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                        print "CWL8"
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div//input")
                        print "CWL9"
                        selenium.input_text("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div//input",watchlistName)
                        print "CWL10"
                        fieldStatus = self.wait_for_element_visible("//table[@id='watchListDialogForm:wlPickList']")
                        print fieldStatus
                        print "CWL11"
                        if fieldStatus == True:
                            print "CWL12"
                            operationStatus = "copy"
                            
                            self.copy_or_remove_the_countries_from_selection_box(actualListOfValues,operationStatus)
                            print "CWL13"
                            self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                            selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                            self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                            print "Country Watch List Created success fully"
                        else:
                            return False
                    except: 
                        print " Country Watch List not Created"
                        return False
                    return True

                def copy_or_remove_the_countries_from_selection_box(self,listOfMoveableElements,operationStatus):
                    """It Will Copy the list of countries to one box to another  while selecting copy and for Remove it will remove from list"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')

                    try:
                        print "CWL8"
                        operationStatus = operationStatus.lower()
                        for cValue in listOfMoveableElements:
                            print "CWL8"
                            if (operationStatus.lower() == 'copy'):
                                print "CWL8CC"
                                self.wait_for_element_visible("//div[@id='watchListDialogForm:wlPickListheaderBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                selenium.click_element("//div[@id='watchListDialogForm:wlPickListheaderBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                self.wait_for_element_visible("//div[contains(@class,'rich-picklist-control-copy')]//div[@class='rich-list-picklist-button-content' and contains(text(),'Copy')]")
                                selenium.click_element("//div[contains(@class,'rich-picklist-control-copy')]//div[@class='rich-list-picklist-button-content' and contains(text(),'Copy')]")
                                bStatus = self.wait_for_element_present("//div[@id='watchListDialogForm:wlPickListtlheaderBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                if bStatus == True:
                                    time.sleep(2)
                                    print "Countriy Copied properly"
                                else:
                                    print "Country not copied properly"
                                    return False
                            else:
                                print "CWLRR"
                                self.wait_for_element_present("//div[@id='watchListEditDialogForm:ofacPickListtlcontentBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                self.wait_and_click_element("//div[@id='watchListEditDialogForm:ofacPickListtlcontentBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                self.wait_for_element_visible("//div[contains(@class,'rich-picklist-control-remove')]//div[@class='rich-list-picklist-button-content' and contains(text(),'Remove')]")
                                self.wait_and_click_element("//div[contains(@class,'rich-picklist-control-remove')]//div[@class='rich-list-picklist-button-content' and contains(text(),'Remove')]")
                                bStatus = self.wait_for_element_present("//div[@id='watchListEditDialogForm:ofacPickListcontentBox']//tr//td[contains(text(),'"+str(cValue)+"')]")
                                print "bStatus: " +str(bStatus)
                                if bStatus == True:
                                    print "Countriy Removed properly"
                                else:
                                    print "Country not Removed properly"
                                    return False
                    except:
                        print " Country Value not Copy/Removed properly"
                        return False
                    return True

                def edit_watch_list(self,fieldName,dialogHeaderName,editDialogHeaderName,watchlistName,actualListOfValues):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "EWL1"
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    print "EWL2"
                    try:
                        list1=[]
                        print "EWL3"
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "EWL4"
                        list1 = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "EWL5"
                        print str(list1)
                        print watchlistName in list1
                        if(watchlistName in list1):
                            print "Select watchlistName from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            print "EWL7"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                            print "EWL8"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Edit')]")
                            selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Edit')]")
                            time.sleep(6)
                            print "EWL9"
                            print "edihrearderName: " +str(editDialogHeaderName)
                            
                            editStatus = self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]","5s")
                            print "EWL9-b"
                            print editStatus
                            if editStatus == True:
                                print "EWL10 - Enter Watch List Values"
                                time.sleep(4)
                                self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea")
                                print "EWL11"
                                self.clear_text("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea")
                                self.type_keys_into_textbox("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea",actualListOfValues)
                                print "EWL12"
                                self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL13"
                                selenium.click_element("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL14"
                                self.wait_for_element_not_present("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL15"
                                time.sleep(4)
                                selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                                print "EWL16"
                                self.wait_for_element_not_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                                print "Watch List Edited success fully"
                    except: 
                        print "Watch List not Edited"
                        return False
                    return True

                def delete_watch_list(self,fieldName,dialogHeaderName,watchlistName,desiredWatchListStatus=False):
                    """Delete Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if str(desiredWatchListStatus) == "True":
                        print "Enter in to block"
                        self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    try:
                        print "Select watchlistName for deletion from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                        print "1"
                        selectedValue = selenium.get_selected_list_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print str(selectedValue)
                        print str(watchlistName)
                        print "2"
                        if selectedValue==watchlistName:
                            print "3"
                            fieldStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                            print str(fieldStatus)
                            if fieldStatus == True:
                                print "4"
                                selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                                print "5"
                                confmStatus = self.wait_for_element_visible("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]","15s")
                                if confmStatus == True:
                                    print "5A"
                                    selenium.click_element("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                    self.wait_for_element_invisible("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                else:
                                   print "5B"
                                   self.delete_watch_list_which_is_associated_with_saved_search(fieldName,dialogHeaderName,watchlistName)
                                   print "5B - 6"
                                   self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                                   print "5B - 7"
                                   self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                                   selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                                   print "5B - 8"
                                   fieldStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                                   if fieldStatus == True:
                                       print "5B - 9"
                                       selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                                       self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Delete')]")
                                       print "5B - 10"
                                       confmStatus = self.wait_for_element_present("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                       selenium.click_element("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                       print "5B - 11"
                                       self.wait_for_element_invisible("//table[@id='actionConfirmDialogContentTable']//a[contains(text(),'Ok')]")
                                       print "Watch List deleted successfully"

                    except:
                        print "Watch List not Deleted"
                        return False
                    return True


                def select_name_from_watchlist(self,fieldName,dialogHeaderName,watchlistName,desiredWatchListResetClickStatus=''):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = self.click_on_desired_watch_list(fieldName,dialogHeaderName,desiredWatchListResetClickStatus)
                    if bStatus == False:
                        print "Click on Desired watchlist failed"
                        return False
                    for iCounter in range(1,5):
                        try:
                            print "Select desired Watch List Name from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            dropDownStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                            return True
                        except:
                            print "Watch List Not Selected"
                    return False


                def wait_for_show_results_compilation(self):
                    """ It will upto serarching complited status"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iIndex in range(1,10):
                        try:
                            time.sleep(2)
                            selenium.wait_until_page_contains_element("//div[@id='subMainForm:cmdStatusWithCtlDialog']/parent::span[@id='cmdStatusWithCtl.start']")
                            attval = selenium.get_element_attribute("//div[@id='subMainForm:cmdStatusWithCtlDialog']/parent::span[@id='cmdStatusWithCtl.start']@style")
                            print "attval: "+ str(attval)
                            if attval.find("display: none")>=0:
                                return True
                        except:
                            print "exception in wait_for_results_status keyword"

                def click_on_show_results(self,expectedLocator=None):
                    """ It will click on Show Results button then wait for the serarching compilation status"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        bStatus = self.wait_and_click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "bStatus="+str(bStatus)
                        if bStatus==True:
                            print "show results clicked successfully"
                            if expectedLocator==None:
                                for iCnt in range(1,1000):
                                    searchingStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${headers.alerts.showresults.searchingdialog}"),"5s")
                                    print "searchingStatus: "+str(searchingStatus)
                                    if searchingStatus == False:
                                        break
                                self.wait_for_search_is_running_in_background_alert_message()
                                noDataStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${label.common.No matching data found}"),"5s")
                                print "No matching data found label Status: "+str(noDataStatus)
                                if bStatus==noDataStatus:
                                    print ("Table is displayed No matching data found label")
                                    return False
                                else:
                                    print "Table is displayed some records"
                            else:
                                print "check expectedLocator "+ str(expectedLocator)
                                bStatus = self.wait_for_element_visible(expectedLocator)
                                return bStatus
                        else:
                            print "show results not clicked"
                    except:
                        print "Got exception"
                        return False
                    return True


                def select_list_option(self,locatorxpath,listVal,timeout=None):
                    """This keyword will select the dropdown value and check the selection status also but locator shoud be xpath"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #locatorxpath = "//select[@id='saveSearchSelect']"
                    if(timeout == None):
                        timeout = "30s"
                    for iCounter in range(1,3):
                        print "iCounter: "+str(iCounter)
                        try:
                            selenium.wait_until_page_contains_element(locatorxpath,timeout)
                            selenium.select_from_list_by_label(locatorxpath,listVal)
                            bStatus = self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                            print "bStatus using list_by_label "+str(bStatus)
                            time.sleep(2)
                            return True
                        except:
                            print "ValueError: Element locator "+str(locatorxpath) +" did not visible within "+str(timeout) +" time out"
                            print "locator: "+str(locatorxpath)
                            try:
                                selenium.click_element(locatorxpath)
                                self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"']")
                                selenium.click_element(locatorxpath+"//option[text()='"+str(listVal)+"']")
                                bStatus = self.wait_for_element_visible(locatorxpath+"//option[text()='"+str(listVal)+"' and @selected='selected']",timeout)
                                print "bStatus using click element "+str(bStatus)
                                time.sleep(2)
                                return bStatus
                            except:
                                print "selection of list item was failed"
                    return False


                def wait_for_element_based_on_attribute_value(self,locatorxpath,attName,expattval):
                    """This keyword will select the dropdown value and check the selection status also but locator shoud be xpath"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "expattval:"+str(expattval)
                    for iCounter in range(1,10):
                        print "iCounter: "+str(iCounter)
                        attVal = self.get_element_attribute_value(locatorxpath+'@'+str(attName))
                        if (str(attVal).lower()).find(str(expattval).lower())>=0:
                            return True
                        else:
                            time.sleep(2)
                    return False
                  
                def multiple_cases_creation(self,rowCount):
                    rowCount = int(rowCount)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selectStatus = self.wait_for_element_visible("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table/tbody/tr/td[4]//div/div[contains(@class,'Selected')]")
                    imageStatus = self.wait_for_element_visible("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div","10s")
                    print "imageStatus:"+str(imageStatus)
                    if imageStatus != True:
                       for iCount in range(1,5):
                          selenium.reload_page()
                          status = self.wait_for_element_visible("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div","30s")
                          if status == True:
                             break                       
                    for icounter in range(1,rowCount+1):
                        selenium.click_element("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table/tbody/tr/td[4]//div/div[contains(@class,'Selected')]")
                        self.wait_for_element_visible("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div","30s")
                        riskLevel = self.get_element_attribute_value("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div@style")
                        status = self.string_should_contain(str(riskLevel),"-20px")
                        print "number of records reading done"+str(icounter)
                        print "image status:"+str(status)
                        if status != True and icounter == rowCount:
                           raise AssertionError("There are no group items to create cases")
                        if status == True:
                            listValues = self.get_table_risk_levels_and_return_caseIds()
                            print "List values"+str(listValues)
                            return listValues
                            break   
                        else:
                           try:
                              self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_down']","10s")
                              self.press_down_key("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_down']")
                           except:
                              print "exception raised"
                              self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_down']","10s")
                              self.press_down_key("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_down']")
                              
                def get_session_count_from_table(self,page):
                    """Returns the count of rows in table by reading label of particulare page """
                    print "SC1"
                    sessionNumber = self.get_text("//div[@class='sessionCounter']")
                    print "SC2"
                    if(page.lower()=='alerts' or page.lower()=='fraudmatch'):
                        print "SC3"
                        sessionNumber = sessionNumber.split(' ')
                        if sessionNumber[0].find('+'):
                            sessionNumberWith = sessionNumber[0].replace('+','')
                            finalSessionCount = str(sessionNumberWith)
                        else:
                            finalSessionCount = str(sessionNumber[0])
                    elif(page.lower()=='managesearch' or page.lower()=='cases' or page.lower()=='admin'):
                        sessionNumber = sessionNumber.split(':')
                        if sessionNumber[1].find('+'):
                            sessionNumberWith = sessionNumber[1].replace('+','')
                            finalSessionCount = str(sessionNumberWith)
                        else:
                            finalSessionCount = str(sessionNumber[1])
                    return finalSessionCount
                
                def validate_watch_list_results_with_search_citeria(self,fieldName,dialogHeaderName,name,values,ActualListOfValues,columnName,NegationSymbol=''):
                    """Click on Desired watch list and i will select the desired name snd hits the show results button and
                        verify the results from search results table with search criteria """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    try:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    except:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    listOfValues = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    if name not in listOfValues:
                        print "Error:" +str(name)+ "in Watch List Dropdown is not Saved."
                        raise AssertionError("Error:" +str(name)+ "in Watch List Dropdown is not Saved.")
                    selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",name)
                    self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    if fieldName== "Account":
                        self.wait_for_element_visible("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element(BuiltIn().get_variable_value("${link.adminUsers.showResults}"))
                    else:
                        self.wait_for_element_visible("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        selenium.click_element("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        valueInField = selenium.get_element_attribute("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input@value")
                        dict = {} 
                        dict[str(fieldName)] = str(valueInField)
                        self.enter_and_validate_advanced_search_fields(dict)
                    locator1 = "//a[@title='Account Detail']"
                    locator2 = BuiltIn().get_variable_value("${label.alerts.noMatchingDataFound}")
                    try:
                        self.any_one_element_should_be_visible(locator1,locator2)
                    except:
                        print "Error in this keyword"
                    pageName = 'alerts'
                    pageName = str(pageName)
                    rowCount = self.get_session_count_from_table(pageName)
                    print "row count "+str(rowCount)
                    listOfDesiredColumnValues = []
                    listOfDesiredColumnValues = self.get_table_values_into_list_by_down_arrow(BuiltIn().get_variable_value("${table.alerts.matchingRows}"),BuiltIn().get_variable_value("${table.alerts.searchResults.knob}"),BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"),columnName,False,rowCount)
                    if NegationSymbol=="-":
                        print "Neagtion Validation"
                        ActualListOfValues
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        if bstatus==True:
                            status=False
                        else:
                            status=True
                      
                    else:
                        print " Validation"
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        status=bstatus
                    combindsStatusList=[]
                    combindsStatusList.append(rowCount)
                    combindsStatusList.append(status)
                    return combindsStatusList

        
                def sub_list_comparision(self,mainList,subList):
                    """ It will return the true if liats  """
                    colt = BuiltIn().get_library_instance('Collections')
                    bStatus = False
                    print "mainList"
                    print mainList
                    print "subList"
                    print subList
                    try:
                        colt.list_should_contain_sub_list(mainList,subList)
                        bStatus = True
                    except:
                        bStatus = False
                    return bStatus

       

                def validate_previous_search_text_for_watch_list(self,locator,expectedText):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    status = False
                    text =''
                    for iCounter in range(1,10):
                        try:                        
                            selenium.click_element(BuiltIn().get_variable_value("${list.reports.riskdropdown}"))
                            self.wait_for_element_visible("${list.accounts.previoussearches.dropdownitem}","4s")
                            hoverLocator = BuiltIn().get_variable_value("${list.accounts.previoussearches.dropdownitem}")
                            selenium.mouse_over(hoverLocator+"/div")
                            text = self.get_text(locator)
                            print str(text)
                            status = self.string_should_contain(text,expectedText)
                            print str(status)
                            if (len(text) and status==True):
                                 break
                        except:
                            print "Unable to Get Text to this iteration"
                    combindsStatusList=[]
                    combindsStatusList.append(status)
                    combindsStatusList.append(text)
                    return combindsStatusList
                def manage_searches_for_selected_record(self,columnNumberCreatedBy,rowCount,expectedName ='',columnNumberVisibility = '',visibiltyName ='',order ='',columnNameForSort=''):
                    """  """
                    rowCount = int(rowCount)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        time.sleep(2)
                        selenium.reload_page()
                        self.wait_for_please_wait_option()
                    except:
                        print "Got exception"
                        self.wait_for_please_wait_option()
                    if order != '' and columnNameForSort == '':
                        sortingStatus = self.click_on_ascend_or_descend_arrow("//table[@class='ajs_tb_table']","Last modified (ET)",str(order))
                        print "sortingStatus: "+str(sortingStatus)
                    elif order == '' and columnNameForSort == '':
                        sortingStatus = self.click_on_ascend_or_descend_arrow("//table[@class='ajs_tb_table']","Last modified (ET)","descend")
                        print "sortingStatus: "+str(sortingStatus)
                    elif order == '' and columnNameForSort != '':
                        sortingStatus = self.click_on_ascend_or_descend_arrow("//table[@class='ajs_tb_table']",str(columnNameForSort),"descend")
                        print "sortingStatus: "+str(sortingStatus)
                    elif order != '' and columnNameForSort != '':
                        sortingStatus = self.click_on_ascend_or_descend_arrow("//table[@class='ajs_tb_table']",str(columnNameForSort),str(order))
                        print "sortingStatus: "+str(sortingStatus)
                    visibleRecordsCount01 = selenium.get_matching_xpath_count("//table[@class='ajs_tb_table']/tbody/tr/td[contains(@id,'SavedSearchTable')]/div/div")
                    print "visibleRecordsCount01: "+str(visibleRecordsCount01)
                    for iCount in range(0,rowCount+1):
                        visibleRecordsCount02 = selenium.get_matching_xpath_count("//table[@class='ajs_tb_table']/tbody/tr/td[contains(@id,'SavedSearchTable')]/div/div")
                        print "visibleRecordsCount02: "+str(visibleRecordsCount02)
                        if int(visibleRecordsCount01)!=int(visibleRecordsCount02):
                            print "Records count was decreased due to Firfox issue"
                        elementStatus = self.wait_for_element_visible("//div[contains(@id,'C"+str(columnNumberCreatedBy)+"') and contains(@class,'Selected')]//span","5s")
                        if elementStatus == True:                                                          
                           self.wait_and_click_element("//div[contains(@id,'C"+str(columnNumberCreatedBy)+"') and contains(@class,'Selected')]//span")
                           expectedNameText = self.get_text("//div[contains(@id,'C"+str(columnNumberCreatedBy)+"') and contains(@class,'Selected')]//span")
                           if str(columnNumberVisibility) != '':
                               print 'column Number'
                               visibilityNameText = self.get_text("//div[contains(@id,'C"+str(columnNumberVisibility)+"') and contains(@class,'Selected')]//span")
                           if str(expectedName) != '':
                               print 'expected name'
                               logedInUserStatus = self.string_should_contain(str(expectedNameText),str(expectedName))
                               print 'Loged In User Status:'+str(logedInUserStatus)
                           if str(visibiltyName) != '':
                               print 'visibility name'
                               searchTextStatus = self.string_should_contain(str(visibilityNameText),str(visibiltyName))
                               print 'Search Text Status:'+str(searchTextStatus)
                           if str(expectedName) and str(visibiltyName) != '':
                               if logedInUserStatus and searchTextStatus == True:
                                   print 'Both are not none'
                                   break
                               else:
                                  if logedInUserStatus and searchTextStatus != True and rowCount == iCount:
                                     print 'All records reading done'
                           if str(expectedName) != '' and str(visibiltyName) == '':
                               if logedInUserStatus == True:
                                   print 'loged in user= '+ str(expectedName)
                                   break
                               else:
                                  if logedInUserStatus != True and rowCount == iCount:
                                     print 'No record found'
                           self.press_down_key("//div[contains(@id,'ajs_T_SavedSearchTable_tSavedSearches_F_SavedSearchTable_tSavedSearches_bar_container')]")
                        else:
                            self.searching_for_specific_record_until_success(columnNumberCreatedBy,rowCount,expectedName ='',columnNumberVisibility = '',visibiltyName ='')

                def click_on_ascend_or_descend_arrow(self,tableLocator,colName,order='ascend'):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bstatus = self.wait_for_element_visible(tableLocator)
                    if bstatus==False:
                        return False
                    if str(type(colName)).find("str"):
                        colNumber = self.table_get_column_no(tableLocator,colName)
                    else:
                        colNumber = str(colName)
                    headerLocator = tableLocator+"/tbody/tr/td["+str(colNumber)+"]/div/div"
                    bstatus = self.wait_for_element_visible(headerLocator)
                    if bstatus==False:
                        return False
                    arrowLocator = headerLocator+"/div[2]"
                    for iCount in range(5):
                        try:
                            selenium.click_element(headerLocator)
                            time.sleep(2)
                            if self.wait_for_element_visible(arrowLocator,"5s")==True:
                                print "arrow status True"
                                imagestyle = self.get_element_attribute_value(arrowLocator+"@style")
                                print imagestyle
                                if order.lower()=='ascend':
                                    status = self.string_should_contain(imagestyle,"images/a1.gif")
                                    if status==True:
                                        return True
                                elif order.lower()=='descend':
                                    status = self.string_should_contain(imagestyle,"images/a2.gif")
                                    if status==True:
                                        return True    
                        except:
                            print("Sort order icons are not displayed")
                    return False

                def searching_for_specific_record_until_success(self,columnNumberCreatedBy,rowCount,expectedName ='',columnNumberVisibility = '',visibiltyName =''):
                   selenium = BuiltIn().get_library_instance('Selenium2Library')
                   self.wait_for_element_visible("//a[contains(text(),'Show Results')]")
                   selenium.click_element("//a[contains(text(),'Show Results')]")
                   time.sleep(5)
                   self.manage_searches_for_selected_record(columnNumberCreatedBy,rowCount,expectedName ='',columnNumberVisibility = '',visibiltyName ='')

                def open_context_menu_and_mouseover_on_menu_item(self,headerlocator,itemName='None'):
                    """open context menu for the graph and mouse over on the element"""
                    headerlocator = str(headerlocator)

                    if itemName == 'None':
                        itemlocator = "//span[contains(text(),'Line Scatter')]"
                    else:
                        itemlocator = "//span[contains(text(),'"+str(itemName)+"')]"
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(1,5):
                        try:
                            headerStatus = self.wait_for_element_visible(headerlocator)
                            if headerStatus ==True:
                                selenium.mouse_over(headerlocator)
                                selenium.open_context_menu(headerlocator)
                                selenium.mouse_over(itemlocator)
                                time.sleep(2)
                                return True
                            else:
                                time.sleep(4)
                        except:
                            print "context menu item not read successfully"
                    return False

                def do_customize_columns(self,headerlocator=None):
                    """customize the columns"""
                    if headerlocator == None:
                        headerlocator = "//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_th_R0C8']/div/div[1]"
                    headerlocator = str(headerlocator)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        for iCounter in range(1,5):
                            mStatus = self.wait_for_element_visible(headerlocator)
                            if mStatus ==True:
                                selenium.mouse_over(headerlocator)
                                selenium.open_context_menu(headerlocator)
                                self.wait_for_element_visible("//span[contains(text(),'Customize columns')]")
                                selenium.mouse_over("//span[contains(text(),'Customize columns')]")
                                selenium.click_element("//span[contains(text(),'Customize columns')]")
                                break
                            else:
                                time.sleep(4)

                    except:
                        print "customize columns coloumn not succeded"
                        return False
                    return True


                def wait_for_new_window(self,expectedCount=2,timeout=None):
                    """Select a window by window title"""
                    if (timeout==None):
                        timeout=5                    
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icount in range(10):
                        try:
                            windows=selenium.get_window_titles()
                            count=len(windows)
                            if(int(count)==int(expectedCount)):
                                print "window names are"
                                print windows
                                return True
                            else:
                                print "expected window not opened"
                                time.sleep(timeout)
                        except:
                            print "exception occured"
                    return False
                
                def get_value_of_locator(self,locator):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCount in range(10):
                        try:
                            print "iteration count is "+str(iCount)
                            value=selenium.get_value(locator)
                            if(len(value)!=0):
                                return value
                        except:
                            print "Exception occured"

                def drag_and_drop_action(self, source, target):
                    """Drags element identified with `source` which is a locator.
                    Element can be moved on top of another element with `target`argument.
                    `target` is a locator of the element where the dragged object is dropped.
                    Examples:
                        | Drag And Drop | elem1 | elem2 | # Move elem1 over elem2. |"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')   
                    try:
                        src_elem = selenium._element_find(source,True,True)
                        trg_elem =  selenium._element_find(target,True,True)
                        ActionChains(selenium._current_browser()).drag_and_drop(src_elem, trg_elem).perform()
                    except:
                        print "exception occured"
                        src_elem = selenium._element_find(source,True,True)
                        trg_elem =  selenium._element_find(target,True,True)
                        ActionChains(selenium._current_browser()).drag_and_drop(src_elem, trg_elem).perform()
                            


                def do_search_in_the_reports_page(self,dictVar,hideFilters=True,expectedLocator=None,reset=True):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    bStatus = self.do_basic_search(dictVar)
                    print "bStatus: "+str(bStatus)
                    if bStatus==False:
                        return False
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    print "resetStatus: "+str(resetStatus)
                    if reset==True:
                        self.wait_and_click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "ipaddress":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.IPAddress}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "sessionrange":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.SessionRange}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "accessmode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.accessmode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "country":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.country}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "osbrowser":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.osbrowser}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "iptype":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "state":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.state}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "useragent":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"))
                                    if fieldStatus == True:
                                        print "${textbox.advanceSearch.useragent}: "+str(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"))
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.useragent}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "riskfactor":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.riskfactor}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "provider":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.provider}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "city":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.city}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "activity":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.activity}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)                                                                
                        except:
                            print "entering search details failed"
                        showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "showResultsStatus: " +str(showResultsStatus)
                        if showResultsStatus == True:
                            selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            time.sleep(5)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${headers.alerts.showresults.searchingdialog}"),"5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                        else:
                            print "check expectedLocator "+ str(expectedLocator)
                            self.wait_for_element_visible(expectedLocator)
                        searchStatus = self.check_search_checkbox(dictVar)
                        print "searchStatus: "+str(searchStatus)
                        if searchStatus == True:
                            showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            print "showResultsStatus: " +str(showResultsStatus)
                            if showResultsStatus == True:
                                time.sleep(2)
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                if expectedLocator==None:
                                    for iCnt in range(1,1000):
                                        searchingStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${headers.alerts.showresults.searchingdialog}"),"5s")
                                        print "searchingStatus: "+str(searchingStatus)
                                        if searchingStatus == False:
                                            break
                                    self.wait_for_search_is_running_in_background_alert_message()
                                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                                else:
                                    print "check expectedLocator "+ str(expectedLocator)
                                    self.wait_for_element_visible(expectedLocator)
                        else:
                            break;
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']","5s") == True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                            print "hiding Filters section done"
                        except:
                            print "hiding Filters failed"
                    return True

                def get_table_cell_value_using_java_script(self, locator,columnName):
                    """Returns the cell value of table displayed under 'columnName' from the table located at 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        dataType = str(type(columnName))
                        print "dataType:"+str(dataType)
                        try:
                            columnName = int(columnName)
                            keyColNum = str(columnName)
                        except:
                            print "data type not int"
                            keyColNum = self._table_get_column_no(locator,columnName)
                        print "keyColNum:" +str(keyColNum)
                        if int(keyColNum)==0:
                            print "Table Column name "+str(columnName) + " is not displayed"
                        elementId = self.get_element_attribute_value(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[contains(@class,"Selected")]@id')
                        elementText = selenium.execute_javascript('return document.getElementById("'+str(elementId)+'").getElementsByTagName("div")[0].textContent')
                        return elementText
                        print "elementText:" + str(elementText)
                    except:
                        print "Got exception"
                        raise AssertionError("Exception: Unable to read cell value using java scripts")
                def get_table_risk_levels_and_return_caseIds(self):
                  selenium = BuiltIn().get_library_instance("Selenium2Library")
                  account = self.get_text("//div[contains(@id,'C3') and contains(@class,'Selected')]/div")
                  print "account:"+str(account)
                  account1 = account.split('(')
                  accountName = account1[0]
                  print "AccountName :"+str(accountName)
                  accountName1 = account.split(' ')
                  print "AccountName after split with empty:"+str(accountName1)
                  account2 = account1[1].split(')')
                  print "Risk Number:"+str(account2)
                  riskNumber = int(account2[0])
                  accountFieldStatus = self.wait_for_element_visible("//input[@id='accountFilter']","10s")
                  count = 0
                  if accountFieldStatus == True:
                     BuiltIn().run_keyword("inputtext","//input[@id='accountFilter']",str(accountName.rstrip()))
                     time.sleep(5)
                     count1 = self.get_count_for_caseopen_and_case_closed()
                     count = count1
                     print "Main Method"
                     self.wait_and_click_element("//a[@title='Case Open']")
                     self.wait_and_click_element("//a[@title='Case Closed']")
                     self.wait_and_click_element("//a[@title='Not Viewed']")
                  self.wait_and_click_element("mainForm:showResults")
                  self.wait_for_element_visible("//a[@title='Fraud Match']","20s")
                  noMatchingStatus = self.wait_for_element_visible("//div[@id='tAlerts']//div[contains(text(),' No matching data found')]","5s")
                  groupStatus = self.wait_for_element_visible("//label[contains(@id,'groupingControlLabel')and text()='Group']","5s")
                  if groupStatus == True:
                     selenium.click_element("//label[contains(@id,'groupingControlLabel')and text()='Group']")
                     imageStatus = self.wait_for_element_visible("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div","10s")
                     self.wait_and_click_element("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div")
                     print "imageStatus:"+str(imageStatus)
                     if imageStatus != True:
                       for iCount in range(1,5):
                          selenium.reload_page()
                          status = self.wait_for_element_visible("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div","30s")
                          if status == True:
                             break                           
                  else:
                     for iCount in range(1,5):
                        print "clicking on blue image button"
                        self.wait_and_click_element("//div[contains(@class,'Selected')]/div/table/tbody/tr/td/div")
                        if(BuiltIn().get_variable_value("${BROWSER}") != "ie"):
                            print "Enter in to if block"
                            expandStatus = self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_R0C0' and contains(@class,'Selected')]//div[contains(@style,'no-repeat -0px')]","10s")
                        else:
                            print "Enter in to else block"
                            time.sleep(5)
                            #expandStatus = self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_R0C0' and contains(@class,'Selected')]//div[contains(@style,'background: url("+"'../images/icons.gif'"+") no-repeat 0px')]","10s")
                            expandStatus = True
                        print "expandStatus:"+str(expandStatus)
                        if expandStatus == True:
                           break
                  sessionCount = self.get_text("//div[@class='sessionCounter']")
                  sessionCount1 = sessionCount.split(' ')
                  riskCount = sessionCount1[0]
                  status = self.string_should_contain(riskCount,"+")
                  if status == True:
                     riskCount1 = riskCount.split('+')
                     finalRiskCount = int(riskCount1[1])
                  else:
                     finalRiskCount = int(riskCount)
                  print "Final Risk Count:"+str(finalRiskCount)
                  for icount in range(0,2):
                     text = BuiltIn().run_keyword("Cases.Get Tooltip Text","//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_col_R0C1']/div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_R"+str(icount)+"C1' and contains(@class,'Selected')]")
                     print "status:"+str(text)
                     notViewedStatus = self.string_should_contain(text,"Not Viewed")
                     print "notViewedStatus"+str(notViewedStatus)
                     if notViewedStatus != True:
                        count = count + 1
                        self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","5s")
                        self.press_down_key("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']")
                     else:
                        caseId = self.case_creation_from_main_window(accountName)
                        count = count + 1
                        if icount == 1:
                           return caseId,count

                def verify_watchlist_status(self,timeout="2s"):
                    """Returns the cell value of table displayed under 'columnName' from the table located at 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    locator = "//div[@id='watchListDialog' and contains(@style,'display: none')]//div[@id='watchListDialogHeader']"
                    time.sleep(3)
                    for iCnt in range(0,20):
                        try:
                            selenium.wait_until_page_contains_element(locator,timeout)
                            print "watchlist not opened"
                        except:
                            print "watchlist opened"
                            return True
                    return False

                def get_application_current_version(self):
                    """Returns the cell value of table displayed under 'columnName' from the table located at 'locator'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    currentVersion = ""
                    try:
                        self.wait_for_element_visible("//img[@alt='Show Menu']")
                        selenium.mouse_over("//img[@alt='Show Menu']")
                        self.wait_for_element_visible("//span[contains(@id,'globalBanner') and text()='About']")
                        selenium.click_element("//span[contains(@id,'globalBanner') and text()='About']")
                        self.wait_for_new_window(2)
                        selenium.select_window("FraudMAP - About")
                        currentVersion = self.get_text("//p[contains(text(),'Version:')]")
                        print "version details "+str(currentVersion)
                        if currentVersion.find("Version:")>=0:
                            currentVersion = currentVersion.replace("Version:","")
                        currentVersion = currentVersion.strip()
                        print "currentVersion: "+str(currentVersion)
                        return currentVersion
                    except:
                        print "got exception"
                        return currentVersion

                def mouse_down_and_mouse_up(self,locator,timeout="10s"):
                    """It will perform mouse down and up on specified element based  locator """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCounter in range(0,3):
                        print "iCounter Val: "+str(iCounter)
                        try:
                           bStatus = self.wait_for_element_visible(locator,timeout)
                           if bStatus==True:
                               selenium.mouse_down(locator)
                               selenium.mouse_up(locator)
                               return True
                           else:
                               print "Required element not visble"
                               continue
                        except:
                            print "got exception while doing mouse actions"
                            continue
                    return False


                def select_shared_search_item_from_dropdown(self,itemName=None):
                    """It will select required values or random Shared Search Item From Dropdown """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    BuiltIn().get_variable_value()
                    self.mouse_down_and_mouse_up(BuiltIn().get_variable_value("${list.reports.customDropDown}"))
                    listStatus = self.wait_and_click_element(BuiltIn().get_variable_value("${list.reports.customDropDown}"))
                    print "listStatus: "+str(listStatus)
                    
                def case_creation_from_main_window(self,accountName):
                  selenium = BuiltIn().get_library_instance("Selenium2Library")
                  self.wait_for_element_visible("//div[@id='createCaseButton']/a/img","10s")
                  selenium.mouse_over("//div[@id='createCaseButton']/a/img")
                  selenium.click_element("//div[@id='createCaseButton']/a/img")
                  time.sleep(5)
                  self.wait_for_new_window(2)
                  windowNames = selenium.get_window_names()
                  windowsLength = int(len(windowNames))
                  print "window names"+str(windowNames)
                  for iCount in range(0,windowsLength):
                     status = self.string_should_contain(windowNames[iCount],"acc")
                     if status == True:
                        selenium.select_window(windowNames[iCount])
                        break
                     if iCount == windowsLength -1 and status == False:
                        raise AssertionError("Desired Window is not opend")
                  accountDetailsName = self.get_text("accountExternalInfoButton")
                  BuiltIn().should_contain(accountName,accountDetailsName,"Account Names are Mismatched")
                  currentTime = self.get_current_time()
                  self.wait_for_element_visible("//span[@class='caseDescription']//table//textarea","30s")
                  selenium.input_text("//span[@class='caseDescription']//table//textarea","created by offshore "+str(currentTime))
                  self.wait_and_click_element("//a[contains(text(),'Save')]")
                  self.wait_for_element_invisible("//a[contains(text(),'Save')]","5s")
                  self.wait_for_element_visible("//select[contains(@id,'caseList') and contains(@class,'inline')]//option","10s")
                  createCaseId = self.get_element_attribute_value("//select[contains(@id,'caseList') and contains(@class,'inline')]//option@value")
                  print "createCaseId:"+str(createCaseId)
                  selenium.select_window("FraudMAP - Main")
                  try:
                     print "Try block"
                     self.wait_for_element_visible("//div[contains(@id,'C3') and contains(@class,'Selected')]/div","10s")
                     selenium.mouse_over("//div[contains(@id,'C3') and contains(@class,'Selected')]/div")
                     self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","10s")
                     self.press_down_key("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']")
                  except:
                     print "Exception raised"
                     self.wait_for_element_visible("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","10s")
                     self.press_down_key("//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']")
                  return createCaseId
                
                def get_count_for_caseopen_and_case_closed(self):
                    print "get_count_for_caseopen_and_case_closed"
                    self.wait_and_click_element("//a[@title='Not Viewed']")
                    self.wait_and_click_element("//a[@title='Case Open']")
                    self.wait_and_click_element("//a[@title='Case Closed']")
                    self.wait_and_click_element("mainForm:showResults")
                    self.wait_for_element_visible("//div[@id='tAlerts']//div[contains(text(),' No matching data found')]","20s")
                    count = BuiltIn().run_keyword("fraudMatch.Get Table Rows Count In IE Browser")
                    Count = int(count)
                    print "Count:"+str(Count)
                    return Count

                def get_table_data_in_fraudMatch_page(self):
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    OperatingSystem = BuiltIn().get_library_instance('OperatingSystem')
                    autoit = BuiltIn().get_library_instance('AutoItLibrary')
                    try:
                        self.wait_and_click_element("//img[contains(@src,'fraudMatchAction')]")
                        time.sleep(3)
                        self.wait_for_new_window(2)
                        windowTitles=selenium.get_window_titles()
                        print windowTitles
                        for wName in windowTitles:
                            if 'Fraud Match' in wName:
                                self.select_window_by_title(wName)
                                time.sleep(3)
                                selenium.maximize_browser_window()
                                selenium.select_from_list_by_label("//select[@id='mainForm:dateFilter']","All Time")
                                self.select_risk_in_basic_search("Red")
                                self.wait_for_element_visible(BuiltIn().get_variable_value("${table.fraudMatch.matchingRows}"))
                                filters={'Activity':'ACH*','Risk Factor':'ACH*','Session Range':1,'City':'charlotte*'}
                                self.enter_and_validate_advanced_search_fields(filters,'False')
                                self.wait_for_element_visible(BuiltIn().get_variable_value("${label.alerts.selectedRecord}"))
                                self.rest_default_columns()
                                headers=self.get_table_columns_into_list(BuiltIn().get_variable_value("${table.fraudMatch.matchingRows}"))
                                totalrows=self.get_session_count_from_table('fraudmatch')
                                actuallist=[]
                                for header in headers:
                                    actuallist.append(header)
                                    status = self.string_should_contain(header,'Activity')
                                    statuss = self.string_should_contain(header,'Risk Factor')
                                    if status == True:
                                        values=self.get_table_values_into_list_by_down_arrow("//div[@id='tAlerts']/div[2]/table/tbody/tr/td/table","//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","//div[contains(@id,'ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_container')]",header,'False',totalrows,'True')
                                        self.match_result_values_to_pattern(values,'ACH*')
                                        actuallist.append(values)
                                    elif statuss == True:
                                        values=self.get_table_values_into_list_by_down_arrow("//div[@id='tAlerts']/div[2]/table/tbody/tr/td/table","//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","//div[contains(@id,'ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_container')]",header,'False',totalrows,'True')
                                        self.match_result_values_to_pattern(values,'ACH*')
                                        actuallist.append(values)
                                return actuallist
                    except:
                        print "exception occured"

                def get_table_all_column_values_into_list_by_down_arrow(self, locator,scrollbar_locator,parentLocator,columnName,unique='',totalrows='',useJavaScript=False):
                    """returns the list of values for each row values for all columns """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    keyColNum = self._table_get_column_no(locator,columnName)
                    time.sleep(2)
                    Counter = 0
                    if totalrows=='':
                        rowsCount=int(self.get_table_rows_count_by_scrolling(scrollbar_locator,parentLocator))
                    else:
                        rowsCount=totalrows
                    rowsCount=int(rowsCount)
                    
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    print "elements:"+str(elements)
                    if int(elements)==0:
                        raise AssertionError("the table rows are empty")
                    #rowValues=[]
                    valuesOfAllCols = []
                    iCounter=0
                    #for iValue in range(1,int(elements)-1):
                    iValue=1
                    time.sleep(2)
                    while(iValue<=int(elements)-2 and iValue<=rowsCount):
                        iValue=iValue+1
                        print "iValue: "+str(iValue)
                        if (iValue==2):
                            try:
                                self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div[2]')
                            except:
                                print "click elemet keyword got failed at table row"
                                selenium.capture_page_screenshot()
                        else:
                            try:
                                selenium.click_element(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                                selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            except:
                                print "mouse over keyword got failed at table row"
                                selenium.capture_page_screenshot()
                            try:
                                selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                                self.wait_for_please_wait_option()
                            except:
                                print "Arrow down failed at table row"
                                selenium.capture_page_screenshot()

                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValues=[]
                                colValues = selenium.get_matching_xpath_count(locator+'/tbody/tr/td')
                                print "colValues:"+str(colValues)
                                for ele in range(1,int(colValues)+1):
                                    rowValue=self.get_text(locator+'/tbody/tr/td['+str(ele)+']/div/div'+'['+str(iValue)+']')
                                    rowValues.append(rowValue)
                                    if ((rowValue == " ") or (rowValue == "")):
                                        print "removed"
                                        rowValues.remove(rowValue)
                                print "rowValues"
                                print rowValues
                                valuesOfAllCols.append(rowValues)
                        except:
                            print "got exception while reading row values"
                            selenium.capture_page_screenshot()
                        iCounter=iCounter+1
                    iValue=int(elements)-1
                    while(iCounter<rowsCount):
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            selenium.mouse_over(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']',True,True).send_keys(Keys.ARROW_DOWN)
                            self.wait_for_please_wait_option()
                        except:
                            selenium.capture_page_screenshot()
                        try:
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div'+'['+str(iValue)+']')
                            if useJavaScript==True:
                                rowValue = self.get_table_cell_value_using_java_script(locator,keyColNum)
                            else:
                                rowValues=[]
                                colValues = selenium.get_matching_xpath_count(locator+'/tbody/tr/td')
                                print "colValues:"+str(colValues)
                                for ele in range(1,int(colValues)+1):
                                    rowValue=self.get_text(locator+'/tbody/tr/td['+str(ele)+']/div/div'+'['+str(iValue)+']')
                                    rowValues.append(rowValue)
                                    if ((rowValue == " ") or (rowValue == "")):
                                        print "removed"
                                        rowValues.remove(rowValue)
                                print "rowValues"
                                print rowValues
                                valuesOfAllCols.append(rowValues)
                        except:
                            selenium.capture_page_screenshot()
                        iCounter=iCounter+1
                        if iCounter==rowsCount:
                            break
                    self.verify_table_read_all_rows(rowsCount,scrollbar_locator)
                    return valuesOfAllCols

                def export_displayed_session_records(self,filepath,number,menu,browser,downloadpath):
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    OperatingSystem = BuiltIn().get_library_instance('OperatingSystem')
                    autoit = BuiltIn().get_library_instance('AutoItLibrary')
                    if os.path.exists(filepath):
                        os.remove(filepath)
                    else:
                        print "file isnot exported before"
                    bStatus=self.wait_for_element_visible("//a[@title='Export']")
                    if bStatus==True:
                        self.wait_for_element_visible("//a[@title='Export']/img")
                        selenium.simulate("//a[@title='Export']/img",'click')
                        if menu.lower()=='cases':
                            self.wait_for_element_visible("//table[@id='exportCasesDialogContentTable']//table//table//input")
                            selenium.input_text("//table[@id='exportCasesDialogContentTable']//table//table//input","Export_Displayed_Session_File"+str(number))
                            time.sleep(3)
                            self.wait_and_click_element("//table[contains(@id,'exportTypeSelectFD')]/tbody/tr["+str(number)+"]//input[contains(@name,'exportTypeSelectFD')]")
                            bStatuss=self.wait_for_element_visible("//table[contains(@id,'exportTypeSelectFD')]/tbody/tr["+str(number)+"]//input[contains(@name,'exportTypeSelectFD') and contains(@checked,'checked')]")
                            if bStatuss==False:
                                if int(number)==1:
                                    self.wait_and_click_element("//label[contains(text(),'Export displayed cases')]")
                                else:
                                    self.wait_and_click_element("//label[contains(text(),'Export ALL recorded cases')]")
                            self.wait_for_element_visible("//table[@id='exportCasesDialogContentTable']//table//a[contains(text(),'Export')]")
                            self.wait_and_click_element("//table[@id='exportCasesDialogContentTable']//table//a[contains(text(),'Export')]")
                        else:
                            self.wait_for_element_visible("//table[@id='exportSessionsDialogContentTable']//table//table//input")
                            selenium.input_text("//table[@id='exportSessionsDialogContentTable']//table//table//input","Export_Displayed_Session_File"+str(number))
                            time.sleep(3)
                            self.wait_and_click_element("//table[contains(@id,'exportTypeSelectFD')]/tbody/tr["+str(number)+"]//input[contains(@name,'exportTypeSelectFD')]")
                            bStatuss=self.wait_for_element_visible("//table[contains(@id,'exportTypeSelectFD')]/tbody/tr["+str(number)+"]//input[contains(@name,'exportTypeSelectFD') and contains(@checked,'checked')]")
                            if bStatuss==False:
                                if int(number)==1:
                                    self.wait_and_click_element("//label[contains(text(),'Export displayed cases')]")
                                else:
                                    self.wait_and_click_element("//label[contains(text(),'Export ALL recorded cases')]")
                            self.wait_for_element_visible("//table[@id='exportSessionsDialogContentTable']//table//a[contains(text(),'Export')]")
                            self.wait_and_click_element("//table[@id='exportSessionsDialogContentTable']//table//a[contains(text(),'Export')]")
                        if browser.lower()=='ie':
                            time.sleep(10)
                            if os.path.exists(filepath):
                                return True
                            else:
                                actuallenght=OperatingSystem.count_files_in_directory(downloadpath)
                                for iCount in range(10):
                                    autoit.Send("!S")
                                    time.sleep(3)
                                    expectedlenght=OperatingSystem.count_files_in_directory(downloadpath)
                                    diff = expectedlenght - actuallenght
                                    if diff != 0:
                                        if os.path.exists(filepath):
                                            return True
                        for iCount in range(10):
                            if os.path.exists(filepath):
                                break
                            else:
                                time.sleep(5)
                        self.close_alert_message()
                        selenium.reload_page()
                        autoit.Send("F5")
      
                def get_column_names_in_fraudmatch(self,columncount):
                    """return the coulmn names in farudmatch page after scrolling"""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    actualHeaders = []
                    try:
                        for iCount in range(columncount):
                            columnName = self.get_text("//div[@id='tAlerts']//table/tbody/tr/td[${index}]/div/div")
                            actualHeaders.appand(columnName)
                    except:
                        print "got exception while reading column names in fraudmatch page"
                        selenium.capture_page_screenshot()
                    return actualHeaders

                def Mouse_Over_To_Get_Risk_Order_Values(self):
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    listOfImages = []
                    for icount in range(4):
                        self.mouse_over_on_element(BuiltIn().get_variable_value("${text.fraudmatch.selectedRecord.activity}"))
                        activityDataxpathCount = selenium.get_matching_xpath_count("//div[@id='ArdentEdge.Util.tooltipId_tc']/table/tbody/tr")
                        print "activityDataxpathCount: "+str(activityDataxpathCount)
                        if activityDataxpathCount==0:
                            continue
                        else:
                            break
                    
                    for jCount in range(int(activityDataxpathCount)):
                        for count in range(5):
                            selenium.mouse_over(BuiltIn().get_variable_value("${text.fraudmatch.selectedRecord.activity}"))
                            searchCriteriaEntered=self.get_element_attribute_value("//div[@id='ArdentEdge.Util.tooltipId_tc']/table/tbody/tr["+str((int(jCount)+1))+"]/td/span@style")
                            print "searchCriteriaEntered: "+str(searchCriteriaEntered)
                            if len(searchCriteriaEntered)==0:
                                continue
                            else:
                                break
                        list1 = searchCriteriaEntered.split("\"")
                        list2 = list1[1].split("_")
                        list3 = list2[2].split(".")
                        print "after split value is:"+str(list3[0])
                        listOfImages.append(list3[0])
                        print listOfImages
                    orderOfRisks = self.verify_activity_data_displayed_in_risk_order_or_not(listOfImages)
                    return orderOfRisks

                def Validate_the_Search_Results_for_Activities(self,columnDataToBeRead,search):
                    """Verifies the activity column contains activity filter values."""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    try:
                        sessionCount = self.get_session_count_from_table("fraudmatch")
                        self.wait_and_click_element(columnDataToBeRead)
                        for icount in range(int(sessionCount)):
                            selenium.mouse_over(columnDataToBeRead)
                            activities = self.get_activities_from_selected_record_on_fraudmatch_page()
                            self.press_down_key(columnDataToBeRead)
                            bStatus = self.validate_the_activities_of_the_selected_record(search,activities)
                            if bStatus!=True:
                                return False
                            self.press_down_key(columnDataToBeRead)
                        return bStatus
                    except:
                        print "got exception while validating the activity field"
                    
                def Advance_Filter_on_Fraud_Match_Page(self,advanceSearchValues,columnHeader,searchCriteriaEnteredInTheField):
                    """Verifies the time line values contains the corresponding filter values """
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    self.enter_and_validate_advanced_search_fields(advanceSearchValues,False)
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${table.alerts.fraudMatch.matchingTable}"))
                    sessionCount = self.get_session_count_from_table("fraudmatch")
                    print "sessionCount: "+str(sessionCount)
                    listOfValuesDisplayed = []
                    listOfValuesDisplayed = self.get_table_values_into_list_by_down_arrow("//div[@id='tAlerts']/div[2]/table/tbody/tr/td/table","//div[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_knob']","//div[contains(@id,'ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_bar_container')]",columnHeader,True,sessionCount)
                    print "listOfValuesDisplayed"
                    print listOfValuesDisplayed
                    searchCriteriaEntered=self.get_element_attribute_value(searchCriteriaEnteredInTheField)
                    print "searchCriteriaEntered: "+str(searchCriteriaEntered)
                    listOfSearchCriteriaEnteredItems = searchCriteriaEnteredInTheField.split(",")
                    for ele in listOfSearchCriteriaEnteredItems:
                        if ele in listOfValuesDisplayed:
                            continue
                        else:
                            return False
                            raise AssertionError('table values not having the entered search ctiteria values')
                    return True
                
                def Verify_Disabled_Items_on_Table_in_Fraud_Match(self,tableName,disableItem):
                    """Opens the context menu and Reads the Columns displayed after the column is disabled and verifies the column is not displayed."""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    dashBoard = BuiltIn().get_library_instance("Dashboard")
                    colt = BuiltIn().get_library_instance('Collections')
                    self.wait_and_click_element(BuiltIn().get_variable_value("${table.fraudMatch.moveableElement}"))
                    selenium.capture_page_screenshot()
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${table.alert.searchResults.columnHeaderEighthColumn}"))
                    selenium.open_context_menu(BuiltIn().get_variable_value("${table.alert.searchResults.columnHeaderEighthColumn}"))
                    self.wait_and_click_element(BuiltIn().get_variable_value("${list.contextMenu.enableAll}"))
                    self.do_customize_columns(BuiltIn().get_variable_value("${table.alert.searchResults.columnHeaderEighthColumn}"))
                    selenium.capture_page_screenshot()
                    disableCustomItem = disableItem
                    enabledColumnCount = selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.dashboard.highAlertsRiskTodayCustomizedColumnEnabledColumnCount}"))
                    enabledColumnCount = int(enabledColumnCount)
                    print "Column Count:"+str(enabledColumnCount)
                    for iCount in range(enabledColumnCount):
                        enabledItemText = self.get_text("//div[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_cell_R"+str(iCount)+"C0']/div/span")
                        print enabledItemText
                        print disableCustomItem
                        if enabledItemText == disableCustomItem:
                            self.wait_and_click_element("//div[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_cell_R"+str(iCount)+"C2']/div/input")
                            break
                    listAfterUnCheck = dashBoard.get_enabled_custom_columns_from_table(tableName)
                    colt.list_should_not_contain_value(listAfterUnCheck,disableItem)
                    selenium.open_context_menu(BuiltIn().get_variable_value("${table.alert.searchResults.columnHeaderEighthColumn}"))
                    self.wait_and_click_element(BuiltIn().get_variable_value("${list.contextMenu.enableAll}"))

                def get_first_and_last_values(self,columnNumber,header):
                    """Returns first ten rows and last ten rows values for specified header"""
                    tableList = list()
                    text =''
                    for icount in range(2,12):
                        self.wait_and_click_element("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        cellValue = self.get_text("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        columnStatus1 = (str("Risk Factor") == str(header))
                        columnStatus2 = (str("Activity") == str(header))
                        print "columnStatus1:"+str(columnStatus1)
                        print "columnStatus2:"+str(columnStatus2)
                        columnStatus=''
                        if(str(columnStatus1) == "True" or str(columnStatus2) == "True"):
                            columnStatus = "True"
                        else:
                            columnStatus = "False"
                        print "columnStatus:"+str(columnStatus)
                        iCount1 = icount - 2
                        if str(columnStatus) == "True":
                            rfValue = self.get_cell_value_from_tool_tip_of_column("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']",header)
                            text = rfValue
                        else:
                            text = cellValue
                        tableList.append(text)
                        self.press_down_key("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]")
                    self.press_end_key("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']")
                    time.sleep(2)
                    for iCount in range(2,11):
                        self.wait_and_click_element("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        self.press_up_key("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td[3]/div[contains(@id,'C2')]/div[contains(@class,'Selected')]")
                    text1 = ''
                    for icount in range(2,12):
                        self.wait_and_click_element("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        cellValue = self.get_text("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        columnStatus1 = (str("Risk Factor") == str(header))
                        columnStatus2 = (str("Activity") == str(header))    
                        columnStatus=''
                        if(str(columnStatus1) == "True" or str(columnStatus2) == "True"):
                            columnStatus = "True"
                        else:
                            columnStatus = "False"
                        print "columnStatus in second for loop:"+str(columnStatus)
                        iCount1 = icount - 2
                        if str(columnStatus) == "True":
                            rfValue = self.get_cell_value_from_tool_tip_of_column("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']",header)
                            text1 = rfValue
                        else:
                            text1 = cellValue
                        tableList.append(text1)
                        self.press_down_key("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]")
                    return tableList

                def get_first_ten_values(self,columnNumber,header):
                    """Returns First top ten rows values for specified header"""
                    tableList = list()
                    self.wait_and_click_element("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                    for icount in range(2,12):
                        columnStatus1 = (str("Risk Factor") == str(header))
                        columnStatus2 = (str("Activity") == str(header))
                        if(str(columnStatus1) == "True" or str(columnStatus2) == "True"):
                            text = self.get_cell_value_from_tool_tip_of_column("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']",header)
                        else:
                            text = self.get_text("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]/div")
                        tableList.append(text)
                        self.press_down_key("//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_body']/table[@class='ajs_tb_table']/tbody/tr/td["+str(columnNumber+1)+"]/div[contains(@id,'C"+str(columnNumber)+"')]/div[contains(@class,'Selected')]")
                    return tableList

                def get_cell_value_from_tool_tip_of_column(self,table_locator,columnName):
                    """Returns values for RiskFactor and Activity columns into a list"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    columnNo = self.get_column_no_from_table(table_locator,columnName)
                    print columnNo
                    colno = columnNo-1
                    print colno
                    attval = self.get_element_attribute_value("//div[contains(@class,'Selected')]@id")
                    print attval
                    attval = attval.split("cell_")
                    print "got attribute value"
                    rowCount = attval[1].split("C")
                    rowCount = rowCount[0]
                    print rowCount
                    id = "ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_cell_"+str(rowCount)+"C"+str(colno)
                    return selenium.execute_javascript('return document.getElementById("'+id+'").textContent')

                def Validate_Up_One_Record_in_FraudMatch(self,table,position,customizeColumnsCount,customizeRowsCount='',record=''):
                    dashboard = BuiltIn().get_library_instance('Dashboard')
                    collection = BuiltIn().get_library_instance('Collections')
                    if record != '':
                        self.wait_and_click_element("//span[contains(text(),'"+str(record)+"')]")
                    selectedColumn = self.get_text(BuiltIn().get_variable_value("${table.alerts.customizedcolumns.selectedrecord}"))
                    selectedColumn = int(selectedColumn)
                    print "selectedColumn:"+str(selectedColumn)
                    self.wait_and_click_element(BuiltIn().get_variable_value("${button.customizeColumns."+str(position)+"OneRec}"))
                    newSelectedColumn = self.get_text(BuiltIn().get_variable_value("${table.alerts.customizedcolumns.selectedrecord}"))
                    newSelectedColumn = int(newSelectedColumn)
                    print "newSelectedColumn:"+str(newSelectedColumn)
                    if selectedColumn == 1:
                        BuiltIn().should_be_equal_as_integers(selectedColumn,newSelectedColumn)
                    if selectedColumn > 1 and str(position) == "down":
                        BuiltIn().should_be_equal_as_integers(selectedColumn+1,newSelectedColumn)
                    if selectedColumn > 1 and str(position) == "up":
                        BuiltIn().should_be_equal_as_integers(selectedColumn,newSelectedColumn+1)
                    enabledRecords = dashboard.get_enabled_custom_columns("//td[@id='ajs_ArdentEdge.Table.T_columns_ArdentEdge.Table.F_columns_th_R0C0']/div/div",customizeColumnsCount)
                    enabledRecords = collection.remove_duplicates(enabledRecords)
                    print "enabledRecords:"+str(enabledRecords)
                    loopCount = BuiltIn().get_length(enabledRecords)
                    print "enabledRecords loopCount:"+str(loopCount)
                    self.wait_and_click_element(BuiltIn().get_variable_value("${table.fraudmatch.moveableElement}"))
                    columnHeadres = dashboard.get_enabled_custom_columns_from_table(table)
                    columnHeadres = collection.remove_duplicates(columnHeadres)
                    print "columnHeadres:"+str(columnHeadres)
                    loopCount = BuiltIn().get_length(columnHeadres)
                    print "columnHeadresCount:"+str(loopCount)
                    for iCount in range(0,int(loopCount)):
                        print str(columnHeadres[iCount])
                        print str(enabledRecords[iCount])
                        if str(columnHeadres[iCount])!="":
                            BuiltIn().should_be_equal_as_strings(columnHeadres[iCount],enabledRecords[iCount],"Table header value and enabled custom column value not matching")

                def MenuSelect(self,mainmenuitem):
                    """Select the desired menu in FraudMap"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    locator = BuiltIn().get_variable_value("${link.common."+str(mainmenuitem)+"}")
                    print locator
                    time.sleep(5)
                    #for icount in range(1,4):
                    try:
                        selenium.wait_until_page_contains_element(BuiltIn().get_variable_value("${link.common."+str(mainmenuitem)+"}"),"30s")
                        selenium.simulate(BuiltIn().get_variable_value("${link.common."+str(mainmenuitem)+"}"),'click')
                        self.wait_for_element_visible(locator+"/parent::div[@class='chosenElement']")
                        time.sleep(5)
                    except:
                        print "got exception while selecting menu"
                        selenium.capture_page_screenshot()
                        return False
                    if str(mainmenuitem).lower()!='admin' and str(mainmenuitem).lower()!='dashboard' and str(mainmenuitem).lower()!='reports' and str(mainmenuitem).lower()!='research':
                        try:
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${list.alerts.date}"),"10s")
                            selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.alerts.date}"), "All Time")
                            time.sleep(3)
                        except:
                            print "when selecting date dropdown got exception"
                        
                        for jcount in range(1,4):
                            try:
                                self.wait_for_element_visible(BuiltIn().get_variable_value("${text.alerts.fromDate}"))
                                selenium.input_text(BuiltIn().get_variable_value("${text.alerts.fromDate}"),'')
                                time.sleep(2)
                                selenium.input_text(BuiltIn().get_variable_value("${text.alerts.toDate}"),'')
                                time.sleep(2)
                                break
                            except:
                                print "when setting dates as empty values got exception"
                    return True

                def Get_Table_Random_RowNo(self,table_locator):
                    """Select the row number randomly from the visible rows"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icounter in range(1,3):
                        try:
                            self.wait_for_element_visible(table_locator+"/tbody/tr[1]/td[1]/div/div","5s")
                            visibleRows = selenium.get_matching_xpath_count(table_locator+"/tbody/tr[1]/td[1]/div/div")
                            emptyRows = selenium.get_matching_xpath_count(table_locator+"/tbody/tr[1]/td[1]/div/div[contains(@class,'empty_cell')]")
                            visibleRows = int(visibleRows)-2-int(emptyRows)
                            randomRowNo = self.get_random_number_in_given_range(1,visibleRows)
                            print "randomRowNo"+str(randomRowNo)
                            return randomRowNo
                        except:
                            print "while selecting the rownumber randomly got exception"

                def Logout(self):
                    """logout from application"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.select_window_by_title("FraudMAP - Main")
                    time.sleep(5)
                    for icounter in range(1,4):
                        try:
                            selenium.wait_until_element_is_visible("//img[@alt='Show Menu']","30s")
                            selenium.mouse_over("//img[@alt='Show Menu']")
                            selenium.click_element("//img[@alt='Show Menu']")
                            selenium.wait_until_element_is_visible(BuiltIn().get_variable_value("${link.common.logout}"),"30s")
                            selenium.click_element(BuiltIn().get_variable_value("${link.common.logout}"))
                            self.wait_for_element_visible("//a[@id='loginForm:trylogin']","10s")
                            BuiltIn().run_keyword("Set Global Variable","${global_Logout_Status}",True)
                            break
                        except:
                            print "while logout from fraudmap got exception"
                            BuiltIn().run_keyword("Set Global Variable","${global_Logout_Status}",False)

                def Open_My_Account(self):
                    """open myaccount page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icounter in range(1,4):
                        try:
                            selenium.wait_until_element_is_visible("//img[@alt='Show Menu']","30s")
                            selenium.mouse_over("//img[@alt='Show Menu']")
                            selenium.click_element("//img[@alt='Show Menu']")
                            selenium.wait_until_element_is_visible(BuiltIn().get_variable_value("${link.common.showMenu.myAccount}"),"30s")
                            selenium.click_element(BuiltIn().get_variable_value("${link.common.showMenu.myAccount}"))
                            self.wait_for_element_visible("//img[@class='returnIcon']","10s")
                            break
                        except:
                            print "while opening my account got exception"

                def Privacy_Policy(self):
                    """Open the privacy policy of fraudmap application"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for icounter in range(1,4):
                        try:
                            selenium.wait_until_element_is_visible("//img[@alt='Show Menu']","30s")
                            selenium.mouse_over("//img[@alt='Show Menu']")
                            selenium.click_element("//img[@alt='Show Menu']")
                            selenium.wait_until_element_is_visible("//div[@class='rich-menu-list-bg']//span[contains(text(),'Privacy Policy')]","30s")
                            selenium.click_element("//div[@class='rich-menu-list-bg']//span[contains(text(),'Privacy Policy')]")
                            self.select_window_by_title("Guardian Analytics Privacy Policy")
                            self.wait_for_element_visible("//a[contains(text(),'Back')]","20s")
                            selenium.simulate("//a[contains(text(),'Back')]",'click')
                            break
                        except:
                            "while opening privacy policy got exception"
                def verify_number_of_session_for_each_risk_level(self,color,filterVal,filterData,reportsSelectedSessionNum):
                    """verifies the number of sessions for each risk levels on alerts page sessions count and check sessions count same or not"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    reportsSessionNum = int(reportsSelectedSessionNum)
                    reportsSessionNumGrtrthan500 = ""
                    reportsSessionNumLessthan500 = ""
                    if reportsSessionNum > 500:
                        reportsSessionNumGrtrthan500 = "+500"
                    elif reportsSessionNum < 500 :
                        reportsSessionNumLessthan500 = reportsSelectedSessionNum
                    print "reportsSessionNum is:" +str(reportsSessionNum)
                    self.wait_for_element_visible("//div[@id='showAlertsButton']/a")
                    self.wait_and_click_element("//div[@id='showAlertsButton']/a")
                    self.wait_for_element_invisible("//div[@id='chartPlacement_chart_title']")
                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                    #self.click_element_and_check_expected_element(BuiltIn().get_variable_value("${button.alerts.showResults}"),"//div[@class='sessionCounter']")
                    self.click_on_show_results()
                    self.wait_for_element_visible("//div[@class='sessionCounter']")
                    status = self.wait_for_element_visible("//div[@class='sessionCounter']")
                    print status
                    print "getting session numbers from Alerts page"
                    alertsnumOfSessions = self.get_text("//div[@class='sessionCounter']")
                    print reportsSessionNum
                    print alertsnumOfSessions
                    if reportsSessionNum > 500:
                        print "greater than 500"
                        BuiltIn().should_contain(str(alertsnumOfSessions),str(reportsSessionNumGrtrthan500),"NumberOfSessions In reports page for the selected record" +str(reportsSessionNumGrtrthan500)+" is not equal with number of sessions in alerts page "+str(alertsnumOfSessions))
                    elif reportsSessionNum < 500:
                        print "less than 500"
                        BuiltIn().should_contain(str(alertsnumOfSessions),str(reportsSessionNumLessthan500),"NumberOfSessions In reports page for the selected record" +str(reportsSessionNumLessthan500)+" is not equal with number of sessions in alerts page "+str(alertsnumOfSessions))
                    self.MenuSelect("Reports")

                def validate_the_graph_type_on_dashboard_for_alerts_past_week(self,graphtype):
                    """Returns the graph type selected in the graph chart in dashboard page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.primaryColorNode}"))
                    dispdgraphtype = ""
                    if bstatus==False:
                        print "If block"
                        bpresent=selenium._is_element_present(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.secondaryColorNode}"))
                        if bpresent:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.secondaryColorNode}"))
                           if bstatus==True:
                              style1=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.secondaryColorNodeStyle}"))
                              style2=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.secondaryColorNode1}")+"@style")
                              print "style1:"+str(style1)
                              print "style2:"+str(style2)
                    else:
                        print "Else Block"
                        style1=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.primaryColorNodeStyle}"))
                        style2=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastWeek.primaryColorNode1}")+"@style")
                        print "style1:"+str(style1)
                        print "style2:"+str(style2)
                    if "background-color" in style1 and "background-color" in style2 and "left:" in style1 and "left:" in style2:
                        style1List = style1.split(';')
                        style2List = style2.split(';')
                        for item in style1List:
                            if "left" in str(item):
                                left1Value = str(item)
                                print "left1Value"+str(left1Value)
                        for item in style2List:
                            if "left" in str(item):
                                left2Value = str(item)
                                print "left2Value"+str(left2Value)
                        if str(left1Value) == str(left2Value):
                            print "StackedColumn comparison block"
                            dispdgraphtype = "StackedColumn"
                        else:
                            print "Clustered Column comparison block"
                            dispdgraphtype = "Clustered Column"
                    elif "solid" in style1 and "solid" in style2:
                        print "Stacked Area comparison block"
                        dispdgraphtype = "Stacked Area"
                    else:
                        print "Line Scatter comparison block"
                        dispdgraphtype = 'Line Scatter'
                    if dispdgraphtype==graphtype:
                        return True
                
                def validate_the_graph_type_on_dashboard_for_alerts_past_year(self,graphtype):
                    """Returns the graph type selected in the graph chart in dashboard page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    bstatus=self.wait_for_element_visible(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.primaryColorNode}"),"5s")
                    dispdgraphtype = ""
                    if bstatus==False:
                        print "If block"
                        bpresent=selenium._is_element_present(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.secondaryColorNode}"))
                        if bpresent:
                           bstatus=selenium._is_visible(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.secondaryColorNode}"))
                           if bstatus==True:
                              style1=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.secondaryColorNodeStyle}"))
                              style2=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.secondaryColorNode1}")+"@style")
                              print "style1:"+str(style1)
                              print "style2:"+str(style2)
                        else:
                            print "Sibling block"
                            style1=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.siblingColorNode}")+"@style")
                            style2=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.siblingColorNode1}")+"@style")
                            print "style1:"+str(style1)
                            print "style2:"+str(style2)
                            
                    else:
                        print "Else Block"
                        style1=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.primaryColorNodeStyle}"))
                        style2=commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.dashboard.alertsPastYear.primaryColorNode1}")+"@style")
                        print "style1:"+str(style1)
                        print "style2:"+str(style2)
                    if "background-color" in style1 and "background-color" in style2 and "left:" in style1 and "left:" in style2 and "top" not in style1 and "top" not in style2:
                        style1List = style1.split(';')
                        style2List = style2.split(';')
                        for item in style1List:
                            if "left" in str(item):
                                left1Value = str(item)
                                print "left1Value"+str(left1Value)
                        for item in style2List:
                            if "left" in str(item):
                                left2Value = str(item)
                                print "left2Value"+str(left2Value)
                        if str(left1Value) == str(left2Value):
                            print "StackedColumn comparison block"
                            dispdgraphtype = "StackedColumn"
                        else:
                            print "Clustered Column comparison block"
                            dispdgraphtype = "Clustered Column"
                    elif "solid" in style1 and "solid" in style2:
                        print "Stacked Area comparison block"
                        dispdgraphtype = "Stacked Area"
                    else:
                        print "Line Scatter comparison block"
                        dispdgraphtype = 'Line Scatter'
                    if dispdgraphtype==graphtype:
                        return True
                    
                def press_control_key(self):
                    """ Presses the Control Key """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.key_hold(Keys.CONTROL)

                def get_table_values_into_list(self, locator, columnCountry, columnName='all',parentLocator='',parentScroll=''):
                    """Returns the list of values displayed under 'columnName' from the table located at 'locator' by taking the unique column name 'columnCountry' """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        self.wait_for_element_visible(locator,"30s")
                    except:
                        print "Table was Not Displayed with time,Please check above screesnshot" 
                    keyColNum = self._table_get_column_no(locator,columnCountry)
                    print "keyColNum: "+str(keyColNum)
                    #Get the column number
                    if columnName!='all':
                        iColNo = self._table_get_column_no(locator,columnName)
                    #Add code to loop through all the columns here
                    #Get the initial cursor position
                    try:
                        self.wait_for_element_visible('//div['+parentLocator+'@class="ajs_tb_bar_knob"]',"30s")
                    except:
                        print "bar_knob was Not Displayed with time,Please check above screesnshot" 

                    prevvalue = selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:]                    
                    print "First scrool value:" + str(prevvalue)
                    keyelements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                    elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(iColNo)+']/div/div')
                    print "elements:"+str(elements)
                    rowValues = {}
                    #Get the values from current rows
                    for ele in range(1,int(elements)):
                        self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div','5s')
                        keys = selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div',False,False)
                        self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iColNo)+']/div/div','5s')
                        newelements = selenium._element_find(locator+'/tbody/tr/td['+str(iColNo)+']/div/div',False,False)
                        #print len(newelements)
                        rowValues[keys[ele].text]=newelements[ele].text
                        if ((newelements[ele].text == " ") or (newelements[ele].text == "")):
                            del rowValues[keys[ele].text]
                    #Scroll down
                    print "Scroll down"
                    try:
                        self.wait_for_element_visible(parentScroll+'//div[@class="ajs_tb_bar_down"]','5s')
                    except:
                        print parentScroll+'//div[@class="ajs_tb_bar_down"]'+" locator not visible"
                    selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    self.wait_for_please_wait_option()
                    #Get the values from all rows by scrolling down
                    while(not (prevvalue==selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:])):                    
                        try:
                            self.wait_for_element_visible('//div['+parentLocator+'@class="ajs_tb_bar_knob"]','5s')
                        except:
                            print '//div['+parentLocator+'@class="ajs_tb_bar_knob"]'+" locator not visible"
                        prevvalue = selenium.get_element_attribute('//div['+parentLocator+'@class="ajs_tb_bar_knob"]@style')[18:]
                        print "prevvalue="+str(prevvalue)
                        keyelements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div')
                        elements = selenium.get_matching_xpath_count(locator+'/tbody/tr/td['+str(iColNo)+']/div/div')
                        print "second list of ele's:"+str(elements)
                        for ele in range(1,int(elements)):
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div','5s')
                            keys = selenium._element_find(locator+'/tbody/tr/td['+str(keyColNum)+']/div/div',False,False)
                            self.wait_for_element_visible(locator+'/tbody/tr/td['+str(iColNo)+']/div/div','5s')
                            newelements = selenium._element_find(locator+'/tbody/tr/td['+str(iColNo)+']/div/div',False,False)
                            rowValues[keys[ele].text]=newelements[ele].text
                            if newelements[ele].text == " ":
                                del rowValues[keys[ele].text]

                        try:
                            self.wait_for_element_visible(parentScroll+'//div[@class="ajs_tb_bar_down"]','5s')
                        except:
                            print parentScroll+'//div[@class="ajs_tb_bar_down"]'+" locator not visible"
                        selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        self.wait_for_please_wait_option()
                    #Scroll back to the top
                    print "Scroll back to the top"
                    self.scroll_to_top()
                    return rowValues.values()

                def get_session_number_from_linked_session_text(self):
                    """It return the session number from linked session text from view Case Page"""
                    linkedText = self.get_text("//div[@style='display:inline']/parent::span/parent::td")
                    linedSessionNumber = linkedText.split(':')
                    if int(str(linedSessionNumber[1]).find(',')) != 1:
                        sessionNumbers = linedSessionNumber[1].split(',')
                        sessionNumber = int(sessionNumbers[0])
                        return sessionNumber
                    else:
                        sessionNumber = int(linedSessionNumber[1])
                        return sessionNumber

                def get_session_number_from_dropdown_selected_caseList(self):
                    """It return session number from dropdown selected case value"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.wait_for_element_visible("//select[@id='caseList']","10s")
                    selectedDropDownValue = selenium.get_selected_list_label("//select[@id='caseList']")
                    caseNumber = str(selectedDropDownValue).split('Session')
                    sessionNumber = int(str(caseNumber[1]).strip())
                    return sessionNumber

                def start_over_columns(self,headerlocator=None):
                    """Restore the default column"""
                    if headerlocator == None:
                        headerlocator = "//td[@id='ajs_T_AlertsTable_tAlerts_F_AlertsTable_tAlerts_th_R0C8']/div/div[1]"
                    headerlocator = str(headerlocator)
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    try:
                        for iCounter in range(1,5):
                            mStatus = self.wait_for_element_visible(headerlocator)
                            if mStatus ==True:
                                selenium.mouse_over(headerlocator)
                                selenium.open_context_menu(headerlocator)
                                self.wait_for_element_visible("//span[contains(text(),'Start over columns')]")
                                selenium.mouse_over("//span[contains(text(),'Start over columns')]")
                                selenium.click_element("//span[contains(text(),'Start over columns')]")
                                break
                            else:
                                time.sleep(4)

                    except:
                        print "Start over coloumn not succeded"
                        return False
                    return True

                def validate_the_advanced_search_fields_of_the_selected_record_with_star(self,searchcriteriaValue,partialValue,position):
                     """Returns The True If the Activites List contains the Activity Values matching with SearchCriteria by 'searchcriteria' if not return False """
                     if position.lower() == 'starting':
                         print "starting block"
                         partialValue = partialValue.replace('*','')
                         print "partialValue:"+str(partialValue)
                         positionValue = int(searchcriteriaValue.find(partialValue))
                         print "positionValue:"+str(positionValue)
                         if positionValue == 0:
                             print "Expected value at Starting position"
                             return True
                         else:
                             return False
                     elif position.lower() == 'ending':
                         print "ending block"
                         partialValue = partialValue.replace('*','')
                         print "partialValue:"+str(partialValue) 
                         searchcriteriaValueLength = len(searchcriteriaValue)
                         print "searchcriteriaValueLength:"+str(searchcriteriaValueLength)
                         partialValueLength = len(partialValue)
                         print "partialValueLength:"+str(partialValueLength)
                         positionValue = int(searchcriteriaValue.rfind(partialValue))
                         print "positionValue:"+str(positionValue)
                         finalLength = searchcriteriaValueLength - partialValueLength
                         print "finalLength"+str(finalLength)
                         if positionValue == finalLength:
                            print "enter in to if block"
                            return True
                         else:
                            return False

                def validate_activity_details_with_star(self,activityName,activityValue):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    common = BuiltIn().get_library_instance('CommonLibrary')
                    #common.wait_for_element_visible("//label[contains(text(),'"+str(activityName)+"')]/parent::div/following-sibling::div/input")
                    for iCount in range (1,5):
                        common.wait_for_element_visible("//label[text()='"+str(activityName)+"']/parent::div/following-sibling::div/input")
                        #selenium.input_text("//label[contains(text(),'"+str(activityName)+"')]/parent::div/following-sibling::div/input",""+str(activityValue)+"")
                        selenium.input_text("//label[text()='"+str(activityName)+"']/parent::div/following-sibling::div/input",str(activityValue))
                        activityValues = common.get_element_attribute_value("//label[text()='"+str(activityName)+"']/parent::div/following-sibling::div/input@value")
                        print "activityValues:" +str(activityValues)
                        #common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                        common.wait_and_click_element("//label[text()='"+str(activityName)+"']")
                        time.sleep(5)
                        print "loop count is" + str(iCount)
                        #checkBoxStatus1 = common.get_element_attribute_value("//label[contains(text(),'"+str(activityName)+"')]/parent::div/input@checked")
                        checkBoxStatus1 = common.get_element_attribute_value("//label[text()='"+str(activityName)+"']/parent::div/input@checked")
                        if str(checkBoxStatus1) == "true":
                            break
                        else:
                            #common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                            common.wait_and_click_element("//label[text()='"+str(activityName)+"']")
                            time.sleep(5)
                            selenium.capture_page_screenshot()
                            common.wait_and_click_element("//form[@id='filterForm']//a[contains(text(),'Ok')]")
                            self.wait_for_element_invisible("//form[@id='filterForm']//a[contains(text(),'Ok')]","5s")
                            common.wait_and_click_element("//div[@id='advanced']//a[contains(text(),'Edit')]")
                            #checkBoxStatus = common.get_element_attribute_value("//label[contains(text(),'"+str(activityName)+"')]/parent::div/input@checked")
                            checkBoxStatus = common.get_element_attribute_value("//label[text()='"+str(activityName)+"']/parent::div/input@checked")
                            print "checkBoxStatus is" + str(checkBoxStatus)
                            if str(checkBoxStatus) == "true":
                                print "Activity checkbox status in if block: "
                                break
                    common.wait_and_click_element("//form[@id='filterForm']//a[contains(text(),'Ok')]")
                    self.wait_for_element_invisible("//form[@id='filterForm']//a[contains(text(),'Ok')]","5s")
                    for iCount in range(1,6):
                        print "Verify details check box is checked or not"
                        detailsCheckBoxStatus = common.get_element_attribute_value("//div[@id='advanced']//label[contains(text(),'Details')]/preceding-sibling::input@checked")
                        detailsValue = self.get_text("//div[@id='activityFieldList']/div/div")
                        
                        print "detailsValue" +str(detailsValue)
                        if str(detailsCheckBoxStatus) == "true":
                            print "details check box status true in if block"
                            if str(detailsValue).find(activityValues)>=0:
                                print "Entered in if block str(detailsValue).find(activityValues): "
                                indexValue = str(detailsValue).find(activityValues)
                                print "index value of :"+str(indexValue)
                                break
                            else:
                                common.wait_and_click_element("//div[@id='advanced']//a[contains(text(),'Edit')]")
                                self.wait_for_element_visible("//label[text()='"+str(activityName)+"']/parent::div/following-sibling::div/input","10s")
                                activityValues = selenium.input_text("//label[text()='"+str(activityName)+"']/parent::div/following-sibling::div/input",str(activityValue))
                            #common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                            common.wait_and_click_element("//label[text()='"+str(activityName)+"']")
                            time.sleep(5)
                            print "loop count is" + str(iCount)
                            #checkBoxStatus1 = common.get_element_attribute_value("//label[contains(text(),'"+str(activityName)+"')]/parent::div/input@checked")
                            checkBoxStatus1 = common.get_element_attribute_value("//label[text()='"+str(activityName)+"']/parent::div/input@checked")
                            if str(checkBoxStatus1) == "true":
                                break
                            else:
                                #common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                                common.wait_and_click_element("//label[text()='"+str(activityName)+"']")
                                time.sleep(5)
                                selenium.capture_page_screenshot()
                                common.wait_and_click_element("//form[@id='filterForm']//a[contains(text(),'Ok')]")
                                self.wait_for_element_invisible("//form[@id='filterForm']//a[contains(text(),'Ok')]","5s")
                        else:
                            print "details check box status false in else block"
                            common.wait_and_click_element("//div[@id='advanced']//label[contains(text(),'Details')]")
                        
                            
                            

                def enter_and_validate_advanced_search_fields_for_ODFI(self,dictVar,hideFilters=True,expectedLocator=None,reset=True):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    print "resetStatus: "+str(resetStatus)
                    if reset==True:
                        self.wait_and_click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","") == "companyid":
                                    print "enter in to companyid condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.adanceSearch.companyIDforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.adanceSearch.companyIDforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.adanceSearch.companyIDforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyname":
                                    print "enter in to companyname condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "odfi":
                                    print "enter in to odfi condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "seccode":
                                    print "enter in to seccode condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "totalcreditscount":
                                    print "enter in to totalcreditscount condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.advanceSearch.TotalCreditsCount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${text.advanceSearch.TotalCreditsCount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${text.advanceSearch.TotalCreditsCount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "totaldebitscount":
                                    print "enter in to totaldebitscount condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitsCount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitsCount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitsCount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "totalcreditamount":
                                    print "enter in to totalcreditamount condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalCreditAmount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalCreditAmount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalCreditAmount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "totaldebitamount":
                                    print "enter in to totalcreditamount condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitAmount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitAmount}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TotalDebitAmount}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "duedate":
                                    print "enter in to Due Date condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.dueDateforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.dueDateforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.dueDateforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "riskfactor":
                                    print "enter in to Risk Factor condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.riskFactorforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.riskFactorforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.riskFactorforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "batchrange":
                                    print "enter in to Batch Range condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.batchRangeforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.batchRangeforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.batchRangeforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyentrydescription":
                                    print "enter in to Company Entry Description condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.companyEntryDescriptionforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.companyEntryDescriptionforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.companyEntryDescriptionforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companydescdate":
                                    print "enter in to Company Desc Date condition"
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.companyDescDateforODFI}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.companyDescDateforODFI}"), dictVar[keyVal])
                                        if valStatus == False:
                                            selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.companyDescDateforODFI}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                        
                        except:
                            print "entering search details failed"
                        showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "showResultsStatus: " +str(showResultsStatus)
                        if showResultsStatus == True:
                            selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            time.sleep(5)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                        else:
                            print "check expectedLocator "+ str(expectedLocator)
                            self.wait_for_element_visible(expectedLocator)
                        searchStatus = self.check_search_checkbox_for_ODFI(dictVar)
                        print "searchStatus: "+str(searchStatus)
                        if searchStatus == True:
                            showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            print "showResultsStatus: " +str(showResultsStatus)
                            if showResultsStatus == True:
                                time.sleep(2)
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                if expectedLocator==None:
                                    for iCnt in range(1,1000):
                                        searchingStatus = self.wait_for_element_visible("//div[@id='subMainForm:cmdStatusWithCtlDialogHeader' and @class='rich-mpnl-text rich-mpnl-header ']","5s")
                                        print "searchingStatus: "+str(searchingStatus)
                                        if searchingStatus == False:
                                            break
                                    self.wait_for_search_is_running_in_background_alert_message()
                                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                                else:
                                    print "check expectedLocator "+ str(expectedLocator)
                                    self.wait_for_element_visible(expectedLocator)
                        else:
                            break;
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']","5s") == True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                            print "hiding Filters section done"
                        except:
                            print "hiding Filters failed"
                    return True

                def check_search_checkbox_for_ODFI(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "check : "+str(keyVal) + " checkbox"
                        try:
                            if keyVal.lower().replace(" ","") == "riskfactor":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.riskfactor}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Risk Factor']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "provider":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.provider}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Provider']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "activity":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.activity}"))
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Activity']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "seccode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.SECCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='SEC Code']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "odfi":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.ODFI}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='ODFI']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companyid":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.companyIDforODFI}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company Id']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companyname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.CompanyName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company Name']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "totalcreditscount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TotalCreditsCount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Total Credits Count']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "totaldebitscount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TotalDebitsCount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Total Debits Count']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "totalcreditamount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TotalCreditAmount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Total Credit Amount']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "totaldebitamount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.TotalDebitAmount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Total Debit Amount']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "riskfactor":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.riskFactorforODFI}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Risk Factor']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "batchrange":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.batchRange}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Batch Range']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companyentrydescription":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.companyEntryDescription}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company Entry Description']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "companydescdate":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.companyDescDate}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Company Desc Date']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")

                            elif keyVal.lower().replace(" ","") == "duedate":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.advanceSearch.dueDate}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    selenium.click_element("//div[@id='advanced']//label[text()='Due Date']")
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                            print "fieldStatus: "+str(fieldStatus)
                        except:
                            print "all checkboxes are not selected" + str(keyVal) + " check box not checked"
                       
                    return bStatus

                def enter_two_activities_into_activityfield_with_OR(self,textboxName,first,second,delimiter):
                  """Returns two activities by combining both of them with a delimiter between them """
                  selenium = BuiltIn().get_library_instance('Selenium2Library')
                  CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                  CommonLibrary.wait_for_element_visible("//input[@class='searchField-"+str(textboxName)+"']")
                  time.sleep(5)
                  activities = [first,delimiter,second]
                  try:
                    activitycol=selenium.input_text("//input[@class='searchField-"+str(textboxName)+"']",activities)
                    print "activitycol="+str(activitycol)
                    return activitycol
                  except:
                    print "Unable to enter text"

                def validate_activity_details_with_OR(self,activityName,textboxName,value1,value2,delimiter):
                  selenium = BuiltIn().get_library_instance('Selenium2Library')
                  reports = BuiltIn().get_library_instance('Reports')
                  common = BuiltIn().get_library_instance('CommonLibrary')
                  common.wait_for_element_visible("//label[contains(text(),'"+str(activityName)+"')]/parent::div/following-sibling::div/input")
                  for iCount in range (1,5):
                    common.enter_two_activities_into_activityfield_with_OR(textboxName,value1,value2,delimiter)
                    print "enter two activities"
                    common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                    time.sleep(5)
                    print "loop count is" + str(iCount)
                    checkBoxStatus1 = common.get_element_attribute_value("//label[contains(text(),'"+str(activityName)+"')]/parent::div/input@checked")
                    if str(checkBoxStatus1) == "true":
                      break
                    else:
                      common.wait_and_click_element("//label[contains(text(),'"+str(activityName)+"')]")
                      time.sleep(5)
                      selenium.capture_page_screenshot()
                      common.wait_and_click_element("//form[@id='filterForm']//a[contains(text(),'Ok')]")
                      common.wait_and_click_element("//div[@id='advanced']//a[contains(text(),'Edit')]")
                      checkBoxStatus = common.get_element_attribute_value("//label[contains(text(),'"+str(activityName)+"')]/parent::div/input@checked")
                      print "checkBoxStatus is" + str(checkBoxStatus)
                      if str(checkBoxStatus) == "true":
                        break
                  common.wait_and_click_element("//form[@id='filterForm']//a[contains(text(),'Ok')]")
                  common.wait_for_element_invisible("//form[@id='filterForm']//a[contains(text(),'Ok')]","5s")
                  print "Added wait_for_element_invisible"
                  for iCount in range(1,6):
                      print "Verify details check box is checked or not"
                      detailsCheckBoxStatus = common.get_element_attribute_value("//div[@id='advanced']//label[contains(text(),'Details')]/preceding-sibling::input@checked")
                      if str(detailsCheckBoxStatus) == "true":
                        print "details check box status true"
                        break
                      else:
                        print "details check box status false"
                        common.wait_and_click_element("//div[@id='advanced']//label[contains(text(),'Details')]")

                def remove_empty_values_from_list(self,listItems):
                    length = len(listItems)
                    print length
                    expectedLstItems = list()
                    for icount in range(0,length):
                        if str(listItems[icount]) != "":
                            print "enter in to if block"
                            expectedLstItems.append(listItems[icount])
                    print expectedLstItems
                    return expectedLstItems

                def get_advanced_search_lables(self):
                    """It returns all advanced search labels into list"""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    hideStatus = self.verify_element_visible("//a[@class='hideAdvancedFilters']")
                    advancedSearchLabels = list()
                    if hideStatus==True:
                        count = int(selenium.get_matching_xpath_count("//div[@id='advanced']//div[@class='fadvRow']"))
                        print "count:"+str(count)
                        for icount in range(1,count+1):
                            innerCount = int(selenium.get_matching_xpath_count("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]"))
                            print "innerCount:"+str(innerCount)
                            if innerCount == 1:
                                text = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]/label")
                                text = text.strip()
                                print "text after strip:"+str(text)
                                advancedSearchLabels.append(text)
                            else:
                                print "else block"
                                for jCount in range(1,innerCount+1):
                                    if icount == count and jCount == 2:
                                        text1 = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]["+str(jCount)+"]//a")
                                        advancedSearchLabels.append(text1)
                                    else:
                                        text1 = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]["+str(jCount)+"]/label")
                                        print "text1:"+str(text1)
                                        advancedSearchLabels.append(text1)
                        print advancedSearchLabels
                        return advancedSearchLabels
                    else:
                        showStatus = self.verify_element_visible("//a[@class='showAdvancedFilters']")
                        if showStatus == True:
                            for iCount in range(1,6):
                                self.wait_and_click_element("//a[@class='showAdvancedFilters']")
                                status = self.wait_for_element_visible("//a[@class='hideAdvancedFilters']")
                                if status == True:
                                    break
                            count = int(selenium.get_matching_xpath_count("//div[@id='advanced']//div[@class='fadvRow']"))
                            print "count:"+str(count)
                            for icount in range(1,count+1):
                                innerCount = int(selenium.get_matching_xpath_count("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]"))
                                print "innerCount:"+str(innerCount)
                                if innerCount == 1:
                                    text = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]/label")
                                    text = text.strip()
                                    print "text after strip:"+str(text)
                                    advancedSearchLabels.append(text)
                                else:
                                    print "else block"
                                    for jCount in range(1,innerCount+1):
                                        if icount == count and jCount == 2:
                                            text1 = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]["+str(jCount)+"]//a")
                                            advancedSearchLabels.append(text1)
                                        else:
                                            text1 = self.get_text("//div[@id='advanced']//div[@class='fadvRow']["+str(icount)+"]/div[contains(@class,'fadvChkAndTitleCell')]["+str(jCount)+"]/label")
                                            print "text1:"+str(text1)
                                            advancedSearchLabels.append(text1)
                            print advancedSearchLabels
                            return advancedSearchLabels
                        else:
                            raise AssertionError("This key word is working only where the advanced search fields are available")
    
                def do_search_in_the_reports_page_RDFI(self,dictVar,hideFilters=True,expectedLocator=None,reset=True):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    bStatus = self.do_basic_search(dictVar)
                    print "bStatus: "+str(bStatus)
                    if bStatus==False:
                        return False
                    advancedFilterStatus = self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                    if advancedFilterStatus == True:
                        selenium.click_element("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']")
                    resetStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.reports.advSearchReset}"),"10s")
                    print "resetStatus: "+str(resetStatus)
                    if reset==True:
                        self.wait_and_click_element(BuiltIn().get_variable_value("${button.reports.advSearchReset}"))
                        time.sleep(5)
                    
                    for iCounter in range(1,4):
                        try:
                            for keyVal in dictKeys:
                                print "keyVal1: "+str(keyVal)
                                dctVal = str(dictVar[keyVal])
                                valStatus = (dctVal.find("*")>=0)
                                if keyVal.lower().replace(" ","")== "recipientname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"))
                                    if fieldStatus == True:
                                        # get the checkbox status, if not checked enter the details                                        
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "amount":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.Amount}"),True,True).send_keys(Keys.TAB)                                        
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "tracenumber":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TraceNumber}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                elif keyVal.lower().replace(" ","") == "recipientaccountnumber":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RecipientAccountNumber}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "riskfactor":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.RiskFactor}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "iptype":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.iptype}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "seccode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advancesearch.SecCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "odfiid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"))
                                    if fieldStatus == True:
                                        print "${textbox.advanceSearch.ODFIID}: "+str(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"))
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.ODFIID}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "transactioncode":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.TransactionCode}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyid":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advanceSearch.CompanyID}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)

                                elif keyVal.lower().replace(" ","") == "companyname":
                                    fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${textbox.advancesearch.CompanyName}"))
                                    if fieldStatus == True:
                                        selenium.input_text(BuiltIn().get_variable_value("${textbox.advancesearch.CompanyName}"), dictVar[keyVal])
                                        selenium._element_find(BuiltIn().get_variable_value("${textbox.advancesearch.CompanyName}"),True,True).send_keys(Keys.TAB)
                                        time.sleep(2)
                                                                
                        except:
                            print "entering search details failed"
                        showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                        print "showResultsStatus: " +str(showResultsStatus)
                        if showResultsStatus == True:
                            selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            time.sleep(5)
                        if expectedLocator==None:
                            for iCnt in range(1,1000):
                                searchingStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${headers.alerts.showresults.searchingdialog}"),"5s")
                                print "searchingStatus: "+str(searchingStatus)
                                if searchingStatus == False:
                                    break
                            self.wait_for_search_is_running_in_background_alert_message()
                            self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                        else:
                            print "check expectedLocator "+ str(expectedLocator)
                            self.wait_for_element_visible(expectedLocator)
                        searchStatus = self.check_search_checkbox(dictVar)
                        print "searchStatus: "+str(searchStatus)
                        if searchStatus == True:
                            showResultsStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                            print "showResultsStatus: " +str(showResultsStatus)
                            if showResultsStatus == True:
                                time.sleep(2)
                                selenium.click_element(BuiltIn().get_variable_value("${button.alerts.showResults}"))
                                if expectedLocator==None:
                                    for iCnt in range(1,1000):
                                        searchingStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${headers.alerts.showresults.searchingdialog}"),"5s")
                                        print "searchingStatus: "+str(searchingStatus)
                                        if searchingStatus == False:
                                            break
                                    self.wait_for_search_is_running_in_background_alert_message()
                                    self.wait_for_element_visible(BuiltIn().get_variable_value("${button.alerts.export}"),"30s")
                                else:
                                    print "check expectedLocator "+ str(expectedLocator)
                                    self.wait_for_element_visible(expectedLocator)
                        else:
                            break;
                    if hideFilters==True and self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']","5s") == True:
                        try:
                            selenium.click_element("//div[@class='advancedFilterControlRegion']//a[@class='hideAdvancedFilters']")
                            self.wait_for_element_visible("//div[@class='advancedFilterControlRegion']/a[@class='showAdvancedFilters']","5s")
                            print "hiding Filters section done"
                        except:
                            print "hiding Filters failed"
                    return True

                def removing_square_brackets_for_watchlist(self,watchlistName):
                    openBracketStatus = self.string_should_contain(watchlistName,"[")
                    print "openBracketStatus" +str(openBracketStatus)
                    if openBracketStatus:
                        watchlistName = watchlistName.split("[")
                        print "watchListName" +str(watchlistName)
                        watchlistName = watchlistName[1]
                        closedBracketStatus = self.string_should_contain(watchlistName,"]")
                        print "closedBracketStatus:" +str(closedBracketStatus)
                        if closedBracketStatus:
                            watchlistName = watchlistName.split("]")
                            watchlistName = watchlistName[0]
                            print "watchListName" +str(watchlistName)
                            return watchlistName
                        else:
                            return watchlistName 
                    else:
                        closedBracketStatus = self.string_should_contain(watchlistName,"]")
                        if closedBracketStatus:
                            watchlistName = watchlistName.split("]")
                            watchlistName = watchlistName[0]
                            print "watchListName" +str(watchlistName)
                            return watchlistName
                        else:
                            return watchlistName

                def select_user_from_users_table(self,expectedUser):
                    """it returns true if expected user record is selected otherwise it returns false"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    mainPageStatus = self.verify_element_present(BuiltIn().get_variable_value("${link.admin.users}"))
                    print "mainPageStatus:"+str(mainPageStatus)
                    if mainPageStatus == True:
                        selenium.click_element(BuiltIn().get_variable_value("${link.admin.users}"))
                        returnToFraudMapStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${image.users.returnToFraudMap}"),"30s")
                        print "returnToFraudMapStatus:"+str(returnToFraudMapStatus)
                        if returnToFraudMapStatus != True:
                            raise AssertionError("After click on Users,it is not navigating to User Page.")
                        recordsStatus = self.verify_element_present("//div[contains(@id,'userTable')]//div[text()='No Results Found']")
                        print "recordsStatus:"+str(recordsStatus)
                        if recordsStatus == True:
                            raise AssertionError("No Results Found in the Users table")
                        
                        previousButtonDisabledStatus = self.verify_element_present("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']")
                        print "previousButtonDisabledStatus:"+str(previousButtonDisabledStatus)
                        if previousButtonDisabledStatus!= True:
                            for iCount in range(5):
                                previousButtonEnabledStatus = self.verify_element_present("//a[@class='rf-ds-btn rf-ds-btn-prev']")
                                print "previousButtonEnabledStatus:"+str(previousButtonEnabledStatus)
                                if previousButtonEnabledStatus == True:
                                    selenium.click_element("//a[@class='rf-ds-btn rf-ds-btn-prev']")
                                    previousButtonDisabledStatus = self.wait_for_element_visible("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']","10s")
                                    if previousButtonDisabledStatus == True:
                                        break
                                else:
                                    previousButtonDisabledStatus = self.verify_element_present("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']")
                                    if previousButtonDisabledStatus == True:
                                        break
                        numberOfPages = int(selenium.get_matching_xpath_count("//*[contains(@class,'rf-ds-nmb-btn')]"))
                        print "numberOfPages"+str(numberOfPages)
                        for pCount in range(1,numberOfPages+1):
                            totalRecords = int(selenium.get_matching_xpath_count("//div[contains(@id,'userTable:body')]/table//tr"))
                            print "totalRecords:"+str(totalRecords)
                            for iCount in range(1,totalRecords + 1):
                                userFromTable = self.get_text("//div[contains(@id,'userTable:body')]/table//tr["+str(iCount)+"]/td[3]/div/div")
                                if str(expectedUser) == str(userFromTable):
                                    selenium.click_element("//div[contains(@id,'userTable:body')]/table//tr["+str(iCount)+"]/td[3]/div/div")
                                    self.wait_for_element_visible("//div[contains(@id,'userTable:body')]/table//tr[@class='uacTableRow rf-edt-r-sel rf-edt-r-act']/td[3]/div/div","30s")
                                    userAfterSelectedTheRecord = self.get_text("//div[contains(@id,'userTable:body')]/table//tr[@class='uacTableRow rf-edt-r-sel rf-edt-r-act']/td[3]/div/div")
                                    print "userAfterSelectedTheRecord:"+str(userAfterSelectedTheRecord)
                                    if str(userAfterSelectedTheRecord) == str(expectedUser):
                                        print "Condition true"
                                        return True
                                    else:
                                        return False
                                elif str(userFromTable) != str(expectedUser) and int(iCount) == int(totalRecords) and int(pCount) ==  int(numberOfPages):
                                    print "Second if condition"
                                    return False
                                elif str(userFromTable) != str(expectedUser) and int(iCount) == int(totalRecords) and int(pCount) !=  int(numberOfPages):
                                    print "third condition"
                                    selenium.click_element("//a[@class='rf-ds-btn rf-ds-btn-next']")
                                    self.wait_for_element_visible("//a[@class='rf-ds-btn rf-ds-btn-first']","30s")
                                    selectedPageStatus = self.wait_for_element_visible("//span[contains(@class,'rf-ds-nmb-btn rf-ds-act') and contains(text(),'"+str(pCount+1)+"')]","30s")
                                    print "selectedPageStatus:"+str(selectedPageStatus)                    
                    else:
                        print "Enter in to else block"
                        returnToFraudMapStatus = self.verify_element_present(BuiltIn().get_variable_value("${image.users.returnToFraudMap}"))
                        print "returnToFraudMapStatus:"+str(returnToFraudMapStatus)
                        if returnToFraudMapStatus != True:
                            raise AssertionError("This keyword should be called from either main page or Users Page but not others page/Window")
                        recordsStatus = self.verify_element_present("//div[contains(@id,'userTable')]//div[text()='No Results Found']")
                        print "recordsStatus:"+str(recordsStatus)
                        if recordsStatus == True:
                            raise AssertionError("No Results Found in the Users table")
                        totalRecords = int(selenium.get_matching_xpath_count("//div[contains(@id,'userTable:body')]/table//tr"))
                        print "totalRecords:"+str(totalRecords)
                        previousButtonDisabledStatus = self.verify_element_present("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']")
                        print "previousButtonDisabledStatus:"+str(previousButtonDisabledStatus)
                        if previousButtonDisabledStatus!= True:
                            for iCount in range(5):
                                previousButtonEnabledStatus = self.verify_element_present("//a[@class='rf-ds-btn rf-ds-btn-prev']")
                                print "previousButtonEnabledStatus:"+str(previousButtonEnabledStatus)
                                if previousButtonEnabledStatus == True:
                                    selenium.click_element("//a[@class='rf-ds-btn rf-ds-btn-prev']")
                                    previousButtonDisabledStatus = self.wait_for_element_visible("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']","10s")
                                    if previousButtonDisabledStatus == True:
                                        break
                                else:
                                    previousButtonDisabledStatus = self.verify_element_present("//span[@class='rf-ds-btn rf-ds-btn-prev rf-ds-dis']")
                                    if previousButtonDisabledStatus == True:
                                        break
                        numberOfPages = int(selenium.get_matching_xpath_count("//*[contains(@class,'rf-ds-nmb-btn')]"))
                        print "numberOfPages"+str(numberOfPages)
                        for pCount in range(1,numberOfPages+1):
                            totalRecords = int(selenium.get_matching_xpath_count("//div[contains(@id,'userTable:body')]/table//tr"))
                            print "totalRecords:"+str(totalRecords)
                            for iCount in range(1,totalRecords + 1):
                                userFromTable = self.get_text("//div[contains(@id,'userTable:body')]/table//tr["+str(iCount)+"]/td[3]/div/div")
                                if str(expectedUser) == str(userFromTable):
                                    selenium.click_element("//div[contains(@id,'userTable:body')]/table//tr["+str(iCount)+"]/td[3]/div/div")
                                    self.wait_for_element_visible("//div[contains(@id,'userTable:body')]/table//tr[@class='uacTableRow rf-edt-r-sel rf-edt-r-act']/td[3]/div/div","30s")
                                    userAfterSelectedTheRecord = self.get_text("//div[contains(@id,'userTable:body')]/table//tr[@class='uacTableRow rf-edt-r-sel rf-edt-r-act']/td[3]/div/div")
                                    if str(userAfterSelectedTheRecord) == str(expectedUser):
                                        print "Condition true"
                                        return True
                                    else:
                                        return False
                                elif str(userFromTable) != str(expectedUser) and int(iCount) == int(totalRecords) and int(pCount) ==  int(numberOfPages):
                                    print "Second condition"
                                    return False
                                elif str(userFromTable) != str(expectedUser) and int(iCount) == int(totalRecords) and int(pCount) !=  int(numberOfPages):
                                    print "Third condition"
                                    selenium.click_element("//a[@class='rf-ds-btn rf-ds-btn-next']")
                                    self.wait_for_element_visible("//a[@class='rf-ds-btn rf-ds-btn-first']","30s")
                                    selectedPageStatus = self.wait_for_element_visible("//span[contains(@class,'rf-ds-nmb-btn rf-ds-act)' and contains(text(),'"+str(pCount+1)+"')]","30s")
                                    print "selectedPageStatus:"+str(selectedPageStatus)

                def check_search_checkbox_for_ODFI_batch_entry_details(self,dictVar):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    for keyVal in dictKeys:
                        print "check : "+str(keyVal) + " checkbox"
                        try:
                            if keyVal.lower().replace(" ","") == "amount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.Amount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                print "fieldStatus" +str(fieldStatus)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.amount}"))
                                    #self.wait_and_click_element(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "rdfi":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.RDFI}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.RDFI}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "transcode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.transCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.transCode}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "recipientname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.RecipientName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.RecipientName}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "tracenumber":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.traceNumber}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.traceNumber}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "gatewayoperatorofacscreeningindicator":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.gatewayOperatorOFACScreeningIndicator}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.gatewayOperatorOFACScreeningIndicator}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorbankid":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.OriginatorBankId}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.OriginatorBankId}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorcity":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.OriginatorCity}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.OriginatorCity}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorcountry":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.OriginatorCountry}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.OriginatorCountry}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorpostalcode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.OriginatorPostalCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.OriginatorPostalCode}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorbankname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.originatorBankName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.originatorBankName}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "transactiontypecode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.TransactionTypeCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.transactionTypeCode}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)    
                            elif keyVal.lower().replace(" ","") == "recipientaccount":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.recipientAccount}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.recipientAccount}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorbranchcountrycode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.originatorBranchCountryCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.originatoBranchCountryCode}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "receiverbankcountrycode":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.receiverBankCountryCode}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.receiverBankCountryCode}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "receivercountry":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.receiverCountry}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.receiverCountry}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorname":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.originatorName}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.originatorName}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorstreetaddress":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.originatorStreetAddress}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.originatorStreetAddress}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "terminallocation":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.terminalLocation}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.terminalLocation}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "terminalid":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.terminalId}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.terminalId}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "paymentrelatedinformation":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.paymentRelatedInformation}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.paymentRelatedInformation}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "originatorstate":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.originatorState}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.originatorState}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "receiverstate":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.receiverState}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.batchEntryDetails.receiverState}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                            elif keyVal.lower().replace(" ","") == "checkserialnumber":
                                fieldStatus = selenium.get_element_attribute(BuiltIn().get_variable_value("${checkbox.batchEntryDetail.checkSerialNumber}"))
                                print "checkbox attribute val ="+str(fieldStatus)
                                fieldStatus = (str(fieldStatus).find("checked")>=0 or str(fieldStatus).find("true")>=0)
                                if fieldStatus == True:
                                    print str(keyVal) + str(" checkbox was selected/ checked ")
                                    bStatus = True
                                else:
                                    print str(keyVal) + str(" checkbox was not selected / unchecked ")
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${label.BatchEntryDetail.CheckSerialNumber}"))
                                    bStatus = True
                                    print str(keyVal) + str(" checkbox was selected using click element keyword")
                                print "fieldStatus: "+str(fieldStatus)
                        except:
                            print "all checkboxes are not selected" + str(keyVal) + " check box not checked"
                       
                    return bStatus
                
                def enter_and_validate_batch_entry__details_fields(self,dictVar,pagedisplayed,SECCode='',hideFilters=True,expectedLocator=None,reset=True):
                    """Returns the status of Get Previous search text for hide functionality"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = False
                    print "dictVar:"
                    print dictVar
                    dictVals = dictVar.values()
                    dictKeys = dictVar.keys()
                    filterStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${header.accountDetails.batchEntryDetails}","5s"))
                    if filterStatus == True:
                        for iCounter in range(1,4):
                            try:
                                for keyVal in dictKeys:
                                    print "keyVal1: "+str(keyVal)
                                    dctVal = str(dictVar[keyVal])
                                    valStatus = (dctVal.find("*")>=0)
                                    if keyVal.lower().replace(" ","")== "amount":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.Amount}"))
                                        if fieldStatus == True:
                                            # get the checkbox status, if not checked enter the details
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.Amount}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.Amount}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "rdfi":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.RDFI}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.RDFI}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.RDFI}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "transcode":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.transCode}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.transCode}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.transCode}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "recipientname":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetail.RecipientName}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetail.RecipientName}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetail.RecipientName}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "tracenumber":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetail.traceNumber}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetail.traceNumber}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetail.traceNumber}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "gatewayoperatorofacscreeningindicator":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetail.GatewayOperatorOFACScreeningIndicator}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetail.GatewayOperatorOFACScreeningIndicator}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetail.GatewayOperatorOFACScreeningIndicator}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorbankid":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankID}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankID}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankID}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorcity":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCity}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCity}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCity}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorcountry":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCountry}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCountry}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorCountry}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorpostalcode":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorPostalCode}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorPostalCode}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorPostalCode}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorbankname":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankName}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankName}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBankName}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "transactiontypecode":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${list.batchEntryDetails.transactionTypeCode}"))
                                        if fieldStatus == True:
                                            selenium.select_from_list_by_label(BuiltIn().get_variable_value("${list.batchEntryDetails.transactionTypeCode}"), dictVar[keyVal])
                                            #selenium._element_find(BuiltIn().get_variable_value("${list.batchEntryDetails.transactionTypeCode}"),True,True).send_keys(Keys.TAB)
                                            #time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "recipientaccount":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.recipientAccount}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.recipientAccount}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.recipientAccount}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorbranchcountrycode":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBranchCountryCode}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBranchCountryCode}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorBranchCountryCode}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "receiverbankcountrycode":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverBranchCountryCode}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverBranchCountryCode}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverBranchCountryCode}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "receivercountry":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverCountry}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverCountry}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverCountry}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorname":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorName}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorName}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorName}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorstreetaddress":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorStreetAddress}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorStreetAddress}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorStreetAddress}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "terminalid":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalId}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalId}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalId}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "terminallocation":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalLocation}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalLocation}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.terminalLocation}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "paymentrelatedinformation":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.paymentRelatedInformation}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.paymentRelatedInformation}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.paymentRelatedInformation}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "originatorstate":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorState}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorState}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.originatorState}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "receiverstate":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverState}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverState}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.receiverState}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                                    elif keyVal.lower().replace(" ","") == "checkserialnumber":
                                        fieldStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${text.batchEntryDetails.checkSerialNumber}"))
                                        if fieldStatus == True:
                                            selenium.input_text(BuiltIn().get_variable_value("${text.batchEntryDetails.checkSerialNumber}"), dictVar[keyVal])
                                            selenium._element_find(BuiltIn().get_variable_value("${text.batchEntryDetails.checkSerialNumber}"),True,True).send_keys(Keys.TAB)
                                            time.sleep(2)
                            except:
                                print "entering search details failed"
                            resultsStatus = self.verify_element_present(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                            print "Ok: " +str(resultsStatus)
                            self.wait_and_click_element(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                            print "search options clicked"
                            if resultsStatus == True:
                                for iCount in range(1,5):
                                    self.press_down_key(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                                    print "press down key"
                                    okStatus = self.verify_element_visible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                    print "okStatus" +str(okStatus)
                                    #if okStatus == False:
                                        #self.press_down_key(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                                        #self.press_down_key("//span[contains(text(),'32 fields found in following SEC Code(s): IAT'")
                                        #print "press down key after verifying ok button status"
                                for iCount in range(1,8):
                                    print "iCount: " +str(iCount)
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                    self.wait_for_element_invisible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"),"5s")
                                    visibleStatus = self.verify_element_visible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                    print "visibleStatus" +str(visibleStatus)
                                    if visibleStatus == False:
                                        bStatus = True
                                        break
                                    elif visibleStatus == True and iCount == 7:
                                       bStatus = False
                                       break
                                if pagedisplayed.lower().replace(" ","") == "accountdetails":
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${button.batchEntries.filterBatchEntries}"))
                                else:
                                    print "Alerts Page Batch Entry Details"
                                    self.wait_and_click_element(BuiltIn().get_variable_value("${button.advanceSearch.edit}"))
                                    if SECCode=='IAT':
                                        print "SEC Code : IAT"
                                        noOfFields = self.get_text("//table[@id='filterAdvancedActivityFieldsDialogContentTable']//span")
                                        if str(noOfFields)!='31 fields found in following SEC Code(s): IAT':
                                            raise AssertionError("31 fields found in following SEC Code(s): IAT")
                                filterStatus = self.wait_for_element_visible(BuiltIn().get_variable_value("${header.accountDetails.batchEntryDetails}","5s"))
                                searchStatus = self.check_search_checkbox_for_ODFI_batch_entry_details(dictVar)
                                print "searchStatus: "+str(searchStatus)
                                if searchStatus == True:
                                    selenium.click_element(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                                    for iCount in range(1,20):
                                        print "iCount: "+str(iCount)
                                        self.press_down_key(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                                        print "press down key"
                                        okStatus = self.verify_element_visible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                        print "okStatus" +str(okStatus)
                                        #if okStatus == False:
                                            #self.press_down_key(BuiltIn().get_variable_value("${header.batchEntryDetails.searchOptions}"))
                                            #self.press_down_key("//span[contains(text(),'32 fields found in following SEC Code(s): IAT'")
                                            #print "press down key after checking oKStatus"
                                        okBtnStatus = BuiltIn().run_keyword_and_return_status("Selenium2Library.focus",BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                        print"okBtnStatus is: "+str(okBtnStatus)
                                        if okBtnStatus==True:
                                            break
                                    for iCount in range(1,8):
                                        print "iCount: " +str(iCount)
                                        self.wait_and_click_element(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                        self.wait_for_element_invisible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"),"5s")
                                        visibleStatus = self.verify_element_visible(BuiltIn().get_variable_value("${button.batchEntryDetails.Ok}"))
                                        print "visibleStatus:" +str(visibleStatus)
                                        if visibleStatus == False:
                                            bStatus = True
                                            break
                                        elif visibleStatus == True and iCount == 7:
                                           bStatus = False
                                           break 
                                return bStatus

                       
                def get_table_rows_count_by_scrolling_Batch_Entries(self, parentLocator,parentScroll=''):
                    """Returns the total no of rows in a table by scrolling specifying scrolling knob locator"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #selenium.reload_page()
                    bStatus = True
                    while bStatus:
                        try:
                            self.wait_for_element_visible(parentLocator)
                            selenium.mouse_down(parentLocator)
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentLocator)
                            selenium.mouse_down(parentLocator)
                        try:
                            selenium.mouse_up(parentLocator)
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentLocator)
                            selenium.mouse_up(parentLocator)
                        try:
                            prevvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        except:
                            selenium.capture_page_screenshot()
                            print "selenium getattribute failed at: "+str(parentLocator+'@style')
                            prevvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        
                        print "Prev value: "+str(prevvalue)
                        #selenium.mouse_up(parentLocator)
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse down failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        try:
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        except:
                            selenium.capture_page_screenshot()
                            print "mouse up failed at: "+str(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')

                        try:
                            postvvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        except:
                            selenium.capture_page_screenshot()
                            print "selenium getattribute failed at: "+str(parentLocator+'@style')
                            postvvalue = selenium.get_element_attribute(parentLocator+'@style')[18:]
                        
                        print "Post value: "+str(postvvalue)
                        if(prevvalue!=postvvalue):
                            selenium.mouse_down(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                            selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                        else:
                            bStatus = False
                            break
                    print 'selenium.mouse_down'
                    #selenium.mouse_up(parentScroll+'//div[@class="ajs_tb_bar_down"]')
                    print 'selenium.mouse_up'
                    for iIndex in range(1,5):
                        self.wait_for_element_visible(parentLocator)
                        try:
                            selenium.mouse_over(BuiltIn().get_variable_value("${image.batchEntriePane.revert}"))
                        except:
                            print "mouser over on revert button"
                        selenium.mouse_over(parentLocator)
                        selenium.mouse_over(parentLocator)
                        self.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                        rwCnt = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                        if len(rwCnt)>1 and (str(rwCnt).find("-"))>0:
                            break
                    print "tooltip text - rwCnt:"+str(rwCnt)
                    rwCnt = rwCnt.split("-")
                    rwCnt = rwCnt[1].replace(" ","")
                    print "rwCnt:"+str(rwCnt)
                    #time.sleep(5)
                    #selenium.reload_page()
                    #self.wait_for_please_wait_option()
                    #time.sleep(5)
                    if rwCnt >= 1:
                        self.scroll_to_top()
                    return str(rwCnt)

                def date_comparison(self,date1,date2,symbol):
                    """It returns True or False"""
                    try:
                        print date1
                        print date2
                        dates = date1.split("/")
                        date1 = dates[1]+"/"+dates[0]+"/"+dates[2]
                        dates = date2.split("/")
                        date2 = dates[1]+"/"+dates[0]+"/"+dates[2]
                        newdate1 = time.strptime(str(date1), "%d/%m/%Y")
                        print "newdate1"+str(newdate1)
                        newdate2 = time.strptime(str(date2), "%d/%m/%Y")
                        print "newdate2"+str(newdate2)
                        if str(symbol) == ">":
                            print "Enterd in > conditon if block"
                            return newdate1 > newdate2
                        elif str(symbol) == "<":
                            print "Enterd in < conditon if block"
                            return newdate1 < newdate2
                        elif str(symbol) == "==":
                            print "Enterd in == conditon if block"
                            return newdate1 == newdate2
                        elif str(symbol)==">=":
                            print "Enterd in >= conditon if block"
                            return newdate1 >= newdate2
                        elif str(symbol)=="<=":
                            print "Enterd in <= conditon if block"
                            return newdate1 <= newdate2
                        else:
                            raise AssertionError("Please pass third argument either < or > or == or >= or<= and also check date values")
                    except:
                        raise AssertionError("Please pass third argument either < or > or == or >= or<= and also check date values")  

   
                def create_watch_list_for_ODFI_batch_entry_details(self,fieldName,dialogHeaderName,watchlistName,actualListOfValues,negationSymbol=''):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "CWL1"
                    self.click_on_desired_watch_list_for_ODFI_batch_entry_details(fieldName,dialogHeaderName)
                    print "CWL2"
                    for iCounter in range(0,3):
                        try:
                            list1=[]
                            print "CWL3"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            print "CWL4"
                            list1 = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            print "CWL5"
                            print str(list1)
                            print watchlistName in list1
                            if(watchlistName in list1):
                                print "CWL6 - DWL1"
                                desiredStatus = "False"
                                self.delete_watch_list(fieldName,dialogHeaderName,watchlistName,desiredStatus)
                            print "Select New.. from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            print "CWL7"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            print "CWL8"
                            dropdownSlectionStatus = self.wait_for_dropdown_selection("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            print "dropdownSlectionStatus: "+str(dropdownSlectionStatus)
                            if dropdownSlectionStatus==False:
                                selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select","New...")
                            fieldStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div[contains(@id,'watchListDialogForm')]//input")
                            if fieldStatus == True:
                                print "CWL9 - Enter Watch List Name"
                                selenium.input_text("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Name:')]/parent::div[contains(@id,'watchListDialogForm')]//input",watchlistName)
                                time.sleep(2)
                                try:
                                    selenium.capture_page_screenshot()
                                    print "screen captured"
                                except:
                                    print "Exception while capturing screenshot"
                                if negationSymbol=="-":
                                    print "CWL10 - Acct Text"
                                    negationValue = "-"+str(actualListOfValues)
                                    self.type_keys_into_textbox("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div[contains(@id,'watchListDialogForm')]//textarea",negationValue)
                                else:
                                    print "CWL10 - Rem Text"
                                    print "else part"
                                    self.type_keys_into_textbox("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div[contains(@id,'watchListDialogForm')]//textarea",actualListOfValues)
                                self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                self.wait_and_click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                saveButtonInvisibleStatus = self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "saveButtonInvisibleStatus: " +str(saveButtonInvisibleStatus)
                                if saveButtonInvisibleStatus == False:
                                    saveButtonInvisibleStatus = self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                    print "saveButtonInvisibleStatus: " +str(saveButtonInvisibleStatus)
                                print "Watch List Created success fully"
                                return True
                            else:
                                continue
                        except: 
                            print "Watch List creation failed"
                            continue
                    return False

                def select_name_from_watchlist_for_ODFI_batch_entry_details(self,fieldName,dialogHeaderName,watchlistName,desiredWatchListResetClickStatus=''):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    bStatus = self.click_on_desired_watch_list_for_ODFI_batch_entry_details(fieldName,dialogHeaderName,desiredWatchListResetClickStatus)
                    if bStatus == False:
                        print "Click on Desired watchlist failed"
                        return False
                    for iCounter in range(1,5):
                        try:
                            print "Select desired Watch List Name from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            dropDownStatus = self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                            return True
                        except:
                            print "Watch List Not Selected"
                    return False
                
                def click_on_desired_watch_list_for_ODFI_batch_entry_details(self,fieldName,dialogHeaderName,clickOnResetStatusInWatchlist=''):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    wStatus = False
                    for iCont in range(0,5):
                        print "iCont: "+str(iCont)
                        try:
                            print "batchEntryDetailsDialogBox is visible: "+str(self.wait_for_element_present("//table[@id='filterAdvancedActivityFieldsDialogContentTable']"))
                            selenium.click_element("//div[@class='fadvChkAndTitleCell']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                            try:
                                selenium.mouse_over("//div[@class='fadvChkAndTitleCell']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                print "Mouse hovering done"
                            except:
                                print "Mouse hvering not done"
                            try:
                                selenium.click_element("//div[@class='fadvChkAndTitleCell']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input/parent::div//img[contains(@class,'watchListIcon')]")
                                print "clicked icon"
                            except:
                                print "not clicked"
                            print "entered verify wl status"
                            wStatus =  self.verify_watchlist_status("5s")
                            print "Watch List opened successfully : " +str(wStatus)
                            if wStatus == True:
                                listStatus = self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                                print "listStatus:"+str(listStatus)
                                return True
                        except:
                            print "Watch List not opened" +str(wStatus)
                            continue
                    return False

                def edit_watch_list_for_ODFI_batch_entry_details(self,fieldName,dialogHeaderName,editDialogHeaderName,watchlistName,actualListOfValues):
                    """Create Watch List for desired advance search Field"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    print "EWL1"
                    self.click_on_desired_watch_list_for_ODFI_batch_entry_details(fieldName,dialogHeaderName)
                    print "EWL2"
                    try:
                        list1=[]
                        print "EWL3"
                        self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "EWL4"
                        list1 = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                        print "EWL5"
                        print str(list1)
                        print watchlistName in list1
                        if(watchlistName in list1):
                            print "Select watchlistName from Dropdown field status "+ str(self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select"))
                            print "EWL7"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                            selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",watchlistName)
                            print "EWL8"
                            self.wait_for_element_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Edit')]")
                            selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Edit')]")
                            time.sleep(6)
                            print "EWL9"
                            print "edihrearderName: " +str(editDialogHeaderName)
                            
                            editStatus = self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]","5s")
                            print "EWL9-b"
                            print editStatus
                            if editStatus == True:
                                print "EWL10 - Enter Watch List Values"
                                time.sleep(4)
                                self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea")
                                print "EWL11"
                                self.clear_text("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea")
                                self.type_keys_into_textbox("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//b[contains(text(),'Values:')]/parent::div//textarea",actualListOfValues)
                                print "EWL12"
                                self.wait_for_element_visible("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL13"
                                selenium.click_element("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL14"
                                self.wait_for_element_not_present("//div[contains(text(),'"+str(editDialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Save')]")
                                print "EWL15"
                                time.sleep(4)
                                selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                                print "EWL16"
                                self.wait_for_element_not_present("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                                print "Watch List Edited success fully"
                    except: 
                        print "Watch List not Edited"
                        return False
                    return True
                
                def validate_watch_list_results_with_search_citeria_in_ODFI(self,fieldName,dialogHeaderName,name,values,ActualListOfValues,columnName,NegationSymbol=''):
                    """Click on Desired watch list and i will select the desired name snd hits the show results button and
                        verify the results from search results table with search criteria """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    try:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    except:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    listOfValues = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    if name not in listOfValues:
                        print "Error:" +str(name)+ "in Watch List Dropdown is not Saved."
                        raise AssertionError("Error:" +str(name)+ "in Watch List Dropdown is not Saved.")
                    selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",name)
                    self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    if fieldName== "Account":
                        self.wait_for_element_visible("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element(BuiltIn().get_variable_value("${link.adminUsers.showResults}"))
                    else:
                        self.wait_for_element_visible("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        selenium.click_element("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        valueInField = selenium.get_element_attribute("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input@value")
                        dict = {} 
                        dict[str(fieldName)] = str(valueInField)
                        self.enter_and_validate_advanced_search_fields_for_ODFI(dict)
                    locator1 = "//a[@title='Account Detail']"
                    locator2 = BuiltIn().get_variable_value("${label.alerts.noMatchingDataFound}")
                    try:
                        self.any_one_element_should_be_visible(locator1,locator2)
                    except:
                        print "Error in this keyword"
                    pageName = 'alerts'
                    pageName = str(pageName)
                    rowCount = self.get_session_count_from_table(pageName)
                    print "row count "+str(rowCount)
                    listOfDesiredColumnValues = []
                    listOfDesiredColumnValues = self.get_table_values_into_list_by_down_arrow(BuiltIn().get_variable_value("${table.alerts.matchingRows}"),BuiltIn().get_variable_value("${table.alerts.searchResults.knob}"),BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"),columnName,False,rowCount)
                    if NegationSymbol=="-":
                        print "Neagtion Validation"
                        ActualListOfValues
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        if bstatus==True:
                            status=False
                        else:
                            status=True
                      
                    else:
                        print " Validation"
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        status=bstatus
                    combindsStatusList=[]
                    combindsStatusList.append(rowCount)
                    combindsStatusList.append(status)
                    return combindsStatusList

                def validate_watch_list_results_with_search_citeria_in_ODFI(self,fieldName,dialogHeaderName,name,values,ActualListOfValues,columnName,NegationSymbol=''):
                    """Click on Desired watch list and i will select the desired name snd hits the show results button and
                        verify the results from search results table with search criteria """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    self.click_on_desired_watch_list(fieldName,dialogHeaderName)
                    try:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    except:
                        self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    listOfValues = selenium.get_list_items("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select")
                    if name not in listOfValues:
                        print "Error:" +str(name)+ "in Watch List Dropdown is not Saved."
                        raise AssertionError("Error:" +str(name)+ "in Watch List Dropdown is not Saved.")
                    selenium.select_from_list_by_label("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//select",name)
                    self.wait_for_element_visible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    selenium.click_element("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    self.wait_for_element_invisible("//div[contains(text(),'"+str(dialogHeaderName)+"')]/parent::td/parent::tr/parent::tbody//parent::table//a[contains(text(),'Select')]")
                    if fieldName== "Account":
                        self.wait_for_element_visible("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element("//label[contains(text(),'"+str(fieldName)+"')]/parent::div//input")
                        selenium.click_element(BuiltIn().get_variable_value("${link.adminUsers.showResults}"))
                    else:
                        self.wait_for_element_visible("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        selenium.click_element("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input")
                        valueInField = selenium.get_element_attribute("//div[@id='advanced']//label[contains(text(),'"+str(fieldName)+"')]/parent::div/following-sibling::div//input@value")
                        dict = {} 
                        dict[str(fieldName)] = str(valueInField)
                        self.enter_and_validate_advanced_search_fields_for_ODFI(dict)
                    locator1 = "//a[@title='Account Detail']"
                    locator2 = BuiltIn().get_variable_value("${label.alerts.noMatchingDataFound}")
                    try:
                        self.any_one_element_should_be_visible(locator1,locator2)
                    except:
                        print "Error in this keyword"
                    pageName = 'alerts'
                    pageName = str(pageName)
                    rowCount = self.get_session_count_from_table(pageName)
                    print "row count "+str(rowCount)
                    listOfDesiredColumnValues = []
                    listOfDesiredColumnValues = self.get_table_values_into_list_by_down_arrow(BuiltIn().get_variable_value("${table.alerts.matchingRows}"),BuiltIn().get_variable_value("${table.alerts.searchResults.knob}"),BuiltIn().get_variable_value("${table.alerts.searchResults.barContainer}"),columnName,False,rowCount)
                    if NegationSymbol=="-":
                        print "Neagtion Validation"
                        ActualListOfValues
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        if bstatus==True:
                            status=False
                        else:
                            status=True
                      
                    else:
                        print " Validation"
                        bstatus = self.sub_list_comparision(ActualListOfValues,listOfDesiredColumnValues)
                        status=bstatus
                    combindsStatusList=[]
                    combindsStatusList.append(rowCount)
                    combindsStatusList.append(status)
                    return combindsStatusList

                def get_riskfactor_fullname_for_ODFI_advance_search(self,shortname):
                    riskFactorDict = {'BCreditAmt':'Batch Credit Amt',
                                      'BCreditCnt':'Batch Credits Count',
                                      'BDebitAmt':'Batch Debit Amt',
                                      'BDebitCnt':'Batch Debits Count',
                                      'BNewRecipRatio':'Batch New Recipient Ratio',
                                      'BCompanyName':'New Company Name',
                                      'BSECCode':'Batch SEC Code',
                                      'BVelocity':'Batch Velocity',
                                      'SuspAcct':'Suspicious Account',
                                      'TCreditAmt':'Originator Transaction Amount (Credit)',
                                      'TDebitAmt':'Originator Transaction Amount (Debit)',
                                      'TDuplicateCheck':'Duplicate check number',
                                      'TNewRecipient':'New Recipient for this Originator',
                                      'TRecipAcctDtl':'Originator Recipient Account Details',
                                      'TTRxnLocation':'Unusual Transaction Location',
                                      'TNewRecipient':'New Recipient',
                                      'BNewRecipPrcnt':'Batch New Recipient Percent'}
                    return riskFactorDict[shortname]

                def get_riskfactor_shortname_for_ODFI_advance_search(self,fullname):
                    riskFactorDict = {'Batch Credit Amt':'BCreditAmt',
                                      'Batch Credits Count':'BCreditCnt',
                                      'Batch Debit Amt':'BDebitAmt',
                                      'Batch Debits Count':'BDebitCnt',
                                      'Batch New Recipient Ratio':'BNewRecipRatio',
                                      'New Company Name':'BCompanyName',
                                      'Batch SEC Code':'BSECCode',
                                      'Batch Velocity':'BVelocity',
                                      'Suspicious Account':'SuspAcct',
                                      'Originator Transaction Amount (Credit)':'TCreditAmt',
                                      'Originator Transaction Amount (Debit)':'TDebitAmt',
                                      'Duplicate check number':'TDuplicateCheck',
                                      'New Recipient for this Originator':'TNewRecipient',
                                      'Originator Recipient Account Details':'TRecipAcctDtl',
                                      'Unusual Transaction Location':'TTRxnLocation',
                                      'New Recipient':'TNewRecipient',
                                      'Batch New Recipient Percent':'BNewRecipPrcnt'}
                    return riskFactorDict[fullname]

                def get_transactionlevel_riskfactors(self,riskfactors):
                    """getting transaction level risk factors short names"""
                    transactionRiskfactors = []
                    for icount in riskfactors:
                        shortname = self.get_riskfactor_shortname_for_ODFI_advance_search(icount)
                        print "getting transaction level risk factors short names"
                        transactionRiskfactors.append(shortname)
                    return transactionRiskfactors

                def get_batchlevel_riskfactors(self,riskfactors):
                    """getting transaction level risk factors ,which are starting with B"""
                    batchRiskfactors = []
                    for icount in riskfactors:
                        print "icount: "+str(icount)
                        shortname = self.get_riskfactor_shortname_for_ODFI_advance_search(icount)
                        print "getting transaction level risk factors ,which are starting with B"
                        if shortname[0] == 'B':
                            batchRiskfactors.append(shortname)
                    return batchRiskfactors
                
                def click_on_element(self,locator):
                    """It will click on expected element for 5times if exception occured"""
                    selenium = BuiltIn().get_library_instance("Selenium2Library")
                    elementStatus = self.wait_for_element_visible(locator,"30s")
                    if elementStatus == True:
                        for iCount in range(1,6):
                            try:
                                print "iCount:"+str(iCount)
                                selenium.click_element(locator)
                                return True
                            except:
                                print "exception raised"
                                if iCount == 5:
                                    print iCount+"in exception"
                                    print "Exception raised after five times also"
                                    return False
                    else:
                        print str(locator)+" is not in visible state"
                        return False

                def get_graph_color_for_ODFI(self):
                     """Returns the list of colors displayed on Graph by taking the 'colorIndex' as argument """
                     selenium = BuiltIn().get_library_instance('Selenium2Library')
                     CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                     iCount = 0
                     colorList = []
                     while(iCount<=int(4)):
                         #bStatus = CommonLibrary.wait_for_element_visible("//div[@id='chartPlacement_chart_grid']//div[contains(@id,'chartPlacement_acb_"+str(iCount)+"_0')]")
                         bStatus = selenium._is_visible("//div[@id='chartPlacement_chart_grid']//div[contains(@id,'chartPlacement_acb_"+str(iCount)+"_0')]")
                         print "visibility:"+str(bStatus)
                         if str(bStatus)!='None':
                             #index = self.get_element_index("//div[contains(@id,'chartPlacement_acb_"+str(colorIndex)+"_0')]")
                             sessionStyle = selenium.get_element_attribute("//div[@id='chartPlacement_chart_grid']//div[contains(@id,'chartPlacement_acb_"+str(iCount)+"_0')]@style")
                             print "sessionStyle://div[@id='chartPlacement_chart_grid']//div[contains(@id,'chartPlacement_acb_"+str(iCount)+"_0')]"+str(sessionStyle)
                             if sessionStyle.find('rgb(7, 183, 12)') > 0:
                                 colorList.append('green')
                             if sessionStyle.find('rgb(155, 226, 158)') > 0:
                                 colorList.append('lightGreen')
                             if sessionStyle.find('rgb(231, 207, 24)') > 0:
                                 colorList.append('yellow')
                             if sessionStyle.find('rgb(173, 32, 33)') > 0:
                                 colorList.append('red')
                         iCount = iCount + 1
                     return colorList

                def convert_one_timezone_to_other(self,timeToConvert,fromZone,toZone):
                    server_timezone = pytz.timezone(fromZone)
                    new_timezone = pytz.timezone(toZone)
                    dt = parse(timeToConvert)
                    current_time_in_new_timezone = server_timezone.localize(dt).astimezone(new_timezone)
                    return str(current_time_in_new_timezone.strftime("%m/%d/%Y %I:%M %p"))
                
                def get_chrome_browser_options(self):
                    
                    dictionary= {'profile.default_content_settings.popups':'0'} 
                    chrome_options = Options()
                    chrome_options.add_argument("--disable-extensions")
                    chrome_options.add_argument("test-type")
                    #chrome_options.add_argument("-incognito")
                    chrome_options.add_argument("--disable-popup-blocking")
                    chrome_options=chrome_options
                    return chrome_options

                
class est(datetime.tzinfo):
    def utcoffset(self, dt):
        """ returns the time and date"""
        return datetime.timedelta(hours=-4)
    def dst(self, dt):
        return datetime.timedelta(0)
