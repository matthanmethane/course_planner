import requests
import copy
from html_table_parser import HTMLTableParser
from collections import defaultdict

payload = {
    'p_exam_dt': '',
    'p_start_time': '',
    'p_dept': '',
    'p_subj': '',
    'p_venue': '',
    'p_matric': '',
    'academic_session': 'Semester+2+Academic+Year+2020-2021',
    'p_plan_no': '104',
    'p_exam_yr': '2020',
    'p_semester': '2',
    'p_type': 'UE',
    'bOption': 'Next',
}

def table_response(course_code = ""):
    payload = {
        'p_exam_dt': '',
        'p_start_time': '',
        'p_dept': '',
        'p_subj': course_code,
        'p_venue': '',
        'p_matric': '',
        'academic_session': 'Semester+2+Academic+Year+2020-2021',
        'p_plan_no': '104',
        'p_exam_yr': '2020',
        'p_semester': '2',
        'p_type': 'UE',
        'bOption': 'Next',
    } 
    response = requests.post("https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.Get_detail", data = payload)
    parser = HTMLTableParser()
    parser.feed(response.text)
    table = parser.tables
    return(table[1][1])

def exam_crash_bool(courseList):
    exam_date_list = {}
    rev_exam_date_list = {}
    for course in courseList:
        exam_date_response = table_response(course)
        exam_date_str = exam_date_response[6]+ exam_date_response[7]+ exam_date_response[8]
        exam_date_list[exam_date_response[9]] = exam_date_str
    rev_exam_date_list = invert_dict(exam_date_list)
    print(rev_exam_date_list)
    crash_list = [values for key, values in rev_exam_date_list.items() if len(values) > 1]
    if(crash_list):
        crash_list.append("exam_crash")
        return crash_list
    else:
        return False

def exam_list_generator(courseList):
    exam_dict = {}
    for course in courseList:
        exam_info = table_response(course)
        exam_dict[course] = exam_info
    return exam_dict
        
def invert_dict(d):
    d_inv = defaultdict(list)
    for k, v in d.items():
        d_inv[v].append(k)
    return d_inv

#print(table_response("CZ3002"))
# 0Date 1Day 2Time 3CourseCode 4CourseName
#print(exam_crash_bool(["AAB20D","AC1103"]))
