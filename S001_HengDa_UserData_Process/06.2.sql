"""
@File               : 06.2.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:03
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:03 
@Version            : 1.0
@Description        : 身份证号码重复 - 同1身份证号下，全有身份证，或者全无身份证
"""

-- 还剩1569个身份证号存在重复，对应4248条记录
SELECT *
FROM hengda
WHERE idCard IN (
    SELECT t.idCard
    FROM (
        -- 2627个身份证号重复
        -- 此时1569个身份证号重复，去掉了1058个
        SELECT idCard, COUNT(idCard)
        FROM hengda
        GROUP BY idCard
        HAVING COUNT(idCard) > 1
    ) t
)
ORDER BY idCard


-- 1569个身份证号重复，对应4248条记录
-- 找出1569个最小的ID
SELECT idCard, MIN(id) AS minID
FROM hengda
WHERE idCard IN (
    SELECT t.idCard
    FROM (
        -- 2627个身份证号重复
        -- 此时1569个身份证号重复
        SELECT idCard, COUNT(idCard)
        FROM hengda
        GROUP BY idCard
        HAVING COUNT(idCard) > 1
    ) t
)
GROUP BY idCard
ORDER BY idCard


-- 在身份证号重复的4248条记录里，找出ID不等于最小ID的记录，注意两个限制条件
-- 返回条数2679
SELECT *
FROM hengda
WHERE idCard IN (
        SELECT t.idCard
        FROM (
            SELECT idCard, COUNT(idCard)
            FROM hengda
            GROUP BY idCard
            HAVING COUNT(idCard) > 1
        ) t
    )
    AND id NOT IN (
        SELECT tt.minID
        FROM (
            SELECT idCard, MIN(id) AS minID
            FROM hengda
            WHERE idCard IN (
                SELECT t.idCard
                FROM (
                    -- 2627个身份证号重复
                    -- 此时1569个身份证号重复
                    SELECT idCard, COUNT(idCard)
                    FROM hengda
                    GROUP BY idCard
                    HAVING COUNT(idCard) > 1
                ) t
            )
            GROUP BY idCard
        ) tt
    )
ORDER BY idCard


-- 在身份证号重复的4248条记录里，将ID不等于最小ID的记录共2679条，中的身份证号清空
-- 清空 不是删除，不影响总条数
-- Affected rows: 2679
UPDATE hengda
SET idCard = NULL
WHERE idCard IN (
        SELECT t.idCard
        FROM (
            SELECT idCard, COUNT(idCard)
            FROM hengda
            GROUP BY idCard
            HAVING COUNT(idCard) > 1
        ) t
    )
    AND id NOT IN (
        SELECT tt.minID
        FROM (
            SELECT idCard, MIN(id) AS minID
            FROM hengda
            WHERE idCard IN (
                SELECT t.idCard
                FROM (
                    -- 2627个身份证号重复
                    -- 此时1569个身份证号重复
                    SELECT idCard, COUNT(idCard)
                    FROM hengda
                    GROUP BY idCard
                    HAVING COUNT(idCard) > 1
                ) t
            )
            GROUP BY idCard
        ) tt
    )


-- 至此，身份证号码重复全部清理完成
-- 确认重复的身份证号码，本条返回为0
SELECT idCard,COUNT(idCard) FROM hengda GROUP BY idCard HAVING COUNT(idCard) > 1


-- 确认总数仍为 416674-1=416673
SELECT COUNT(*) FROM hengda;
