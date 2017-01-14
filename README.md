TraceroutePlus
=============

Adds various interesting pieces of information to a standard traceroute call, including AS number, information from a whois call for each hop, and server location calculated using an IP location service. Intended purely for satisfying curiosity. 

Modified from VisualTraceroute by Kyle Flanagan.

Usage
----------

Uses Python 3 and works on Linux. Ensure the tracerouteplus.py file is set to be executable.

```bash
./tracerouteplus.py google.com
```

IP location service
------------------------------

Currently the script uses [ipinfo.io's](http://ipinfo.io/) API (free for 1000 requests per day), but could easily be configured to use a different service.