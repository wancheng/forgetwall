#!/bin/sh
# coding=utf-8  
import xlrd
import MySQLdb
import sys

def open_excel(file="file.xls"):
	reload(sys)
	print sys.setdefaultencoding("utf-8")
	try:
		print("================ get data ===============")
		print(file)
		data = xlrd.open_workbook(file,encoding_override="gbk")
		return data
	except Exception,e:
		print str(e)

def excel_table_byindex(file="file.xls",colnameindex=0,by_index=0):

	conn = MySQLdb.connect(host='localhost',user='root',passwd='rootroot',db='blog')
	cursor = conn.cursor()
	# cursor.execute""()
	data = open_excel(file)
	table = data.sheets()[by_index]
	nrows = table.nrows
	ncols = table.ncols
	colnames = table.row_values(colnameindex)

	tables = [];
	for rownum in range(1,nrows):
		row = table.row_values(rownum)
		if row:
			app = []
			for i in range(len(colnames)):
				if i==0:
					app.append(row[i])
				elif i==1:
					s=1
					if row[i]=='F':
						s=0
					app.append(s)
				else:
					app.append(row[i])
			tables.append(app)
			sql="INSERT INTO employee (employeeid,sex,ename,efname,cname) VALUES ('%s',%d,'%s','%s','%s')"%(int(app[0]),int(app[1]),str(app[2]),str(app[3]),str(app[4]))
			print sql
			try:
				cursor.execute(sql)
			except Exception,e:
				print e
	cursor.close()
	conn.commit()
	conn.close()

def main():
	excel_table_byindex(file="dao.xlsx")

if __name__ == "__main__":
	main()
