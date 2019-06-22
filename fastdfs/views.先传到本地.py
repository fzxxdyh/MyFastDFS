from django.shortcuts import render, HttpResponse
from MyFastDFS import settings
import os
import json
import subprocess
from fastdfs import utils
from django.http import FileResponse
from django.http.response import JsonResponse
import configparser


def upload(request):
    resp = {}
    if request.method == "POST": #上传文件
        storage_conf = os.path.join(settings.CONF_DIR, 'storage.conf')
        conf_obj = configparser.ConfigParser()
        conf_obj.read(storage_conf, encoding="utf-8")
        ip = conf_obj.get('localhost', 'ip')

        #print(request.FILES)
        file_list = request.FILES.getlist("file")
        for file in file_list:
            print(type(file))
            filename = os.path.join(settings.DATA_DIR, file.name)
            resp[filename] = {}
            resp[filename]["file_name"] = file.name

            f = open(filename, 'wb')
            for chunk in file.chunks():
                f.write(chunk)
            f.close()

            fdfs_test = os.path.join(settings.BIN_DIR, 'fdfs_test')
            client_conf = os.path.join(settings.CONF_DIR, 'client.conf')
            cmd = "%s %s upload %s" % (fdfs_test, client_conf, filename)
            p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            p.wait()

            for line in p.stderr.readlines():
                print("error in views.index:", str(line, encoding="utf-8"))

            for line in p.stdout.readlines():
                #print('out',type(line), str(line, encoding="gbk"))
                line = str(line, encoding="utf-8")
                if line.strip().startswith("group_name="):
                    # group_name=group1, remote_filename=M00/00/00/CgoKAlzvYwuALUMpAAAAE62Yg7k847.txt
                    group_name = line.split(",")[0].split("=")[1].strip()
                    file_path = line.split(",")[1].split("=")[1].strip()
                    resp[filename]['group_name'] = group_name
                    resp[filename]['file_id'] = "%s/%s" % (group_name, file_path)
                    resp[filename]['file_url'] = "http://{ip}/download/{file_id}".format(ip=ip, file_id=resp[filename]['file_id'])
                elif line.strip().startswith("file timestamp="):
                    # file timestamp=2019-05-30 12:58:51
                    upload_time = line.split("=")[1].strip()
                    resp[filename]['upload_time'] = upload_time
                elif line.strip().startswith("file size="):
                    # file size=19
                    file_size = line.split("=")[1].strip()
                    resp[filename]['file_size'] = file_size
                elif line.strip().startswith("file crc32="):
                    # file crc32=2912453561
                    file_crc32 = line.split("=")[1].strip()
                    resp[filename]['file_crc32'] = file_crc32

        return JsonResponse(resp)





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
