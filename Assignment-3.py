#!/usr/bin/env python3

# 20201020 - Add a function to add a single prefix to a local prefixlist - Dan
import cloudgenix
import argparse
from cloudgenix import jd, jd_detailed
import cloudgenix_settings
import sys
import logging
import os
import datetime
import collections
import csv 
from geopy import distance
import xmltodict
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global Vars
TIME_BETWEEN_API_UPDATES = 60       # seconds
REFRESH_LOGIN_TOKEN_INTERVAL = 7    # hours
SDK_VERSION = cloudgenix.version
SCRIPT_NAME = 'CloudGenix: Example script: Get IONs'
SCRIPT_VERSION = "v1"

# Set NON-SYSLOG logging to use function name
logger = logging.getLogger(__name__)


####################################################################
# Read cloudgenix_settings file for auth token or username/password
####################################################################

sys.path.append(os.getcwd())
try:
    from cloudgenix_settings import CLOUDGENIX_AUTH_TOKEN

except ImportError:
    # Get AUTH_TOKEN/X_AUTH_TOKEN from env variable, if it exists. X_AUTH_TOKEN takes priority.
    if "X_AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('X_AUTH_TOKEN')
    elif "AUTH_TOKEN" in os.environ:
        CLOUDGENIX_AUTH_TOKEN = os.environ.get('AUTH_TOKEN')
    else:
        # not set
        CLOUDGENIX_AUTH_TOKEN = None

try:
    from cloudgenix_settings import CLOUDGENIX_USER, CLOUDGENIX_PASSWORD

except ImportError:
    # will get caught below
    CLOUDGENIX_USER = None
    CLOUDGENIX_PASSWORD = None

try:
    from cloudgenix_settings import PANORAMA_IP, PANORAMA_API_KEY

except ImportError:
    # will get caught below
    PANORAMA_IP = None
    PANORAMA_API_KEY = None

paList = [
	{
		'name':"us-east-1",
        'region' : "US East",
		'coordinates': (37.45244, -76.41686)
	},
	{
		'name':"us-northeast",
        'region' : "US East",
        'coordinates': (40.71455, -74.00714)
	},
	{
		'name':"us-southeast",
        'region' : "US Southeast",
        'coordinates': (33.74832, -84.39111)
	},
	{
		'name':"us-south",
        'region' : "US South",
        'coordinates': (29.76059, -95.36968)
	},
	{
		'name':"us-east-2",
        'region' : "US Central",
        'coordinates': (39.7392, -104.9903)
	},
	{
		'name':"us-west-201",
        'region' : "US Southwest",
        'coordinates': (34.0522, -118.2437)
	},
	{
		'name':"us-west-1",
        'region' : "US West",
        'coordinates': (37.7749, -122.4194)
	},
	{
		'name':"us-west-2",
        'region' : "US Northwest",
        'coordinates': (43.8041, -120.5542)
	}
]

def get(cgx):
    
    ion_list = []
    
    #### Your Code Goes Here #####
    for sites in cgx.get.sites().cgx_content['items']:
        if sites["element_cluster_role"] == "SPOKE":
            print("You should have removed this section with your code ")
            return
            #### example start #####
            coordinates = {}
            coordinates['latitude'] = 35.85522398035947 
            coordinates['longitude'] = -118.38336067394894
            
            region = None
            #### Standalone Example #####
            region = find_region(coordinates)
            print(region)
            #### Panorama Example #####
            #region = find_region_panorama(coordinates)
    
    
    csv_columns = ['Site_Name', 'Region']
    csv_file = "site_regions.csv"
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in ion_list:
                writer.writerow(data)
            print("Saved site_regions.csv file")
    except IOError:
        print("CSV Write Failed")
    
    
    return

def find_region(coordinates):
    
    site_coordinates = (coordinates['latitude'], coordinates['longitude'])
    best_region = None
    best_distance = None
    
    for region in paList:
        if best_region == None:
            best_region = region["name"]
            best_distance = distance.distance(site_coordinates, region["coordinates"]).miles
        else:
            distance_check = distance.distance(site_coordinates, region["coordinates"]).miles
            if distance_check < best_distance:
                best_region = region["name"]
                best_distance = distance_check
    
    return best_region
    
def find_region_panorama(coordinates):
    best_region = None
    if PANORAMA_IP == None or PANORAMA_API_KEY == None:
        print("Sorry no Panorama IP or APK Key configured")
        return best_region
    
    xml_command = "/api/?type=op&cmd=<request><plugins><cloud_services><prisma-access><get-best-locations-by-latitude-longitude><nr-locations>1</nr-locations><latitude>"+str(coordinates['latitude'])+"</latitude><longitude>"+str(coordinates['longitude'])+"</longitude></get-best-locations-by-latitude-longitude></prisma-access></cloud_services></plugins></request>"
    api_url = "https://"+PANORAMA_IP+xml_command+"&key="+PANORAMA_API_KEY
    urllib3.disable_warnings()
    api_request = requests.get(url=api_url,verify=False)
    api_response = api_request.text

    data = xmltodict.parse(api_response)
    best_region = data["response"]["result"]["result"]["msg"]["location_info"]["entry"]["edge_location_name"]
    return best_region

def spn_panorama():
    if PANORAMA_IP == None or PANORAMA_API_KEY == None:
        print("Sorry no Panorama IP or APK Key configured")
        return
    xml_command = "/api/?type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/remote-networks/agg-bandwidth/region"
    api_url = "https://"+PANORAMA_IP+xml_command+"&key="+PANORAMA_API_KEY
    urllib3.disable_warnings()
    api_request = requests.get(url=api_url,verify=False)
    api_response = api_request.text

    data = xmltodict.parse(api_response)
    regions = data["response"]["result"]["region"]["entry"]
    if type(regions) == list:
        for region in regions:
            print(region)
    else:
        print(regions)
    return
    
def onboarding_panorama():
    if PANORAMA_IP == None or PANORAMA_API_KEY == None:
        print("Sorry no Panorama IP or APK Key configured")
        return
    xml_command = "/api/?type=config&action=get&xpath=/config/devices/entry[@name='localhost.localdomain']/plugins/cloud_services/remote-networks/onboarding"
    api_url = "https://"+PANORAMA_IP+xml_command+"&key="+PANORAMA_API_KEY
    urllib3.disable_warnings()
    api_request = requests.get(url=api_url,verify=False)
    api_response = api_request.text

    data = xmltodict.parse(api_response)
    onboarding = data["response"]["result"]["onboarding"]["entry"]
    if type(onboarding) == list:
        for item in onboarding:
            print(item)
    else:
        print(onboarding)
    return
                                      
def go():
    ############################################################################
    # Begin Script, parse arguments.
    ############################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(SCRIPT_NAME))

    # Allow Controller modification and debug level sets.
    controller_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    controller_group.add_argument("--controller", "-C",
                                  help="Controller URI, ex. "
                                       "Alpha: https://api-alpha.elcapitan.cloudgenix.com"
                                       "C-Prod: https://api.elcapitan.cloudgenix.com",
                                  default=None)
    controller_group.add_argument("--insecure", "-I", help="Disable SSL certificate and hostname verification",
                                  dest='verify', action='store_false', default=True)
    login_group = parser.add_argument_group('Login', 'These options allow skipping of interactive login')
    login_group.add_argument("--email", "-E", help="Use this email as User Name instead of prompting",
                             default=None)
    login_group.add_argument("--pass", "-PW", help="Use this Password instead of prompting",
                             default=None)
    debug_group = parser.add_argument_group('Debug', 'These options enable debugging output')
    debug_group.add_argument("--debug", "-D", help="Verbose Debug info, levels 0-2", type=int,
                             default=0)
    
    args = vars(parser.parse_args())
                             
    ############################################################################
    # Instantiate API
    ############################################################################
    cgx_session = cloudgenix.API(controller=args["controller"], ssl_verify=args["verify"])

    # set debug
    cgx_session.set_debug(args["debug"])

    ##
    # ##########################################################################
    # Draw Interactive login banner, run interactive login including args above.
    ############################################################################
    print("{0} v{1} ({2})\n".format(SCRIPT_NAME, SCRIPT_VERSION, cgx_session.controller))

    # login logic. Use cmdline if set, use AUTH_TOKEN next, finally user/pass from config file, then prompt.
    # figure out user
    if args["email"]:
        user_email = args["email"]
    elif CLOUDGENIX_USER:
        user_email = CLOUDGENIX_USER
    else:
        user_email = None

    # figure out password
    if args["pass"]:
        user_password = args["pass"]
    elif CLOUDGENIX_PASSWORD:
        user_password = CLOUDGENIX_PASSWORD
    else:
        user_password = None

    # check for token
    if CLOUDGENIX_AUTH_TOKEN and not args["email"] and not args["pass"]:
        cgx_session.interactive.use_token(CLOUDGENIX_AUTH_TOKEN)
        if cgx_session.tenant_id is None:
            print("AUTH_TOKEN login failure, please check token.")
            sys.exit()

    else:
        while cgx_session.tenant_id is None:
            cgx_session.interactive.login(user_email, user_password)
            # clear after one failed login, force relogin.
            if not cgx_session.tenant_id:
                user_email = None
                user_password = None

    ############################################################################
    # End Login handling, begin script..
    ############################################################################

    # get time now.
    curtime_str = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H-%M-%S')

    # create file-system friendly tenant str.
    tenant_str = "".join(x for x in cgx_session.tenant_name if x.isalnum()).lower()
    cgx = cgx_session
    

    get(cgx)
    
    # end of script, run logout to clear session.
    cgx_session.get.logout()

if __name__ == "__main__":
    go()