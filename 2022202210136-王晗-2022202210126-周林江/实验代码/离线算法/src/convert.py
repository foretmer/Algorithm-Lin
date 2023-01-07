'''
C (587 233 220)
B [(108 76 30 40), (110 43 25 33), (92 81 55 39)]
LWH
WDH
//E1-2
C (587 233 220)
B [(91 54 45 32), (105 77 72 24), (79 78 48 30)]
'''
import csv
id=0
def generate(Width,Depth,Height,number,writer,flip_ratio):
	global id
	volume=Width*Depth*Height
	#with open("test.csv", "w") as csvfile:
		#writer = csv.writer(csvfile)
	
	ro_number = int(number * flip_ratio)
	
	for i in range(ro_number):
		id += 1
		writer.writerow([id, Depth, Width, Height, 1, volume])
	
	for i in range(number-ro_number):
		id += 1
		writer.writerow([id, Width, Depth, Height, 1, volume])

def convert(flip_ratio):
	file=open('../data.txt')
	lines=file.readlines()
	#lines[0]
	number=0
	isNumber=0
	con1=[]
	con=[]
	for i in lines[0]:
		if (i == ' ' or i == ')') and isNumber == 1 :
			con1.append(number)
			number = 0
			isNumber = 0
		if i >= '0' and i <= '9':
			number = number * 10 + int(i)
			isNumber = 1
	
	csvfile=open("../data/test.csv", "w", newline='')
	writer = csv.writer(csvfile)
	writer.writerow(["id", "width", "depth", "height", "weight", "volume"])
	tot=0
	for i in lines[1]:
		if i == ' ' and isNumber == 1 :
			con.append(number)
			number = 0
			isNumber = 0
		if i == ')':
			con.append(number)
			number = 0
			isNumber = 0
			generate(con[1],con[0],con[2],con[3],writer,flip_ratio)
			tot+=con[3]
			con.clear()
		if i >= '0' and i <= '9':
			number = number * 10 + int(i)
			isNumber = 1
	con1.append(tot)
	return con1

def pre_convert(start):
	file=open('../data2.txt','r')
	lines=file.readlines()
	with open("../data.txt", "w") as file2:
		file2.write(lines[start])
		file2.write(lines[start+1])
	
	return

