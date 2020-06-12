import json
import time
import urllib.error
import urllib.request

import environment as env
import toolkit


def beautify(demo_path):
    http_url = 'https://api-cn.faceplusplus.com/facepp/v2/beautify'

    boundary = '----------%s' % hex(int(time.time() * 1000))
    data = []
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_key')
    data.append(env.API_KEY)
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'api_secret')
    data.append(env.API_SECRET)
    data.append('--%s' % boundary)
    fr = open(demo_path, 'rb')
    data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'image_file')
    data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    data.append(fr.read())
    fr.close()
    # data.append('--%s' % boundary)
    # fr = open(merge_path, 'rb')
    # data.append('Content-Disposition: form-data; name="%s"; filename=" "' % 'merge_file')
    # data.append('Content-Type: %s\r\n' % 'application/octet-stream')
    # data.append(fr.read())
    # fr.close()
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'whitening')
    data.append('30')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'smoothing')
    data.append('40')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'thinface')
    data.append('0')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'shrink_face')
    data.append('0')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'enlarge_eye')
    data.append('0')
    data.append('--%s' % boundary)
    data.append('Content-Disposition: form-data; name="%s"\r\n' % 'remove_eyebrow')
    data.append('0')
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
    merge_base64 = beautify(r"demo.jpg")
    # target_base64 = toolkit.load_file_in_base64("target.png")  # 载入目标图
    # template_base64 = toolkit.load_file_in_base64("template.png")  # 载入模板图
    # merge_base64 = face_merge(target_base64, template_base64)  # 请求API
    toolkit.save_file_as_base64("beautify.png", merge_base64)  # 将结果图存入到文件中
