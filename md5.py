import hashlib
import subprocess
import os
from time import sleep

local_file_path = "/Users/suman.mandal/pricing-engine/target/pricing-engine-1.153-SNAPSHOT.jar"
local_tar_file_path = "/Users/suman.mandal/pricing-engine/target/pricing.tar.gz"
hostname = "ssh -tt jumpStg ssh -tt 10.200.3.149"
remote_file_path = "/home/sumanmandal/currentBuild/pricing-engine-1.153-SNAPSHOT.jar"


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def md5Remote(host,remote_file_path):
    cmd =host + " md5sum "+remote_file_path
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout
    stdout = pipe.read()
    stdout = getSpaceSperatedOutput(stdout)
    outputArray = stdout.split(' ')
    for output in outputArray:
        if(len(output) == 32):
            return output


def getSpaceSperatedOutput(stdout):
    delimiters = ['\n', '\r', ',t']
    for delimiter in delimiters:
        stdout = stdout.replace(delimiter, ' ')
    return stdout


def copyFileToStage(local_file_path, remote_file_path):
    cmd ="ssh -L 2222:10.200.3.149:22 jumpStg"
    killCmd = "lsof -ti:2222 | xargs kill"
    subprocess.Popen(cmd,shell=True, stdout=subprocess.PIPE)
    sleep(10)
    subprocess.Popen("scp -P 2222 " + local_file_path + " sumanmandal@localhost:"+remote_file_path,shell=True).wait()
    subprocess.Popen(killCmd,shell=True).wait()


def main():
    local_md5 = md5(local_file_path)
    remote_md5 = md5Remote(hostname, remote_file_path)
    if(local_md5 != remote_md5):
        copyFileToStage(local_file_path,remote_file_path)
        print "Copied modified file to stage"
    else:
        print "File is not modified"
if __name__ == "__main__":
    main()