from alibabacloud_alidns20150109.client import Client as Alidns20150109Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alidns20150109 import models as alidns_20150109_models
from alibabacloud_tea_util import models as util_models
from logger import log_exc


class Domain:
    def __init__(self):
        self.client = None
        self.runtime = util_models.RuntimeOptions()

    def create_client(self, accessKeyId, accessKeySecret):
        """
        使用AK&SK初始化账号Client
        :param accessKeyId:
        :param accessKeySecret:
        :return client:
        """
        config = open_api_models.Config(
            access_key_id=accessKeyId, access_key_secret=accessKeySecret)
        config.endpoint = 'alidns.cn-shanghai.aliyuncs.com'
        self.client = Alidns20150109Client(config)

    @log_exc('获取域名列表')
    def get_domainList(self):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/DescribeDomains?params={}&sdkStyle=dara&lang=PYTHON
        :return:
        """
        describe_domains_request = alidns_20150109_models.DescribeDomainsRequest()
        response = self.client.describe_domains_with_options(describe_domains_request, self.runtime)
        result = [i.puny_code for i in response.body.domains.domain]
        return result

    @log_exc('生成txt记录')
    def get_txtRecord(self, domain):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/GetTxtRecordForVerify?params={}&sdkStyle=dara&lang=PYTHON
        :param domain:
        :return:
        """
        get_txt_record_for_verify_request = alidns_20150109_models.GetTxtRecordForVerifyRequest(
            type='ADD_SUB_DOMAIN', domain_name=domain
        )
        response = self.client.get_txt_record_for_verify_with_options(get_txt_record_for_verify_request, self.runtime)
        return response.body.value

    @log_exc('获取解析记录id')
    def get_recordID(self, domain_name):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/DescribeDomainRecords?params={}&sdkStyle=dara&lang=PYTHON
        :param domain_name:
        :return recordID:
        """
        describe_domain_records_request = alidns_20150109_models.DescribeDomainRecordsRequest(domain_name=domain_name)
        response = self.client.describe_domain_records_with_options(describe_domain_records_request, self.runtime)
        if response.body.domain_records.record:
            return response.body.domain_records.record[0].record_id
        return ''

    @log_exc('获取解析记录详细信息')
    def describe_domainInfo(self, recordID):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/DescribeDomainRecordInfo?params={}&sdkStyle=dara&lang=PYTHON
        :param recordID:
        :return:
        """
        describe_domain_record_info_request = alidns_20150109_models.DescribeDomainRecordInfoRequest(record_id=recordID)
        result = self.client.describe_domain_record_info_with_options(describe_domain_record_info_request, self.runtime)
        return result

    @log_exc('添加解析记录')
    def add_domainRecord(self, domain_name, rr, type, value):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/AddDomainRecord?params={}&sdkStyle=dara&lang=PYTHON
        :param domain_name:
        :param rr:
        :param type:
        :param value:
        :return result:
        """
        add_domain_record_request = alidns_20150109_models.AddDomainRecordRequest(
            domain_name=domain_name, rr=rr, type=type, value=value
        )
        result = self.client.add_domain_record_with_options(add_domain_record_request, self.runtime)
        return result

    @log_exc('修改解析记录')
    def update_domainRecord(self, recordID, rr, type, value):
        """
        https://next.api.aliyun.com/api/Alidns/2015-01-09/UpdateDomainRecord?params={}&sdkStyle=dara&lang=PYTHON
        :param recordID:
        :param rr:
        :param type:
        :param value:
        :return:
        """
        update_domain_record_request = alidns_20150109_models.UpdateDomainRecordRequest(
            record_id=recordID, rr=rr, type=type, value=value
        )
        self.client.update_domain_record_with_options(update_domain_record_request, self.runtime)
