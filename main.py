import yaml, os, re, subprocess, sys
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
  if conf['ipv6']['enabled']:
    if conf['ipv6']['target'] == '':
      print('IPv6 is enabled but not target host has been set.')
      exit()

    ipv6_prefix = ':'.join(fc.call_action('WANIPConn1', 'X_AVM_DE_GetIPv6Prefix')['NewIPv6Prefix'].split(':')[0:4])

    process = subprocess.Popen(
      f"/usr/bin/host -6 -v { conf['ipv6']['target'] } { re.sub(r'https?://', '', conf['fritzbox']['address']) }".split(' '),
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()

    external_ipv6 = re.search(fr"{ ipv6_prefix }.+", stdout.decode('utf-8')).group(0)
  else:
    external_ipv6 = ''

  # print(external_ipv6)
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
