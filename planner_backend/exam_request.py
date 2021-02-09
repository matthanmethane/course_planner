import requests
import copy
from html_table_parser import HTMLTableParser

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

def table_response(payload):
    response = requests.post("https://wis.ntu.edu.sg/webexe/owa/exam_timetable_und.Get_detail", data = payload)
    parser = HTMLTableParser()
    parser.feed(response.text)
    table = parser.tables
    return(table)

print(table_response(payload))
# 0Date 1Day 2Time 3CourseCode 4CourseName

