import requests

class NamecheapClient:
  def __init__(self, config):
    with open(config['apiKeyPath'], 'r') as f:
      token = f.read().strip()

    self.baseParams = {
      'ApiUser': config['user'],
      'ApiKey': token,
      'UserName': config['user'],

    }
  
  def set_dns_records(self, records, current_records, external_ipv4, external_ipv6):
    for r in records:
      ip = external_ipv4 if r['type'] == 'A' else external_ipv6

      requests.post('https://api.namecheap.com/xml.response?Command=namecheap.domains.dns.setHosts', )

      body = {
        'apiuser': '',
        'apikey': '',
        'HostName': r['name'],
        'RecordType': r['type'],
        'Address': ip,
      }
      

  def get_dns_records(self, domain):
    pass