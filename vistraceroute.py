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
# URL for Google Static Map API
google_map_base_url = "http://maps.googleapis.com/maps/api/staticmap?"

def getURLDict(ips):
    """
    Returns a dictionary consisting of URL paramenters to pass to the Google
    static map api. The IP addresses in ips are looked up using the IPInfo
    class from pyipinfodb and constructed into the url_dict.
    """
    url_dict = {'zoom' : '', 
            'maptype':'roadmap', 
            'sensor':'false', 
            'size':'1200x600', 
            'markers':[], 
            'path':'color:0x0000ff|weight:3',
            'center':''}
    for x, ip in enumerate(ips):
        ipi = IPInfo(API_KEY, ip, city=True) # get city, state
        location = ipi.getCity() + ',' + ipi.getRegion()
        print "IP: " + ip + " Location: " + location 

        # the IPInfo class returns '-' if it cannot find a city or
        # state, so ignore these values
        if '-' in location:
            continue

        # we could use the heuristic below to find an approximate center
        # for the map, but since we're passing markers and a path, Google
        # will find the center for us
        ##if len(ips) / 2 <= x and url_dict['center'] == None:
        ##    url_dict['center'] = ipi.getCity() + ',' + ipi.getRegion() 

        # append markers
        if x == len(ips)-1: # end with red marker
            url_dict['markers'].append('color:red|label:' + str(x) + '|' + location)
        else: # else use a green one
            url_dict['markers'].append('color:green|label:' + str(x) + '|' + location)

        # append to the path route
        url_dict['path'] = url_dict['path'] + "|" + location
    return url_dict

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
    print "Visual traceroute to IP: " + IP

    # determine system
    posix_system = True
    traceroute = 'traceroute'
    args = [IP]
    args.insert(0, '-m30') # Limit maximum num of hope to 30
    args.insert(0, '-w1') # Limit maximum wait time per hop to 1 sec
    if (os.name != "posix"):
        # assume windows
        posix_system = False
        traceroute = 'tracert'
        args.insert(0, '-d') # for windows traceroute to just get IP

    args.insert(0, traceroute)
    # args now looks like: traceroute, [flag,] IP
    # start traceroute
    print "Starting traceroute..."
    process = subprocess.Popen(args, 
            shell=False, 
            stdout=subprocess.PIPE)

    # wait for traceroute to finish
    print "Traceroute running. Please wait..."
    if process.wait() != 0:
        print "Traceroute error. Exiting."
        #print process.communicate()[1]
        return
    
    # read data from traceroute and split it into lines
    lines = process.communicate()[0].split('\n')
    # print out traceroute data for user
    for line in lines:
        print line

    print "Traceroute finished. Looking up IP addresses. Please wait..."
    # first line is traceroute info output, remove it
    lines.pop(0)
    # and there are extra lines on windows output
    if not posix_system:
        lines.pop(0)
        lines.pop(0)
        lines.pop(0)
        lines.pop()
        lines.pop()
        lines.pop()
    # now get hostname, ip from each line
    ips = []
    for line in lines:
        if line != "":
            # if we didn't get a reply from a gateway, ignore that line in the
            # traceroute output
            if '*' in line:
                continue
            
            # Split the line and extract the hostname and IP address
            if posix_system:
                split_line = line.split('  ')
                if split_line[0] != '':
                    ips.append(split_line[1].split(' ')[1][1:-1])
                else:
                    ips.append(split_line[2].split(' ')[1][1:-1])
            else: 
                line = line.lstrip()
                line = line.rstrip()
                split_line = line.split(' ')
                ips.append(split_line[-1])

    print "IP addresses to be looked up:"
    for ip in ips:
        args = [ip]
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
        output = process.communicate()[0]
        reg_org = re.findall("OrgName:.*", output)
        if len(reg_org) == 0:
            reg_org.insert(0, "No OrgName found")
        print ip, " ", reg_org[0]

    url_dict = getURLDict(ips)

    urldata = urllib.urlencode(url_dict, True)
    #print "Google Map URL (copy and paste into your web browser):"
    url = google_map_base_url + urldata
    #print url

if __name__ == "__main__":
    main()
