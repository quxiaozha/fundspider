# -*- coding:utf-8 -*-

"""
# 参考https://blog.csdn.net/yuzhucu/article/details/55261024
"""
from bs4 import BeautifulSoup
import time
import demjson
from database_helper import PyMySQL
from request_helper import getURL


class FundSpiders():
    def __init__(self):
        self.database = PyMySQL()

    def getCurrentTime(self):
        # 获取当前时间
        return time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime(time.time()))

    def getAllFundManagerUrl(self):
        """
        基金经理大全
        :return:
        """
        try:
            fund_url = "http://fund.eastmoney.com/Data/FundDataPortfolio_Interface.aspx?dt=14&mc=returnjson&ft=all&pn" \
                       "=5000&pi=1&sc=abbname&st=asc "
            res = getURL(fund_url)
        except Exception as e:
            print(self.getCurrentTime(), 'getAllFundManager', fund_url, e)

        records = res.text.split("=")[1].strip()
        json = demjson.decode(records)
        manager_id = [x[0] for x in json['data']]  # 基金经理id
        manager_url = []
        for mid in manager_id:
            url = "http://fund.eastmoney.com/manager/" + mid + ".html"
            manager_url.append(url)
        return manager_url

    def getFundManager(self, manager_url):
        """
        基金经理大全
        :return:
        """
        try:
            res = getURL(manager_url)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
        except Exception as e:
            print(self.getCurrentTime(), 'getAllFundManager', manager_url, e)

        try:
            m_info = soup.select_one('.jlinfo.clearfix')
            manager_info = {}
            try:
                manager_info['manager_id'] = manager_url.strip('http://fund.eastmoney.com/manager/.html')
                manager_info['manager_name'] = m_info.select_one('#name_1').getText().strip()
                manager_info['manager_url'] = manager_url
                info = m_info.select('.right.jd')[0].getText().strip().replace(' ', '').replace('\r', '').split('\n')
                manager_info['employment_time'] = info[0].split('：')[1].strip()
                manager_info['employment_date'] = info[1].split('：')[1].strip()
                manager_info['company_name'] = info[3].split('：')[1].strip()
                management_info = m_info.select_one('.gmContainer')
                # 部分基金经理现任基金资产总规模为 --
                try:
                    manager_info['management_scale'] = management_info.select('.redText')[0].getText().strip() + \
                                                       management_info.select('.textText')[0].getText().strip()
                except Exception as e:
                    manager_info['management_scale'] = management_info.select('.numtext')[0].getText().strip()
                # 部分基金经理任期最大回报为 --
                try:
                    manager_info['best_return'] = management_info.select('.redText')[1].getText().strip()
                except Exception as e:
                    manager_info['best_return'] = management_info.select('.numtext')[1].getText().strip()

                manager_info['created_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                manager_info['updated_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                manager_info['data_source'] = 'eastmoney'
            except Exception as e:
                print(self.getCurrentTime(), 'managerInfo', manager_url, e)
            # print(manager_info)

            try:
                self.database.insertData('fund_manager', manager_info)
            except Exception as e:
                print(self.getCurrentTime(), 'insert fund_manager error', manager_url, e)

            f_info = soup.findAll('table')

            preManaged = f_info[1].findAll('tbody')[0]
            for tr in preManaged.findAll('tr'):
                prefund_info = {}
                try:
                    prefund_info['manager_id'] = manager_url.strip('http://fund.eastmoney.com/manager/.html')
                    prefund_info['fund_code'] = (tr.select('td:nth-of-type(1)')[0].getText().strip())
                    prefund_info['fund_name'] = (tr.select('td:nth-of-type(2)')[0].getText().strip())
                    prefund_info['fund_type'] = (tr.select('td:nth-of-type(4)')[0].getText().strip())
                    prefund_info['fund_scale'] = (tr.select('td:nth-of-type(5)')[0].getText().strip())
                    prefund_info['employment_time'] = (tr.select('td:nth-of-type(6)')[0].getText().strip())
                    prefund_info['employment_date'] = (tr.select('td:nth-of-type(7)')[0].getText().strip())
                    prefund_info['employment_return'] = (tr.select('td:nth-of-type(8)')[0].getText().strip())
                    prefund_info['created_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    prefund_info['updated_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    prefund_info['data_source'] = 'eastmoney'
                except Exception as e:
                    print(self.getCurrentTime(), 'previousManaged', manager_url, e)
                # print(prefund_info)

                try:
                    self.database.insertData('previous_managed_info', prefund_info)
                except Exception as e:
                    print(self.getCurrentTime(), 'insert previous_managed error', manager_url, e)

            curManaged = f_info[2].findAll('tbody')[0]
            for tr in curManaged.findAll('tr'):
                curfund_info = {}
                try:
                    curfund_info['manager_id'] = manager_url.strip('http://fund.eastmoney.com/manager/.html')
                    curfund_info['fund_code'] = (tr.select('td:nth-of-type(1)')[0].getText().strip())
                    curfund_info['fund_name'] = (tr.select('td:nth-of-type(2)')[0].getText().strip())
                    curfund_info['fund_type'] = (tr.select('td:nth-of-type(3)')[0].getText().strip())
                    curfund_info['three_months_income'] = (tr.select('td:nth-of-type(4)')[0].getText().strip())
                    curfund_info['three_months_rank'] = (tr.select('td:nth-of-type(5)')[0].getText().strip())
                    curfund_info['six_months_income'] = (tr.select('td:nth-of-type(6)')[0].getText().strip())
                    curfund_info['six_months_rank'] = (tr.select('td:nth-of-type(7)')[0].getText().strip())
                    curfund_info['one_year_income'] = (tr.select('td:nth-of-type(8)')[0].getText().strip())
                    curfund_info['one_year_rank'] = (tr.select('td:nth-of-type(9)')[0].getText().strip())
                    curfund_info['two_years_income'] = (tr.select('td:nth-of-type(10)')[0].getText().strip())
                    curfund_info['two_years_rank'] = (tr.select('td:nth-of-type(11)')[0].getText().strip())
                    curfund_info['this_year_income'] = (tr.select('td:nth-of-type(12)')[0].getText().strip())
                    curfund_info['this_year_rank'] = (tr.select('td:nth-of-type(13)')[0].getText().strip())
                    curfund_info['created_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    curfund_info['updated_date'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                    curfund_info['data_source'] = 'eastmoney'
                except Exception as e:
                    print(self.getCurrentTime(), 'currentManaged', manager_url, e)
                # print(curfund_info)

                try:
                    self.database.insertData('current_managed_info', curfund_info)
                except Exception as e:
                    print(self.getCurrentTime(), 'insert current_managed error', manager_url, e)
            print(manager_info)
        except Exception as e:
            print(self.getCurrentTime(), 'getFundManager(self, manager_url)', manager_url, e)


