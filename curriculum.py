#!/usr/bin/env python
# -*- coding: utf-8 -*-
from prettytable import PrettyTable


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
					
	def __init__(self, line):
		super(curriculum, self).__init__()
		line = line.strip().split()
		self.info = line
		self.number = line[0]
		self.name = line[1]
		self.school = line[3]
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
		self.time = rst				

	def printInfo(self):
		print self.number,
		print self.name,
		print self.time,
		print self.school

def FullTimeTable(assemble, course):
	timeTable = [[0]*16 for i in range(5)]
	rst = []
	time = []
	flag = False
	cnt = 0
	ctcnt = [0]
	thcnt = [0]
	for psb in assemble:
		psb = zip(range(len(psb[:])), psb[:])
		flag = False
		ctcnt[cnt] = 0
		thcnt[cnt] = 0
		for i in psb:
			thisCourse = course[i[0]][i[1]]
			time = thisCourse.time
			for t in time:
				if timeTable[t[0]][t[1]] == 0:
					#timeTable[t[0]][t[1]] = thisCourse.number
					timeTable[t[0]][t[1]] = thisCourse.name
				else:
					flag = True
					#timeTable = [[0]*16 for i in range(5)]
					break;
			# for count the curriculum number
			if thisCourse.school == "NTHU":
				thcnt[cnt] += 1
			elif thisCourse.school == "NCTU":
				ctcnt[cnt] += 1
				
			# if time collide, break
			if flag:
				break;
		
		if not flag:
			cnt += 1
			thcnt.append(0)
			ctcnt.append(1)
			rst = rst + timeTable 
		# reset timetable for next for loop
		timeTable = [[0]*16 for i in range(5)]
	return [cnt, thcnt, ctcnt], rst

if __name__ == '__main__':
	# file operation
	file = open("curriculum.txt")
	lines = file.readlines()
	file.close()

	# declare
	th = [' ', ' ', '1', '2', '3', '4', 'n', '5', '6', '7', '8', '9', 'a', 'b', 'c', ' ']
	ct = ['M', 'N', 'A', 'B', 'C', 'D', 'X', 'E', 'F', 'G', 'H', 'Y', 'I', 'J', 'K', 'L']
	th_week = ['M', 'T', 'W', 'R', 'F']
	ct_week = ['1', '2', '3', '4', '5']
	th_dic = dict(zip(th, range(len(th))))
	ct_dic = dict(zip(ct, range(len(ct))))
	th_week_dic = dict(zip(th_week, range(len(th_week))))
	ct_week_dic = dict(zip(ct_week, range(len(ct_week))))

	# the number of curriculums
	courseNum = int(lines[-1][0])+1
	
	# course is a list to store the curriculum object
	course = [[] for i in range(courseNum)]
	for i in range(len(lines)):
		course[int(lines[i][0])].append(curriculum(lines[i]))
	
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
	
	# full the table and print 
	rst = FullTimeTable(assemble, course)
	cnt = rst[0][0]
	thcnt = rst[0][1]
	ctcnt = rst[0][2]
	timeTable = rst[1]
	if timeTable == [[0]*16 for i in range(5)]:
		print "no such timetable, find more curriculums!"
	else:
		print "%d alternative" % (cnt)
		for c in range(cnt):
			info = '''
No. {0}
NTHU: {1}
NCTU: {2}
			
			'''.format(c+1, thcnt[c],  ctcnt[c])
			print info
			
			file = open('rst.txt', 'a')
			file.writelines(info)
			file.close()
			
			tabel = PrettyTable(["NCTU", "NTHU", "M(1)", "T(2)", "W(3)", "R(4)", "F(5)"])
			for classes in range(16):
				tabel.padding_width = 1
				tabel.add_row([ct[classes], th[classes]] + [ timeTable[i][classes] for i in range(c*5,(c+1)*5) ])
			print tabel
			tabelStr = tabel.get_string()
			file = open('rst.txt', 'a')
			file.writelines(tabelStr.encode('utf8'))
			# file.
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
