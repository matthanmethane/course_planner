from course import Course

class CourseIndex:
    def __init__(self,code,index):
        self.code = code
        self.index = index
        self.Courses = []
    def addCourse(self,course):
        self.Courses.append(course)
        return self       