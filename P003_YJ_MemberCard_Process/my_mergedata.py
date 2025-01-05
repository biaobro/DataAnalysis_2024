# Coding: UTF-8
"""
# Created On: 2021/5/15 19:03
# Author: biaobro
# Project: M_003_YJ_Card_Data_Process
# File Name: mergedata.py
# Description:
"""
import os
import pandas as pd
import logging
import my_gui

import warnings

warnings.filterwarnings("ignore")

data_logger = logging.getLogger(my_gui.log_file + ".merge_data")
print = data_logger.info


class MergeData:
    def __init__(self, path_before=None, path_after=None, file_dict=None):
        self.df_dict = {key: None for key in my_gui.dict_keys}

        # 获取路径
        self.path_before = 'data_before/' if path_before is None else path_before
        self.path_after = 'data_after/' if path_after is None else path_after
        self.output_filename = None
        self.default_card_pwd = '670b14728ad9902aecba32e22fa4f6bd'

        # the order is 'member', 'member_card', 'pwd', 'chip_card'
        self.header_dict = {key: value for key, value in zip(my_gui.dict_keys, [1, 1, 0, 1])}

        self.file_dict = file_dict

        try:
            if not os.path.exists(self.path_before):
                os.mkdir(self.path_before)
            if not os.path.exists(self.path_after):
                os.mkdir(self.path_after)
                print("目标文件保存路径创建：完成")
        except Exception as e:
            print("目标文件保存路径创建：失败")
            raise e

    # read excel with pandas
    # 将4个Excel 文件读取为 pandas 数据结构
    def get_df(self):
        for i in range(len(self.file_dict)):
            try:
                print(list(self.file_dict.keys())[i] + " 读取：开始")

                self.df_dict[list(self.df_dict.keys())[i]] = pd.read_excel(
                    self.file_dict[list(self.file_dict.keys())[i]],
                    sheet_name=0,
                    header=self.header_dict[list(self.header_dict.keys())[i]],
                    engine='openpyxl',
                    usecols="A:Z",
                    dtype=str)

                print(
                    list(self.file_dict.keys())[i] + " 读取：完成，共 {} 行 {} 列".format(
                        self.df_dict[list(self.df_dict.keys())[i]].shape[0],
                        self.df_dict[list(self.df_dict.keys())[i]].shape[1])
                )
            except ValueError:
                print(list(self.file_dict.keys())[i] + " 读取：出错，处理停止")
                raise ValueError

    # check if the columns match
    def check_columns(self):
        print("字段检查：开始")
        member_card_columns = ['card_no', 'gmt_create', 'expire_date', 'amount', 'account_id', 'card_type',
                               'use_status', 'id', 'card_name', 'enable_recharge_flag', 'uses_num']
        member_columns = ['account_id', 'real_name', 'id_card_no', 'birthday', 'mobile', 'status', 'total_amount']
        chip_card_columns = ['card_no', 'chip_code']
        pwd_columns = ['影院内码', '影院名称', '卡类型', '卡密', '密码长度']

        columns_predefined_list = [member_columns, member_card_columns, pwd_columns, chip_card_columns]
        columns_predefined_dict = {key: value for key, value in zip(my_gui.dict_keys, columns_predefined_list)}
        result = True

        columns_missing_dict = {key: [] for key in zip(my_gui.dict_keys)}

        # check all dataframe
        for i in range(len(self.df_dict)):
            if self.df_dict[list(self.df_dict.keys())[i]] is not None:
                for specified_column in columns_predefined_dict[list(columns_predefined_dict.keys())[i]]:
                    # columns_dict: pre define columns
                    # df_dict: actual read columns
                    # columns_dict must match with dataframe
                    if specified_column not in self.df_dict[list(self.df_dict.keys())[i]].columns:
                        columns_missing_dict[list(columns_missing_dict.keys())[i]].append(specified_column)
                        result = False

        # output all missing columns in 4 file
        if not result:
            for i in range(len(columns_missing_dict)):
                if len(columns_missing_dict[list(columns_missing_dict.keys())[i]]) > 0:
                    print(list(self.file_dict.keys())[i] + ' 存在字段缺失 ' +
                          ', '.join(columns_missing_dict[list(columns_missing_dict.keys())[i]]))
            return False
        else:
            print("字段检查：通过")
            return True

    #
    def merge_df(self):
        print("字段格式转换：开始")
        try:
            self.df_dict['member']['account_id'] = self.df_dict['member']['account_id'].astype(str)
            self.df_dict['member']['total_amount'] = self.df_dict['member']['total_amount'].fillna(0)

            self.df_dict['member_card']['account_id'] = self.df_dict['member_card']['account_id'].astype(str)
            self.df_dict['member_card']['card_no'] = self.df_dict['member_card']['card_no'].astype(str)
            self.df_dict['member_card']['card_type'] = self.df_dict['member_card']['card_type'].astype(str)

            self.df_dict['pwd']['卡号'] = self.df_dict['pwd']['卡号'].astype(str)

            self.df_dict['chip_card']['card_no'] = self.df_dict['chip_card']['card_no'].astype(str)
            print("字段格式转换：完成")
        except Exception as e:
            print("字段格式转换：失败")
            raise e

        print("file_member_card 和 file_member 连接：开始")
        member_card_df = self.df_dict['member_card'].merge(right=self.df_dict['member'], left_on='account_id',
                                                           right_on='account_id', how='left')
        print("file_member_card 和 file_member 连接：完成")

        print("file_chip_card 连接：开始")
        merge_chip_df = member_card_df.merge(right=self.df_dict['chip_card'], left_on='card_no', right_on='card_no',
                                             how='left')
        print("file_chip_card 连接：完成")

        print("file_pwd 连接：开始")
        merge_df = merge_chip_df.merge(right=self.df_dict['pwd'], left_on='card_no', right_on='卡号', how='left')  # 卡密码合并
        print("file_pwd 连接：完成")

        order_list = ['cinema_card_num', 'cinema_card_level_name', 'cinema_card_balance', 'cinema_card_available_jifen',
                      'cinema_card_total_jifen', 'cinema_upgrade_total_jifen', 'cinema_card_type', 'cinema_card_period',
                      'cinema_card_username', 'cinema_card_idcard', 'cinema_card_addr', 'cinema_card_mobile',
                      'cinema_card_birthday', 'cinema_card_email', 'cinema_card_phone', 'cinema_card_sex',
                      'cinema_card_national', 'cinema_card_birth_place', 'cinema_card_idcard_type',
                      'cinema_create_time',
                      'cinema_card_password', 'cinema_card_chip_id', 'cinema_card_status', 'enable_recharge_flag']
        data_dict = {  # 重命名字段
            'card_no': 'cinema_card_num',
            'card_name': 'cinema_card_level_name',
            'amount': 'cinema_card_balance',
            'chip_code': 'cinema_card_chip_id',
            'total_amount': 'cinema_card_available_jifen',
            '卡密': 'cinema_card_password',  # None
            'real_name': 'cinema_card_username',
            'email': 'cinema_card_email',  # None
            'mobile': 'cinema_card_mobile',
            'phone_no': 'cinema_card_phone',  # None
            'address': 'cinema_card_addr',  # None
            'gmt_create': 'cinema_create_time',
            'expire_date': 'cinema_card_period',
            'id_card_no': 'cinema_card_idcard',
            # 'card_type': 'enable_recharge_flag',  # enable_recharge_flag B：不可充值，C：可充值'
            'account_id': '会员ID',
            'use_status': 'cinema_card_status',
            'birthday': 'cinema_card_birthday',
            '密码长度': 'password_length',
            'enable_recharge_flag': 'enable_recharge_flag'
        }
        merge_df = merge_df.rename(columns=data_dict)
        merge_df['password_length'].fillna(value=str(0), inplace=True)
        merge_df.fillna(value="", inplace=True)
        merge_df['cinema_card_email'] = ''
        merge_df['cinema_card_phone'] = ''
        merge_df['cinema_card_addr'] = ''
        new_df = pd.DataFrame()
        for i in data_dict.values():
            new_df[i] = merge_df[i].astype(str)

        new_df['cinema_card_balance'] = new_df['cinema_card_balance'].map(lambda x: int(x) / 100).astype(str)
        print("会员积分处理：完成")

        new_df['cinema_card_password'] = merge_df[['cinema_card_password', 'password_length']].apply(
            lambda x: x['cinema_card_password'] if int(x['password_length']) == 6 else
            ('' if int(x['password_length']) == 0 else self.default_card_pwd), axis=1).astype(str)
        print("会员卡密码处理：完成")
        # 按会员ID分组统计，得到新df
        # reset_index使用方法：
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.reset_index.html
        df_group_by_account = new_df.groupby(['会员ID', 'cinema_card_status']).agg({"cinema_card_num": 'count'})
        df_group_by_account = df_group_by_account.reset_index().rename(columns={"cinema_card_num": "卡数统计"})
        final_merge_df = new_df.merge(df_group_by_account, left_on=['会员ID', 'cinema_card_status'],
                                      right_on=['会员ID', 'cinema_card_status'], how='left')
        final_merge_df['cinema_card_available_jifen'] = final_merge_df['cinema_card_available_jifen'].astype(float)
        final_merge_df['卡数统计'] = final_merge_df['卡数统计'].astype(int)
        print("会员卡数量统计：完成")
        # 列运算：获取积分
        final_merge_df['cinema_card_available_jifen'] = \
            final_merge_df[['cinema_card_available_jifen', '卡数统计', 'cinema_card_status']].apply(
                lambda x: round(x['cinema_card_available_jifen'] / x['卡数统计'], 2)
                if x['cinema_card_status'] != '3' else 0, axis=1)
        # 鼎新导入卡状态映射
        card_status_dict = {'0': '1', '1': '2', '2': '2', '3': '3', '4': '1'}
        final_merge_df['cinema_card_status'] = final_merge_df['cinema_card_status'].map(card_status_dict)
        final_merge_df = final_merge_df.drop(columns=['卡数统计', '会员ID'], axis=0)
        final_merge_df['cinema_card_total_jifen'] = final_merge_df['cinema_card_available_jifen']
        final_merge_df['cinema_upgrade_total_jifen'] = final_merge_df['cinema_card_available_jifen']
        final_merge_df['cinema_card_type'] = '1'  # 卡介质
        final_merge_df['cinema_card_sex'] = ''  # 性别
        final_merge_df['cinema_card_national'] = ''  # 籍贯
        final_merge_df['cinema_card_birth_place'] = ''  # 出生地
        final_merge_df['cinema_card_idcard_type'] = '身份证'
        final_merge_df = final_merge_df[order_list]
        print("会员卡状态映射：完成")
        return final_merge_df

    def measured_card(self):
        if self.df_dict['member_card'] is not None:
            rename_dict = {'card_no': '会员卡号', 'uses_num': '剩余次数'}
            measured_df = self.df_dict['member_card'][self.df_dict['member_card']['card_type'] == '4']
            measured_df = measured_df[['card_no', 'uses_num']].rename(columns=rename_dict)
            return measured_df
        else:
            return False

    def df_to_excel(self, df, set_dir=None):
        try:
            self.output_filename = 'data_after/member_card_df_new.xlsx'
            set_dir = self.output_filename if set_dir is None else set_dir

            print("写入目标文件 " + set_dir.split('/')[1] + "：开始")

            writer = pd.ExcelWriter(set_dir, engine='xlsxwriter', mode='w')
            df.to_excel(writer, sheet_name='Sheet1', index=False)
            wb = writer.book
            wb.read_only_recommended()
            # wb.close()
            writer.save()

            print("写入目标文件 " + set_dir.split('/')[1] + "：完成")
        except Exception as e:
            print("写入目标文件：失败")
            raise e
