import requests
from requests.packages import urllib3
import json
from prettytable import PrettyTable
import pickle
import re
import time
from CodeClass import YDMHttp

req = requests.Session()


class login(object):

    def __init__(self, username, pwd, date, start, end):

        # 取消证书验证错误
        urllib3.disable_warnings()
        # 保持登录状态
        self.username = username,
        self.password = pwd,
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
                          'Chrome/67.0.3396.87 Safari/537.36 ',
            'Host': 'kyfw.12306.cn',
            # 'Referer': 'https://kyfw.12306.cn/otn/login/init',
            'Referer': 'https://kyfw.12306.cn/otn/resources/login.html',
        }
        # self.session = requests.session()
        self.start = start
        self.end = end
        self.date = date

    # 云打码
    def getCode(self, imgPath):
        # 用户名
        username = 'Ojiasj'

        # 密码
        password = 'Ojiasj3455'

        # 软件ID，开发者分成必要参数。登录开发者后台【我的软件】获得！
        appid = 7778

        # 软件密钥，开发者分成必要参数。登录开发者后台【我的软件】获得！
        appkey = 'b0952546ed2cff28ff408e309dd77bc1'

        # 图片文件
        filename = imgPath

        # 验证码类型，# 例：1004表示4位字母数字，不同类型收费不同。请准确填写，否则影响识别率。在此查询所有类型 http://www.yundama.com/price.html
        codetype = 6701

        # 超时时间，秒
        timeout = 20
        result = None
        # 检查
        if (username == 'username'):
            print('请设置好相关参数再测试')
        else:
            # 初始化
            yundama = YDMHttp(username, password, appid, appkey)

            # 登陆云打码
            uid = yundama.login()
            print('uid: %s' % uid)

            # 查询余额
            balance = yundama.balance()
            print('balance: %s' % balance)

            # 开始识别，图片路径，验证码类型ID，超时时间（秒），识别结果
            cid, result = yundama.decode(filename, codetype, timeout)
            print('cid: %s, result: %s' % (cid, result))

        return result

    # 获取cookies
    def get_web(self):
        global req
        # 获取第一次访问的cookies
        get_web = req.get(
            url="https://kyfw.12306.cn/otn/HttpZF/logdevice?algID=ePDrudm04F&hashCode=LsiGTHjzxZP4Y0CqYMSqB_gCYSxedrZtc-b-Udn5U64&FMQw=1&q4f3=zh-CN&VySQ=FGE5ZXJgSTAVsIIM9ospTQfYHncbH5Ig&VPIf=1&custID=133&VEek=unknown&dzuS=29.0%20r0&yD16=0&EOQP=f57fa883099df9e46e7ee35d22644d2b&jp76=7047dfdd1d9629c1fb64ef50f95be7ab&hAqN=Win32&platform=WEB&ks0Q=6f0fab7b40ee4a476b4b3ade06fe9065&TeRS=1080x1920&tOHY=24xx1080x1920&Fvje=i1l1o1s1&q5aJ=-8&wNLf=99115dfb07133750ba677d055874de87&0aew=Mozilla/5.0%20(Windows%20NT%206.1;%20WOW64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/63.0.3239.132%20Safari/537.36&E3gR=fd7a8adb89dd5bf3a55038ad1adc5d35&timestamp=" + str(
                int(time.time() * 1000)),
            headers=self.headers,
            verify=False,
        )

        rail_deviceid = re.search(r'"dfp":"(.*?)"', get_web.text).group(1)
        req.cookies['RAIL_DEVICEID'] = rail_deviceid

    # 获取验证码和登录
    def get_ver(self):
        with open("Verification.jpg", "wb") as f:
            global req
            res = req.get(
                url="https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.07498399989616189",
                headers=self.headers,
                verify=False,
            )
            f.write(res.content)
            f.close()
        answer = ""
        so = self.getCode("Verification.jpg")
        for s in so:
            if int(s) == 1:
                answer += "38,43,"
            elif int(s) == 2:
                answer += "109,46,"
            elif int(s) == 3:
                answer += "179,44,"
            elif int(s) == 4:
                answer += "257,45,"
            elif int(s) == 5:
                answer += "43,117,"
            elif int(s) == 6:
                answer += "105,108,"
            elif int(s) == 7:
                answer += "183,115,"
            elif int(s) == 8:
                answer += "253,117,"
        print(answer)
        data = {
            "answer": answer,
            "login_site": "E",
            "rand": "sjrand",
        }
        submit_ver = req.get(
            url="https://kyfw.12306.cn/passport/captcha/captcha-check",
            params=data,
            headers=self.headers,
            verify=False,
        )
        passmess = json.loads(submit_ver.text)
        # print(passmess['result_code'])
        if passmess['result_code'] == '4':  # 4代表成功，5代表验证码错误，8代表验证信息为空
            # print(passmess['result_message'])
            print("验证码校验成功")
        else:
            print('验证失败，请重新开始！')
            exit()

        # 登录
        data = {
            "username": self.username,
            "password": self.password,
            "appid": "otn",
            "answer": answer,
        }
        # global req
        login = req.post(
            url="https://kyfw.12306.cn/passport/web/login/",
            data=data,
            headers=self.headers,
        )
        res = login.json()
        print(res)
        if res["result_code"] == 0:
            print("登录成功")
        else:
            print("登录失败,帐号或者密码错误")
            exit()

    # 登录
    # def Final_login(self):
    #     answer = ""
    #     so = input("打开Verification图片，写出对应位置，用1-8：")
    #     for s in so:
    #         if int(s) == 1:
    #             answer += "38,43,"
    #         elif int(s) == 2:
    #             answer += "109,46,"
    #         elif int(s) == 3:
    #             answer += "179,44,"
    #         elif int(s) == 4:
    #             answer += "257,45,"
    #         elif int(s) == 5:
    #             answer += "43,117,"
    #         elif int(s) == 6:
    #             answer += "105,108,"
    #         elif int(s) == 7:
    #             answer += "183,115,"
    #         elif int(s) == 8:
    #             answer += "253,117,"
    #
    #     data = {
    #         "username": self.username,
    #         "password": self.password,
    #         "appid": "otn",
    #         "answer": answer,
    #     }
    #     global req
    #     login = req.post(
    #         url="https://kyfw.12306.cn/passport/web/login/",
    #         data=data,
    #         headers=self.headers,
    #     )
    #     res = login.json()
    #     print(res)
    #     if res["result_code"] == 0:
    #         print("登录成功")
    #     else:
    #         print("登录失败,帐号或者密码错误")
    #         exit()

    # 查询票
    def get_msg(self, start, end, options, site):
        """

        :param start: 开始站点
        :param end:   结束站点
        :param options:  列车型号
        :param site:  站点名称
        :return:
        """
        global req
        get = req.get(
            url="https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes={}".format(
                self.date, site[self.start], site[self.end], "ADULT"),
            headers=self.headers,
            verify=False,
            # data=data,
        )
        msg = get.json()["data"]["result"]
        # print(msg)

        pt = PrettyTable()
        pt._set_field_names('车次 车站 时间 历时 商务座 一等座 二等座 动卧 软卧 硬卧 硬座 无座'.split())
        for raw_train in msg:
            data_list = raw_train.split('|')
            # print(data_list)
            train_no = data_list[3]
            initial = train_no[0].lower()
            if not options or initial in options:
                start_time = data_list[8]
                arrive_time = data_list[9]
                time_duration = data_list[10]
                business_seat = data_list[32] or '--'
                first_class_seat = data_list[31] or '--'
                second_class_seat = data_list[30] or '--'
                pneumatic_sleep = data_list[33] or '--'
                soft_sleep = data_list[23] or '--'
                hard_sleep = data_list[28] or '--'
                hard_seat = data_list[29] or '--'
                no_seat = data_list[26] or '--'
                pt.add_row([train_no,
                            '\n'.join([start, end]),
                            '\n'.join([start_time, arrive_time]),
                            time_duration,
                            business_seat,
                            first_class_seat,
                            second_class_seat,
                            pneumatic_sleep,
                            soft_sleep,
                            hard_sleep,
                            hard_seat,
                            no_seat
                            ])
        print(pt)

        # q = msg.split("|")
        # for i in q:
        #     if len(i) > 11:
        #         q.remove(i)
        #     if '0","' == i:
        #         q.remove(i)
        # count = q.count("预订")
        # for i in range(count):
        #     i += i * 32
        #     print('\033[0;31;40m', q[i:i + 33][0:3], '\033[40m', end=" ")
        #     print('\033[0;31;40m', q[i:i + 33][5:], '\033[40m', end=" ")
        #     print("--" * 60)

    def doall(self):
        self.get_web()
        self.get_ver()
        # self.Final_login()


if __name__ == "__main__":
    # 基本登录信息
    username = input("请输入登录账户：")
    pwd = input("请输入密码：")
    date = input("请输入要查询的车次时间，例如：2018-10-20：")
    start = input("请输入出发地：")
    end = input("请输入目的地：")
    site = pickle.load(open("site", "rb"))
    try:
        if start not in site or end not in site:
            raise Exception
    except Exception as f:
        print("站点不存在")
    else:
        options = input("请输入列车类型（格式g、d、t、k、z，如果不需要可以直接回车）: ")
        login = login(username, pwd, date, start, end)
        login.get_web()
        login.get_ver()
        # login.Final_login()
        login.get_msg(start, end, options, site)
    s = input("按q退出")
    while s == "q":
        exit()
