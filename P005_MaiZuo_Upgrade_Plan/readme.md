### 背景

文件保存时间是在20190113.

4、5版本升级在即，SAAS版本的功能却没有完全补齐，所以需要结合旧版本使用情况，新版本开发情况，制定升级排期。

2个运维同学有数据库访问权限，却不会写SQL，看起来也没有想学的欲望。

为了避免麻烦开发同学，同时尽可能掌握主动权。我找运维同学请教了数据库访问方法，首先基于测试系统弄清楚了各个功能
模块对应哪些数据字段。

然后就开始查询商家系统数据，刚开始为了确保万无一失，从数据库查到数据后，还是要到系统里做最终确认。

几轮下来，字段都熟悉了，就心里有底了，不再每次都验证。

当时比较麻烦的是，每个商家的系统独立部署，数据库也是分开的，每家数据库都有单独的账号和密码。所以写了1个
CustomerDBLists.py 用于保存商家名称，数据库地址，端口，用户名和密码。

同时为了降低耦合，把需要执行的 sql 语句单独放到 sqlFile.py 文件中

现在这两个文件已经都遗失了。

在 system_upgrade_plan 这个文件中，读取 DBLists 建立到数据库的连接，读取 sqlFile 执行sql，然后将
数据写进 Excel. 

这件事情，开启了SQL 学习和实战的序幕。

