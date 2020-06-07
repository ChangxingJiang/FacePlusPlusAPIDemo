import json

KEY_PATH = r"E:\【微云工作台】\环境配置\旷视API环境配置.json"  # 百度API环境配置文件路径

with open(KEY_PATH, "r", encoding="UTF-8") as f:
    setting = json.loads(f.read())

if "API Key" in setting:
    API_KEY = setting["API Key"]
else:
    API_KEY = None
    print("载入旷视API环境配置(API Key)失败")

if "API Secret" in setting:
    API_SECRET = setting["API Secret"]
else:
    API_SECRET = None
    print("载入旷视API环境配置(API Secret)失败")
