import time

time_tuple = time.localtime(time.time())
curYear = time_tuple[0]
curMonth = time_tuple[1]
curDay = time_tuple[2]


class Hope():
    def __init__(self,
                 title='',
                 ddl=str(curYear) + '/' + str(curMonth) + '/' + str(curDay),
                 ) -> None:
        self.id = None
        self.title = title
        self.ddl = ddl
