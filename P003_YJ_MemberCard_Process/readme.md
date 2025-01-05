@20211117
### 目的
- 前后端处理逻辑拆分，尽可能降低耦合
- 增加处理过程消息输出
- 精简重复代码

### 全局
- 定义列表 dict_keys ，用作前后端创建字典（文件、DataFrame、Header等）的共同依据

### 前端
#### 界面
- 定义按钮文本列表 button_text_list，作为后续组件的创建依据 
- 考虑到文件选择按钮 和 单行文本框 总是成对出现，简化为for循环实现，函数：create_widget 。 注意动态创建按钮并绑定事件时的入参调整 
- 调整了组件位置大小以及文本大小 
- 文件选择按钮：将文件名封进字典 entry_text_dict 
- 去掉了状态栏，增加多行文本框，作为日志输出对象 
- 处理过程拆分成3个部分 
  - file_pre_check 检查文件是否选择，以及文件名是否匹配，得到的结果打包进字典，以字典作为参数传递 
  - ui_process 
  - file_next_process 和后端交互，入参格式从4个字符串改为1个字典
- 新增的变量、函数打包进 MyGUI 类 

#### 日志功能
- 本文通过logging实现，也可以通过直接重写print实现
- 在 redir_stdout 中重写了write方法，将sys.stdout 输出对象设为界面上新增的多行文本框
- logger_init 初始化logger，设置输入级别和格式，默认输出对象为控制台，修改为sys.stdout

### 后端
- 参数形式调整：header 打包成字典，文件名用字典
- 去掉了文件名为空的判断，在前端已实现
- 4个文件读取过程 改 for循环实现，结果保存进字典 df_dict
- 4个文件的字段检测过程 改 for循环实现，结果保存进字典 columns_missing_dict
- 增加打印内容，函数名仍用print，保证可以单独运行

### 打包
- 新的打包命令：pyinstaller --upx-dir F:\Python\Wangyi\upx-3.96-win64 -F -w my_gui.py -p my_logger.py -p my_mergedata.py -p my_redirector.py -p my_thread.py 
- 使用upx，文件大小缩小25% ， 但还是很大23MB