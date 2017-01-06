#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prettytable import PrettyTable
import xlwt


def GetAssemble(courseID, current, courseOrder, assemble):
	if courseID >= courseNum:
		assemble.append(current[:])
		current.pop()
		return 
	for i in range(len(courseOrder[courseID])):
		current.append(courseOrder[courseID][i])
		GetAssemble(courseID+1, current, courseOrder, assemble)
	if courseID:
		current.pop()
	return
			
class curriculum(object):
	info = []
	number = '-1'
	name = 'name'
	time = []
	school = 'HFUT'
	credit = -1
					
	def __init__(self, line):
		super(curriculum, self).__init__()
		line = line.strip().split()
		self.info = line
		self.number = line[0]
		self.name = line[1]
		self.school = line[3]
		self.credit = int(line[4])
		self.parseTime()

	def parseTime(self):
		rowTime = self.info[2]
		time = []
		rst = []
		day = '-1'
		#print self.name
		if self.school == "NTHU":
			time = [rowTime[i]+rowTime[i+1] for i in range(len(rowTime)) if i%2==0]
			rst = [[th_week_dic[i[0]],th_dic[i[1]]] for i in time]
		elif self.school == "NCTU":
			for s in rowTime:
				if s.isdigit():
					day = s
				else:
					time.append(day+s)
			rst = [[ct_week_dic[i[0]],ct_dic[i[1]]] for i in time]
		elif self.school == "NCU":
			for s in rowTime:
				if s.isalpha():
					day = s
				else:
					time.append(day+s)
			rst = [[cu_week_dic[i[0]],cu_dic[i[1]]] for i in time]
		# part for handle error inputing
		else:
			raise ValueError("Error School Name! ")
		self.time = rst				

	def printInfo(self):
		print self.number,
		print self.name,
		print self.time,
		print self.school

def FullTimeTable(assemble, course):
	classNum = 18
	timeTable = [['0']*classNum for i in range(5)]
	rst = []
	time = []
	flag = False
	cnt = 0
	thcnt = [0]
	ctcnt = [0]
	cucnt = [0]
	thcrd = [0]
	ctcrd = [0]
	cucrd = [0]
	for psb in assemble:
		psb = zip(range(len(psb[:])), psb[:])
		flag = False
		# reset to 0
		ctcnt[cnt] = 0
		thcnt[cnt] = 0
		cucnt[cnt] = 0
		ctcrd[cnt] = 0
		thcrd[cnt] = 0
		cucrd[cnt] = 0
		for i in psb:
			thisCourse = course[i[0]][i[1]]
			time = thisCourse.time
			for t in time:
				if timeTable[t[0]][t[1]] == '0':
					#timeTable[t[0]][t[1]] = thisCourse.number
					timeTable[t[0]][t[1]] = thisCourse.name
				else:
					flag = True
					#timeTable = [['0']*classNum for i in range(5)]
					break;
			# for count the curriculum number
			if thisCourse.school == "NTHU":
				thcnt[cnt] += 1
				thcrd[cnt] += thisCourse.credit
			elif thisCourse.school == "NCTU":
				ctcnt[cnt] += 1
				ctcrd[cnt] += thisCourse.credit
			elif thisCourse.school == "NCU":
				cucnt[cnt] += 1
				cucrd[cnt] += thisCourse.credit
			
			# there can only no more than 2 currculua from other school
			if ctcnt[cnt] + cucnt[cnt] > 3:
				flag = True


			# if time collide, break
			if flag:
				break;
		
		if not flag:
			cnt += 1
			thcnt.append(0)
			ctcnt.append(0)
			cucnt.append(0)
			thcrd.append(0)
			ctcrd.append(0)
			cucrd.append(0)
			rst = rst + timeTable 
		# reset timetable for next for loop
		timeTable = [['0']*classNum for i in range(5)]
	return [cnt, thcnt, ctcnt, cucnt, thcrd, ctcrd, cucrd], rst

if __name__ == '__main__':
	# file operation
	#file = open("curriculum.txt")
	file = open("current.txt")
	lines = file.readlines()
	file.close()

	# declare
	time = ['6:00~6:50', '7:00~7:50', 
			'8:00~8:50', '9:00~9:50', '下課20分鐘', '10:10~11:00', '11:10~12:00', 
			'12:10~13:00', 
			'13:20~14:10', '14:20~15:10', '下課20分鐘', '15:30~16:20', '16:30~17:20', 
			'17:30~18:20',
			'18:30~19:20', '19:30~20:20', '20:30~21:20', '21:30~22:20']
	th = [' ', ' ', '1', '2', ' ', '3', '4', 'n', '5', '6', ' ', '7', '8', '9', 'a', 'b', 'c', ' ']
	ct = ['M', 'N', 'A', 'B', ' ', 'C', 'D', 'X', 'E', 'F', ' ', 'G', 'H', 'Y', 'I', 'J', 'K', 'L']
	cu = [' ', ' ', '1', '2', ' ', '3', '4', 'Z', '5', '6', ' ',' 7', '8', '9', 'A', 'B', 'C', ' ']
	th_week = ['M', 'T', 'W', 'R', 'F']
	ct_week = ['1', '2', '3', '4', '5']
	cu_week = ['M', 'T', 'W', 'R', 'F']
	th_dic = dict(zip(th, range(len(th))))
	ct_dic = dict(zip(ct, range(len(ct))))
	cu_dic = dict(zip(cu, range(len(cu))))
	th_week_dic = dict(zip(th_week, range(len(th_week))))
	ct_week_dic = dict(zip(ct_week, range(len(ct_week))))
	cu_week_dic = dict(zip(cu_week, range(len(cu_week))))
	classNum = len(time)
	title = ["NCTU", "NTHU", "time", "M(1)", "T(2)", "W(3)", "R(4)", "F(5)"]

	# the number of curriculums
	courseNum = int(lines[-1][0])+1

	# course is a list to store the curriculum object
	course = [[] for i in range(courseNum)]
	for i in range(len(lines)):
		course[int(lines[i][0])].append(curriculum(lines[i]))
	#print course

	# fix the number of curriculum
	for i in range(len(course)):
		for j in range(len(course[i])):
			course[i][j].number = str(i)+str(j)
			#course[i][j].printInfo()

	# assemble is the all possibility 
	assemble = []
	current = []
	courseOrder = [range(len(i)) for i in course]
	GetAssemble(0, current, courseOrder, assemble)
	#print assemble
	#print len(assemble)

	# full the table and print 
	rst = FullTimeTable(assemble, course)
	cnt = rst[0][0]
	thcnt = rst[0][1]
	ctcnt = rst[0][2]
	cucnt = rst[0][3]
	thcrd = rst[0][4]
	ctcrd = rst[0][5]
	cucrd = rst[0][6]
	timeTable = rst[1]
	#print timeTable[0][8].__class__
	#print timeTable[0][8]
	#print thcnt
	#print ctcnt
	
	if timeTable == [['0']*classNum for i in range(5)]:
		print "no such timetable, find more curriculums!"
	else:
		print "%d alternative" % (cnt)
		rst = xlwt.Workbook()
		rstSheet = rst.add_sheet("sheet1", cell_overwrite_ok=True)
		sheetRows = 1 + classNum + 2 

		for c in range(cnt):
			info = '''
No. {0}
NTHU: {1}, credit: {4}
NCTU: {2}, credit: {5}
NCU : {3}, credit: {6}
			
			'''.format(c+1, thcnt[c],  ctcnt[c], cucnt[c], thcrd[c], ctcrd[c], cucrd[c])
			print info

			rstSheet.write(c*sheetRows+0, 0, info)
		
			# write title
			for i in range(len(title)):
				rstSheet.write(c*sheetRows+1, i, title[i])
			# write content
			for classes in range(classNum):
				row = [ct[classes], th[classes], time[classes]] + [ timeTable[i][classes] for i in range(c*5,(c+1)*5) ]
				for i in range(len(row)):
					rstSheet.write(c*sheetRows+1+classes+1, i, row[i].decode('utf-8'))

			# print in terminal
			tabel = PrettyTable(["NCTU", "NTHU", "time", "M(1)", "T(2)", "W(3)", "R(4)", "F(5)"])
			for classes in range(classNum):
				tabel.padding_width = 1
				tabel.add_row([ct[classes], th[classes], time[classes]] + [ timeTable[i][classes] for i in range(c*5,(c+1)*5) ])
			print tabel

		for i in range(len(title)):
			rstSheet.col(i).width = 256*20
		for i in range(cnt+1):
			rstSheet.row(i*sheetRows).set_style(xlwt.easyxf('font:height 720;'))
		rst.save("rst.xls")


# l1 = [1,2]
# l2 = [1,2,3]
# l3 = [1,2]
# l = [l1, l2, l3]
# current = []
# def get(course):
# 	if course > 2:
# 		print current
# 		current.pop()
# 		return
# 	for i in range(len(l[course])):
# 		current.append(l[course][i])
# 		get(course+1)
	
# 	if course:
# 		current.pop()
# 	return

# get(0)
