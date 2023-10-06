# 阿里云DDNS工具

## 创建子域
[链接](https://help.aliyun.com/document_detail/127149.html)

## 创建阿里云accessKey
[链接](https://help.aliyun.com/document_detail/116401.html)

## 运行
### 本工具配置
accessKeyId：上一步中的id  
accessKeySecret：上一步中的serect  
domain_name：你的子域名  
interval：轮询间隔，单位分钟
```json
{
  "accessKeyId": "xxx",
  "accessKeySecret": "xxx",
  "domain_name": "xxx.xxx.xxx",
  "interval": 5
}
```
### 无GUI版
- 只能填写cfg.json
- windows版直接双击exe文件
- linux版命令行执行```./ali_ddns &```
### 有GUI版
- 可进入界面填写配置
