from werkzeug.utils import html
from course import Course
from course_index import CourseIndex
from tabulate import tabulate
import numpy as np
timeSlot = ['0830','0900','0930','1000','1030','1100','1130','1200','1230','1300','1330',\
    '1400','1430','1500','1530','1600','1630','1700','1730','1800','1830','1900','1930']
daySlot = ['MON','TUE','WED','THU','FRI']
weekSlot = []
for i in range(1,14):
    weekSlot.append(i)

class CalendarSpace:
    #def __init__(self):
    #    self.calendar = [[Course('','',',,','','','','','') \
    #        for x in range(len(daySlot))]for x in range(len(timeSlot))]
     #   self.courseIndexes = []
    def __init__(self,calendar= \
                    np.empty((len(weekSlot),len(timeSlot),len(daySlot)),dtype=object)\
                    ,courseIndexes= []):
        self.calendar = calendar        
        self.courseIndexes = courseIndexes
    
    
    def addTime(self,weekList,timeIndex,DayIndex, course):
        for week in weekList:
            self.calendar[week-1][timeIndex][DayIndex] = course
        for courseIndex in self.courseIndexes:
            if (courseIndex.code == course.code) and (courseIndex.index == course.index):
                return
        self.courseIndexes.append(CourseIndex(course.code,course.index))
    
    def removeTime(self,weekList,timeIndex,DayIndex,course):
        for week in weekList:
            self.calendar[week-1][timeIndex][DayIndex] = None
        for courseIndex in self.courseIndexes:
            if (courseIndex.code == course.code) and (courseIndex.index == course.index):
                self.courseIndexes.remove(courseIndex)
    
    def vacancyBool(self,weekList,timeIndex,DayIndex):
        flag = True
        for week in weekList:
            try:
                self.calendar[week-1][timeIndex][DayIndex].code
                flag = False
                break
            except: 
                flag = True
        return flag

    def printCalendar(self):
        print('\t',end='')
        for day in daySlot:
            print(f'{day:^20}',end='')
        print('')
        for idx,time in enumerate(timeSlot):
            calOut = (f'{time}\t|'
                f'{self.calendar[idx][0].index+self.calendar[idx][0].type:20}|'
                f'{self.calendar[idx][1].index+self.calendar[idx][1].type:20}|'
                f'{self.calendar[idx][2].index+self.calendar[idx][2].type:20}|'
                f'{self.calendar[idx][3].index+self.calendar[idx][3].type:20}|'
                f'{self.calendar[idx][4].index+self.calendar[idx][4].type:20}|'
            )
            print(calOut)
        for courseIndex in self.courseIndexes:
            print(f'{courseIndex.code}:{courseIndex.index}')
    
    def outputCalendar(self):
        with open("output.txt","a") as file:
            file.write('\t')
            for day in daySlot:
                file.write(f'{day:^20}')
            file.write('\n')
            for idx,time in enumerate(timeSlot):
                calOut = (f'{time}\t|'
                    f'{self.calendar[idx][0].index+self.calendar[idx][0].type:20}|'
                    f'{self.calendar[idx][1].index+self.calendar[idx][1].type:20}|'
                    f'{self.calendar[idx][2].index+self.calendar[idx][2].type:20}|'
                    f'{self.calendar[idx][3].index+self.calendar[idx][3].type:20}|'
                    f'{self.calendar[idx][4].index+self.calendar[idx][4].type:20}|'
                )
                file.write(calOut+'\n')
            for courseIndex in self.courseIndexes:
                file.write(f'{courseIndex.code}:{courseIndex.index}\n')   

    def calendarToHtml(self):
        htmlTable = []
        htmlHeader = daySlot
        for idx,time in enumerate(timeSlot):
            calList = [time]
            for i in range(5):
                indexDict = {}
                calAdd = "" 
                for j in range(len(weekSlot)):
                    courseIndexAdd =""
                    courseTypeAdd=""
                    try:
                        courseIndexAdd = self.calendar[j][idx][i].index
                        courseTypeAdd = self.calendar[j][idx][i].type 
                        if f"{courseIndexAdd} {courseTypeAdd}" not in indexDict.keys():
                            indexDict[f"{courseIndexAdd} {courseTypeAdd}"] = f"{j+1}|"     
                        else:
                            indexDictValue = indexDict[f"{courseIndexAdd} {courseTypeAdd}"]
                            indexDict[f"{courseIndexAdd} {courseTypeAdd}"] = f"{indexDictValue}{j+1}|"    
                    except:
                        calAdd = calAdd + ""
                for key, val in indexDict.items():
                    calAdd = calAdd + f"{key} {val} "
                calList.append(calAdd)
            htmlTable.append(calList)
        htmlTableAll = tabulate(htmlTable,htmlHeader,tablefmt='html') + '\n'
        db_dict= {}
        for courseIndex in self.courseIndexes:
            htmlTableAll = htmlTableAll + f'<h3>{courseIndex.code}:{courseIndex.index}</h3>'
            db_dict[courseIndex.code] = courseIndex.index
        htmlTableAll = htmlTableAll + "<button name='save' value=0 onclick=\"document.getElementByName('save').value=1\">Save</button>"
        return htmlTableAll, db_dict

    def reset(self):
        self.calendar = [[False for x in range(len(daySlot))]for x in range(len(timeSlot))]