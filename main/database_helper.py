# -*- coding: utf-8 -*-
import time
import pymysql


class PyMySQL:
    # 获取当前时间
    def getcurrenttime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    # 数据库初始化 修改对应的连接信息
    def __init__(self, host='localhost', user='root', passwd='root', db='invest', port=3306, charset='utf8'):
        pymysql.install_as_MySQLdb()
        try:
            self.charset = charset
            self.connect = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=3306, charset='utf8')
            self.connect.ping(True)  # 使用mysql ping来检查连接,实现超时自动重新连接
            print(self.getcurrenttime(), u"MySQL DB Connect Success:", user + '@' + host + ':' + str(port) + '/' + db)
            self.cur = self.connect.cursor()
        except Exception as e:
            print(self.getcurrenttime(), u"MySQL DB Connect Error :%d: %s" % (e.args[0], e.args[1]))

    # 插入数据
    def insertData(self, table, my_dict):
        try:
            # self.db.set_character_set('utf8')
            cols = ', '.join(my_dict.keys())
            values = '","'.join(my_dict.values())
            sql = "replace into %s (%s) values (%s)" % (table, cols, '"' + values + '"')
            # print (sql)
            try:
                result = self.cur.execute(sql)
                insert_id = self.connect.insert_id()
                self.connect.commit()
                # 判断是否执行成功
                if result:
                    # print (self.getCurrentTime(), u"Data Insert Sucess")
                    return insert_id
                else:
                    return 0
            except Exception as e:
                # 发生错误时回滚
                self.connect.rollback()
                print(self.getcurrenttime(), u"Data Insert Failed: %s" % e)
                return 0
        except Exception as e:
            print(self.getcurrenttime(), u"MySQLdb Error: %s" % e)
            return 0
