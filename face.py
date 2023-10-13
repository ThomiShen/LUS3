import base64
import requests
# 定义API Key和Secret Key
APP_ID = '40079341'     #ID短号
API_KEY = '0f5GrnbmAHsksnagaUDpFW3l'  #无规律很长
SECRET_KEY = 'P4MNGHY2m17X3QUUiOaFcxnqhcgSnCTL'   #无规律很长

# 获取access_token
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(API_KEY, SECRET_KEY)
response = requests.get(host)
access_token = response.json()['access_token']

def analyze_face(image_data):
    # 将图片文件转换为base64编码
    base64_data = base64.b64encode(image_data)

    # 调用百度API进行人脸识别
    request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {
        "image": base64_data,
        "image_type": "BASE64",
        "face_field": "age,beauty,expression,face_shape,gender,glasses,emotion,face_type,spoofing",
        "face_type": "LIVE"
    }
    request_url = request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    face_result = response.json()

    # 返回分析结果
    return face_result['result']['face_list'][0]
