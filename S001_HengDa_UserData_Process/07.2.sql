"""
@File               : 07.2.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:04
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:04 
@Version            : 1.0
@Description        : 手机号码重复 - 同1手机号下，全有身份证，或者全没有身份证
"""

-- 再次确认重复手机号
-- 还有933个手机号重复
SELECT phoneNumber,COUNT(phoneNumber)
FROM hengda
GROUP BY phoneNumber
HAVING COUNT(phoneNumber) > 1

SELECT * FROM hengda WHERE phoneNumber = '19877432016'


-- 确认933个重复手机号，对应1879条记录
SELECT * FROM hengda WHERE phoneNumber IN
    (SELECT t.phoneNumber FROM
        (SELECT phoneNumber,COUNT(phoneNumber)
        FROM hengda
        GROUP BY phoneNumber
        HAVING COUNT(phoneNumber) > 1)t
    )
ORDER BY phoneNumber


-- 在剩下的重复手机号对应的记录中，就是要么全有身份证，要么全无身份证的
-- 按照标准思路，筛选出最小ID,返回933条
SELECT tt.phoneNumber,MIN(tt.id) AS minID FROM
(SELECT * FROM hengda WHERE phoneNumber IN
        (SELECT t.phoneNumber FROM
            (SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1)t
        )
        ORDER BY phoneNumber
)tt
GROUP BY phoneNumber


-- 找出这些重复的手机号中，ID不等于最小ID的记录,共946条数据
SELECT * FROM hengda WHERE
phoneNumber IN
(
(SELECT t.phoneNumber FROM
            (SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1)t
        )
)
AND id NOT IN
(
SELECT ttt.minID FROM
(
SELECT tt.phoneNumber,MIN(tt.id) AS minID FROM
(SELECT * FROM hengda WHERE phoneNumber IN
        (SELECT t.phoneNumber FROM
            (SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1)t
        )
        ORDER BY phoneNumber
)tt
GROUP BY phoneNumber
)ttt
)


-- 删除ID不等于最小ID的记录 ，需要删除的数量为1879-933 = 946
-- 注意两个限制条件，1个是重复的手机号，1个是id不等于最小id
DELETE FROM hengda WHERE
phoneNumber IN
(
(SELECT t.phoneNumber FROM
            (SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1)t
        )
)
AND id NOT IN
(
SELECT ttt.minID FROM
(
SELECT tt.phoneNumber,MIN(tt.id) AS minID FROM
(SELECT * FROM hengda WHERE phoneNumber IN
        (SELECT t.phoneNumber FROM
            (SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1)t
        )
        ORDER BY phoneNumber
)tt
GROUP BY phoneNumber
)ttt
)



-- 确认没有重复手机号
-- 返回为0
SELECT phoneNumber,COUNT(phoneNumber)
            FROM hengda
            GROUP BY phoneNumber
            HAVING COUNT(phoneNumber) > 1


-- 确认总数为 416674-1-1707-946=414020
SELECT COUNT(*) FROM hengda;

-- 删除2654条记录
SELECT -1-1707-946
