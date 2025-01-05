# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
"""
@File               : system_upgrade_plan.py
@Project            : M_006_MZ_System_Upgrade_Plan
@CreateTime         : 2023/3/6 16:04
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/6 16:04 
@Version            : 1.0
@Description        : None
"""

# fetchmany method

import CustomerDBLists
import sqlFile
import pymysql
import xlsxwriter
import time

starttime = time.perf_counter()
print(starttime)

# Create workbook and worksheet
wb = xlsxwriter.Workbook('sql20190415_v5_bbc.xlsx')
wks = wb.add_worksheet()  # Default to Sheet1

# initialize the 1st row
row1format = wb.add_format({'font_name': '微软雅黑 Light', 'bold': 'True'})

# In xlsxwriter, row and column are all 0-Index, A1=(0,0)
wks.write(0, 0, '序号', row1format)
wks.write(0, 1, '系统版本', row1format)
wks.write(0, 2, '剧院名称', row1format)
wks.write(0, 3, '项目ID', row1format)
wks.write(0, 4, '项目名称', row1format)
wks.write(0, 5, '场次ID', row1format)
wks.write(0, 6, '场次名称', row1format)
wks.write(0, 7, '开演时间', row1format)

# define the font and date format
fontformat = wb.add_format({'font_name': '微软雅黑 Light'})
dateformat = wb.add_format({'font_name': '微软雅黑 Light', 'num_format': 'yyyy-mm-dd hh:mm'})

# define the variable
rowcount = 1

for i in range(0, len(CustomerDBLists.dbList)):
    # check all V4 databases(117_Normal + 4_Own + 1_Special + 6_Unused + 3_Test)
    if 'V5' in CustomerDBLists.dbList[i][1]:  # Only check 117_Normal Theatre
        # if CustomerDBLists.dbList[i][0] == '天津瑞龙科技':
        try:
            # Create the connection to database
            conn = pymysql.connect(host=CustomerDBLists.dbList[i][5],  # DB_Address
                                   port=3306,  # DB_Port
                                   user=CustomerDBLists.dbList[i][3],  # DB_UserName
                                   passwd=CustomerDBLists.dbList[i][4],  # DB_Password
                                   db=CustomerDBLists.dbList[i][2],  # DB_Name
                                   charset='utf8')

            # Get the cursor of connection
            cursor = conn.cursor()

            # Execute the SQL, return the quantity of result
            count = cursor.execute(sqlFile.sql20190415_v5_bbc)
            print(CustomerDBLists.dbList[i][0], count)

            # Get all the records, looks better than fetchone by one
            result = cursor.fetchmany(count)

            for record in result:
                # print(record)
                wks.write(rowcount, 0, i, fontformat)
                wks.write(rowcount, 1, CustomerDBLists.dbList[i][1], fontformat)  # DB_Version
                wks.write(rowcount, 2, CustomerDBLists.dbList[i][0], fontformat)  # Theatre_Name
                wks.write_string(rowcount, 3, str(record[0]), fontformat)  # Project_ID
                wks.write(rowcount, 4, record[1], fontformat)  # Project_Name
                wks.write_string(rowcount, 5, str(record[2]), fontformat)  # Event_ID
                wks.write(rowcount, 6, record[3], fontformat)  # Event_Name
                wks.write(rowcount, 7, record[4], dateformat)  # Event_ShowTime

                rowcount = rowcount + 1

        except pymysql.Error as err:
            print("Error info:", err)
        finally:
            cursor.close
            conn.close
wb.close()

print(time.perf_counter() - starttime)
