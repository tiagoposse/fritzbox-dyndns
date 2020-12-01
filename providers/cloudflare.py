import CloudFlare

class CloudFlareClient:
  def __init__(self, config):
    with open(config['apiKeyPath'], 'r') as f:
      token = f.read().strip()

    self.cf = CloudFlare.CloudFlare(email=config['email'], token=token)
    self.zone_id = ''

  def get_dns_records(self, domain):
    self.zone_id = self._get_zone_id(domain)

    ret = []
    try:
      current_records = self.cf.zones.dns_records.get(self.zone_id)
    except CloudFlare.exceptions.CloudFlareAPIError as e:
      exit('/zones/dns_records.get %d %s - api call failed' % (e, e))
    
    for r in current_records:
      if r['type'] in ['MX', 'TXT']:
        continue
      
      ret.append(r)

    return ret


  def _get_zone_id(self, domain):
    zones = self.cf.zones.get()

    for zone in zones:
      if zone['name'] == domain:
        return zone['id']


  def set_dns_records(self, records, current_records, external_ipv4, external_ipv6):
    for r in records:
      found = False
      ip = external_ipv4 if r['type'] == 'A' else external_ipv6

      for cr in current_records:
        if cr['name'] == r['name'] and cr['type'] == r['type']:
          if cr['content'] != ip:
            print(f"Updating record { r['name'] }")
            self.cf.zones.dns_records.put(self.zone_id, cr['id'], data={
              'name': r['name'],
              'type': r['type'],
              'content': ip
            })

          found = True

      if not found:
        print(f"Creating { r['type'] } record { r['name'] }")
        self.cf.zones.dns_records.post(self.zone_id, data={
          'name': r['name'],
          'type': r['type'],
          'content': ip,
          'proxied': False
        })