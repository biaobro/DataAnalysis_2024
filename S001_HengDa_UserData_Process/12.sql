"""
@File               : 12.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:06
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:06 
@Version            : 1.0
@Description        : 导入后确认
"""

-- 确认备注为20200721*的共414020条
SELECT COUNT(*)
  FROM crm_customer
 WHERE tenant_id= 17123
   and remark LIKE "20200721%"

-- 确认没有备注的，共10条,创建时间在导入时间范围内的2条
SELECT *
  FROM crm_customer
 WHERE tenant_id= 17123
   AND  gmt_create BETWEEN '2020-07-21 14:06:00'
   AND '2020-07-21 17:31:00'
   AND remark IS NULL
ORDER BY gmt_create DESC
