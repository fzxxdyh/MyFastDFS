from django.shortcuts import render, HttpResponse
from MyFastDFS import settings
import os
import json
import subprocess
from fastdfs import utils
from django.http import FileResponse
from django.http.response import JsonResponse
import configparser
from fdfs_client.client import Fdfs_client


def upload(request):

    '''
>>> client.upload_by_buffer(buffer)
getting connection
<fdfs_client.connection.Connection object at 0x7f6147ae06d8>
<fdfs_client.fdfs_protol.Tracker_header object at 0x7f6147ae0748>
{'Storage IP': '10.10.10.2', 'Group name': 'group1', 'Local file name': '', 'Uploaded size': '11.00KB', 'Remote file_id': 'group1/M00/00/00/CgoKAlz2DNSAbdAEAAAsEIdFPmw7374261', 'Status': 'Upload successed.'}
>>> 
    '''
    if request.method == "POST": #上传文件

        # 获取 http ip
        storage_conf = os.path.join(settings.CONF_DIR, 'storage.conf')
        conf_obj = configparser.ConfigParser()
        conf_obj.read(storage_conf, encoding="utf-8")
        ip = conf_obj.get('localhost', 'ip')

        #print(request.FILES)
        file_list = request.FILES.getlist("file")
        for file in file_list:
            print(type(file))

            # f = open(filename, 'wb')
            # for chunk in file.chunks():
            #     f.write(chunk)
            # f.close()

            client_conf = os.path.join(settings.CONF_DIR, 'client.conf')
            client = Fdfs_client(client_conf)
            file_ext = file.name.split(".")[-1]
            append_flag = False
            for chunk in file.chunks():
                if not append_flag:
                    result = client.upload_by_buffer(chunk, file_ext_name=file_ext)
                    append_flag = True
                else:
                    client.append_by_buffer(chunk, result['Remote file_id'])





        return JsonResponse(result)





def download(request, group_name, m_name, path1, path2, filename):
    print("in download ...")
    storage_conf = os.path.join(settings.CONF_DIR, 'storage.conf')
    conf_obj = configparser.ConfigParser()
    conf_obj.read(storage_conf, encoding="utf-8")
    #print(dir(conf_obj))

    if conf_obj.has_section(group_name):
        m_num = int(m_name[1:])
        store_path = 'store_path%d' % m_num
        store_path = conf_obj.get(group_name, store_path)
        file_path = os.path.join(store_path, 'data', path1, path2, filename)
        #filename = os.path.join(settings.CONF_DIR, 'client.conf')
        file = open(file_path, 'rb')
        response = FileResponse(file)
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename="%s"' % filename
        return response

def test(request):
    print("test page!")
    return HttpResponse("test page !!!2222")
