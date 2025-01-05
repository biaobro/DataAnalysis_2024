"""
@File               : 05.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 18:59
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 18:59 
@Version            : 1.0
@Description        : 手机号码位数不正确
"""

-- 直接删除该条记录
-- 总数：416674
SELECT COUNT(*) FROM hengda;

-- 1, 删除手机号位数不正确的
-- 1.1 查询结果1条 ID=219277
SELECT *
FROM hengda
WHERE phoneNumber IN (
    SELECT t.phoneNumber
    FROM (
        SELECT phoneNumber, LENGTH(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING LENGTH(phoneNumber) <> 11
    ) t
)

-- 1.2 删除手机号码位数不正确的 影响行数1
DELETE FROM hengda
WHERE phoneNumber IN (
        SELECT t.phoneNumber
        FROM (
            SELECT phoneNumber, LENGTH(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING LENGTH(phoneNumber) <> 11
        ) t
    )

-- 1.3 确认结果 无
SELECT *
FROM hengda
WHERE phoneNumber IN (
    SELECT t.phoneNumber
    FROM (
        SELECT phoneNumber, LENGTH(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING LENGTH(phoneNumber) <> 11
    ) t
)

-- 1.4 确认结果 无
SELECT * FROM hengda WHERE id = 219277

-- 总数应为：416674-1=416673
SELECT COUNT(*) FROM hengda;