# /usr/bin/
import sys
import httplib
import json
import re

if len(sys.argv) != 5:
    print "usage python program_name <host_ip_address> <host_count> <vlan> <mac_address> "
    sys.exit()
ipaddress = sys.argv[1]
host_count = sys.argv[2]
net = re.split('\.', ipaddress)
ip1 = int(net[3])
ip2 = int(net[2])
ip3 = int(net[1])
ip4 = int(net[0])
vlan = sys.argv[3]
mac = sys.argv[4]
url = '172.25.241.50'
headers = {
    "Content-type": "application/json"
}
last = int(host_count) + 1
for i in range(1, last):
    ip = str(ip4) + "." + str(ip3) + "." + str(ip2) + "." + str(ip1)
    body = {
        "hosts":
            [{
                "ip": ip,
                "vlan": vlan,
                "mac": mac
            }]
    }
    conn = httplib.HTTPConnection(url, 8181)
    conn.request("POST", "/vnet/host", json.dumps(body), headers)
    response=conn.getresponse()
    if response is not None:
        print response.status, response.reason
        data = response.read()
        print data
    if ip1 == 255:
        ip1 = 0
        ip2 = ip2 + 1
    else:
        ip1 = ip1 + 1
    conn.close()
