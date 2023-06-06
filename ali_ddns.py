import json
import log
import re
import requests
import time
from ali_domain import Domain


class DDdns:
    def __init__(self):
        self.domain_obj = None
        self.mail = None
        self.retry_limit = 5

    def verify_subdomain(self, domain):
        self.domain_obj.get_txtRecord(domain)

    def add_subdomain(self):
        pass

    def get_current_ip(self):
        count = 0
        if count < self.retry_limit:
            try:
                raw = requests.get('https://txt.go.sohu.com/ip/soip', timeout=2)
                current_ip = re.search(r'\d+.\d+.\d+.\d+', raw.text).group()
                return current_ip
            except requests.exceptions.RequestException:
                count += 1
                log.info('尝试获取公网ip，重试第%s次...' % count)
                if count == self.retry_limit:
                    log.info('获取公网ip失败，请检查网络连接')

    def run(self):
        log.info('==========开始运行==========')
        log.info('读取配置')
        with open('cfg.json') as fp:
            cfg = json.load(fp)
        log.info('读取配置成功')
        self.domain_obj = Domain()
        self.domain_obj.create_client(cfg['accessKeyId'], cfg['accessKeySecret'])
        domain_name = cfg['domain_name']
        rr = '@'
        type = 'A'
        recordID = self.domain_obj.get_recordID(domain_name)
        current_ip = self.get_current_ip()
        log.info('当前公网ip:' + current_ip)
        if not recordID:  # 查不到recordID说明没有解析记录
            # 添加解析记录
            add_back_info = self.domain_obj.add_domainRecord(domain_name, rr, type, current_ip)
            recordID = add_back_info.body.record_id
            pre_ip = current_ip
        else:
            # 解析记录中的ip
            pre_ip = self.domain_obj.describe_domainInfo(recordID).body.value

        while True:
            if pre_ip != current_ip:
                log.info('过期ip:' + pre_ip)
                # 将当前ip更新到解析记录
                self.domain_obj.update_domainRecord(recordID, rr, type, current_ip)
                pre_ip = current_ip
            else:
                log.info('ip没有改变，不做任何操作')
            time.sleep(cfg['interval'])
            current_ip = self.get_current_ip()
