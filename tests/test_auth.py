import os
import re
import json
from subprocess import check_call, check_output, Popen

def test_upload0():
    CMD = '''curl -X POST -H "Authorization: mgrast " -F "upload=@data/metadata.simple.xlsx" "https://api.mg-rast.org/inbox"'''
    print(CMD)
    o = check_output(CMD, shell=True)
    print(o)
    assert "authentication fail" in o
    assert "ERROR" in o

def test_upload1():
    if 'MGRKEY' in os.environ:
        MGRKEY = os.environ['MGRKEY']
    else: 
        assert False, "This test does not work without MGRKEY"
    CMD = '''curl -X POST -H "Authorization: mgrast {}" -F "upload=@data/metadata.simple.xlsx" "https://api.mg-rast.org/inbox"'''.format(MGRKEY)
    print(CMD)
    o = check_output(CMD, shell=True)
    print(o)

def test_upload_and_validate():
    if 'MGRKEY' in os.environ:
        MGRKEY = os.environ['MGRKEY']
    else: 
        assert False, "This test does not work without MGRKEY"
    CMD = '''curl -X POST -H "Authorization: mgrast {}" -F "upload=@data/metadata.simple.xlsx" "https://api.mg-rast.org/inbox"'''.format(MGRKEY)
    print(CMD)
    o = check_output(CMD, shell=True)
    j = json.loads(o)    
    ID = re.findall("\((.*)\)", j["status"])[0]
    print(ID)
    assert "metadata.simple.xlsx" in j["status"]
    CMD = '''curl -X GET -H "Authorization: mgrast {}" "https://api.mg-rast.org/inbox/validate/{}"'''.format(MGRKEY, ID)
    o2 = check_output(CMD, shell=True)
    print(o2)
    j2 = json.loads(o2)
    assert j2["status"] == "valid metadata"