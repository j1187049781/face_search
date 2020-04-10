import json
import os

import requests
data_dir='data'
for name in os.listdir(data_dir)[:3]:
    print(name)
    jpg_path = os.path.join(data_dir, name)
    with open(jpg_path, 'rb') as f:
        data = {"img": f}
        param={'duplicate_person':True}
        url = 'http://127.0.0.1:7070/add_person'
        req = requests.post(url,data=param, files=data)
    print(req.text)
    person_id=json.loads(req.text)['data']['person_id']




for name in os.listdir(data_dir)[3:6]:
    print(name)
    jpg_path = os.path.join(data_dir, name)
    with open(jpg_path, 'rb') as f:
        data = {"img": f}
        url = 'http://127.0.0.1:7070/find_person'
        req = requests.post(url, files=data)
    print(req.text)

for name in os.listdir(data_dir)[3:6]:
    print(name)
    jpg_path = os.path.join(data_dir, name)
    with open(jpg_path, 'rb') as f:
        data = {"person_id": person_id}
        url = 'http://127.0.0.1:7070/rm_person'
        req = requests.post(url, data=data)
    print(req.text)