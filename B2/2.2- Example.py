"""
Quản trị CSDL:
- Tạo CSDL: Tạo bảng, Khóa, Mối quan hệ
- Truy vấn trên CSDL: Thêm, Xóa, Sửa, Cập nhật
- Thống kê, Báo cáo
- Quản lý, Phân quyền người sử dụng
- Bảo mật 

SQL, noSQL
"""

#0- Cai dat
pip install pymysql
pip install mysql-connector-python

#Thong tin ve He quan tri CSDL
import sqlalchemy
print(sqlalchemy.__version__)

#1- Ket noi
from sqlalchemy import create_engine
engine = create_engine('sqlite:///:memory:', echo=True)

#2-Define and Create Tables
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
metadata = MetaData()
users = Table('users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

addresses = Table('addresses', metadata,
  Column('id', Integer, primary_key=True),
  Column('user_id', None, ForeignKey('users.id')),
  Column('email_address', String, nullable=False))
metadata.create_all(engine)

#3- Insert Expressions
ins = users.insert().values(name='jack', fullname='Jack Jones')
print(str(ins))
print(ins.compile().params)


conn = engine.connect()
result = conn.execute(ins)
print(result)

ins.bind = engine
print(str(ins))
print(result.inserted_primary_key)

#4- Executing Multiple Statements
ins = users.insert()
conn.execute(ins, id=2, name='wendy', fullname='Wendy Williams')
conn.execute(addresses.insert(), [
{'user_id': 1, 'email_address' : 'jack@yahoo.com'},
   {'user_id': 1, 'email_address' : 'jack@msn.com'},
   {'user_id': 2, 'email_address' : 'www@www.org'},
   {'user_id': 2, 'email_address' : 'wendy@aol.com'},
])



#5- Selecting
from sqlalchemy.sql import select
s = select([users])
result = conn.execute(s)
print(result)


for row in result:
    print(row)

result = conn.execute(s)
row = result.fetchone()
print("name:", row['name'], "; fullname:", row['fullname'])

row = result.fetchone()
print("name:", row[1], "; fullname:", row[2])





for row in conn.execute(s):
    print("name:", row[users.c.name], "; fullname:", row[users.c.fullname])

	
#6- Selecting Specific Columns
s = select([users.c.name, users.c.fullname])
result = conn.execute(s)
for row in result:
    print(row)


	
for row in conn.execute(select([users, addresses])):
    print(row)


s = select([users, addresses]).where(users.c.id == addresses.c.user_id)
for row in conn.execute(s):
    print(row)

#7- Operators
users.c.id == addresses.c.user_id

print(users.c.id == addresses.c.user_id)

print(users.c.id == 7)

(users.c.id == 7).compile().params

print(users.c.id != 7)

print(users.c.name == None)

print('fred' > users.c.name)

print(users.c.id + addresses.c.id)

print(users.c.name + users.c.fullname)

#8- Conjunctions

from sqlalchemy.sql import and_, or_, not_
print(and_(
         users.c.name.like('j%'),
         users.c.id == addresses.c.user_id,
         or_(
              addresses.c.email_address == 'wendy@aol.com',
              addresses.c.email_address == 'jack@yahoo.com'
         ),
         not_(users.c.id > 5)
       )
  )


print(users.c.name.like('j%') & (users.c.id == addresses.c.user_id) &
     (
       (addresses.c.email_address == 'wendy@aol.com') | \
       (addresses.c.email_address == 'jack@yahoo.com')
     ) \
     & ~(users.c.id>5)
 )


s = select([(users.c.fullname +
               ", " + addresses.c.email_address).
                label('title')]).\
        where(
           and_(
               users.c.id == addresses.c.user_id,
               users.c.name.between('m', 'z'),
               or_(
                  addresses.c.email_address.like('%@aol.com'),
                  addresses.c.email_address.like('%@msn.com')
               )
           )
        )
conn.execute(s).fetchall()


s = select([(users.c.fullname +
               ", " + addresses.c.email_address).
                label('title')]).\
        where(users.c.id == addresses.c.user_id).\
        where(users.c.name.between('m', 'z')).\
        where(
               or_(
                  addresses.c.email_address.like('%@aol.com'),
                  addresses.c.email_address.like('%@msn.com')
               )
       )
conn.execute(s).fetchall()

#8-Using Textual SQL
from sqlalchemy.sql import text
s = text(
     "SELECT users.fullname || ', ' || addresses.email_address AS title "
         "FROM users, addresses "
         "WHERE users.id = addresses.user_id "
         "AND users.name BETWEEN :x AND :y "
         "AND (addresses.email_address LIKE :e1 "
             "OR addresses.email_address LIKE :e2)")
conn.execute(s, x='m', y='z', e1='%@aol.com', e2='%@msn.com').fetchall()

#9- Specifying Bound Parameter Behaviors
stmt = text("SELECT * FROM users WHERE users.name BETWEEN :x AND :y")
stmt = stmt.bindparams(x="m", y="z")

from sqlalchemy import bindparam

stmt = stmt.bindparams(bindparam("x", type_=String), bindparam("y", type_=String))
result = conn.execute(stmt, {"x": "m", "y": "z"})


#Specifying Result-Column Behaviors
stmt = stmt.columns(id=Integer, name=String)
stmt = text("SELECT id, name FROM users")
stmt = stmt.columns(users.c.id, users.c.name)

#Loi o phan nay, check lại Version 14 dang su dung khac gi voi Version 13 cua doan code nay?
j = stmt.join(addresses, stmt.c.id == addresses.c.user_id)

new_stmt = select([stmt.c.id, addresses.c.id]).\
    select_from(j).where(stmt.c.name == 'x')


stmt = text("SELECT users.id, addresses.id, users.id, "
     "users.name, addresses.email_address AS email "
     "FROM users JOIN addresses ON users.id=addresses.user_id "
     "WHERE users.id = 1").columns(
        users.c.id,
        addresses.c.id,
        addresses.c.user_id,
        users.c.name,
        addresses.c.email_address
     )
result = conn.execute(stmt)

row = result.fetchone()
print(row[addresses.c.email_address])

#Using text() fragments inside bigger statements

s = select([
        text("users.fullname || ', ' || addresses.email_address AS title")
     ]).\
         where(
             and_(
                 text("users.id = addresses.user_id"),
                 text("users.name BETWEEN 'm' AND 'z'"),
                 text(
                     "(addresses.email_address LIKE :x "
                     "OR addresses.email_address LIKE :y)")
             )
         ).select_from(text('users, addresses'))
conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()

#Using More Specific Text with table(), literal_column(), and column()

from sqlalchemy import select, and_, text, String
from sqlalchemy.sql import table, literal_column
s = select([
    literal_column("users.fullname", String) +
   ', ' +
   literal_column("addresses.email_address").label("title")
]).\
   where(
       and_(
           literal_column("users.id") == literal_column("addresses.user_id"),
           text("users.name BETWEEN 'm' AND 'z'"),
           text(
               "(addresses.email_address LIKE :x OR "
               "addresses.email_address LIKE :y)")
       )
   ).select_from(table('users')).select_from(table('addresses'))

conn.execute(s, x='%@aol.com', y='%@msn.com').fetchall()

#Ordering or Grouping by a Label
from sqlalchemy import func
stmt = select([
        addresses.c.user_id,
        func.count(addresses.c.id).label('num_addresses')]).\
        group_by("user_id").order_by("user_id", "num_addresses")

conn.execute(stmt).fetchall()


from sqlalchemy import func, desc
stmt = select([
        addresses.c.user_id,
        func.count(addresses.c.id).label('num_addresses')]).\
        group_by("user_id").order_by("user_id", desc("num_addresses"))

conn.execute(stmt).fetchall()

u1a, u1b = users.alias(), users.alias()
stmt = select([u1a, u1b]).\
            where(u1a.c.name > u1b.c.name).\
            order_by(u1a.c.name)  # using "name" here would be ambiguous

conn.execute(stmt).fetchall()

#Alias and sub
a1 = addresses.alias()
a2 = addresses.alias()
s = select([users]).\
       where(and_(
           users.c.id == a1.c.user_id,
           users.c.id == a2.c.user_id,
           a1.c.email_address == 'jack@msn.com',
           a2.c.email_address == 'jack@yahoo.com'
       ))
conn.execute(s).fetchall()

#update
stmt = users.update().\
             values(fullname="Fullname: " + users.c.name)
conn.execute(stmt)



stmt = users.insert().\
         values(name=bindparam('_name') + " .. name")
conn.execute(stmt, [
       {'id':4, '_name':'name1'},
       {'id':5, '_name':'name2'},
       {'id':6, '_name':'name3'},
    ])



stmt = users.update().\
             where(users.c.name == 'jack').\
            values(name='ed')

conn.execute(stmt)

stmt = users.update().\
            where(users.c.name == bindparam('oldname')).\
            values(name=bindparam('newname'))
conn.execute(stmt, [
    {'oldname':'jack', 'newname':'ed'},
    {'oldname':'wendy', 'newname':'mary'},
    {'oldname':'jim', 'newname':'jake'},
    ])


#Correlated Updates
stmt = select([addresses.c.email_address]).\
             where(addresses.c.user_id == users.c.id).\
            limit(1)
conn.execute(users.update().values(fullname=stmt))


#Delete
conn.execute(addresses.delete())

conn.execute(users.delete().where(users.c.name > 'm'))

