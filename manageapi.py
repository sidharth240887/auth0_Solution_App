import json
import urllib
import urllib.request  as urllib2 
import requests
import constants
import http.client
import re
from dotenv import load_dotenv, find_dotenv
from os import environ as env
from collections import defaultdict


ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
GRANT_TYPE = "client_credentials" # OAuth 2.0 flow to use
AUTH0_BASE_URL = "https://" + AUTH0_DOMAIN
AUDIENCE = AUTH0_BASE_URL + "/api/v2/"

def get_access_token():
    """
    Function responsible to get access token for management api usage
    :param:
    :return: access_token string for management api authentication.
    """
    #Get an Access Token from Auth0
    try:
        data = urllib.parse.urlencode([('client_id', AUTH0_CLIENT_ID),
                           ('client_secret', AUTH0_CLIENT_SECRET),
                           ('audience', AUDIENCE),
                           ('grant_type', GRANT_TYPE)])		
        data = data.encode('ascii')
        req = urllib2.Request(AUTH0_BASE_URL + "/oauth/token", data)
        response = urllib2.urlopen(req)
        oauth = json.loads(response.read())
        access_token = oauth['access_token']
        return access_token
    except urllib.error.HTTPError as e:
        print(e.read())
    except error.URLError as e:
        print(e.read())


def get_client_list():
    """
    Function to get list of clients for the account
    :param:
    :return: List of all clients associated with account.
    """
    try:
        access_token = get_access_token()
        req = urllib2.Request(AUTH0_BASE_URL + "/api/v2/clients")
        req.add_header('Authorization', "Bearer " + access_token)
        req.add_header('Content-Type', 'application/json')

        response = urllib.request.urlopen(req)
        res = json.loads(response.read())    
        return res
    except urllib.error.HTTPError as e:
        print(e.read())
    except error.URLError as e:
        print(e.read())
    
def get_rule_list():
    """
    Function to get list of rules for the account
    :param:
    :return: List of all rules associated with account.
    """
    try:
        access_token = get_access_token()
        req = urllib2.Request(AUTH0_BASE_URL + "/api/v2/rules")
        req.add_header('Authorization', 'Bearer ' + access_token)
        req.add_header('Content-Type', 'application/json')
            
        response = urllib2.urlopen(req)
        res = json.loads(response.read())
        return res
    except urllib.error.HTTPError as e:
        print(e.read())
    except error.URLError as e:
        print(e.read())


def get_client_rule_map():
    """
    Function to create a list of clients with rule names mapped.
    :param:
    :return: dictionary associated with client name, id and rule name mapping.
    """
    try:    
        clients = get_client_list()
        rules = get_rule_list()
        
        mapping = defaultdict(list)

        for client in clients:
            
            #Skip execution for 'All Application Client'
            if client["name"] == 'All Applications':
                continue

            client_name,client_id = client["name"],client["client_id"]
            key = client_name + "_" + client_id
            for rule in rules:
                ## check for equality or non-equality with client name or ID
                matches = re.findall("(context.clientName|context.clientID) (===|!==) '(.*)'",rule["script"])       
                ## If there is a match, handle cases differently as per equality and non equality
                if(matches):
                    for match in matches:
                        if(((match[2] == client_name) & (match[1] == "===")) | \
                          ((match[2] == client_id) & (match[1] == "==="))):
                            if rule["name"] not in mapping[key]: mapping[key].append(rule["name"])

                        if(not((match[2] == client_name) | (match[2] == client_id))):
                            if((match[1] == "!==")):
                                if rule["name"] not in mapping[key]: mapping[key].append(rule["name"])
                 
                ## If not match, then the rule is applicable to all clients
                else:
                    if rule["name"] not in mapping[key]: mapping[key].append(rule["name"])

        return mapping
    except:
        print("Exception occured in get_client_rule_map")




                    
        
		
	
	
	
	

    
  
  