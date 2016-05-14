Ultimate traceroute / Geolocated traceroute with whois
====================

Adds GeoIP lookup and whois information to traceroute. Running ultimate traceroute to a host will output the IP address, location and ownership information for all hops in the journey.

Usage
======

./vistraceroute.py google.com

Other to look at
====================

https://github.com/ayeowch/traceroute

Modified from VisualTraceroute by Kyle Flanagan. His original README below
==========================================================================

http://kyleflan.wordpress.com/2012/12/13/a-visual-traceroute-program/

Visual Traceroute - vistraceroute v 0.1
(C) 2012 Kyle Flanagan
This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

------------------------------------------------------------------------------
Description
------------------------------------------------------------------------------
Visual Traceroute is a program that uses either the posix or Windows 
traceroute/rt program to find IP addresses of gateways along a traceroute 
route. The program then uses information from www.ipinfodb.com to get the 
locations of these gateways. Finally, the program constructs a URL using 
Google's static map API to display these locations and the path the route 
takes.

Under Linux, the program uses traceroute
Under Windows, the program uses tracert
You must have these programs installed to use vistraceroute

Misc:
The map markers are labeled with the order of each IP address returned from
traceroute (save for the gateways that didn't return any information; these
are ignored). However, after 9, the markers are labeled with simply a dot (.)
because of marker label limitations in the static Google map.

------------------------------------------------------------------------------
Usage
------------------------------------------------------------------------------
Note: You may have to make the files vistraceroute.py and pyipinfodb.py 
executable under Linux (chmod +x vistraceroute.py, chmod +x pyipinfodb.py).

vistraceroute.py ip_address(or hostname)

alternatively

python vistraceroute.py ip_address(or hostname)

The latter usage is necessary to run the program under Windows. Make sure that
you're either in the Python directory or that the location of python.exe is in
your system path.

Example usage:
python vistraceroute.py www.google.com

Once the program is finished, it will display a URL. Copy and paste this URL
in a web browser to view the map.

------------------------------------------------------------------------------
Contact
------------------------------------------------------------------------------
If you find bugs (of which I'm sure there are many) or have any suggestions,
email me.
Kyle Flanagan
kyleflanagan@gmail.com

