import logging
from logger import log
import json
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
        for i in range(self.retry_limit):
            try:
                raw = requests.get('https://txt.go.sohu.com/ip/soip', timeout=5)
                current_ip = re.search(r'\d+.\d+.\d+.\d+', raw.text).group()
                return current_ip
            except requests.exceptions.RequestException:
                log.info(f'尝试获取公网ip，失败第{i + 1}次...')
                if i + 1 != self.retry_limit:
                    time.sleep(2)
                else:
                    log.info('尝试获取公网ip失败，请检查网络连接')

    def run(self, cfg):
        log.info('==========开始运行==========')
        self.domain_obj = Domain()
        self.domain_obj.create_client(cfg['accessKeyId'], cfg['accessKeySecret'])
        domain_name = cfg['domain_name']
        current_ip = self.get_current_ip()
        if current_ip is None:
            return
        log.info('当前公网ip:' + current_ip)
        recordID = self.domain_obj.get_recordID(domain_name)
        if not recordID:  # 查不到recordID说明没有解析记录
            # 添加解析记录
            add_back_info = self.domain_obj.add_domainRecord(domain_name, current_ip)
            recordID = add_back_info.body.record_id
            pre_ip = current_ip
        else:
            # 解析记录中的ip
            pre_ip = self.domain_obj.describe_domainInfo(recordID).body.value
        while True:
            if pre_ip != current_ip:
                log.info('过期ip:' + pre_ip)
                # 将当前ip更新到解析记录
                self.domain_obj.update_domainRecord(recordID, current_ip)
                pre_ip = current_ip
            else:
                log.info('ip没有改变，不做任何操作')
            time.sleep(cfg['interval'] * 60)
            current_ip = self.get_current_ip()


if __name__ == '__main__':
    # 初始化日志
    formatter = logging.Formatter('[%(asctime)s] [%(levelname)5s] %(message)s')
    fh = logging.FileHandler(filename='./ddns.log', encoding='utf8')
    fh.setFormatter(formatter)
    log.addHandler(fh)

    log.info('读取配置')
    with open('cfg.json') as fp:
        cfg = json.load(fp)
    log.info('读取配置成功')
    ddns = DDdns()
    ddns.run(cfg)
