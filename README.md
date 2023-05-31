# 阿里云DDNS工具

## 创建子域
[链接](https://help.aliyun.com/document_detail/127149.html?spm=a2c4g.29719.0.0.39651fa3SfFDWA)

## 创建阿里云accessKey
[链接](https://help.aliyun.com/document_detail/116401.html)

## 运行
### 本工具配置
accessKeyId：上一步中的id  
accessKeySecret：上一步中的serect  
domain_name：你的子域名  
interval：轮询间隔，单位秒
```json
{
  "accessKeyId": "xxx",
  "accessKeySecret": "xxx",
  "domain_name": "xxx.xxx.xxx",
  "interval": 60
}
```
### 无GUI版
只能填写cfg.json
### 有GUI版
可进入界面填写配置，开发中未实装
