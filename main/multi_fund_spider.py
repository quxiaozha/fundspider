# -*- coding: utf-8 -*-
"""
# 多线程爬取信息并写入mysql
# 参考: https://blog.csdn.net/huayanqiaq/article/details/53070768
"""

import threading
from queue import Queue
import queue
import time
from fund_spider import FundSpiders


class Worker(threading.Thread):
    def __init__(self, task):
        threading.Thread.__init__(self)
        self.taskQ = task  # type: Queue
        self.thread_stop = False
        self.fs = FundSpiders()

    def run(self):
        while not self.thread_stop:
            try:
                task = self.taskQ.get(block=True, timeout=20)  # 接收任务 待爬取的url队列
            except queue.Empty:
                print('finish!')
                self.thread_stop = True
                break
            self.fs.getFundManager(task)
            # time.sleep(0.1)
            self.taskQ.task_done()  # 完成一个任务

    def stop(self):
        self.thread_stop = True


if __name__ == "__main__":
    THREAD_NUM = 8
    q = Queue()
    fs = FundSpiders()
    for url in fs.getAllFundManagerUrl():
        q.put(url)

    start_time = time.time()
    for i in range(THREAD_NUM):
        t = Worker(q)
        t.start()
    print("***************wait for finish!")
    q.join()  # 等待所有任务完成
    end_time = time.time()

    print('开始时间: %s' % start_time)
    print('结束时间: %s' % end_time)
    print("总共耗时:{0:.5f}秒".format(end_time - start_time))  # 格式输出耗时
    print("***************all task finished!")



