from datetime import datetime

import pymysql

from hope import Hope
from user import *
from task import *

global db
global cursor
global database


def init_database():
    connect_database()


def connect_database():
    global db, cursor
    db = pymysql.connect(host='rm-2zenyi1t41y3jl9x2uo.mysql.rds.aliyuncs.com',
                         user='buaa_py',
                         password='wyt20041111AA',
                         database='buaapydb')

    cursor = db.cursor()
    global database
    database = 'buaapydb'


def sign_up_database(account, email, password):
    global db, cursor, database
    if str(account) == 0 or str(password) == 0:
        return False, "请输入非空用户名和密码"
    sql = 'select account from {}.user where account = "{}"'.format(database, account)
    cursor.execute(sql)
    if cursor.rowcount:
        return False, "This account has been signed up!\n"
    else:
        cursor.execute('select count(*) from {}.user'.format(database))
        line_num = int(cursor.fetchone()[0])
        if line_num != 0:
            sql = 'select max(id) from {}.user'.format(database)
            cursor.execute(sql)
            max_id = int(cursor.fetchone()[0])
        else:
            max_id = -1
        id = max(max_id + 1, line_num)

        sql = "insert into {0}.user(id, account, password, name, email, start, end, headImage) values('{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}')". \
            format(database, id, account, password, 'buaaer', email, '9:00', '21:00', 'https://i.imgur.com/vUlftac.png')
        cursor.execute(sql)
        db.commit()

        sql = 'use {}'.format(database)
        cursor.execute(sql)

        sql = 'create table user_{}_task (' \
              'id int comment "序号",' \
              'title varchar(500) comment"标题",' \
              'description varchar(500) comment"描述",' \
              'importance int comment "重要性",' \
              'isDaily varchar(500) comment "是否为普通任务",' \
              'type varchar(500) comment "类别",' \
              'ddl varchar(500) comment "截止日期",' \
              'duration int comment "用时",' \
              'state varchar(500) comment "状态"' \
              ')comment "user{}\'s task table"'.format(id, id)
        cursor.execute(sql)

        sql = 'create table user_{}_hope (' \
              'id int comment "序号",' \
              'title varchar(500) comment"标题",' \
              'ddl varchar(500) comment "截止日期"' \
              ')comment "user{}\'s hope table"'.format(id, id)
        cursor.execute(sql)
        db.commit()
        return True, "注册成功"


def login_in_database(account, password):
    global db, cursor, database

    sql = 'select account from {}.user where account = "{}"'.format(database, account)
    cursor.execute(sql)
    if cursor.rowcount == 0:
        return False, None, "该用户未注册"

    sql = 'select password from {}.user where account = "{}"'.format(database, account)
    cursor.execute(sql)
    password_in_database = cursor.fetchone()[0]
    if password_in_database != password:
        return False, None, "密码错误"

    sql = 'select * from {}.user where account = "{}"'.format(database, account)
    cursor.execute(sql)
    user_info_tuple = cursor.fetchone()
    id = int(user_info_tuple[0])
    return True, id, '成功登录\n欢迎用户, {}'.format(account)


def add_task_database(id, task):
    global database
    sql = 'select id from {}.user where id = "{}"'.format(database, id)
    cursor.execute(sql)

    sql = 'select count(*) from {}.user_{}_task'.format(database, id)

    cursor.execute(sql)

    task_num = int(cursor.fetchone()[0])
    sql = 'select max(id) from {}.user_{}_task'.format(database, id)
    cursor.execute(sql)

    if task_num != 0:
        task_id_max = int(cursor.fetchone()[0])
    else:
        task_id_max = 0
    task.id = max(task_num, task_id_max + 1)

    sql = "insert into {0}.user_{1}_task(id, title, description, importance, isDaily, type, ddl, duration, state) " \
          "values('{2}', '{3}', '{4}', '{5}', '{6}', '{7}', '{8}', '{9}', '{10}')". \
        format(database, id, task.id, task.title, task.description,
               task.importance, str(task.isDaily), task.type, task.ddl, task.duration, task.state)
    cursor.execute(sql)
    db.commit()


def get_task_list(fet):
    ls = []
    for _ in fet:
        task_id, title, description, importance, isDaily, type, duration, ddl, state = _
        task = Task(
            title=title,
            description=description,
            importance=importance,
            isDaily=isDaily,
            type=type,
            ddl=ddl,
            duration=duration,
            state=state
        )
        task.id = task_id
        ls.append(task)
    return ls


def get_task_list_database(id):
    global database
    sql = 'select id, title, description, importance, isDaily, type, duration, ddl, state from {}.user_{}_task'.format(
        database, id)
    cursor.execute(sql)
    user_task_tuple = cursor.fetchall()
    tasks = get_task_list(user_task_tuple)
    return tasks


def get_task_database(id, task_id):
    global database
    sql = 'select title, description, importance, isDaily, type, duration, ddl, state from {}.user_{}_task where id = "{}"'.format(
        database, id, task_id)
    cursor.execute(sql)
    tasks = cursor.fetchone()

    title, description, importance, isDaily, type, duration, ddl, state = tasks
    task = Task(
        title=title,
        description=description,
        importance=importance,
        isDaily=isDaily,
        type=type,
        ddl=ddl,
        duration=duration,
        state=state
    )
    task.id = task_id
    return task


def modify_task_database(id, task):
    global database
    sql = 'select id from {}.user where id = "{}"'.format(database, id)
    cursor.execute(sql)
    # 检查用户是否存在
    if not cursor.fetchone():
        return
    # 更新任务
    sql = "update {0}.user_{1}_task set title = '{2}', description = '{3}', importance = '{4}', isDaily = '{5}', " \
          "type = '{6}', ddl = '{7}', duration = '{8}', state = '{9}' where id = '{10}'".format(
        database, id, task.title, task.description, task.importance, str(task.isDaily),
        task.type, task.ddl, task.duration, task.state, task.id
    )
    cursor.execute(sql)
    db.commit()


def delete_task_database(user_id, task_id):
    global db, cursor, database

    try:
        # 检查用户是否存在
        sql = 'select id from {}.user where id = "{}"'.format(database, user_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return False, "用户不存在"
        # 检查任务是否存在
        sql = 'select id from {}.user_{}_task where id = "{}"'.format(database, user_id, task_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return False, "任务不存在"
        # 删除任务
        sql = 'delete from {}.user_{}_task where id = "{}"'.format(database, user_id, task_id)
        cursor.execute(sql)
        db.commit()
        return True, "任务已成功删除"

    except pymysql.Error as e:
        return False, f"数据库错误: {e}"


def update_task_state(id, state):
    global database
    now = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    sql = "select id, ddl, state from {}.user_{}_task".format(database, id)
    cursor.execute(sql)
    tasks = cursor.fetchall()

    for task in tasks:
        task_id, ddl, task_state = task
        task_date = datetime.strptime(ddl, '%Y/%m/%d')
        if task_state == TASK_OVERDUE:
            continue

        if now > task_date:
            update_sql = "update {}.user_{}_task set state = '{}' where id = {}".format(database, id, TASK_OVERDUE,
                                                                                        task_id)
            cursor.execute(update_sql)

        elif now == task_date and task_state == TASK_NOTSTART:
            update_sql = "update {}.user_{}_task set state = '{}' where id = {}".format(database, id, TASK_UNDERWAY,
                                                                                        task_id)
            cursor.execute(update_sql)

    db.commit()


def update_timer_state_database(id):
    update_task_state(id, TASK_OVERDUE)
    print("update finished 5000ms")


def modify_task_state_database(user_id, task_id, new_state):
    global db, cursor, database
    sql = "update {}.user_{}_task set state = '{}' where id = {}".format(database, user_id, new_state, task_id)
    cursor.execute(sql)
    db.commit()
    return True, "Successfully updated task {} in user {}'s account".format(task_id, user_id)


def calendar_get_task_database(id, ddl):
    global database
    sql = 'select id, title, description, importance, isDaily, type, duration, state from {}.user_{}_task where ddl = "{}"'.format(
        database, id, ddl)
    cursor.execute(sql)
    tasks = cursor.fetchall()
    ans = []
    for _ in tasks:
        task_id, title, description, importance, isDaily, type, duration, state = _
        task = Task(
            title=title,
            description=description,
            importance=importance,
            isDaily=isDaily,
            type=type,
            ddl=ddl,
            duration=duration,
            state=state
        )
        task.id = task_id
        ans.append(task)

    db.commit()
    return ans


def get_user_database(id):
    global database
    sql = 'select account, password, name, email, start, end, headImage from {}.user where id = "{}"'.format(database,
                                                                                                             id)
    cursor.execute(sql)
    users = cursor.fetchone()
    account, password, name, email, start, end, headImage = users
    user = User(
        id=id,
        account=account,
        password=password,
        name=name,
        email=email,
        start=start,
        end=end,
        head_image=headImage
    )
    db.commit()
    return user


def modify_user_database(user):
    global database
    sql = "update {0}.user set account = '{1}', password = '{2}', name = '{3}', email = '{4}', " \
          "start = '{5}', end = '{6}', headImage = '{7}' where id = '{8}'".format(
        database, user.account, user.password, user.name, user.email, user.start, user.end, user.head_image, user.id)
    cursor.execute(sql)
    db.commit()


def get_hope_list(fet):
    ls = []
    for _ in fet:
        hope_id, title, ddl = _
        hope = Hope(
            title=title,
            ddl=ddl
        )
        hope.id = hope_id
        ls.append(hope)

    return ls


def get_hope_list_database(id):
    global database
    sql = 'select id, title, ddl from {}.user_{}_hope'.format(database, id)
    cursor.execute(sql)
    user_hope_tuple = cursor.fetchall()
    hopes = get_hope_list(user_hope_tuple)
    return hopes


def add_hope_database(id, hope):
    global database
    sql = 'select id from {}.user where id = "{}"'.format(database, id)
    cursor.execute(sql)

    sql = 'select count(*) from {}.user_{}_hope'.format(database, id)

    cursor.execute(sql)

    hope_num = int(cursor.fetchone()[0])
    sql = 'select max(id) from {}.user_{}_hope'.format(database, id)
    cursor.execute(sql)

    if hope_num != 0:
        hope_id_max = int(cursor.fetchone()[0])
    else:
        hope_id_max = 0
    hope.id = max(hope_num, hope_id_max + 1)

    sql = "insert into {0}.user_{1}_hope(id, title, ddl) " \
          "values('{2}', '{3}', '{4}')". \
        format(database, id, hope.id, hope.title, hope.ddl)
    cursor.execute(sql)
    db.commit()


def modify_hope_database(id, hope):
    global database
    sql = 'select id from {}.user where id = "{}"'.format(database, id)
    cursor.execute(sql)
    # 检查用户是否存在
    if not cursor.fetchone():
        return

    sql = "update {0}.user_{1}_hope set title = '{2}', ddl = '{3}' where id = '{4}'".format(
        database, id, hope.title, hope.ddl, hope.id
    )
    cursor.execute(sql)
    db.commit()


def delete_hope_database(user_id, hope_id):
    global db, cursor, database

    try:
        sql = 'select id from {}.user where id = "{}"'.format(database, user_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return False, "用户不存在"

        sql = 'select id from {}.user_{}_hope where id = "{}"'.format(database, user_id, hope_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return False, "hope不存在"

        sql = 'delete from {}.user_{}_hope where id = "{}"'.format(database, user_id, hope_id)
        cursor.execute(sql)
        db.commit()
        return True, "hope已成功删除"

    except pymysql.Error as e:
        return False, f"数据库错误: {e}"


def delete_user_database(user_id):
    global db, cursor, database

    try:
        # 检查用户是否存在
        sql = 'select id from {}.user where id = "{}"'.format(database, user_id)
        cursor.execute(sql)
        if cursor.rowcount == 0:
            return False, "用户不存在"

        # 删除用户的所有任务
        sql = 'delete from {}.user_{}_task'.format(database, user_id)
        cursor.execute(sql)

        # 删除用户的所有希望
        sql = 'delete from {}.user_{}_hope'.format(database, user_id)
        cursor.execute(sql)

        # 删除用户记录
        sql = 'delete from {}.user where id = "{}"'.format(database, user_id)
        cursor.execute(sql)

        db.commit()
        return True, "用户及其所有数据已成功删除"

    except pymysql.Error as e:
        return False, f"数据库错误: {e}"

