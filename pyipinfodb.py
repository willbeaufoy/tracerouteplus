#!/usr/bin/env python
 
# Copyright (c) 2010, Westly Ward
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the pyipinfodb nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
# 
# THIS SOFTWARE IS PROVIDED BY Westly Ward ''AS IS'' AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL Westly Ward BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#
# Modifications made 2012 by Kyle Flanagan to update this class to version 3
#
#

import json, urllib, urllib2, socket
CITY_URL = "http://api.ipinfodb.com/v3/ip-city/"
COUNTRY_URL = "http://api.ipinfodb.com/v3/ip-country/"
class IPInfo() :
    def __init__(self, apikey, ip=None, city=False, country=False) :
        if ip == None:
            print "Error: No IP address specified."
            return None
        self.apikey = apikey
        if city:
            self.data = self.GetIPInfo(CITY_URL, ip)
        elif country:
            self.data = self.GetIPInfo(COUNTRY_URL, ip)
        else:
            print "Error: No precision specified. Must call with either city=True or country=True"
            return None

    def GetIPInfo(self, baseurl, ip=None, timezone=False) :
        passdict = {"format":"json", "key":self.apikey}
        if ip :
            try :
                passdict["ip"] = socket.gethostbyaddr(ip)[2][0]
            except : passdict["ip"] = ip
        if timezone :
            passdict["timezone"] = "true"
        else :
            passdict["timezone"] = "false"
        urldata = urllib.urlencode(passdict)
        url = baseurl + "?" + urldata
        urlobj = urllib2.urlopen(url)
        #print urlobj
        data = urlobj.read()
        #print '*' * 80
        #print data
        #print '*' * 80
        urlobj.close()
        datadict = json.loads(data)
        return datadict

    def getDict(self):
        return self.data

    def getStatusCode(self):
        return self.data['statusCode']

    def getStatusMessage(self):
        return self.data['statusMessage']

    def getIP(self):
        return self.data['ipAddress']

    def getCountryCode(self):
        return self.data['countryCode']

    def getCountry(self) :
        return self.data['countryName']

    def getRegion(self):
        return self.data['regionName']

    def getCity(self) :
        return self.data['cityName']

    def getZip(self):
        return self.data['zipCode']

    def getLat(self):
        return self.data['latitude']

    def getLong(self):
        return self.data['longitude']

    def getTimezone(self):
        return self.data['timeZone']

