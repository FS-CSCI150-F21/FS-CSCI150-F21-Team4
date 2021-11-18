import requests
import base64
import json
import oauth2 as oauth
import urllib.parse

def twitterMentionScrape(userName, tweetAmount):
    #---------------------- Description ------------------
    #This Function will take the user name of a user and will check all mentions or replies to a tweet.
    #Will ignore all replies the user will make to other tweets mentioning them.
    #userName will hold the Name of the user being searched
    #tweetAmount will contain the number of tweets needed for search
    # - note that the max amount of tweets is 100
    #Output will be a dictionary of collected tweets
    #Last Updated: 10/11/2021
    consumer_key = "iEzt4HCKulumaREJQY1QktzuK"
    consumer_secret = "NgVzacebhTKsAFvBgPlnEbFObhvbn1mrtXnVf3BNTDUdPzFCh8"

    #------------------- secret key generation----------------
    key_secret = f'{consumer_key}:{consumer_secret}'.encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']

    #------------------- Start of Mention Finder--------------
    ##Create HTTP headers
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }

    ## Grab User ID
    httpURL = f"https://api.twitter.com/1.1/users/show.json?screen_name={userName}"
    userMentions = requests.get(url=httpURL, headers=search_headers)
    print(userMentions.status_code)
    userMentions = userMentions.json()
    userID = userMentions['id']
    ##Grab Json tweet results
    #check if tweet amounts exceed 100
    if tweetAmount >= 100:
        #The maximum default is 100
        tweetAmount = 100
    mentionsURL = f"https://api.twitter.com/1.1/search/tweets.json?q={userName}&count={tweetAmount}"
    userMentions = requests.get(url=mentionsURL, headers=search_headers)
    print(userMentions.status_code)
    userMentions = userMentions.json()

    ## Loop through Tweet json and look for
    # -only mentions of user
    # -populate a dictionary to be formatted into json
    textList = []
    statuses = userMentions['statuses']
    for response in statuses:   
        creationTime = response['created_at']
        tweetText = response['text']
        tweetID = response['user']['id']
        if tweetID == userID:
            print(creationTime, "Posted by Fox")
        else:
            # print(creationTime,tweetID, tweetText)
            textList.append(tweetText)
    textDict = {'tweet': textList}
    print("Finished!")
    return textDict

def twitterMentionFunct(userName, tweetAmount):
     #---------------------- Description ------------------
    #This Function will take the user name of a user and will check all mentions or replies to a tweet.
    #Will ignore all replies the user will make to other tweets mentioning them.
    #userName will hold the Name of the user being searched
    #tweetAmount will contain the number of tweets needed for search
    # - note that the max amount of tweets is 100
    #Output will be a dictionary of collected tweets
    #Last Updated: 10/11/2021
    consumer_key = "uaC0BoALYt6SzxdNiWoOpvGym"
    consumer_secret = "NHc7uMZLM3zk77fZ7EuOzqSfuDnpqN52ZsTiLGh2k5CylsEPpj"

    #------------------- secret key generation----------------
    key_secret = f'{consumer_key}:{consumer_secret}'.encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']

    #------------------- Start of Mention Finder--------------
    ##Create HTTP headers
    search_headers = {
        'Authorization': 'Bearer {}'.format(access_token)    
    }
    ## Grab User ID
    httpURL = f"https://api.twitter.com/1.1/users/show.json?screen_name={userName}"
    userMentions = requests.get(url=httpURL, headers=search_headers)
    print(userMentions.status_code)
    userMentions = userMentions.json()
    userID = userMentions['id']
    ##Grab Json tweet results
    #check if tweet amounts exceed 100
    if tweetAmount >= 100:
        #The maximum default is 100
        tweetAmount = 100
    mentionURL = f"https://api.twitter.com/2/users/{userID}/mentions?max_results={tweetAmount}"
    userMentions = requests.get(url=mentionURL, headers=search_headers)
    print(userMentions.status_code)
    userMentions = userMentions.json()
    return userMentions

def tweetFormatJson(filename, data):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False, indent=4)
    print("Json update complete.")
    return

def twitterLogin():
    consumer_key = "uaC0BoALYt6SzxdNiWoOpvGym"
    consumer_secret = "NHc7uMZLM3zk77fZ7EuOzqSfuDnpqN52ZsTiLGh2k5CylsEPpj"

    #------------------- secret key generation----------------
    key_secret = f'{consumer_key}:{consumer_secret}'.encode('ascii')

    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')
    base_url = 'https://api.twitter.com/'
    auth_url = '{}oauth2/token'.format(base_url)

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }

    auth_data = {
        'grant_type': 'client_credentials'
    }

    auth_resp = requests.post(auth_url, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code)
    access_token = auth_resp.json()['access_token']

    #------------------- Start of Mention Finder--------------
    ##Create HTTP headers

    request_token_url = 'https://api.twitter.com/oauth/request_token'
    access_token_url = 'https://api.twitter.com/oauth/access_token'
    authorize_url = 'https://api.twitter.com/oauth/authorize'
    authenticate_url = 'https://api.twitter.com/oauth/authenticate'

    consumer = oauth.Consumer(consumer_key, consumer_secret)
    client = oauth.Client(consumer)

    # Step 1: Get a request token. This is a temporary token that is used for 
    # having the user authorize an access token and to sign the request to obtain 
    # said access token.

    resp, content = client.request(request_token_url, "GET")
    if resp['status'] != '200':
        raise Exception("Invalid response {}".format(resp['status']))

    request_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))


    print ("Request Token:")
    print ("    - oauth_token        = {}".format(request_token['oauth_token']))
    print ("    - oauth_token_secret = {}".format(request_token['oauth_token_secret'])) 

    # Step 2: Redirect to the provider. Since this is a CLI script we do not 
    # redirect. In a web application you would redirect the user to the URL
    # below.

    print ("Go to the following link in your browser:")
    print ("{0}?oauth_token={1}".format(authenticate_url, request_token['oauth_token']))

    # After the user has granted access to you, the consumer, the provider will
    # redirect you to whatever URL you have told them to redirect to. You can 
    # usually define this in the oauth_callback argument as well.
    accepted = 'n'
    while accepted.lower() == 'n':
        accepted = input('Have you authorized me? (y/n) ')
    oauth_verifier = input('What is the PIN? ')

    resp, content = client.request(authenticate_url, "GET")
    print(resp)
    print(content)
    # Step 3: Once the consumer has redirected the user back to the oauth_callback
    # URL you can request the access token the user has approved. You use the 
    # request token to sign this request. After this is done you throw away the
    # request token and use the access token returned. You should store this 
    # access token somewhere safe, like a database, for future use.
    token = oauth.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)

    resp, content = client.request(access_token_url, "POST")
    access_token = dict(urllib.parse.parse_qsl(content.decode("utf-8")))

    print ("Access Token:")
    print ("    - oauth_token        = {}".format(access_token['oauth_token']))
    print ("    - oauth_token_secret = {}".format(access_token['oauth_token_secret']))

    print ("You may now access protected resources using the access tokens above.") 

    return True

# def main():
#     userMentions = twitterMentionFunct("foxstevensonnow", 15)
#     print(userMentions)
#     # successLogin = twitterLogin()
#     # if successLogin == True:
#     #     print("Login Sucessful")
#     # else:
#     #     print("Login Failed")
#     # return

# if __name__ == "__main__":
#     main()