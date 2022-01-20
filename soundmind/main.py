import requests
import os
import json
import csv

from dotenv import load_dotenv
load_dotenv()

def auth():
    return os.environ.get("TOKEN")

def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers

def create_url(id, max_results = 10):
    
    search_url = f"https://api.twitter.com/2/users/{id}/tweets" #Change to the endpoint you want to collect data from
    
    #change params based on the endpoint you are using
    query_params = {'max_results': max_results,
                    'expansions': 'author_id,in_reply_to_user_id,geo.place_id',
                    'tweet.fields': 'id,text,author_id,in_reply_to_user_id,geo,conversation_id,created_at,lang,public_metrics,referenced_tweets,reply_settings,source',
                    'user.fields': 'id,name,username,created_at,description,public_metrics,verified',
                    'place.fields': 'full_name,id,country,country_code,geo,name,place_type',
                    'next_token': {}}
    return (search_url, query_params)


def connect_to_endpoint(url, headers, params, next_token = None):
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

def get_userid(name,headers,next_token = None):
    url_ = f'https://api.twitter.com/2/users/by/username/{name}'
    params = { }
    params['next_token'] = next_token   #params object received from create_url function
    response = requests.request("GET", url_, headers = headers, params = params)
    print("Endpoint Response Code: " + str(response.status_code))
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()

token = auth()
header = create_headers(token)
max_results = 30


name = input("Enter twitter username : ")
idjson =  get_userid(name,header)
# print(json.dumps(idjson, indent=4, sort_keys=True))
id = idjson['data']['id']
# print(id)
url = create_url(id,max_results)
resp = connect_to_endpoint(url[0],header,url[1])

res = json.dumps(resp, indent=4, sort_keys=True)

csvFile = open("data.csv",'w',newline="",encoding="utf-8")
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['Id','TweetText'])

for index,twt in enumerate(resp['data'],1):
    row = [index, twt['text']]
    csvWriter.writerow(row)

csvFile.close()
print(res[0])


