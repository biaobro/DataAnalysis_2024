"""
@File               : 09.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:05
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:05 
@Version            : 1.0
@Description        : 补全其他信息
"""

-- 补齐省份和城市代号
-- 广东-892
-- 广州-893
SELECT COUNT(*) FROM hengda WHERE provinceID IS NULL
SELECT COUNT(*) FROM hengda WHERE cityID IS NULL

-- 414020条记录
-- Affected rows: 414020
UPDATE hengda SET provinceID = 892,cityID = 893

-- 确认变更成功
SELECT COUNT(*) FROM hengda WHERE provinceID IS NULL
SELECT COUNT(*) FROM hengda WHERE cityID IS NULL
SELECT * FROM hengda LIMIT 10

-- 补齐名字为空的
-- 共37249条记录
SELECT COUNT(*) FROM hengda WHERE personName IS NULL

-- Affected rows: 37249
UPDATE hengda SET personName = '未设置' WHERE personName IS NULL

-- 确认
SELECT COUNT(*) FROM hengda WHERE personName IS NULL

-- `是否开通余额账户（必填）`全部为否
UPDATE hengda SET account = '否'


