import requests
import copy
from pprint import pprint
from html_table_parser import HTMLTableParser
from course import Course
from course_index import CourseIndex
from calendarSpace import CalendarSpace
from exam_request import table_response as exam_tb_response

payload = {'acadsem': '2020;2',
    'r_course_yr': '',
    'r_subj_code': '',
    'r_search_type': 'F',
    'boption': 'Search',
    'acadsem': '2020;2',
    'staff_access': 'false'}


def table_response(payload):
    response = requests.post("https://wish.wis.ntu.edu.sg/webexe/owa/AUS_SCHEDULE.main_display1", data = payload)
    parser = HTMLTableParser()
    parser.feed(response.text)
    table = parser.tables
    return(table)
    

def request_course_name(link):   
    payload_cp = payload
    payload_cp['r_subj_code']=link
    table = table_response(payload_cp)  
    
    for i in range(0,len(table),2):
        course_code = table[i][0][0]
        course_title = table[i][0][1]
        print(f'{course_code}:{course_title}')

def get_course_schedule(link):   
    payload_cp = payload
    payload_cp['r_subj_code']=link
    table = table_response(payload_cp)  
    course_index = ''
    course_list = []
    for rows in table[1][1:]:
        
        if rows[0] != '':
            course_index = rows[0]
        course_type = rows[1]
        course_group = rows[2]
        course_day = rows[3]
        course_time = rows[4]
        course_location = rows[5]
        course_wk = rows[6]
        course = \
            Course(link,course_index,course_type,course_group,course_location,course_day,course_time,course_wk)
        course_list.append(course)
    course_index_list = []
    for course in course_list:
        flag = True
        #iIndex = 0
        for index_no in course_index_list:
            try:
                if course.index == index_no.index:
                    flag = False
                    index_no.addCourse(course)
                    #iIndex = i
                    break
            except:
                pass
        if(flag):
            course_index_list.append(CourseIndex(course.code,course.index).addCourse(course))
        #else:
            #course_index_list[iIndex].addCourse(course)
    return(course_index_list)




timeSlot = ['0830','0900','0930','1000','1030','1100','1130','1200','1230','1300','1330',\
    '1400','1430','1500','1530','1600','1630','1700','1730','1800','1830','1900','1930']
daySlot = ['MON','TUE','WED','THU','FRI']

def course_plan_bool(calendarSpace, courseIndex):
    flagAvail = True #Flag to make sure the index is good to be added
    for course in courseIndex.Courses:
        weekList = []
        weekList = course.week
        dayIndex,timeStartIndex,timeEndIndex = 0,0,0
        dayIndex = daySlot.index(course.day)
        timeStartIndex = timeSlot.index(course.timeStart)
        timeEndIndex = timeSlot.index(course.timeEnd)
        for i in range(timeStartIndex,timeEndIndex):
            if(calendarSpace.vacancyBool(weekList,i,dayIndex)):    
                flagAvail = (flagAvail and True) #All lec/tut/lab should be abled to added    
            else:
                flagAvail = False
    return flagAvail

def calendar_modify(courseIndex, calendarSpace, action):
    for course in courseIndex.Courses:
        weekList = copy.deepcopy(course.week)
        dayIndex,timeStartIndex,timeEndIndex = 0,0,0
        dayIndex = daySlot.index(course.day)
        timeStartIndex = timeSlot.index(course.timeStart)
        timeEndIndex = timeSlot.index(course.timeEnd)
        for i in range(timeStartIndex,timeEndIndex):
            if(action=='add'):
                calendarSpace.addTime(weekList,i,dayIndex,course)
            else:
                calendarSpace.removeTime(weekList,i,dayIndex,course)


def course_planner(courseList,calendarSpace=CalendarSpace(),resultList=None):
    if resultList == None:
        resultList = []
    for courseIndexes in courseList:
        for courseIndex in courseIndexes:
            if(course_plan_bool(calendarSpace,courseIndex)):
                calendar_modify(courseIndex,calendarSpace,'add')
                if(len(courseList)) == 1:
                    calendarSpaceAdd = copy.deepcopy(calendarSpace) 
                        #Deep Copy is used to create a clone with no shared variables
                        #between the original CalendarSpace and the copy
                    resultList.append(calendarSpaceAdd)
                    calendar_modify(courseIndex,calendarSpace,'remove')
                else:
                    course_planner(courseList[1:],calendarSpace,resultList)
                    calendar_modify(courseIndex,calendarSpace,'remove')
    return resultList
    
def exam_crash_bool(courseList):
    flag = False
    
    return flag


def ScheduleCtr(list): #Should return [[CalendarSpace]]
    courseScheduleList = []
    if len(list) < 1:
        return 
    else:
        for course in list:
            courseScheduleList.append(get_course_schedule(course))
        
        resultList = course_planner(courseScheduleList) 
        return resultList
