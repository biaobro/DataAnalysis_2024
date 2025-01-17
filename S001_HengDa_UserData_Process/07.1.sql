"""
@File               : 07.1.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:03 
@Version            : 1.0
@Description        : 手机号码重复 - 同1手机号下，有的有身份证，有的没有身份证
"""

-- 确认总数仍为 416674-1=416673
SELECT COUNT(*) FROM hengda;

-- 确认1734个手机号重复
SELECT phoneNumber,COUNT(phoneNumber)
FROM hengda
GROUP BY phoneNumber
HAVING COUNT(phoneNumber) > 1

-- 确认1734个重复手机号，对应4387条记录
SELECT * FROM hengda WHERE phoneNumber IN
    (SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
    )
ORDER BY phoneNumber


-- 重复手机号中，同1条下，有的有身份证，有的没有
-- 处理思路：删除没有身份证的，保留有身份证的

-- 1734个手机号，4387条记录记录中，身份证号为空的记录1826条
-- 1826条记录，对应 DISTINCT(phoneNumber)=856个手机号
SELECT * FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)

-- 1826条记录，856个手机号，又有身份证的805条
-- DISTINCT(phoneNumber),对应手机号803个
SELECT  DISTINCT(phoneNumber) FROM hengda WHERE idCard IS NOT NULL AND phoneNumber IN
(
SELECT phoneNumber FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)
)


-- 这803个手机号，对应2512条记录
SELECT * FROM hengda WHERE phoneNumber IN
(
SELECT DISTINCT(phoneNumber) FROM hengda WHERE idCard IS NOT NULL AND phoneNumber IN
(
SELECT phoneNumber FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)
)
)
ORDER BY phoneNumber


-- 这803个手机号,2512条记录中，身份证号为空的1707条
SELECT * FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(
SELECT DISTINCT(phoneNumber) FROM hengda WHERE idCard IS NOT NULL AND phoneNumber IN
(
SELECT phoneNumber FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)
)
)
ORDER BY phoneNumber

SELECT * FROM hengda WHERE phoneNumber = '13025791529'

-- 删除这1707条 Affected rows: 1707
DELETE FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(
SELECT tt.phoneNumber FROM
(
SELECT DISTINCT(phoneNumber) FROM hengda WHERE idCard IS NOT NULL AND phoneNumber IN
(
SELECT phoneNumber FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)
)
)tt
)


-- 确认不再存在这样的手机号：有的有身份证，有的没有
-- 返回为0
SELECT DISTINCT(phoneNumber) FROM hengda WHERE idCard IS NOT NULL AND phoneNumber IN
(
SELECT phoneNumber FROM hengda WHERE idCard IS NULL AND phoneNumber IN
(SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
)
)
