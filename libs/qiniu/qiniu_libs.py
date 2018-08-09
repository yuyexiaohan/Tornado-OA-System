# coding=utf-8 
# @Time : 2018/8/8 22:03 
# @Author : achjiang
# @File : qiniu_libs.py

# 导入七牛的用户及上传数据包

from qiniu import Auth, put_data

access_key ='AnE70UQaiqokVXUT7v3BGYNAVWo5oey8UA3fEdsD'
secret_key ='BIGPCz55HcnTtq3RqDgMfeLUtvwTaBGnVKNs4gyN'
bucket_name =' achjiangspace'
q = Auth(access_key, secret_key)

def upload_qiniu_file_content(content):
    # 七牛上传文件
    token = q.upload_token(bucket_name)

    ret, info = put_data(token, None, content)
    return ret['key'], info


def down_qiniu_file(qiniu_url):
    # 七牛下载文件
    url = q.private_download_url(qiniu_url, expires=10)
    return url