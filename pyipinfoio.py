import requests

def get_ip_location(ip):
  url = "http://ipinfo.io/" + ip + "/geo"
  r = requests.get(url)
  return r.json()
