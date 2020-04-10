
# 部署
```bash
docker run --net host  -d face_search:latest
```
# 接口

- post http://ip:7070/find_person
- form-data   

|参数名|类型|含义|   
| --- | --- | --- |    
| img | file | 传入人脸图片|

```json
{
  "data": {
    "face_sim": 1.0,
    "person_id": "dd0feb516b4acf2566fd894431132f"
  },
  "status": 1
}

```
----------
- post http://ip:7070/rm_person 
 
|参数名|类型|含义|   
| --- | --- | --- |    
| person_id | string | 传入人脸id|
```json
{
  "data": {
    "success": false
  },
  "status": 1
}
```
----------
- post http://ip:7070/add_person

|参数名|类型|含义|
| --- | --- |---|
| img | file | 传入人脸图片|
| duplicate_person | bool | 如果人脸有相似的，是否去重|

```json
{
  "person_id": "4ea9cac5b6b2ab44fe63616b661291",
  "status": 1,
  "success": false
}
```
