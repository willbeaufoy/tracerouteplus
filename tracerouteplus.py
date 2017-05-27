#!/usr/bin/env python3

import sys, re, requests, subprocess
from urllib.parse import urlparse

# Change this function to use a different IP info API
def get_ip_location(ip):
    url = "http://ipinfo.io/" + ip + "/geo"
    r = requests.get(url)
    return r.json()

if len(sys.argv) < 2:
    print("Usage: trp <ip_address / hostname>")
    sys.exit()

address = sys.argv[1]
print('\n***** Running TraceroutePlus on {} *****\n'.format(address))

# Full response headers of destination
print('***** Full response headers of destination *****\n')
subprocess.call(['curl', '-I', address])

# Start traceroute
print("***** TraceroutePlus hops *****\n")

traceroute = 'traceroute'
args = [address]
args.insert(0, '-A') # Add Autonomous System (AS) path lookups

args.insert(0, traceroute)

tr_process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE)

for line in tr_process.stdout:
    line = line.decode("utf-8")

    # Print whole traceroute line for testing
    # print(line)

    # Skip the first line as it contains the traceroute 'intro'
    if re.search('^traceroute', line):
        continue

    split_line = line.split('  ')
    output = {}

    if '* * *' in line:
        output['hop'] = split_line[0].strip()
        print('Hop: ' + output['hop'] + ' ***\n')
        continue

    # Split the line and extract the hostname, IP address and AS number
    print(split_line)
    output['hop'] = split_line[0].strip()
    output['hostname'] = re.findall('^(.+)\s', split_line[1])[0]
    output['ip'] = re.findall('\((.+)\)', split_line[1])[0]
    output['asn'] = re.findall('\[(.+)\]', split_line[1])[0]
    output['rtt'] = []
    if len(split_line) > 2:
        output['rtt'].append(split_line[2])
    if len(split_line) > 3:
        output['rtt'].append(split_line[3])
    if len(split_line) > 4:
        output['rtt'].append(split_line[4])

    # start whois
    process = subprocess.Popen(['whois', '-H', output['ip']], shell=False, stdout=subprocess.PIPE)

    if process.wait() != 0:
        print("Whois error. Exiting.")
        sys.exit()

    # read Registrant Organisation from whois
    whois_output = process.communicate()[0]
    whois_output = whois_output.decode("utf-8")

    # print raw whois output for testing
    # print(whois_output)

    if re.findall("descr:.*", whois_output):
        output['descr'] = re.findall("descr:.*", whois_output)[0].replace('descr:', '').strip()
    if re.findall("person:.*", whois_output):
        output['person'] = re.findall("person:.*", whois_output)[0].replace('person:', '').strip()
    if re.findall("address:.*", whois_output):
        output['address'] = re.findall("address:.*", whois_output)[0].replace('address:', '').strip()
    if re.findall("OrgName:.*", whois_output):
        output['OrgName'] = re.findall("OrgName:.*", whois_output)[0].replace('OrgName:', '').strip()
    if re.findall("org-name:.*", whois_output):
        output['org-name'] = re.findall("org-name:.*", whois_output)[0]
    if re.findall("country:.*", whois_output):
        output['country'] = re.findall("country:.*", whois_output)[0].replace('country:', '').strip()
    if re.findall("Registrant Name:.*", whois_output):
        output['Registrant Name'] = re.findall("Registrant Name:.*", whois_output)[0]
    if re.findall("Registrant Organisation:.*", whois_output):
        output['Registrant Organisation'] = re.findall("Registrant Organisation:.*", whois_output)[0]
    if re.findall("Registrant Street:.*", whois_output):
        output['Registrant Street'] = re.findall("Registrant Street:.*", whois_output)[0]
    if re.findall("Registrant City:.*", whois_output):
        output['Registrant City'] = re.findall("Registrant City:.*", whois_output)[0]

    ipinfoio_data = get_ip_location(output['ip'])
    # Assume if city exists then region will too, at least as a key
    if 'city' in ipinfoio_data and ipinfoio_data['city'] != '':
        output['location'] = '{}, {}'.format(ipinfoio_data['city'], ipinfoio_data['region'])

    print('Hop: ' + output['hop'])
    print('Hostname: ' + output['hostname'])
    print('IP: ' + output['ip'])
    print('AS Number: ' + output['asn'])
    if 'descr' in output:
        print('Descr: ' + output['descr'])
    if 'OrgName' in output:
        print('OrgName: ' + output['OrgName'])
    if 'person' in output:
        print('Contact Person: ' + output['person'])
    if 'address' in output:
        print('Contact Address: ' + output['address'])
    if 'Registrant Name' in output:
        print('Registrant Name: ' + output['Registrant Name'])
    if 'location' in output:
        print('Server location: ' + output['location'])
    if 'country' in output:
        print('Country: ' + output['country'])
    rtt_output = 'RTT: '
    for e in output['rtt']:
        rtt_output = rtt_output + e + ', '
    print(rtt_output.rstrip(', '))
    print('')