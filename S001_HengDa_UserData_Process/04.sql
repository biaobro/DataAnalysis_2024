-- noinspection SqlDialectInspectionForFile

"""
@File               : 04.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 18:57
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 18:57 
@Version            : 1.0
@Description        : 整体处理
"""

-- 总数416674
SELECT COUNT(*) FROM hengda;
SELECT * FROM hengda LIMIT 10;

-- 增加id列 作为主键 自增
-- 需要注意书写顺序 FIRST 在最后
ALTER TABLE hengda ADD id INT NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;

-- 确认id添加成功
SELECT * FROM hengda ORDER BY id DESC LIMIT 10;

-- 创建索引
ALTER TABLE hengda Add KEY idxName(id);

-- 以下为数据确认SQL
-- 这个手机号有9条重复记录 包含身份证号
SELECT * FROM hengda WHERE phoneNumber = '19877432016';

-- 查看其他个字段是否有异常
SELECT DISTINCT(gender),DISTINCT(account),COUNT(mailbox),DISTINCT(cardType) FROM hengda