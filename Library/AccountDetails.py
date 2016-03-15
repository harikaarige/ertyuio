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
import CommonLibrary
import win32clipboard
import collections

class AccountDetails:
    
                def session_bitmap_width(self,style):
                    '''Returns the session bitmap width'''
                    firstsessionstyle = style
                    sessionbitmapwidth = []
                    sessionbitmapwidth = firstsessionstyle.split(';')[2].split(':')[1].replace(' ','').replace('px','')
                    return sessionbitmapwidth

                def validate_timestamp_on_activities_pane(self,tStamp):
                    """Returns True if the 'tStamp' matches the pattern else Fails"""
                    pat='[0-9][0-9]:[0-9][0-9]'
                    if tStamp==(re.match(pat,tStamp)).group():
                        return True
                    raise AssertionError("Time Stamp does not match the expected Pattern")

                def _check_id_attribute_return_id(self,locator):
                    """Returns True id attribute has a value at the 'locator' else returns False """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sID = selenium.get_element_attribute(locator + "@id")
                    sID = sID.strip()
                    return sID

                def get_timeline_header_subvalues_by_mouseover_on_session_of_timeline(self, table_locator, headerName,session_number):
                    """Returns color for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    #rowStartIndex = int(self._get_element_index(table_locator+ "/tbody/tr/..//strong"),headerName)
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))                    
                    timeline_header = {}
                    iSessionCounter = 0
                    getlistofvaluesbymouseover = []
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            idvalue = self._check_id_attribute_return_id(table_locator+'/tbody/tr['+str(iCounter)+']')
                            print idvalue
                            idrow = idvalue.split('_')
                            lenidrow = len(idrow)
                            getrow = idrow[lenidrow-1]
                            CommonLibrary.wait_for_element_visible("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']")
                            selenium.mouse_over("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']")
                            valuedisplayed = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            getlistofvaluesbymouseover.append(valuedisplayed)
                        if not self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            break
                    return getlistofvaluesbymouseover
                    
                def get_timeline_sessionbitmap_hovered_text(self, table_locator, headerName,session_number):
                    """Returns color for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    print "rowCount="+str(rowCount)
                    gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    print "gettextofheader="+str(gettextofheader)
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))
                    print "rowSatrtIndex="+str(rowStartIndex)
                    sessionbitmapvalues = []
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            idvalue = self._check_id_attribute_return_id(table_locator+'/tbody/tr['+str(iCounter)+']')
                            print "id:"+idvalue
                            idrow = idvalue.split('_')
                            lenidrow = len(idrow)
                            getrow = idrow[lenidrow-1]
                            CommonLibrary.wait_for_element_visible("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']")
                            selenium.mouse_over("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']")
                            CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                            valuedisplayed = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            print "valuedisplayed="+str(valuedisplayed)
                            sessionbitmapvalues.append(valuedisplayed)
                        if not self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            break
                    return sessionbitmapvalues

                def match_activities_displayed_after_mouseover_on_sessionbitmap_to_actual_activities_displayed_on_pane(self,listofactivities):
                    """Takes list of activities displayed after mouse over on the selected session and returns a list by appending each activity based on
                       the number displayed beside the activity"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    mouseoveredactivities = []
                    mouseoveredactivities = listofactivities
                    listofactivitiesthathascnt = [x for x in mouseoveredactivities if any(c.isdigit() for c in x)]
                    listofactivitiessplitwithdelimiter = [words for segments in listofactivitiesthathascnt for words in segments.split(':')]
                    textcnt = range(0,len(listofactivitiessplitwithdelimiter),2)
                    exacttext = []
                    for icnt in textcnt:
                        exacttext.append(listofactivitiessplitwithdelimiter[icnt])
                    numberscnt = range(1,len(listofactivitiessplitwithdelimiter),2)
                    exactnums = []
                    for ele in numberscnt:
                        exactnums.append(int(listofactivitiessplitwithdelimiter[ele].replace('(','').replace(')','')))
                    appendnumberoftimesofeachactivity = []
                    for ele in range(0,len(exactnums)):
                        for iCount in range(1,int(exactnums[ele])+1):
                            appendnumberoftimesofeachactivity.append(exacttext[ele])
                    return appendnumberoftimesofeachactivity

                def get_activities_color_in_activity_graph(self):
                    """ Return square boxes color in activity graph"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    colorList=[]
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${label.accountDetail.detachedAcivitiesPane.activityGraph.nodesCount}"))
                    activityCntWithRisks = selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${label.accountDetail.detachedAcivitiesPane.activityGraph.nodesCount}"))
                    print "activityCntWithRisks:"+str(activityCntWithRisks)
                    for iCounter in range(1,int(activityCntWithRisks)+1):
                        currColor = selenium.get_element_attribute("//div[contains(@id,'wjstc_moveable_container_div_') and contains(@id,'_body_a_graph')]//div[contains(@onclick,'var _ai=timeline_activityGraph')]["+str(iCounter)+"]@style")
                        print "currColor:"+str(currColor)
                        if currColor.find('rgb(113, 190, 68)') > 0:
                        #if currColor.find('#71be44') > 0:
                            colorList.append('green')
                        elif currColor.find('rgb(234, 29, 49)') > 0:
                        #elif currColor.find('#ea1d31') > 0:
                            colorList.append('red')
                        #elif currColor.find('#ffde66') > 0:
                        elif currColor.find('rgb(255, 222, 102)') > 0:
                            colorList.append('yellow')
                        #elif currColor.find('#b8dbc4') > 0:
                        elif currColor.find('rgb(184, 219, 196)') > 0:
                            colorList.append('blue')
                    return colorList


                def get_class_color_for_activity_graph(self, color):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    color = str(color)
                    if color=='green':
                        return 'TLRisk1'
                    if color=='red':
                        return 'TLRisk4'
                    if color=='yellow':
                        return 'TLRisk3'
                    if color=='blue':
                        return 'TLRisk2'


                def get_timeline_sessionbitmap_hovered_text_for_entered_session(self, table_locator, headerName,session_number):
                    """Returns color for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))
                    sessionbitmapvalues = []
                    colorsdisplayed = []
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            idvalue = self._check_id_attribute_return_id(table_locator+'/tbody/tr['+str(iCounter)+']')
                            idrow = idvalue.split('_')
                            lenidrow = len(idrow)
                            getrow = idrow[lenidrow-1]
                            if selenium._is_element_present("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']//div[contains(@style,'ga_grad_4.gif') and contains(@style,'left:18px')]"):
                                selenium.mouse_over("//table[@id='ga_timelineTable_viewBodyTable']//tr[@id='ga_timeline_view_row_"+str(getrow)+"']//div[contains(@style,'ga_grad_4.gif') and contains(@style,'left:18px')]")
                                CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${text.tooltip}"))
                                valuedisplayed = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                                print "valuedisplayed"+valuedisplayed
                                sessionbitmapvalues.append(valuedisplayed)
                        if not self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            break
                    return sessionbitmapvalues


                def validate_session_pagination(self, table_locator, headerName):
                    """Validates the session pagination on Account Detail page according to the modefs alignment on the timeline. """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                   #gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            idvalue = self._check_id_attribute_return_id(table_locator+'/tbody/tr['+str(iCounter)+']')
                            print "id:"+idvalue
                            idrow = idvalue.split('_')
                            lenidrow = len(idrow)
                            getrow = idrow[lenidrow-1]
                            if selenium._is_element_present("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"r_td']/div/img"):
                                sessionselected = int(selenium.get_element_attribute("//input[@id='ga_next_session_entry_box']@value"))
                                CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"r_td']")
                                selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"r_td']")
                                CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"r_td']/div/img")
                                selenium.click_element("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"r_td']/div/img")
                                CommonLibrary.wait_for_element_invisible("//table[@id='detailsForm:cmdStatusOnlyDialogContentTable']//b[contains(text(),'Please wait')]")
                                time.sleep(5)
                                sessionafterrightpagination = int(selenium.get_element_attribute(BuiltIn().get_variable_value("${text.accountdetail.displayedsessionnumber}")))
                                sessiondiff = sessionafterrightpagination - sessionselected
                                if sessiondiff > 1:
                                    for iCounter in range(1,sessiondiff+1):
                                        sessioncolors = self.get_timeline_headers_color(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}"),headerName,sessionselected+iCounter)
                                        sessioncolorslist = sessioncolors.values()
                                        print 'none' not in sessioncolorslist
                                        if 'none' not in sessioncolorslist:
                                            raise AssertionError("pagination between Sessions does not selected the desired session")
                            if selenium._is_element_present("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"l_td']/div/img"):
                                CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"l_td']")
                                selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"l_td']")
                                CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"l_td']/div/img")
                                selenium.click_element("//div[@id='ga_timelineTable_viewTitleContainer']//tr[@id='ga_timeline_title_row_"+str(getrow)+"']//td[@id='ga_timeline_title_row_search_"+str(getrow)+"l_td']/div/img")
                                CommonLibrary.wait_for_element_invisible("//table[@id='detailsForm:cmdStatusOnlyDialogContentTable']//b[contains(text(),'Please wait')]")
                                time.sleep(5)
                                sessionafterleftpagination = int(selenium.get_element_attribute(BuiltIn().get_variable_value("${text.accountdetail.displayedsessionnumber}")))
                                sessiondiff = sessionafterrightpagination - sessionafterleftpagination
                                if sessiondiff > 1:
                                    for iCounter in range(1,sessiondiff+1):
                                        sessioncolors = self.get_timeline_headers_color(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}"),headerName,sessionafterrightpagination+iCounter)
                                        sessioncolorslist = sessioncolors.values()
                                        print 'none' not in sessioncolorslist
                                        if 'none' not in sessioncolorslist:
                                            raise AssertionError("pagination between Sessions does not selected the desired session")
                        if not self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            break
                    
                def convert_month_num_to_month_name(self,monthNum):
                    """"Returns month name for the given month number say as for '03' it returns 'march'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    monthNme = {'01':'January 2014','02':'February 2014','03':'March 2014','04':'April 2014','05':'May 2014','06 2014':'June 2014','07':'July 2014','08':'August 2014','09':'September 2014','10':'October 2014','11':'November 2014','12':'December 2014'}
                    return monthNme[monthNum]

                def get_activities_activity_popup(self,table_locator):
                    """Returns a list contains Activities of the Activities table located by 'table_locator' on Account Detail Page.
                    """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    list = []
                    iCounter = 2
                    while iCounter <= rowCount:
                        #currValue = selenium._get_text(table_locator+'/tbody/tr['+str(iCounter)+']/td[3]/span')
                        CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr['+str(iCounter)+']')
                        currValue = CommonLibrary.get_element_text(table_locator+'/tbody/tr['+str(iCounter)+']',2)
                        list.append(currValue)
                        iCounter+=2
                    return list

                def get_activities_from_activity_graph(self, activities_locator):
                    """Returns a list containing activities located at location 'activities_locator' from Account Detail page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    stateofactivitieslocator = selenium._is_element_present(activities_locator+'//div')
                    print "locator: "+str(activities_locator+'//div')
                    print "stateofactivitieslocator:"+str(stateofactivitieslocator)
                    rowCount = selenium.get_matching_xpath_count(activities_locator+'//div')
                    rowCount = int(rowCount)
                    print "rowCount:"+str(rowCount)
                    list = []
                    for iCounter in range(1,rowCount+1):
                        time.sleep(2)
                        CommonLibrary.wait_for_element_visible(activities_locator+'//div['+str(iCounter)+']')
                        currValue = selenium._get_text(activities_locator+'//div['+str(iCounter)+']')
                        print "currValue: "+str(currValue)
                        currValue = currValue.replace("...","")
                        currValue = currValue.strip()
                        list.append(currValue)
                    return list

                def get_session_num_with_color(self, locator, color):
                    """Takes arguments 'locator' and 'color' and returns the session number matching the color from the timeline sessions table   """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(locator)
                    sessionCnt = selenium.get_matching_xpath_count(locator)
                    print "sessionCnt: "+str(sessionCnt)
                    sessionCnt = int(sessionCnt)
                    if sessionCnt <= 2:
                       raise AssertionError("sessions not found")
                    iCounter=1
                    while iCounter <= sessionCnt-2:
                        CommonLibrary.wait_for_element_visible(locator)
                        sessionStyle = selenium.get_element_attribute(locator+'['+str(iCounter)+']@style')
                        print "success1"
                        dict = {'red': 'ga_rgrad_4.gif', 'green': 'ga_rgrad_1.gif', 'blue': 'ga_rgrad_2.gif'}
                        bStatus = dict[str(color)] in sessionStyle
                        print "success2"
                        if dict[str(color)] in sessionStyle:
                            print "success3"
                            return iCounter
                        iCounter+=1
                    return iCounter

                def get_timeline_sessions_color(self):
                    """Returns the list of colors from the timelineHeader of Account Detail page """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sessionCnt = selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineHeader}"))
                    sessionCnt = int(sessionCnt)
                    if sessionCnt <= 2:
                       raise AssertionError("sessions not found")
                    iCounter=1
                    colorlist=[]
                    while iCounter <= sessionCnt-2:
                        sessionStyle = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.timeLineHeader}") + "["+str(iCounter)+']@style')
                        if sessionStyle.find('ga_rgrad_4.gif') > 0:
                            colorlist.append('red')
                        elif sessionStyle.find('ga_rgrad_1.gif') > 0:
                            colorlist.append('green')
                        elif sessionStyle.find('ga_rgrad_2.gif') > 0:
                            colorlist.append('blue')
                        iCounter+=1
                    return colorlist

                def _check_id_attribute(self,locator):
                    """Returns True id attribute has a value at the 'locator' else returns False """
                    try:
                        selenium = BuiltIn().get_library_instance('Selenium2Library')
                        CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                        CommonLibrary.wait_for_element_visible(locator,"5s")
                        sID = selenium.get_element_attribute(locator + "@id")
                        sID = sID.strip()
                        print "id:" + sID + " locator:" + locator
                        if len(sID) == 0 :
                            return False
                        else:
                            return True
                    except:
                        return False

                def get_timeline_headers_color(self, table_locator, headerName,session_number):
                    """Returns color for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr',"5s")
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    #rowStartIndex = int(self._get_element_index(table_locator+ "/tbody/tr/..//strong"),headerName)
                    print "locator:"+table_locator+'/tbody/tr'
                    #gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr[3]',"5s")
                    gettextofheader = selenium.get_text(table_locator+'/tbody/tr[3]')
                    print "headertext:"+gettextofheader
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))                    
                    timeline_header = {}
                    iSessionCounter = 0
                    
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        #pending
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            #currText = selenium._get_text(table_locator+'/tbody/tr['+str(iCounter)+']/td[2]')
                            print "locator:"+table_locator+'/tbody/tr['+str(iCounter)+']'
                            #currText = CommonLibrary.get_element_text(table_locator+'/tbody/tr['+str(iCounter)+']',1)
                            CommonLibrary.wait_for_element_visible(table_locator+'/tbody/tr['+str(iCounter)+']',"5s")
                            currText = selenium.get_text(table_locator+'/tbody/tr['+str(iCounter)+']')
                            currText = currText.replace("...","")
                            print "currtext:"+str(currText)                                                
                            currText = currText.strip()
                            currColor = ''
                           
                            styleXpathCount = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}")+ "/tbody/tr["+str(iCounter)+"]/td[1]/div/div"))                            
                            for iStyleCounter in range(1,styleXpathCount+1):
                                currStyle = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}") + "/tbody/tr["+str(iCounter)+"]/td[1]/div/div[" + str(iStyleCounter)+"]@style")
                                print "currStyle:"+str(currStyle)
                                #check for bullets
                                ibulletPos1 = currStyle.find('background: url')
                                ibulletPos2 = currStyle.find('background: transparent url')
                                print "ibulletPos1:"+str(ibulletPos1)
                                print "ibulletPos2:"+str(ibulletPos2)
                                if(BuiltIn().get_variable_value('${BROWSER}') == 'ie'):
                                    if ibulletPos1<0:
                                        currColor = currStyle
                                        continue
                                else:
                                    if ibulletPos2<0:
                                        currColor = currStyle
                                        continue
                                if session_number == 1:                                    
                                    currColor = currStyle
                                    break                                
                                iLeft = currStyle.find("left")
                                
                                if iLeft <= 0:
                                    continue
                                #get the left value
                                start = 'left: '
                                end = 'px;'
                                iLeftValue = currStyle.split(start)[1].split(end)[0].strip()
                                iLeftValue = int(iLeftValue)
                                                                
                                #get the width
                                start = 'width: '
                                iWidthValue = currStyle.split(start)[1].split(end)[0].strip()
                                iWidthValue = int(iWidthValue)
                                
                                if iLeftValue == 1:
                                    iSessionStart = 1
                                else:
                                    iSessionStart = int(iLeftValue/17)
                                    iSessionStart = iSessionStart+1
                                    print "session start:" + str(iSessionStart)
                                    
                                if iSessionStart == session_number:
                                    currColor = currStyle
                                    break
                                
                                if iWidthValue == 14:
                                    iNoSessionInStyle = 1
                                else:
                                    iWidthValue = iWidthValue + 3 
                                    iNoSessionInStyle = int(iWidthValue/17)

                                   
                                iSessions = iSessionStart + (iNoSessionInStyle-1)
                                session_number = int(session_number)
                                print "session_number:"+str(session_number)
                                print "iSessions:"+str(iSessions)
                                print "iSessionStart:"+str(iSessionStart)
                                if (session_number <= iSessions) and (session_number >= iSessionStart) :
                                    currColor = currStyle
                                    print "currColor bfr:"+str(currColor)
                                    break
                            print "currColor:"+str(currColor)
                            if currColor.find('ga_grad_1.gif') > 0:
                                timeline_header[currText] = "green"
                            elif currColor.find('ga_grad_2.gif') > 0:
                                timeline_header[currText] = "blue"
                            elif currColor.find('ga_grad_3.gif') > 0:
                                timeline_header[currText] = "yellow"
                            elif currColor.find('ga_grad_4.gif') > 0:
                                timeline_header[currText] = "red"
                            else:
                                timeline_header[currText] = "none"     
                        else:
                            break
                    return timeline_header

                def get_headername_entries_from_tooltip(self,headername,session_number):
                    """Returns color for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    rowCount = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}")+'/tbody/tr'))
                    #rowStartIndex = int(self._get_element_index(table_locator+ "/tbody/tr/..//strong"),headerName)
                    rowStartIndex = int(CommonLibrary._get_element_index(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}")+ "/tbody/tr",headername))                    
                    timeline_header = {}
                    iSessionCounter = 0
                    self.collapse_time_line_details_pane()
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        
                        if self._check_id_attribute(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}")+'/tbody/tr['+str(iCounter)+']'):
                            #currText = selenium._get_text(table_locator+'/tbody/tr['+str(iCounter)+']/td[2]')
                            CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}")+'/tbody/tr['+str(iCounter)+']',1)
                            currText = CommonLibrary.get_element_text(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}")+'/tbody/tr['+str(iCounter)+']',1)
                            currText = currText.replace("...","")
                            currText = currText.strip()
                            print "currText:"+str(currText)
                        else:
                            break
                        if self._check_id_attribute("//table[@id='ga_timelineTable_viewBodyTable']/tbody/tr["+str(iCounter)+"]"):
                            CommonLibrary.wait_for_element_visible("//table[@id='ga_timelineTable_viewBodyTable']/tbody/tr["+str(iCounter)+"]/td/div/div")
                            selenium.mouse_over("//table[@id='ga_timelineTable_viewBodyTable']/tbody/tr["+str(iCounter)+"]/td/div/div")
                            toolTipText = selenium.execute_javascript("return document.getElementById('ArdentEdge.Util.tooltipId_tc').textContent")
                            #toolTipText = selinium.get_text("//div[@id='ArdentEdge.Util.tooltipId_tc']")
                            toolTipText = toolTipText.replace("...","")
                            toolTipText = toolTipText.strip()
                            print "toolTipText:"+str(toolTipText)
                        else:
                            break
                        timeline_header[currText] =  toolTipText
                    self.expand_time_line_details_pane()
                    return timeline_header.values()

                def get_timeline_details_having_multiple_values(self,headername,session_number):
                    """Returns values for specified headers 'headername' having multiple values """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    timelinedts = self.get_timeline_headers_color(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}"),headername,session_number)
                    timelist=[]
                    for timelineKey in timelinedts:
                        timelineValue = timelinedts.get(timelineKey)
                        if timelineValue == "none":
                            continue
                        timelist.append(timelineKey)
                        timelist.append(timelineValue)
                        break
                    return timelist

                def expand(self,locator):
                    """Expands heatmap headers pane """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sSrc = selenium.get_element_attribute(locator + "@src")
                    if "ga_Nw.png" in sSrc:
                        selenium.mouse_down(locator)
                        selenium.mouse_up(locator)

                def collapse(self,locator):
                    """collapse heatmap headers pane """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sSrc = selenium.get_element_attribute(locator + "@src")
                    if "ga_Yw.png" in sSrc:
                        selenium.mouse_down(locator)
                        selenium.mouse_up(locator)

                def expand_time_line_details_pane(self):
                    """Expands timeline details pane """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sStyleAtrr = selenium.get_element_attribute(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}") + "@style")                    
                    if 'zoom_carrot_up.png' in sStyleAtrr:
                        selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')

                def collapse_time_line_details_pane(self):
                    """Collapse timeline details pane"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sStyleAtrr = selenium.get_element_attribute(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}") + "@style")                    
                    if 'zoom_carrot_down.png' in sStyleAtrr:
                        selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')

                def verify_riskfactor_heatmap_with_pane_details(self,session_number):
                    """Verifies Riskfactor header details in heatmap with details in risk factor pane for the specified session number """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    self.expand("ga_activityDetails_expand_collaps_all_sections")
                    self.collapse_time_line_details_pane()
                    rfHeatMapdts = self.get_timeline_headers_color(BuiltIn().get_variable_value("${table.accountDetail.heatmapHeaders}"),"Risk Factor",session_number)
                    print "rfHeatMapdts:"+str(rfHeatMapdts)
                    self.expand_time_line_details_pane()
                    sDictValues = ''.join('{}:{}\n'.format(key, val) for key, val in sorted(rfHeatMapdts.items()))
                    print 'Risk Factor Time Line and Color displayed in heat map:\n' + sDictValues
                    self.expand_time_line_details_pane()
                    for sRFKey in rfHeatMapdts:
                        sRFValue = rfHeatMapdts.get(sRFKey)
                        if (sRFValue != "red") and (sRFValue != "yellow"):
                            CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${table.accountDetail.riskFactorPane}") + "/tbody/tr/..//span[contains(text(),'" +sRFKey + "')]","5s")
                            bExists = selenium._is_element_present(BuiltIn().get_variable_value("${table.accountDetail.riskFactorPane}") + "/tbody/tr/..//span[contains(text(),'" +sRFKey + "')]")
                            selenium.click_element("//div[@id='ga_riskFactors_container_']")
                            #CommonLibrary.press_down_key("//div[@id='ga_riskFactors_container_']")
                            if bExists == True:
                               raise AssertionError(sRFKey + ' is displayed in lower Risk Factor Pane when there is no color')
                            else:
                                print sRFKey + ' is not displayed in lower Risk Factor Pane as there is no color'
                            selenium.click_element("//div[@id='ga_riskFactors_container_']")
                            CommonLibrary.press_down_key("//div[@id='ga_riskFactors_container_']")
                            #CommonLibrary.press_down_key("//div[@id='ga_riskFactors_container_']")
                            continue
                        
                        colorAlert = sRFValue + "Alert"
                        sRFKey = sRFKey.replace("...","")
                        #selenium.mouse_scroll("//div[@id='ga_riskFactors_container_']")
                        print "entered:"
                        CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${table.accountDetail.riskFactorPane}") + "/tbody/tr/..//span[contains(text(),'" +sRFKey + "')]")
                        bExists = selenium._is_element_present(BuiltIn().get_variable_value("${table.accountDetail.riskFactorPane}") + "/tbody/tr/..//span[contains(text(),'" +sRFKey + "')]")
                        selenium.click_element("//div[@id='ga_riskFactors_container_']")
                        #CommonLibrary.press_down_key("//div[@id='ga_riskFactors_container_']")
                        #selenium.mouse_scroll("//div[@id='ga_riskFactors_container_']")
                        print "bExists:"+str(bExists)
                        if bExists == False:                            
                            raise AssertionError(sRFKey + ' is not displayed in Risk Factor Pane')
                        try:
                            actualColorAlert = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.riskFactorPane}") + "/tbody/tr/..//span[contains(text(),'" +sRFKey + "')]@class")
                            if actualColorAlert != colorAlert:
                                raise AssertionError(sRFKey + ' is displayed in Risk Factor Pane but the expected underline color is not displayed. Expected color:' + colorAlert + ', Actual color:'+ actualColorAlert)
                            print sRFKey + ' is displayed in Risk Factor Pane with underlined color as ' + sRFValue
                        except:
                            raise AssertionError(sRFKey + ' is displayed in Risk Factor Pane but not underlined with any color.  Expected color:' + sRFValue)                    
                    
                    return True

                def get_session_time_chart_sessions_color(self):
                    """Returns colors in the timechart"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${table.accountDetail.sessionTimeChart}") + "[contains(@id,'body_time_')]")
                    sessionCnt = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.sessionTimeChart}") + "[contains(@id,'body_time_')]"))
                    iCounter=0
                    colorlist=[]
                    while iCounter <= sessionCnt-1:                        
                        sessionStyle = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.sessionTimeChart}") + "[contains(@id,'body_time_"+str(iCounter)+ "')]@style")                        
                        if sessionStyle.find('rgb(234, 29, 49)') > 0:
                            colorlist.append('red')
                        elif sessionStyle.find('rgb(113, 190, 68)') > 0:
                            colorlist.append('green')
                        iCounter+=1
                    return colorlist

                def get_heatmap_headers(self, table_locator):
                    """Returns header names in heatmap(in timeline) """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')
                    headers = selenium._get_text(table_locator)
                    selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')
                    print headers
                    #tabseparated = headers.replace(" combined \(\d\)", "\t");
                    #tabseparated = re.sub(" \ncombined \(\d\)" ,"\t",headers);                    
                    #tabseparated = tabseparated.strip()
                    #hdrs = tabseparated.split("\t")
                    
                    tabseparated = re.sub("  combined \(\d\)  \n" ,"",headers);
                    tabseparated = re.sub("  combined \(\d\)  " ,"",tabseparated);
                    tabseparated = re.sub("combined \(\d\)" ,"",tabseparated);
                    hdrs = tabseparated.split("\n")
                    print hdrs
                    list = []
                    print "length:"+str(len(hdrs))
                    for iCounter in range(len(hdrs)):
                        sValue = hdrs[iCounter]
                        currValue = sValue.strip()
                        list.append(currValue)
                        if currValue=='':
                            list.remove(currValue)
                    return list

                def get_heatmap_headers_by_scrolling(self, table_locator):
                    """Returns header names in heatmap(in timeline) """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')
                    headers = selenium._get_text(table_locator)
                    #selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')
                    print headers
                    #tabseparated = headers.replace(" combined \(\d\)", "\t");
                    #tabseparated = re.sub(" \ncombined \(\d\)" ,"\t",headers);                    
                    #tabseparated = tabseparated.strip()
                    #hdrs = tabseparated.split("\t")
                    temp='combined'
                    tabseparated = re.sub("  combined \(\d\)  \n" ,"",headers);
                    tabseparated= re.sub("  combined \(\d\)  " ,"",tabseparated);
                    tabseparated = re.sub("combined \(\d\)" ,"",tabseparated);
                    hdrs = tabseparated.split("\n")
                    print hdrs
                    subheaders = []
                    print "length:"+str(len(hdrs))
                    for iCounter in hdrs:
                        sValue = iCounter
                        sValue=str(sValue)
                        sValue=sValue.lstrip()
                        sValue=sValue.rstrip()
                        if int(len(sValue))<=3:
                            print "spaces displayed in this index" + str(iCounter)
                        elif temp in sValue:
                            print "combined present in list"
                        else:
                            if sValue not in subheaders:
                                subheaders.append(str(sValue))
                    return subheaders

                def get_dts_in_session_pane(self, table_locator):
                    """Returns details in session pane in account details page  """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    rowCnt = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    list = []
                    for iCounter in range(rowCnt-1):
                            #classname = selenium.get_element_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'+'@class')
                        currValue = selenium.execute_javascript("return document.getElementsByClassName('sessOverviewTableBody')[0].getElementsByTagName('tr')["+str(iCounter)+"].getElementsByTagName('td')[0].textContent").strip()
                            #currValue = self.get_element_text(table_locator+'/tbody/tr['+str(iCounter)+']',0)
                        if len(currValue ) !=0:
                            list.append(currValue)
                    return list

                def select_session_in_timeline_table(self, sessionNumber):
                    """Clicks on the Session from the Timeline Session Header matched by the argument 'sessionNumber'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    totalSessions = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineSessionHeader}") + "/div/div"))
                    print "totalSessions:"+str(totalSessions)
                    CommonLibrary.wait_for_element_visible("//input[@id='ga_next_session_entry_box']")
                    selenium.input_text("//input[@id='ga_next_session_entry_box']","1")
                    CommonLibrary.wait_and_click_element("//div[@id='ga_accdet_btnPageGoto']/img")
                    time.sleep(8)
                    if sessionNumber <= totalSessions-2:
                        selenium.click_element(BuiltIn().get_variable_value("${table.accountDetail.timeLineSessionHeader}") + "/div/div["+str(sessionNumber)+"]")
                    else:
                         raise AssertionError('Session is not existing')

                def get_index_val(self,locator,expected):
                    """ Returns index value for the exact match with the expected value"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    rowCount = int(selenium.get_matching_xpath_count(locator))
                    print "rowCount:"+str(rowCount)
                    for iCounter in range(1,rowCount+1):
                        for index in range(1,5):
                            eleStatus = selenium._is_visible(locator+'['+str(iCounter)+']/td[2]')
                            print "eleStatus"+str(eleStatus)
                            actualVal = selenium.get_text(locator+'['+str(iCounter)+']/td[2]')
                            print "actualVal:"+str(actualVal)
                            if len(actualVal)>0:
                                break
                            else:
                                continue
                        if actualVal==expected:
                            return iCounter

                def verify_merged_or_not(self, table_locator, headerName, batchEntryVal, sessionNum):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sessionStart = sessionNum
                    print "headerName:"+str(headerName)
                    print "batchEntryVal:"+str(batchEntryVal)
                    print "sessionNum:"+str(sessionNum)
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    print "rowCount:"+str(rowCount)
                    rowStartIndex = int(self.get_index_val(table_locator+ "/tbody/tr",headerName))
                    print "rowStartIndex:"+str(rowStartIndex)
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        statusOfId = self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']')
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            timelineVal = selenium.get_text(table_locator+'/tbody/tr['+str(iCounter)+']')
                            print "timelineVal:"+str(timelineVal)
                            if timelineVal in batchEntryVal:
                                print "timelineVal matches batchEntryVal :"+str(timelineVal)
                                currStyle = selenium.get_element_attribute("//table[@id='ga_timelineTable_viewBodyTable']/tbody/tr["+str(iCounter)+"]/td/div/div@style")
                                print "currStyle" +str(currStyle)
                                strtIndex = currStyle.index('width: ')
                                print "strtIndex" +str(strtIndex)
                                index  = currStyle[strtIndex:].index('px')
                                print "index" +str(index)
                                widthVal = currStyle[strtIndex+7:strtIndex+index]
                                print "widthVal:"+str(widthVal)
                                NumOfSessions = (int(widthVal)+3)/17
                                print "NumOfSessions:"+str(NumOfSessions)
                                print "sessionStart:"+str(sessionStart)
                                widthStatus1 = str(currStyle).find('width: 14px')>0
                                widthStatus2 = str(currStyle).find('width: 17px')>0
                                if ((str(currStyle).find('width: 14px')>=0) or (str(currStyle).find('width: 17px')>=0)):
                                    return False
                                else:
                                    return True
                            else:
                                continue


                def verify_merged_colored_squares_for_headers_in_timeline(self, table_locator, headerName,batchEntryVal,sessionNum):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    #self.select_session_in_timeline_table(sessionNum)
                    bStatus = self.verify_merged_or_not(table_locator,headerName,batchEntryVal,sessionNum)
                    print "merged bstatus:"+str(bStatus)
                    # self.select_session_in_timeline_table(sessionNum)
                    timelineHdrsColorPrevSession = self.get_timeline_headers_color(table_locator,headerName,sessionNum)
                    print timelineHdrsColorPrevSession.values()
                    print "prevSession:"
                    prevSession = timelineHdrsColorPrevSession[batchEntryVal]
                    print prevSession
                    nextSessionNum = int(sessionNum)+1
                    print "nextSessionNum:"+str(nextSessionNum)
                    #self.select_session_in_timeline_table(str(sessionNum))
                    timelineHdrsColorCurrSession = self.get_timeline_headers_color(table_locator,headerName,str(nextSessionNum))
                    print timelineHdrsColorCurrSession.values()
                    print "currSession:"
                    currSession = timelineHdrsColorCurrSession[batchEntryVal]
                    print currSession
                    if bStatus == True:
                        if prevSession==currSession:
                            return True
                        else:
                                
                            raise AssertionError("mismatch in color for "+str(batchEntryVal)+" in Sessions "+str(sessionNum)+" and "+str(nextSessionNum)+"")

                    else:
                        if prevSession!=currSession:
                            return True
                        else:
                            raise AssertionError("cells are merged for mismatch of data and color for batch entry "+str(batchEntryVal)+ " in sessions "+str(sessionNum)+" and "+str(nextSessionNum)+"")


                def get_timeline_headers_subheaders(self, table_locator, headerName,session_number):
                    """Returns subheader names for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    #rowStartIndex = int(self._get_element_index(table_locator+ "/tbody/tr/..//strong"),headerName)
                    print "locator:"+table_locator+'/tbody/tr'
                    #gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    gettextofheader = selenium.get_text(table_locator+'/tbody/tr[3]')
                    print "headertext:"+gettextofheader
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))                    
                    timeline_header = {}
                    iSessionCounter = 0
                    
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        #pending
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            #currText = selenium._get_text(table_locator+'/tbody/tr['+str(iCounter)+']/td[2]')
                            print "locator:"+table_locator+'/tbody/tr['+str(iCounter)+']'
                            #currText = CommonLibrary.get_element_text(table_locator+'/tbody/tr['+str(iCounter)+']',1)
                            currText = selenium.get_text(table_locator+'/tbody/tr['+str(iCounter)+']')
                            currText = currText.replace("...","")
                            print "currtext:"+currText                                                
                            currText = currText.strip()
                            currColor = ''
                           
                            styleXpathCount = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}")+ "/tbody/tr["+str(iCounter)+"]/td[1]/div/div"))                            
                            for iStyleCounter in range(1,styleXpathCount+1):
                                currStyle = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}") + "/tbody/tr["+str(iCounter)+"]/td[1]/div/div[" + str(iStyleCounter)+"]@style")
                                
                                #check for bullets
                                ibulletPos = currStyle.find('BACKGROUND: url')
                               
                                if ibulletPos<=0:
                                    continue                                
                                if session_number == 1:                                    
                                    currColor = currStyle
                                    break                                
                                iLeft = currStyle.find("LEFT")
                                
                                if iLeft <= 0:
                                    continue
                                #get the left value
                                start = 'LEFT: '
                                end = 'px;'
                                iLeftValue = currStyle.split(start)[1].split(end)[0].strip()
                                iLeftValue = int(iLeftValue)
                                                                
                                #get the width
                                start = 'WIDTH: '
                                iWidthValue = currStyle.split(start)[1].split(end)[0].strip()
                                iWidthValue = int(iWidthValue)
                                
                                if iLeftValue == 1:
                                    iSessionStart = 1
                                else:
                                    iSessionStart = int(iLeftValue/17)
                                    iSessionStart = iSessionStart+1
                                    print "session start:" + str(iSessionStart)
                                    
                                if iSessionStart == session_number:
                                    currColor = currStyle
                                    break
                                
                                if iWidthValue == 14:
                                    iNoSessionInStyle = 1
                                else:
                                    iWidthValue = iWidthValue + 3 
                                    iNoSessionInStyle = int(iWidthValue/17)

                                   
                                iSessions = iSessionStart + (iNoSessionInStyle-1)
                                session_number = int(session_number)
                                if (session_number <= iSessions) and (session_number >= iSessionStart) :
                                    currColor = currStyle
                                    break
                            
                            if currColor.find('ga_grad_1.gif') > 0:
                                timeline_header[currText] = "green"
                            elif currColor.find('ga_grad_2.gif') > 0:
                                timeline_header[currText] = "blue"
                            elif currColor.find('ga_grad_3.gif') > 0:
                                timeline_header[currText] = "yellow"
                            elif currColor.find('ga_grad_4.gif') > 0:
                                timeline_header[currText] = "red"
                            else:
                                timeline_header[currText] = "none" 
                        else:
                            break
                    return timeline_header.keys()

                def get_timeline_header_colors(self, table_locator, headerName,session_number):
                    """Returns colors for specified header in timeline in account details page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    rowCount = int(selenium.get_matching_xpath_count(table_locator+'/tbody/tr'))
                    #rowStartIndex = int(self._get_element_index(table_locator+ "/tbody/tr/..//strong"),headerName)
                    print "locator:"+table_locator+'/tbody/tr'
                    #gettextofheader = CommonLibrary.get_element_text(table_locator+'/tbody/tr[3]',1)
                    gettextofheader = selenium.get_text(table_locator+'/tbody/tr[3]')
                    print "headertext:"+gettextofheader
                    rowStartIndex = int(CommonLibrary.get_index_val(table_locator+ "/tbody/tr",headerName))                    
                    timeline_header = {}
                    iSessionCounter = 0
                    
                    for iCounter in range(rowStartIndex+2,rowCount+1):
                        #pending
                        if self._check_id_attribute(table_locator+'/tbody/tr['+str(iCounter)+']'):
                            #currText = selenium._get_text(table_locator+'/tbody/tr['+str(iCounter)+']/td[2]')
                            print "locator:"+table_locator+'/tbody/tr['+str(iCounter)+']'
                            #currText = CommonLibrary.get_element_text(table_locator+'/tbody/tr['+str(iCounter)+']',1)
                            currText = selenium.get_text(table_locator+'/tbody/tr['+str(iCounter)+']')
                            currText = currText.replace("...","")
                            print "currtext:"+currText                                                
                            currText = currText.strip()
                            currColor = ''
                           
                            styleXpathCount = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}")+ "/tbody/tr["+str(iCounter)+"]/td[1]/div/div"))                            
                            for iStyleCounter in range(1,styleXpathCount+1):
                                currStyle = selenium.get_element_attribute(BuiltIn().get_variable_value("${table.accountDetail.timeLineViewBody}") + "/tbody/tr["+str(iCounter)+"]/td[1]/div/div[" + str(iStyleCounter)+"]@style")
                                print "currStyle:"+str(currStyle)
                                #check for bullets
                                ibulletPos = currStyle.find('background: url')
                                print "ibulletPos: "+str(ibulletPos)
                                if ibulletPos<=0:
                                    continue                                
                                if session_number == 1:                                    
                                    currColor = currStyle
                                    break
                                print "before ileft currStyle: "+str(currStyle)
                                iLeft = currStyle.find("left")
                                print "iLeft: "+str(iLeft)
                                if iLeft <= 0:
                                    continue
                                #get the left value
                                start = 'left: '
                                end = 'px;'
                                iLeftValue = currStyle.split(start)[1].split(end)[0].strip()
                                iLeftValue = int(iLeftValue)
                                print "iLeftValue: "+str(iLeftValue)
                                                                
                                #get the width
                                start = 'width: '
                                iWidthValue = currStyle.split(start)[1].split(end)[0].strip()
                                iWidthValue = int(iWidthValue)
                                print "iWidthValue: "+str(iWidthValue)
                                
                                if iLeftValue == 1:
                                    iSessionStart = 1
                                else:
                                    iSessionStart = int(iLeftValue/17)
                                    iSessionStart = iSessionStart+1
                                    print "session start:" + str(iSessionStart)
                                    
                                if iSessionStart == session_number:
                                    currColor = currStyle
                                    break
                                
                                if iWidthValue == 14:
                                    iNoSessionInStyle = 1
                                else:
                                    iWidthValue = iWidthValue + 3 
                                    iNoSessionInStyle = int(iWidthValue/17)

                                   
                                iSessions = iSessionStart + (iNoSessionInStyle-1)
                                session_number = int(session_number)
                                if (session_number <= iSessions) and (session_number >= iSessionStart) :
                                    currColor = currStyle
                                    break
                            print "currColor: "+str(currColor)
                            if currColor.find('ga_grad_1.gif') > 0:
                                timeline_header[currText] = "green"
                            elif currColor.find('ga_grad_2.gif') > 0:
                                timeline_header[currText] = "blue"
                            elif currColor.find('ga_grad_3.gif') > 0:
                                timeline_header[currText] = "yellow"
                            elif currColor.find('ga_grad_4.gif') > 0:
                                timeline_header[currText] = "red"
                            else:
                                timeline_header[currText] = "none" 
                        else:
                            break
                    return timeline_header.values()

                def get_tooltip_values_of_subheader_in_timeline(self,headerName):
                     selenium = BuiltIn().get_library_instance('Selenium2Library')
                     CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                     subheaderVal = selenium.get_text("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr/td[2]")
                     print "subheaderVal:"+str(subheaderVal)
                     valCnt = subheaderVal[subheaderVal.index('(')+1:subheaderVal.index(')')]
                     #self.collapse_time_line_details_pane()
                     actualList=[]
                     selenium.click_element("//table[@class='TLPageBackground']//td/strong[contains(text(),'"+str(headerName)+"')]/../preceding-sibling::td/img")
                     time.sleep(10)
                     for counter in range(1,int(valCnt)+1):
                        try:
                           print "Try block"
                           CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                           print("press down key in if condition1")
                           time.sleep(3)
                           if CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]","10s"):
                             CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                             print("press down key in if condition2")
                             time.sleep(3)
                             CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                             selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                             toolTipText = selenium.execute_javascript("return document.getElementById('ArdentEdge.Util.tooltipId_tc').textContent")
                             toolTipText = toolTipText.replace("...","")
                             toolTipText = toolTipText.strip()
                             print "toolTipText:"+str(toolTipText)
                             actualList.append(toolTipText)
                           else:
                             selenium.click_element("//div[@id='ga_timelineTable_viewBody']")
                             CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                             print("press down key in else condition")
                             time.sleep(5)
                             if CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]","10s"):
                                 CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                                 time.sleep(3)
                                 CommonLibrary.wait_for_element_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                                 selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                                 toolTipText = selenium.execute_javascript("return document.getElementById('ArdentEdge.Util.tooltipId_tc').textContent")
                                 toolTipText = toolTipText.replace("...","")
                                 toolTipText = toolTipText.strip()
                                 print "toolTipText:"+str(toolTipText)
                                 actualList.append(toolTipText)
                        except:
                           print "Exception"
                     return actualList

                #def get_tooltip_values_of_subheader_in_timeline(self,headerName):
                     selenium = BuiltIn().get_library_instance('Selenium2Library')
                     CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                     subheaderVal = selenium.get_text("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr/td[2]")
                     print "subheaderVal:"+str(subheaderVal)
                     valCnt = subheaderVal[subheaderVal.index('(')+1:subheaderVal.index(')')]
                     #self.collapse_time_line_details_pane()
                     actualList=[]
                     selenium.click_element("//table[@class='TLPageBackground']//td/strong[contains(text(),'"+str(headerName)+"')]/../preceding-sibling::td/img")
                     for counter in range(1,int(valCnt)+1):
                          if selenium._is_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]"):
                            selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                            toolTipText = selenium.execute_javascript("return document.getElementById('ArdentEdge.Util.tooltipId_tc').textContent")
                            toolTipText = toolTipText.replace("...","")
                            toolTipText = toolTipText.strip()
                            print "toolTipText:"+str(toolTipText)
                            actualList.append(toolTipText)
                          else:
                            CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                            CommonLibrary.press_down_key("//div[@id='ga_timelineTable_viewBody']")
                            if selenium._is_visible("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]"):
                                selenium.mouse_over("//div[@id='ga_timelineTable_viewTitleContainer']/table/tbody//tr//td[2]/strong[text()='"+str(headerName)+"']/../../following-sibling::tr["+str(counter+1)+"]")
                                toolTipText = selenium.execute_javascript("return document.getElementById('ArdentEdge.Util.tooltipId_tc').textContent")
                                toolTipText = toolTipText.replace("...","")
                                toolTipText = toolTipText.strip()
                                print "toolTipText:"+str(toolTipText)
                                actualList.append(toolTipText)
                     return actualList

                def get_session_months(self):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    sessionCnt = int(selenium.get_matching_xpath_count("//div[@id='ga_timelineTable_sliderBodyContainer']/div"))-1
                    print "sessionCnt:"+str(sessionCnt)
                    monthValues = []
                    dict = {'F':'February','S':'September','O':'October','N':'November','D':'December'}
                    for iCounter in range(1,sessionCnt+1):
                        print "iCounter:"+str(iCounter)
                        monthName = selenium.get_text("//div[@id='ga_timelineTable_sliderBodyContainer']/div["+str(iCounter)+"]")
                        print "monthName:"+str(monthName)
                        monthNameBfrSplit = monthName
                        monthName = monthName.split(' ')
                        print "monthName after split:"+str(monthName)
                        monthName = monthName[0][0]
                        print "Bfr monthName validation:"+str(monthName)
                        if iCounter==1 and sessionCnt>1:
                            nxtMonthName = selenium.get_text("//div[@id='ga_timelineTable_sliderBodyContainer']/div["+str(iCounter+1)+"]")
                            print "nxtMonthName:"+str(nxtMonthName)
                            nxtMonthName = nxtMonthName.split(' ')
                            nxtMonthName = nxtMonthName[0][0]
                            print "Bfr nxtMonthName validation:"+str(nxtMonthName)
                            if monthName == 'J' or monthName =='M' or monthName=='A':
                                if monthName == 'J':
                                    if nxtMonthName == 'F':
                                        monthVal = 'January'
                                        #continue
                                    elif nxtMonthName == 'J':
                                        monthVal = 'June'
                                        #continue
                                    elif nxtMonthName == 'A':
                                        monthVal = 'July'
                                        #continue
                                if monthName == 'M':
                                    if nxtMonthName == 'A':
                                        monthVal = 'March'
                                        #continue
                                    if nxtMonthName == 'J':
                                        monthVal = 'May'
                                        #continue
                                if monthName == 'A':
                                    if nxtMonthName == 'M':
                                        monthVal = 'April'
                                        #continue
                                    if nxtMonthName == 'S':
                                        monthVal = 'August'
                                        #continue
                            else:
                                monthVal = dict[monthName]
                        #elif iCounter == sessionCnt or iCounter > 1:
                        elif iCounter > 1:    
                            prevMonthName = selenium.get_text("//div[@id='ga_timelineTable_sliderBodyContainer']/div["+str(iCounter-1)+"]")
                            prevMonthName = prevMonthName.split(' ')
                            prevMonthName = prevMonthName[0][0]
                            print "Bfr prevMonthName validation:"+str(prevMonthName)
                            if monthName == 'J' or monthName =='M' or monthName=='A':
                                if monthName == 'J':
                                    if prevMonthName == 'D':
                                        monthVal = 'January'
                                        #continue
                                    elif prevMonthName == 'M':
                                        monthVal = 'June'
                                        #continue
                                    elif prevMonthName == 'J':
                                        monthVal = 'July'
                                        #continue
                                if monthName == 'M':
                                    if prevMonthName == 'F':
                                        monthVal = 'March'
                                        #continue
                                    if prevMonthName == 'A':
                                        monthVal = 'May'
                                        #continue
                                if monthName == 'A':
                                    if prevMonthName == 'M':
                                        monthVal = 'April'
                                        #continue
                                    if nxtMonthName == 'J':
                                        monthVal = 'August'
                                        #continue
                            else:
                                monthVal = dict[monthName]
                        elif sessionCnt==1:
                            monthValues.append(monthNameBfrSplit)
                            return monthValues
                            #monthVal = dict[monthName]
                        monthValues.append(monthVal)
                        print "lenghof the list:"+str(len(monthValues))
                        #print monthValues
                    return monthValues
                        
                                 
                     
                def collapse_and_expand_sessionDetails(self,action="collapse"):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    if str(action).lower()=="expand":
                        bstatus=CommonLibrary.wait_for_element_visible("//div[@id='ga_timeline_exp' and contains(@style,'zoom_carrot_up.png')]")
                        print "expand button status :"+str(bstatus)
                        if bstatus==True:
                            #selenium.click_element("//div[@id='ga_timeline_exp']/parent::div")
                            selenium.simulate("//div[@id='ga_timeline_exp']/parent::div","click")
                            CommonLibrary.wait_for_element_visible("//div[@id='ga_timeline_exp']/parent::div")
                    else:
                        bstatus=CommonLibrary.wait_for_element_visible("//div[@id='ga_timeline_exp' and contains(@style,'zoom_carrot_down.png')]")
                        print "collapse button status :"+str(bstatus)
                        if bstatus==True:
                            #selenium.click_element("//div[@id='ga_timeline_exp']/parent::div")
                            selenium.simulate("//div[@id='ga_timeline_exp']/parent::div","click")
                            CommonLibrary.wait_for_element_visible("//div[@id='ga_timeline_exp']/parent::div")

                def get_heatmap_headers_of_BW(self, table_locator):
                    """Returns header names in heatmap(in timeline) """
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium.simulate(BuiltIn().get_variable_value("${image.accountDetail.expandOrCollapseTimeLine}"),'click')
                    subheaders = []
                    temp='combined'
                    for iCount in range(0,5):
                        headers = selenium._get_text(table_locator)
                        print "headers text is" + headers
                        tabseparated = re.sub("  combined \(\d\)  \n" ,"",headers);
                        tabseparated = re.sub("  combined \(\d\)  " ,"",tabseparated);
                        tabseparated = re.sub("combined \(\d\)" ,"",tabseparated);
                        hdrs = tabseparated.split("\n")
                        header=[item for item in hdrs if item not in subheaders]
                        print "diffrence headers list is:"
                        print header
                        for iCounter in header:
                            sValue = iCounter
                            sValue=str(sValue)
                            sValue=sValue.lstrip()
                            sValue=sValue.rstrip()
                            if int(len(sValue))<=3:
                                print "spaces displayed in this index" + iCounter
                            elif temp in sValue:
                                print "combined present in list"
                            else:
                                if sValue not in subheaders:
                                    subheaders.append(str(sValue))
                        CommonLibrary.press_down_key("ga_timelineTable_viewBody")
                    return subheaders

                def get_timeline_sessionbitmap_values(self,headerName):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    bstatus=CommonLibrary.wait_for_element_visible("//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Yw.png']")
                    if bstatus==True:
                        CommonLibrary.click_element_and_check_expected_element("//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Yw.png']","//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Nw.png']")
                    count=selenium._get_text("//strong[contains(text(),'"+str(headerName)+"')]/parent::td/parent::tr/following-sibling::tr[1]/td[2]")
                    print "value is"+str(count)
                    count=str(count)
                    bstatus=CommonLibrary.wait_for_element_visible("//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Nw.png']")
                    if bstatus==True:
                        CommonLibrary.click_element_and_check_expected_element("//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Nw.png']","//img[@id='ga_activityDetails_expand_collaps_all_sections' and @src='../images/ga_Yw.png']")
                    count=count.split(' ')
                    cnt=count[1]
                    cnt=str(cnt)
                    cnt=cnt.replace('(','')
                    cnt=str(cnt)
                    cnt=cnt.replace(')','')
                    cnt=int(cnt)
                    values=[]
                    length=int(cnt)+2
                    print "length is ="+ str(length)
                    for counter in range (2,length):
                        print "counter value is"+ str(counter)
                        temp=selenium._get_text("//strong[contains(text(),'"+str(headerName)+"')]/parent::td/parent::tr/following-sibling::tr["+str(counter)+"]/td[2]")
                        print str(temp)
                        if temp.find("..")>=0:
                            temp=self.get_tooltip_value("//strong[contains(text(),'"+str(headerName)+"')]/parent::td/parent::tr/following-sibling::tr["+str(counter)+"]/td[2]")
                        values.append(str(temp))
                    return values

                def expand_or_collapse_AccountDetail_External_Info(self,action="collapse"):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    if str(action).lower()=="expand":
                        bstatus=CommonLibrary.wait_for_element_visible("//a[@id='accountExternalInfoButton' and @class='showAccountInfo']")
                        print "expand button status :"+str(bstatus)
                        if bstatus==True:
                            for iCounter in range(1,10):
                                print "Expand Status iCounter value is "+str(iCounter)
                                try:
                                    selenium.simulate("//a[@id='accountExternalInfoButton' and @class='showAccountInfo']","click")
                                    CommonLibrary.wait_for_element_visible("//a[@id='accountExternalInfoButton' and @class='hideAccountInfo']")
                                    return True
                                except:
                                    print "Account Details External Info button was not expandable"
                    else:
                        bstatus=CommonLibrary.wait_for_element_visible("//a[@id='accountExternalInfoButton' and @class='hideAccountInfo']")
                        print "collapse button status :"+str(bstatus)
                        if bstatus==True:
                            for icounter in range(1,10):
                                print "collapse Status iCounter value"+str(icounter)
                                try:
                                    selenium.simulate("//a[@id='accountExternalInfoButton' and @class='hideAccountInfo']","click")
                                    CommonLibrary.wait_for_element_visible("//a[@id='accountExternalInfoButton' and @class='showAccountInfo']")
                                    return True
                                except:
                                    print "Account Details External Info button was not collapsed"

                def get_tooltip_value(self,locator,tooltiplocaor=None):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    for icount in range(10):
                        try:
                            CommonLibrary.wait_for_element_visible(locator)
                            selenium.mouse_over(locator)
                            if tooltiplocaor==None:
                                valuedisplayed = selenium.get_text(BuiltIn().get_variable_value("${text.tooltip}"))
                            else:
                                valuedisplayed = selenium.get_text(tooltiplocaor)
                            length=len(valuedisplayed)
                            if length>=1:
                                print "Tool tip displayed"
                                return valuedisplayed 
                            else:
                                print "tooltip is not displayed for this locator"
                        except:
                            print "tooltip not displayed"

                def open_and_select_account_details_or_FraudMatch_window(self,table_locator,buttonLocator,columnName,accountName,expectedWindowName,windowsCount=2):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    try:
                        colNo=CommonLibrary.get_column_no_from_table(table_locator, columnName)
                        CommonLibrary.left_click_on_table_row(table_locator,colNo,accountName)
                        bStatus=CommonLibrary.wait_for_element_visible(buttonLocator)
                        if bStatus == True:
                            selenium.click_element(buttonLocator)
                            CommonLibrary.wait_for_new_window(windowsCount)
                            if expectedWindowName == 'acc':
                                windows=selenium.get_window_names()
                            else:
                                windows=selenium.get_window_titles()
                            for wName in windows:
                                bStats=CommonLibrary.string_should_contain(wName,expectedWindowName)
                                if bStats==True:
                                    selenium.select_window(wName)
                                    return wName
                    except:
                        print "exception occured while excuting this keyword"

                def validate_Account_Name_in_AccountDetail_Page(self,AccountName):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    for iCount in range(3):
                        try:
                            bStatus=CommonLibrary.wait_for_element_visible("accountExternalInfoButton")
                            if bStatus==True:
                                account=CommonLibrary.get_text("accountExternalInfoButton")
                                if AccountName==account:
                                    return True
                        except:
                            print "exception occured"
                    raise AssertionError("Account Names in Alerts page,Account Details page are different")

                def select_session_in_timeline(self,sessionNumber):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    sessionNumber=int(sessionNumber)
                    for iCount in range(3):
                        '''try:'''
                        bStatus=CommonLibrary.wait_for_element_visible("ga_next_session_entry_box")
                        if bStatus==True:
                            selenium.focus("ga_next_session_entry_box")
                            selenium.press_key("ga_next_session_entry_box","\b")
                            selenium.input_text("ga_next_session_entry_box",sessionNumber)
                            CommonLibrary.wait_and_click_element("//div[@id='ga_accdet_btnPageGoto']")
                            bstatus=CommonLibrary.wait_for_element_invisible("//div[contains(text(),'Searching...') and @id='detailsForm:cmdStatusOnlyDialogHeader']")
                            for iCount in range(10):
                                Session=CommonLibrary.get_text("//div[@id='sessionOverviewTableHdr']//b")
                                bStatus=CommonLibrary.string_should_contain(str(Session),str(sessionNumber))
                                if bStatus==True:
                                    return True
                        '''except:
                            print "exception occurred"'''
                    raise AssertionError("expected session is not selected")

                def verify_and_validate_the_attributes_of_activity_details(self,activityName,listofActivityValues):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    expectedList=[]
                    count=selenium.get_matching_xpath_count("//div[@id='availableFields']/div/div")
                    print "xpath count is "+str(count)
                    for iCount in range(1,int(count)+1):
                        innerRowCount=selenium.get_matching_xpath_count("//div[@id='availableFields']/div/div["+str(iCount)+"]/div")
                        print "innerRow count is "+str(innerRowCount)
                        count1=1
                        bStatus=CommonLibrary.wait_for_element_visible("//div[@id='availableFields']/div/div["+str(iCount)+"]/div["+str(count1)+"]//label")
                        if bStatus==True:
                            text=CommonLibrary.get_text("//div[@id='availableFields']/div/div["+str(iCount)+"]/div["+str(count1)+"]//label")
                            print "text is "+str(text)
                            expectedList.append(text)
                            if int(innerRowCount)>2:
                                count1=int(count1)+2
                                text=CommonLibrary.get_text("//div[@id='availableFields']/div/div["+str(iCount)+"]/div["+str(count1)+"]//label")
                                expectedList.append(text)
                    print "list value is "
                    print expectedList
                    if ((len(expectedList) == len(listofActivityValues)) and(all(i in expectedList for i in listofActivityValues))):
                        print 'True'
                    else:
                        raise AssertionError("Lists are not equal")
                    CommonLibrary.wait_for_element_visible("//table[@id='filterAdvancedActivityFieldsDialogContentTable']//a[contains(text(),'Ok')]")
                    selenium.click_element("//table[@id='filterAdvancedActivityFieldsDialogContentTable']//a[contains(text(),'Ok')]")
               
                def verify_account_dts_info_displayed_on_top_of_page(self,totalSessionCount,account,url=''):
                    """1)verify account detail information button displayed on the top of the page.
                       2)validate the hide records after clicking on Account detail information button."""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    if url == '':
                        url = BuiltIn().get_variable_value("${SUBDOMAINURL}")
                    bStatus = CommonLibrary.verify_element_present("//a[@id='accountExternalInfoButton' and @class='hideAccountInfo']")
                    if bStatus==False:
                        CommonLibrary.click_element_and_check_expected_element(BuiltIn().get_variable_value("${link.accountDetail.accountInfo}"))
                    if url == BuiltIn().get_variable_value("${SUBDOMAINURL}"):
                        actualTotalSessions = CommonLibrary.get_text("//b[contains(text(),'Total Sessions:')]/parent::th/following-sibling::td/div")
                    else:
                        actualTotalSessions = CommonLibrary.get_text("//b[contains(text(),'Total Transfers:')]/parent::th/following-sibling::td/div")
                    actualTotalSessionslen = len(actualTotalSessions)
                    if actualTotalSessionslen == 0:
                        print "Total session or Total transfer in account detail pane doesnot displayed."
                    BuiltIn().should_be_equal_as_strings(totalSessionCount,actualTotalSessions)
                    actualAccountInAccountDetail = CommonLibrary.get_text("//a[@id='accountExternalInfoButton']/h2")
                    BuiltIn().should_be_equal(account,actualAccountInAccountDetail)
                    if url == BuiltIn().get_variable_value("${SUBDOMAINURL}"):
                        firstSessionTime = CommonLibrary.get_text("//div[@id='accountExternalInfo']//th/b[contains(text(),'First Session')]/../following-sibling::td/div")
                        lastSessionTime = CommonLibrary.get_text("//div[@id='accountExternalInfo']//th/b[contains(text(),'Last Session')]/../following-sibling::td/div")
                    else:
                        firstSessionTime = CommonLibrary.get_text("//div[@id='accountExternalInfo']//tr//b[contains(text(),'First Transfer')]/../following-sibling::td/div")
                        lastSessionTime = CommonLibrary.get_text("//div[@id='accountExternalInfo']//tr//b[contains(text(),'Last Transfer')]/../following-sibling::td/div")
                    lengthOfFirstSession = len(firstSessionTime)
                    if lengthOfFirstSession == 0:
                        print "FirstSession or FirstTransfer Time is not displayed"
                    lengthOfLastSession = len(lastSessionTime)
                    if lengthOfLastSession == 0:
                        print "LastSession or LastTransfer Time is not displayed"

                def get_total_number_of_sessions(self):
                    """Getting the total number of session in the account detail page"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')                    
                    bStatus = CommonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${header.accountDetail.sessionDetails}"))
                    #selenium.element_should_be_visible(BuiltIn().get_variable_value("${header.accountDetail.sessionDetails}"))
                    sessionCount = selenium.get_matching_xpath_count("//div[@id='ga_timelineTable_viewHeaderContainer']/div")
                    print "sessionCount:" +str(sessionCount)
                    sessionCount = BuiltIn().convert_to_integer(sessionCount)
                    totalSessionCount = sessionCount-2
                    return totalSessionCount

                def select_session_for_account_detail(self,sessionNumber):
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    elementStatus = commonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${text.accountDetail.goToSession}"),"30s")
                    print "elementStatus:"+str(elementStatus)
                    if elementStatus != True:
                        BuiltIn().fail("'GoTo' entry box is not displayed in account details page.")
                    selenium.focus(BuiltIn().get_variable_value("${text.accountDetail.goToSession}"))
                    selenium.press_key(BuiltIn().get_variable_value("${text.accountDetail.goToSession}"),"\b")
                    selenium.input_text(BuiltIn().get_variable_value("${text.accountDetail.goToSession}"),sessionNumber)
                    commonLibrary.wait_and_click_element(BuiltIn().get_variable_value("${image.accountDetail.goToSession}"))
                    commonLibrary.wait_for_element_invisible("//div[contains(text(),'Searching...') and @id='detailsForm:cmdStatusOnlyDialogHeader']","30s")
                    for iCount in range(1,10):
                        newSession = commonLibrary.get_text("//div[@id='sessionOverviewTableHdr']//b")
                        print "newSession:"+str(newSession)
                        newSessionStatus = commonLibrary.string_should_contain(newSession,str(sessionNumber))
                        print "newSessionStatus:"+str(newSessionStatus)
                        if newSessionStatus == True:
                            break
                    
                def expand_or_collapse_headers_for_account_details(self):
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    for iCount in range(1,10):
                        commonLibrary.wait_for_element_visible("//img[@id='ga_activityDetails_expand_collaps_all_sections']","5s")
                        selenium.click_element("//img[@id='ga_activityDetails_expand_collaps_all_sections']")
                        src = commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${image.cases.expandOrCollapseAllSections}")+"@src")
                        print "src:"+str(src)
                        status = commonLibrary.string_should_contain(str(src),"ga_Yw.png")
                        print "status:"+str(status)
                        if status == True:
                            break
    
                def get_activites_from_account_detail_page_for_account_detail(self):
                    """It returns activities list from account details page"""
                    activitiesList = list()
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    activities = commonLibrary.get_text("//div[@id='activityListContainer']//table//td")
                    print "activities from sbefore plit(:"+str(activities)
                    activities = activities.split('(')
                    print "activities from split(:"+str(activities)
                    activities = activities[1].split(')')
                    print "activities from after split):"+str(activities)
                    numberOfActivities = int(activities[0])
                    print "numberOfActivities:"+str(numberOfActivities)
                    if numberOfActivities <= 4:
                        BuiltIn().fail("session range must be >4")
                    commonLibrary.wait_and_click_element("//img[@id='ga_activityDetails_expand_collaps_all_activities']")
                    numberOfActivities1 = selenium.get_matching_xpath_count("//div[@id='ga_activityDetails_container_']//table//tr[contains(@id,'row')]")
                    print "numberOfActivities1:"+str(numberOfActivities1)
                    numberOfActivities1 = int(numberOfActivities1)
                    for iCount in range(2,(numberOfActivities1 + 1),2):
                        activities = commonLibrary.get_text("//div[@id='ga_activityDetails_container_']//table//tr["+str(iCount)+"]//td[3]/span")
                        activitiesList.append(activities)
                        commonLibrary.press_down_key("//div[@id='ga_activityDetails_container_']")
                    print "activitiesList:"+str(activitiesList)
                    return activitiesList

                def get_wire_events_from_account_detail_page(self):
                    """return the activities from account details page in list format"""
                    activitiesList = list()
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    commonLibrary.wait_and_click_element(BuiltIn().get_variable_value("${button.alerts.accountDetailIcon}"))
                    time.sleep(5)
                    windowNames = selenium.get_window_names()
                    for window in windowNames:
                        bstatus = commonLibrary.string_should_contain(str(window),"acc")
                        if bstatus == True:
                            break
                    selenium.select_window(window)
                    activities = commonLibrary.get_text("//div[@id='activityListContainer']//table//td")
                    print "activities:"+str(activities)
                    commonLibrary.wait_and_click_element("//img[@id='ga_activityDetails_expand_collaps_all_activities']")
                    numberOfActivities = int(selenium.get_matching_xpath_count("//div[@id='ga_activityDetails_container_']//table//tr[contains(@id,'row')]"))
                    for iCount in range(2,numberOfActivities+1,2):
                        activity = commonLibrary.get_text("//div[@id='ga_activityDetails_container_']//table//tr["+str(iCount)+"]//td[3]/span")
                        print "activity:"+str(activity)
                        activitiesList.append(activity)
                        commonLibrary.press_down_key("//div[@id='ga_activityDetails_container_']")
                    print activitiesList
                    return activitiesList
                    
                def verify_expand_or_collapse_status_for_each_header_in_timeline(self,expandOrCollapseImageSource,URL):
                    """verifying the risk components groups are in expanded state or in collapsed state."""
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if URL == BuiltIn().get_variable_value("${SUBDOMAINURL}"):
                        timeLineHeadersList = ["Activity","Risk Factor","Country","State, City","Channel","Provider","Network","IPType","OS/Browser","User Agent"]
                    else:
                        timeLineHeadersList = ["Activity","Risk Factor","Originator Country","Originator State","Beneficiary Country","Beneficiary State","Direction","Business Code","Type","Subtype","Payment Method","Origination Method","Source","Transaction Amount","User Time","Time since last","Transfer Status"]
                    lengthOfHeaders = len(timeLineHeadersList)
                    for iCount in range(0,lengthOfHeaders):
                        statusOfEachHeader = commonLibrary.get_element_attribute_value("//table[@class='TLPageBackground']//strong[text()='"+str(timeLineHeadersList[iCount])+"']/../../td/img@src")
                        if str(expandOrCollapseImageSource) =="../images/ga_Nw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_N.png","Header:"+str(timeLineHeadersList[iCount])+" is not collapsed")
                        if str(expandOrCollapseImageSource) =="../images/ga_Yw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_Y.png","Header:"+str(timeLineHeadersList[iCount])+" is not expanded")
                def verify_scale_buttons(self):
                    """Verify scale buttons 1x, 2x, 3x"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    commonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${button.accountDetail.zoomMode3x}"))
                    selenium.simulate(BuiltIn().get_variable_value("${button.accountDetail.zoomMode3x}"),"click")
                    sessionColorStyleFor3xScaleButton = commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.accountDetail.sessionBitMapStyle}"))
                    sessionWidthFor3xZoom = self.session_bitmap_width(sessionColorStyleFor3xScaleButton)
                    commonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${button.accountDetail.zoomMode2x}"))
                    selenium.simulate(BuiltIn().get_variable_value("${button.accountDetail.zoomMode2x}"),"click")
                    sessionColorStyleFor3xScaleButton = commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.accountDetail.sessionBitMapStyle}"))
                    sessionWidthFor2xZoom = self.session_bitmap_width(sessionColorStyleFor3xScaleButton)
                    print "When click on the 2x button, each session bitmap icon width decrease to 2/3 of the full size icon"
                    widthOf3xZoom = int(int(sessionWidthFor3xZoom)*(0.666))
                    print int(int(sessionWidthFor3xZoom)*(0.666))
                    if int(sessionWidthFor2xZoom) != widthOf3xZoom:
                        raise AssertionError(str(sessionWidthFor2xZoom)+" and "+str(widthOf3xZoom)+" are not equal")
                    commonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${button.accountDetail.zoomMode1x}"))
                    selenium.simulate(BuiltIn().get_variable_value("${button.accountDetail.zoomMode1x}"),"click")
                    sessionColorStyleFor1xScaleButton = commonLibrary.get_element_attribute_value(BuiltIn().get_variable_value("${label.accountDetail.sessionBitMapStyle}"))
                    sessionWidthFor1xZoom = self.session_bitmap_width(sessionColorStyleFor1xScaleButton)
                    print "When click on the 1x button, each session bitmap icon width decrease to 1/3 of the full size icon"
                    widthOf2xZoom = int(int(sessionWidthFor2xZoom)*(0.666))
                    if int(sessionWidthFor1xZoom) != widthOf2xZoom:
                        raise AssertionError(str(sessionWidthFor1xZoom)+" and "+str(widthOf2xZoom)+" are not equal")
                    
                def collapse_headers_in_activities_container(self):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    for iCount in range(1,10):
                        commonLibrary.wait_for_element_visible(BuiltIn().get_variable_value("${image.activityDetailWndw.expandOrCollapse}"))
                        selenium.click_element(BuiltIn().get_variable_value("${image.activityDetailWndw.expandOrCollapse}"))
                        src = commonLibrary.get_element_attribute_value("//img[@id='ga_activityDetails_expand_collaps_all_activitieswindow']@src")
                        bStatus = commonLibrary.string_should_contain(str(src),"ga_Nw.png")
                        if bStatus ==  True:
                            break

                def Select_Item_and_view_account_detail_in_Alerts(self,table_locator,colNo,accountName,account='',row=0):
                    """it returns account detail window name"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    CommonLibrary.left_click_on_table_row(table_locator,colNo,accountName)
                    selenium.wait_until_page_contains_element("//a[@title='Account Detail']","5s")
                    selenium.page_should_contain_element("//a[@title='Account Detail']")
                    selenium.click_element("//a[@title='Account Detail']")
                    CommonLibrary.wait_for_new_window(2)
                    time.sleep(5)
                    windowNames=selenium.get_window_names()
                    windowsCount = 0
                    for wName in windowNames:
                      windowsCount = windowsCount + 1
                      bStatus=CommonLibrary.string_should_contain(str(wName),"acc")
                      print "account details window status" +str(bStatus)
                      if bStatus==True:
                         break
                      elif bStatus !=True and windowsCount == len(windowNames):
                        raise AssertionError("Expected window is not opened")
                    return wName

                def get_activites_from_account_detail_page_for_account_detail_BW(self):
                    """It returns activities list from account details page"""
                    activitiesList = list()
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    activities = commonLibrary.get_text("//div[@id='activityListContainer']//table//td")
                    commonLibrary.wait_and_click_element("//img[@id='ga_activityDetails_expand_collaps_all_activities']")
                    numberOfActivities1 = selenium.get_matching_xpath_count("//div[@id='ga_activityDetails_container_']//table//tr[contains(@id,'row')]")
                    print "numberOfActivities1:"+str(numberOfActivities1)
                    numberOfActivities1 = int(numberOfActivities1)
                    for iCount in range(2,(numberOfActivities1 + 1),2):
                        activities = commonLibrary.get_text("//div[@id='ga_activityDetails_container_']//table//tr["+str(iCount)+"]//td[3]/span")
                        activitiesList.append(activities)
                        commonLibrary.press_down_key("//div[@id='ga_activityDetails_container_']")
                    print "activitiesList:"+str(activitiesList)
                    return activitiesList

                def select_session_with_out_having_dot_symbols(self):
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    dotCount = int(selenium.get_matching_xpath_count("//div[contains(@id,'ga_timelineTable_case_2_')]"))
                    print "dotCount: "+str(dotCount)
                    if dotCount!= 0:
                        sessionNumber = 0
                        for icount in range(0,int(dotCount)):
                            print "0 iteration in if blosk"
                            bstatus = CommonLibrary.verify_element_visible("//div[contains(@id,'ga_timelineTable_case_2_"+str(icount)+"_0')]")
                            print "bstatus: "+str(bstatus)
                            if bstatus:
                                print "sessionNumber"+str(sessionNumber)
                                sessionNumber = sessionNumber + 1
                                if bstatus and icount == dotCount - 1:
                                    return sessionNumber + 1
                            else:
                                print "Enter in to else block"
                                bstatus1 = CommonLibrary.verify_element_visible("//div[contains(@id,'ga_timelineTable_case_2_"+str(icount)+"_1')]")
                                print "bstatus1"+str(bstatus1)
                                if bstatus1:
                                    sessionNumber = sessionNumber + 1
                                    print "sessionNumber"+str(sessionNumber) 
                                if (bstatus1 != True and icount >= 0) or (icount == dotCount - 1):
                                    return sessionNumber + 1    
                    else:
                        return 1

                def select_session_with_ctrl_click_in_timeline_table(self, sessionNumber):
                    """Clicks on the Session from the Timeline Session Header matched by the argument 'sessionNumber'"""
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    CommonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    print "sessionNumber: "+str(sessionNumber)
                    totalSessions = int(selenium.get_matching_xpath_count(BuiltIn().get_variable_value("${table.accountDetail.timeLineSessionHeader}") + "/div/div"))
                    print "totalSessions:"+str(totalSessions)
                    CommonLibrary.wait_for_element_visible("//input[@id='ga_next_session_entry_box']")
                    selenium.input_text("//input[@id='ga_next_session_entry_box']",sessionNumber)
                    CommonLibrary.wait_and_click_element("//div[@id='ga_accdet_btnPageGoto']/img")
                    time.sleep(5)
                    CommonLibrary.wait_for_element_invisible("//div[@id='detailsForm:cmdStatusOnlyDialogHeader']","10s")
                    print "wait_for_element_invisible"
                    #CommonLibrary.wait_and_click_element(BuiltIn().get_variable_value("${table.accountDetail.timeLineSessionHeader}"))
                    if int(sessionNumber) <= totalSessions-2:
                        CommonLibrary.press_control_key()
                        CommonLibrary.wait_and_click_element(BuiltIn().get_variable_value("${table.accountDetail.timeLineSessionHeader}") + "/div/div["+str(sessionNumber)+"]")
                    #else:
                         #raise AssertionError('Session is not existing')

                def verify_expand_or_collapse_status_for_each_header_in_timeline_for_RDFI(self,expandOrCollapseImageSource,URL):
                    """verifying the risk components groups are in expanded state or in collapsed state."""
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if URL == BuiltIn().get_variable_value("${RDFIURL}"):
                        timeLineHeadersList = ["Recipient Account Number","Risk Factor","SEC Code","Transaction Code","Recipient Name","Company Name","Company ID","ODFI ID"]
                    else:
                        timeLineHeadersList = ["Recipient Account Number","Risk Factor","SEC Code","Transaction Code","Recipient Name","Company Name","Company ID","ODFI ID"]
                    lengthOfHeaders = len(timeLineHeadersList)
                    for iCount in range(0,lengthOfHeaders):
                        statusOfEachHeader = commonLibrary.get_element_attribute_value("//table[@class='TLPageBackground']//strong[text()='"+str(timeLineHeadersList[iCount])+"']/../../td/img@src")
                        if str(expandOrCollapseImageSource) =="../images/ga_Nw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_N.png","Header:"+str(timeLineHeadersList[iCount])+" is not collapsed")
                        if str(expandOrCollapseImageSource) =="../images/ga_Yw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_Y.png","Header:"+str(timeLineHeadersList[iCount])+" is not expanded")

                def verify_expand_or_collapse_status_for_each_header_in_timeline_for_ODFI(self,expandOrCollapseImageSource,URL):
                    """verifying the risk components groups are in expanded state or in collapsed state."""
                    commonLibrary = BuiltIn().get_library_instance('CommonLibrary')
                    selenium = BuiltIn().get_library_instance('Selenium2Library')
                    if URL == BuiltIn().get_variable_value("${RDFIURL}"):
                        timeLineHeadersList = ["Company Name","Risk Factor","Trans Code","SEC Code","Company Id","Time since last"]
                    else:
                        timeLineHeadersList = ["Company Name","Risk Factor","Trans Code","SEC Code","Company Id","Time since last"]
                    lengthOfHeaders = len(timeLineHeadersList)
                    for iCount in range(0,lengthOfHeaders):
                        statusOfEachHeader = commonLibrary.get_element_attribute_value("//table[@class='TLPageBackground']//strong[text()='"+str(timeLineHeadersList[iCount])+"']/../../td/img@src")
                        if str(expandOrCollapseImageSource) =="../images/ga_Nw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_N.png","Header:"+str(timeLineHeadersList[iCount])+" is not collapsed")
                        if str(expandOrCollapseImageSource) =="../images/ga_Yw.png ":
                            BuiltIn().should_contain(statusOfEachHeader,"ga_Y.png","Header:"+str(timeLineHeadersList[iCount])+" is not expanded")            
