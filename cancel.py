import requests
import json

# 登录URL和其他URL
login_url = "https://www.letuo.club/apis/auth/login"
event_url = "https://www.letuo.club/apis/orderEvent/activeEvents"
cancel_order_url = "https://www.letuo.club/apis/order/cancel"

# 定义请求头
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Host": "www.letuo.club",
    "Origin": "https://www.letuo.club",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
}

# 定义登录信息
login_data = {
    "username": "zhuhr@digiwin.com",
    "password": "Zhuhaoran1209",
    "validateCode": "",
    "token": "",
    "code": ""
}

# 登录并获取会话
def login(url, data):
    session = requests.Session()
    response = session.post(url, headers=headers, data=json.dumps(data))

    # 打印登录响应以检查成功
    print("登录请求状态码:", response.status_code)
    print("登录响应内容:", response.text)

    # 检查登录是否成功
    if response.status_code == 200:
        print("登录成功")
        return session
    else:
        print("登录失败")
        return None

# 调用登录函数
session = login(login_url, login_data)

# 检查会话是否成功创建
if session:
    cookies = session.cookies.get_dict()
    print("Cookies:", cookies)

    if 'JSESSIONID' in cookies:
        jsessionid = cookies['JSESSIONID']
        headers["Cookie"] = f"JSESSIONID={jsessionid}"

        # 获取事件ID
        event_payload = {"ids": [11]}
        response = session.post(event_url, headers=headers, data=json.dumps(event_payload))

        # 打印获取事件ID响应
        print("获取事件ID请求状态码:", response.status_code)
        print("获取事件ID响应内容:", response.text)

        if response.status_code == 200:
            event_data = response.json()
            print("获取的事件数据:", event_data)
            active_events = event_data.get("data", [])

            if active_events:
                event_id = active_events[0].get("eventId")
                print(f"获取到的eventId: {event_id}")

                # 定义取消点餐请求的payload
                cancel_order_data = {
                    "avatar": "https://www.letuo.club/meal/meal/36_896c0708258c4aefacedaee94d93361a.jpeg",
                    "createTime": 1719388984266,
                    "description": "18104",
                    "eventId": event_id,
                    "id": 9995,
                    "imgs": "",
                    "jobCode": "18104",
                    "name": "紫燕夫妻肺片套餐",
                    "num": 1,
                    "price": 3000,
                    "productId": 16,
                    "productName": "紫燕夫妻肺片套餐",
                    "shopId": 7,
                    "status": 0,
                    "teamId": 11,
                    "unitColor": "#A7C0CA",
                    "unitId": 36,
                    "unitName": "数据中台",
                    "userId": 463,
                    "userName": "何杰"
                }

                # 发送取消点餐请求
                response = session.post(cancel_order_url, headers=headers, data=json.dumps(cancel_order_data))

                # 打印取消点餐响应
                print("取消点餐请求状态码:", response.status_code)
                print("取消点餐响应内容:", response.text)

                if response.status_code == 200:
                    print("取消点餐成功")
                else:
                    print("取消点餐失败")
            else:
                print("未能获取到有效的事件ID")
        else:
            print("获取事件ID失败")
    else:
        print("未能提取JSESSIONID cookie")
else:
    print("会话创建失败")
