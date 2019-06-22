import subprocess
from MyFastDFS import settings
import os

def upload_file(filename):
    if filename:
        fdfs_test = os.path.join(settings.BIN_DIR, 'fdfs_test')
        client_conf = os.path.join(settings.CONF_DIR, 'client.conf')
        cmd = "%s %s upload %s" % (fdfs_test, client_conf, filename)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        ret = p.stdout
        for line in p.stderr:
            print("ERROR in utils.upload_file:", line)

        for line in p.stdout:
            print("OUT in utils.upload_file:", line)

        return ret
