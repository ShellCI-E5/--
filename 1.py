# -*- coding: UTF-8 -*-
import requests as req
import json,sys,time
#先注册azure应用,确保应用有以下权限:
#files:	Files.Read.All、Files.ReadWrite.All、Sites.Read.All、Sites.ReadWrite.All
#user:	User.Read.All、User.ReadWrite.All、Directory.Read.All、Directory.ReadWrite.All
#mail:  Mail.Read、Mail.ReadWrite、MailboxSettings.Read、MailboxSettings.ReadWrite
#注册后一定要再点代表xxx授予管理员同意,否则outlook api无法调用






path=sys.path[0]+r'/1.txt'
num1 = 0

def gettoken(refresh_token):
    headers={'Content-Type':'application/x-www-form-urlencoded'
            }
    data={'grant_type': 'refresh_token',
          'refresh_token': refresh_token,
          'client_id':id,
          'client_secret':secret,
          'redirect_uri':'http://localhost:53682/'
         }
    html = req.post('https://login.microsoftonline.com/common/oauth2/v2.0/token',data=data,headers=headers)
    jsontxt = json.loads(html.text)
    refresh_token = jsontxt['refresh_token']
    access_token = jsontxt['access_token']
    with open(path, 'w+') as f:
        f.write(refresh_token)
    return access_token
def main():
    fo = open(path, "r+")
    refresh_token = fo.read()
    fo.close()
    global num1
    localtime = time.asctime( time.localtime(time.time()) )
    access_token=gettoken(refresh_token)
    headers={
    'Authorization':access_token,
    'Content-Type':'application/json'
    }
    try:
        if req.get(r'https://graph.microsoft.com/beta/users',headers=headers).status_code == 200:#组织中的所有用户调用
            num1+=1
            print("1调用成功"+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/users/${{ secrets.USER_ID }}/presence',headers=headers).status_code == 200:#用户当前状态调用
            num1+=1
            print("2调用成功"+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/security/alerts?$top=1',headers=headers).status_code == 200:#警告
            num1+=1
            print('3调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/security/secureScores?$top=5',headers=headers).status_code == 200:#安全功能分数 (beta)
            num1+=1
            print('4调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/security/secureScoreControlProfiles?$top=5',headers=headers).status_code == 200:#安全功能分数控制配置文件 (beta)
            num1+=1
            print('5调用成功'+str(num1)+'次')    
        if req.get(r'https://graph.microsoft.com/beta/identity/conditionalAccess/namedLocations',headers=headers).status_code == 200:#获取所有命名位置（beta 版本）
            num1+=1
            print('6调用成功'+str(num1)+'次')    
        if req.get(r'https://graph.microsoft.com/beta/identity/conditionalAccess/policies',headers=headers).status_code == 200:#获取所有条件访问策略
            num1+=1
            print('7调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/applications?$count=true',headers=headers).status_code == 200:#列出所有应用及计数
            num1+=1
            print('8调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/identityProtection/riskDetections',headers=headers).status_code == 200:#获取风险检测
            num1+=1
            print('8调用成功'+str(num1)+'次') 
        if req.get(r'https://graph.microsoft.com/beta/devices',headers=headers).status_code == 200:#列出 Azure AD 设备
            num1+=1
            print('9调用成功'+str(num1)+'次')
        if req.get(r'https://graph.microsoft.com/beta/applications/${{ secrets.APP_ID }}',headers=headers).status_code == 200:#检索应用程序属性
            num1+=1
            print('10调用成功'+str(num1)+'次')
            print('此次运行结束时间为 :', localtime)
    except:
        print("pass")
        pass
for _ in range(3):
    main()
