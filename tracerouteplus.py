#!/usr/bin/env python

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
import subprocess, urllib, urllib2, sys, os, re

# api key for ipinfodb.com
API_KEY = "687f07cd5c6a20f0d7a6890751f049a3745c95f98c7706500bfd1fce73f0a1d0"

def main():
    """
    Usage: vistraceroute ip_address
    ---
    vistraceroute uses data from traceroute to query locations of IP addresses.
    Using these locations, it constructs a Google Static Map URL to plot the
    locations and also draws the path from location to location so that the
    user can see a visual represenation of the traceroute data.
    """
    if len(sys.argv) < 2:
        print "Usage: vistraceroute <ip_address>"
        return
    IP = sys.argv[1]
    args = ['whois', IP]
    process = subprocess.Popen(args,
                    shell=False,
                    stdout=subprocess.PIPE)

    print(process.communicate()[0])

    print "Visual traceroute to IP: " + IP

    # determine system
    posix_system = True
    traceroute = 'traceroute'
    args = [IP]
    args.insert(0, '-m30') # Limit maximum num of hope to 30
    args.insert(0, '-w1') # Limit maximum wait time per hop to 1 sec
    # if (os.name != "posix"):
    #     # assume windows
    #     posix_system = False
    #     traceroute = 'tracert'
    #     args.insert(0, '-d') # for windows traceroute to just get IP

    args.insert(0, traceroute)
    # args now looks like: traceroute, [flag,] IP
    # start traceroute
    output = []

    print "Starting traceroute..."
    process = subprocess.Popen(args, 
            shell=False, 
            stdout=subprocess.PIPE)

    # wait for traceroute to finish
    print "Traceroute running. Please wait...\n"
    if process.wait() != 0:
        print "Traceroute error. Exiting."
        #print process.communicate()[1]
        return
    
    # read data from traceroute and split it into lines
    lines = process.communicate()[0].split('\n')
    # First line of traceroute outpout is general info - remove it
    for line in lines[1:]:
        output.append({'trt': line})
        # print line
    # print out traceroute data for user
    # for line in lines:
    #     print line
    # print output
    # print "Traceroute finished. Looking up IP addresses. Please wait..."
    # first line is traceroute info output, remove it
    lines.pop(0)
    # now get hostname, ip from each line
    ips = []
    for i,txt in enumerate(output):
        if txt['trt'] != "":
            # if we didn't get a reply from a gateway, ignore that line in the
            # traceroute output
            if '*' in line:
                # continue
                output[i]['ip'] = 'No IP'
                print(output[i])
                continue
            # Split the line and extract the hostname and IP address
            split_line = txt['trt'].split('  ')
            if split_line[0] != '':
                output[i]['hop'] = split_line[0].strip()
                output[i]['ip'] = split_line[1].split(' ')[1][1:-1]
            else:
                output[i]['hop'] = split_line[1].strip()
                output[i]['ip'] = split_line[2].split(' ')[1][1:-1]

            args = [output[i]['ip']]
            args.insert(0, 'whois')
            # args now looks like: whois IP
            # start whois
            process = subprocess.Popen(args,
                    shell=False,
                    stdout=subprocess.PIPE)

            if process.wait() != 0:
                print "Whois error. Exiting."
                #print process.communicate()[1]
                return
            
            # read Registrant Organisation from whois
            whois_output = process.communicate()[0]

            # print raw whois output for testing
            # print(whois_output)

            if re.findall("descr:.*", whois_output):
                output[i]['descr'] = re.findall("descr:.*", whois_output)[0].replace('descr:', '').strip()            
            if re.findall("person:.*", whois_output):
                output[i]['person'] = re.findall("person:.*", whois_output)[0].replace('person:', '').strip()
            if re.findall("address:.*", whois_output):
                output[i]['address'] = re.findall("address:.*", whois_output)[0].replace('address:', '').strip()
            if re.findall("OrgName:.*", whois_output):
                output[i]['OrgName'] = re.findall("OrgName:.*", whois_output)[0].replace('OrgName:', '').strip()
            if re.findall("org-name:.*", whois_output):
                output[i]['org-name'] = re.findall("org-name:.*", whois_output)[0]
            if re.findall("Registrant Name:.*", whois_output):
                output[i]['Registrant Name'] = re.findall("Registrant Name:.*", whois_output)[0]
            if re.findall("Registrant Organisation:.*", whois_output):
                output[i]['Registrant Organisation'] = re.findall("Registrant Organisation:.*", whois_output)[0]
            if re.findall("Registrant Street:.*", whois_output):
                output[i]['Registrant Street'] = re.findall("Registrant Street:.*", whois_output)[0]
            if re.findall("Registrant City:.*", whois_output):
                output[i]['Registrant City'] = re.findall("Registrant City:.*", whois_output)[0]

            ipi = IPInfo(API_KEY, output[i]['ip'], city=True) # get city, state
            output[i]['location'] = ipi.getCity() + ', ' + ipi.getRegion()

            # Print raw dictionary output for testing
            # print(output[i], '\n')

            print('Hop: ' + output[i]['hop'])
            print('IP: ' + output[i]['ip'])
            if 'descr' in output[i]:
                print('Descr: ' + output[i]['descr'])
            if 'OrgName' in output[i]:
                print('OrgName: ' + output[i]['OrgName'])
            if 'person' in output[i]:
                print('Contact Person: ' + output[i]['person'])
            if 'address' in output[i]:
                print('Contact Address: ' + output[i]['address'])
            print('Server location: ' + output[i]['location'])
            print('')

if __name__ == "__main__":
    main()
