"""
@File               : 08.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:04
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:04 
@Version            : 1.0
@Description        : 身份证号为空的，将证件类型置为空
"""

-- 确认总数为 416674-1-1707-946=414020
SELECT COUNT(*) FROM hengda;


-- 身份证号码为空的  需要将证件类型置为空
-- 共39844条记录
SELECT COUNT(*) FROM hengda WHERE idCard IS NULL

-- 有身份证号码的记录374176条
SELECT COUNT(*) FROM hengda WHERE idCard IS NOT NULL

-- Affected rows: 39844
UPDATE hengda SET cardType = NULL WHERE idCard IS NULL

-- 确认
SELECT * FROM hengda WHERE cardType IS NULL AND idCard is NOT NULL;
SELECT * FROM hengda WHERE cardType IS NOT NULL AND idCard is NULL;
