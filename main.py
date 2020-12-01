import yaml, os, sys
import xml.etree.ElementTree as ET

os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

from fritzconnection import FritzConnection
import providers.namecheap as ncc
import providers.cloudflare as cfc

def main():
  try:
    with open(os.environ['CONFIG_PATH'], 'r') as f:
      conf = yaml.safe_load(f.read())
  except:
    print("Error getting config file")
    exit()

  fc = FritzConnection(conf['fritzbox']['address'])
  if conf['externalIPv6Suffix'] != "":
    ipv6_prefix = fc.call_action('WANIPConn1', 'X_AVM_DE_GetIPv6Prefix')
    external_ipv6 = ':'.join(ipv6_prefix['NewIPv6Prefix'].split(':')[0:4]) + ':' + conf['externalIPv6Suffix']
  else:
    external_ipv6 = ''

  external_ipv4 = fc.call_action('WANIPConn1', 'GetExternalIPAddress')['NewExternalIPAddress']

  if 'namecheap' in conf:
    c = ncc.NamecheapClient(conf['namecheap'])
  elif 'cloudflare' in conf:
    c = cfc.CloudFlareClient(conf['cloudflare'])
  else:
    exit()

  existing = c.get_dns_records(conf['domain'])

  c.set_dns_records(conf['records'], existing, external_ipv4, external_ipv6)


if __name__ == '__main__':
    main()