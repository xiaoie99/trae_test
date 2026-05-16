import urllib3
import requests
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
DEVICE_IP = "10.10.1.201"
url = f"https://{DEVICE_IP}/level/15/exec/-/show/ip/interface/brief/CR"
USERNAME = "admin"
PASSWORD = "Cisc0123"
response = requests.get(url, auth=(USERNAME, PASSWORD), verify=False, timeout=15)
print(response.text)
