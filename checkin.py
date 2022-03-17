import requests
"""
第一次post请求：postA、postA_headers、resp_postA、、、、
第二次get请求 ：getB、、、、
第三次post请求：postC、、、、
"""
username = ""
password = ""
mycontent = ""
# 获取idToken

postA_headers = {'Content-Length': '0', 'Host': 'token.huanghuai.edu.cn', 'Connection': 'Keep-Alive',
                 'Accept-Encoding': 'gzip', 'User-Agent': 'okhttp/3.12.1'
                 }
postA_datas = {'username': username, 'password': password, 'appId': 'com.lantu.MobileCampus.huanghuai', 'geo': '',
               'deviceId': 'Yi90WtKZsAcDAAT1xuUPijdI', 'osType': 'android',
               'clientId': 'c2a1e8ef01e8cbd6b559eab9cd946cad'
               }
resp_postA = requests.post("https://token.huanghuai.edu.cn/password/passwordLogin", data=postA_datas,
                           headers=postA_headers)
resp_dictA = resp_postA.json()
resp_data = resp_dictA['data']
idToken = resp_data['idToken']

# 获取cookie和token
getB_headers = {
    'Host': 'yq.huanghuai.edu.cn:7992',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 4LTE Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.82 Mobile Safari/537.36 SuperApp',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'userToken': idToken,
    'X-Id-Token': idToken,
    'X-Requested-With': 'com.lantu.MobileCampus.huanghuai',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}
getB_cookies = {
    'userToken': idToken, 'Domain': '.huanghuai.edu.cn', 'Path': '/'
}
resp_getB = requests.get("https://yq.huanghuai.edu.cn:7992/cas/studentLogin", headers=getB_headers,
                         cookies=getB_cookies,
                         allow_redirects=False)
p_cookie = resp_getB.headers["Set-Cookie"]
p_token = resp_getB.headers["Location"]
mytoken = p_token[p_token.find('token=') + 6:]
mysession = p_cookie[p_cookie.find('SESSION=') + 8:p_cookie.find('; Path=/; Ht')]

#打卡
postC_headers = {
    'Host': 'yq.huanghuai.edu.cn:7992',
    'Connection': 'keep-alive',
    'Accept': 'application/json, text/plain, */*',
    'x-auth-token': mytoken,
    'User-Agent': 'Mozilla/5.0 (Linux; Android 9; MI 4LTE Build/PQ3A.190801.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/90.0.4430.82 Mobile Safari/537.36 SuperApp',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Origin': 'https://yk.huanghuai.edu.cn:8993',
    'X-Requested-With': 'com.lantu.MobileCampus.huanghuai',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Dest': 'empty',
    'Referer': 'https://yk.huanghuai.edu.cn:8993',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
}
postC_cookies = {
    'userToken': idToken, 'Domain': '.huanghuai.edu.cn', 'Path': '/',
    'SESSION': mysession
}
postC_datas = {
    'content': mycontent
}
resp_postC = requests.post("https://yq.huanghuai.edu.cn:7992/questionAndAnser/wenjuanSubmit",
                           headers=postC_headers, cookies=postC_cookies, data=postC_datas)
resp_dictC = resp_postC.json()
success = resp_dictC['successful']
message = resp_dictC['message']
#发邮件模块

import smtplib
from email.mime.text import MIMEText
from_addr = "xxxxxxxxx" #发送方的邮箱
from_pwd = "xxxxxxxx" #发送方的授权码
to_addr = "xxxxxxxxx" #接收方的邮箱
smtp_srv = "smtp.qq.com"
if not (success):
    text="自动打卡失败，请手动打卡并检查问题！[" + message + "]"
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "打卡失败"
    msg['From'] = from_addr
    msg['To'] = to_addr

    try:
        # 不能直接使用smtplib.SMTP来实例化，第三方邮箱会认为它是不安全的而报错
        # 使用加密过的SMTP_SSL来实例化，它负责让服务器做出具体操作，它有两个参数
        # 第一个是服务器地址，但它是bytes格式，所以需要编码
        # 第二个参数是服务器的接受访问端口，SMTP_SSL协议默认端口是465
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        # 使用授权码登录你的QQ邮箱
        srv.login(from_addr, from_pwd)
        # 使用sendmail方法来发送邮件，它有三个参数
        # 第一个是发送地址
        # 第二个是接受地址，是list格式，意在同时发送给多个邮箱
        # 第三个是发送内容，作为字符串发送
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        print('发送成功-打卡失败')
    except Exception as e:
        print('发送失败-打卡失败')
    finally:
        # 无论发送成功还是失败都要退出你的QQ邮箱
        srv.quit()
else:
    text = "已打卡！[" + message + "]"
    msg = MIMEText(text, "plain", "utf-8")
    msg['Subject'] = "Successful"
    msg['From'] = from_addr
    msg['To'] = to_addr
    try:
        srv = smtplib.SMTP_SSL(smtp_srv.encode(), 465)
        srv.login(from_addr, from_pwd)
        srv.sendmail(from_addr, [to_addr], msg.as_string())
        print('发送成功-打卡成功')
    except Exception as e:
        print('发送失败-打卡成功')
    finally:
        srv.quit()