class Course:
    def __init__(self, code,index, type, group,location, day, time,week):
        self.code = code
        self.index = index
        self.location = location
        self.type = type
        self.group= group
        self.day = day
        if time == '':
            self.timeStart = ''
            self.timeEnd = ''
        else:
            timeList = time.split('-')
            self.timeStart = timeList[0]
            self.timeEnd = timeList[1]
        def weekCreation(week):
            if(week == ''):
                weekList = [1,2,3,4,5,6,7,8,9,10,11,12,13]
            else:
                for word in week:
                    if word in '123456789':
                        break
                    week = week.replace(word,'')
                weekList = []
                if '-' in week:
                    weekList = week.split('-')
                    weekListCp = weekList
                    weekList = []
                    for i in range(int(weekListCp[0]),int(weekListCp[1])+1):
                        weekList.append(i)
                elif ',' in week:
                    weekList = week.split(',')
                    weekList = [int(i) for i in weekList]
                else:
                    weekList = [1,2,3,4,5,6,7,8,9,10,11,12,13] 
            return weekList
        self.week = weekCreation(week)

test = Course("CZ3005","10218","LAB","TS1 ","SWLAB2 ","THU","1530-1730","Teaching Wk2,4,6,8,10,12")

