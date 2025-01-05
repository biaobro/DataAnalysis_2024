"""
@File               : Delete_Duplicate_Email.sql
@Project            : S_001_Delete_Duplicate_Email
@CreateTime         : 2023/3/6 15:16
@Author             : biaobro
@Software           : PyCharm
@Last Modify Time   : 2023/3/6 15:16 
@Version            : 1.0
@Description        : None
"""

DELETE FROM person WHERE id in
(
	select t.id from
	(
		SELECT id FROM person
		WHERE id not in
		(
				select min(t.tid) from
				(
					# 存在重复记录的 id
					select id as tid, email as temail from Person where email in
					(
						select email
						from Person
						group by email
						having count(email) > 1
					)
				)t
				group by temail
		)

		and id not in
		(
			# 保留没有重复email 的记录
			select id from person WHERE email in
			(
				select email
				from Person
				group by email
				having count(email) = 1
			)
		)
	)t
)
