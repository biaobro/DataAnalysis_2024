"""
@File               : 10.sql
@Project            : M_001_Hengda
@CreateTime         : 2023/3/5 19:05
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/5 19:05 
@Version            : 1.0
@Description        : 导出数据
"""

SELECT
    personName AS '姓名（必填）',
    phoneNumber AS '电话（必填）',
    provinceID AS '会员所属省份ID（必填）',
    cityID AS '会员所属城市ID（必填）',
    account AS '是否开通余额账户（必填）',
    gender AS '性别',
    mailbox AS '邮箱',
    birthday AS '生日',
    cardType AS '证件类型',
    idCard AS '身份证号',
    comments AS '备注',
    thirdID AS '第三方ID',
    memberLevelID AS '会员级别ID',
    memberTypeID AS '会员类型ID',
    payPassword AS '余额支付密码',
    point AS '积分余额',
    money AS '充值余额',
    growPoint AS '成长值余额'
FROM
    hengda
