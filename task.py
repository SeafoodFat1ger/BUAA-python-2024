import time

time_tuple = time.localtime(time.time())
curYear = time_tuple[0]
curMonth = time_tuple[1]
curDay = time_tuple[2]

TASK_FINISHED = "已完成"
TASK_OVERDUE = "已过期"
TASK_UNDERWAY = "正在进行"
TASK_NOTSTART = "未启动"

TASK_TYPE_OTHER = "其他"
TASK_TYPE_WORK = "工作"
TASK_TYPE_STUDY = "学习"


class Task():
    def __init__(self,
                 title='',
                 description='',
                 importance=1,
                 isDaily=False,
                 type=TASK_TYPE_OTHER,
                 ddl=str(curYear) + '/' + str(curMonth) + '/' + str(curDay),
                 duration=1,
                 state=TASK_NOTSTART,
                 ) -> None:
        self.id = None
        self.title = title
        self.description = description
        self.importance = importance
        self.isDaily = isDaily
        self.type = type
        self.ddl = ddl
        self.duration = duration  # int 1-10
        self.state = state
