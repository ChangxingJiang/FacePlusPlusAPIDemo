import json
import time
import urllib.error
import urllib.request

import requests

import environment as env
import toolkit


def face_merge():
    http_url = 'https://api-cn.faceplusplus.com/imagepp/v1/mergeface'
    template_path = r"template.png"
    merge_path = r"target.png"

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(env.API_KEY)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(env.API_SECRET)
    data.append('--%s' % boundary)
    fr = open(template_path, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'template_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    fr = open(merge_path, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'merge_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'merge_rate')
    data.append('100')
    data.append('--%s--\r\n' % boundary)

    for i, d in enumerate(data):
        if isinstance(d, str):
            data[i] = d.encode('utf-8')

    http_body = b'\r\n'.join(data)

    # build http request
    req = urllib.request.Request(url=http_url, data=http_body)

    # header
    req.add_header('Content-Type', 'multipart/form-data; boundary=%s' % boundary)

    try:
        request = urllib.request.urlopen(req, timeout=5)  # 执行请求
        response = request.read()  # 获取返回结果
        answer_json = json.loads(response.decode('utf-8'))
        if "result" in answer_json and answer_json["result"] is not None:
            return answer_json["result"]
        else:
            print("调用人脸融合API失败，未找到result属性:", answer_json)
    except urllib.error.HTTPError as e:
        print(e.read().decode('utf-8'))



if __name__ == "__main__":
    merge_base64 = face_merge()
    # target_base64 = toolkit.load_file_in_base64("target.png")  # 载入目标图
    # template_base64 = toolkit.load_file_in_base64("template.png")  # 载入模板图
    # merge_base64 = face_merge(target_base64, template_base64)  # 请求API
    toolkit.save_file_as_base64("merge.png", merge_base64)  # 将结果图存入到文件中
