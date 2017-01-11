#!/usr/bin/env python3

# (C) Kyle Flanagan 2012
# vistraceroute
#
# This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pyipinfodb import *
import subprocess, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, sys, os, re, time

def main():

    if len(sys.argv) < 2:
        print("Usage: trp <ip_address / hostname>")
        return

    IP = sys.argv[1]

    # Full whois of destination
    # print('***** Full whois of destination *****\n')
    # subprocess.call(['whois', '-H', IP])

    # Full response headers of destination
    print('\n***** Full response headers of destination *****\n')
    subprocess.call(['curl', '-I', IP])

    # Start traceroute
    print("\n***** TraceroutePlus to destination *****\n")

    traceroute = 'traceroute'
    args = [IP]
    # args.insert(0, '-m30') # Limit maximum num of hops to 30
    # args.insert(0, '-w1') # Limit maximum wait time per hop to 1 sec
    args.insert(0, '-A') # Add Autonomous System (AS) path lookups

    args.insert(0, traceroute)
    # args now looks like: traceroute, [flag,] IP
    # start traceroute

    print("Starting traceroute...\n")
    # tr_process = subprocess.check_output(args)
    tr_process = subprocess.Popen(args,
            shell=False,
            stdout=subprocess.PIPE)

    # Each line from the process will be 'dealt with' by the for loop as it appears.
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
        output['hop'] = split_line[0].strip()
        output['hostname'] = re.findall('^(.+)\s', split_line[1])[0]
        output['ip'] = re.findall('\((.+)\)', split_line[1])[0]
        output['asn'] = re.findall('\[(.+)\]', split_line[1])[0]
        output['rtt1'] = split_line[2]
        output['rtt2'] = split_line[3]
        output['rtt3'] = split_line[4]

        # start whois
        process = subprocess.Popen(['whois', '-H', output['ip']], shell=False, stdout=subprocess.PIPE)

        if process.wait() != 0:
            print("Whois error. Exiting.")
            return
        
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

        # Removed this functionality Jan 2016 as website stopped working
        # ipi = IPInfo(API_KEY, output['ip'], city=True) # get city, state
        # output['location'] = ipi.getCity() + ', ' + ipi.getRegion()

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
        print('RTT: ' + output['rtt1'] + ', ' + output['rtt2'] + ', ' + output['rtt3'])
        print('')

if __name__ == "__main__":
    main()
