"""
Twitter: Suchwort in Umgebung
"""
import base64
import requests
import twitter_credentials

class TwitterCounts:
    """This class takes search parameters and makes the Twitter request"""
    
    def __init__(self):

        self.keyword = ""
        self.latitude = ""
        self.longitude = ""
        self.radius = ""
        self.unit = ""
        


    def set_parameters(self, keyword, latitude, longitude, radius, unit):
        """ Ser new parameters for request."""
        self.keyword = keyword
        self.latitude = latitude
        self.longitude = longitude
        self.radius = radius
        self.unit = unit


    def get_search_results(self):
        """Make search request with preset search parameters."""


        list_of_results = list()
        last_id = 0
        max_result = 100
        length_of_results = 0


        # OAuth2 authentication, create base64 key
        key_secret = '{}:{}'.format(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET).encode('ascii')
        b64_encoded_key = base64.b64encode(key_secret)
        b64_encoded_key = b64_encoded_key.decode('ascii')

        # Obtain bearer token
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

        access_token = auth_resp.json()['access_token']

        # Request header
        self.search_headers = {
            'Authorization': 'Bearer {}'.format(access_token)    
                }

        # Search parameters
        self.search_params = {
            'q': self.keyword, ## See boiler plate
            'result_type': 'recent', ## default: 'mixed', others: 'recent', 'popular'
            'count': 100,            ## This is the max amount
            'geocode': "{},{},{}{}".format(self.latitude, self.longitude, self.radius, self.unit), ## See boiler plate
            # 'max_id' : '1062271063617429504' ## Use this parameter to make a second search beyong the first 100
            }

        # Base url + search URL
        self.search_url = '{}1.1/search/tweets.json'.format(base_url)
        search_results = requests.get(self.search_url, headers=self.search_headers, params=self.search_params)
        #print(search_results.json())

        # Abort if there are not tweets
        if len(search_results.json()['statuses']) == 0:
            print('There are not tweets.')
            return list_of_results

        list_of_results.append(search_results)

        ### Get Tweet-ID from last tweet.
        ### Bigger means newer. I want the oldest as max_id.
        first_id = search_results.json()['statuses'][0]['id']
        last_id = search_results.json()['statuses'][-1]['id']
        #print(first_id)
        #print(last_id)
        #print(first_id > last_id)
        

        length_of_results = len(search_results.json()['statuses'])

        # This loop makes sure the items beyond the first 100 are received.
        while  length_of_results == 100:
            print('Weiterer Request, da der vorherige 100 Eintraege hat.')

            # Search parameters with max_id
            self.search_params = {
                'q': self.keyword, ## See boiler plate
                'result_type': 'recent', ## default: 'mixed', others: 'recent', 'popular'
                'count': 100,            ## This is the max amount
                'geocode': "{},{},{}{}".format(self.latitude, self.longitude, self.radius, self.unit), ## See boiler plate
                'max_id' : last_id ## Use this parameter to make a second search beyong the first 100
                }

            # Base url + search URL
            self.search_url = '{}1.1/search/tweets.json'.format(base_url)
            search_results = requests.get(self.search_url, headers=self.search_headers, params=self.search_params)
            #print(search_results.json())        
            list_of_results.append(search_results)

            length_of_results = len(search_results.json()['statuses'])


        return(list_of_results)


    def clean_search_results(self, list_of_search_results):
        """Clean list of raw request results for further use."""
        
        if len(list_of_search_results) == 0:
            return 0
        else:
            count = 0
            for item in list_of_search_results:
                tweet_data = item.json()
                print("-" * 10)
                #print(len(tweet_data)) ## result always 2
                #print(tweet_data.keys()) ## result always [u'search_metadata', u'statuses']
                print(len(tweet_data['statuses']))

                for item in tweet_data['statuses'][:-1]: # Without eliminating the last item, lists overlap

                    #if item['geo']:
                    #print(item['user']['screen_name'], item['geo'], item['coordinates'], item['place']) #, item['user']['location']
                    print(item['id'], item['text'].encode('utf-8'))
                    
                count += len(tweet_data['statuses'])

            return count


    # Check status code
    #search_results.status_code

    def check_status_code(self):
        """Check status code"""
        print(auth_resp.status_code)

if __name__ == '__main__':
    keyword = 'Schwebebahn'
    latitude = '51.270086'
    longitude = '7.191741'
    radius = '4'
    unit = 'km'
    
    twittercounts = TwitterCounts()
    twittercounts.set_parameters(keyword, latitude, longitude, radius, unit)
    print(twittercounts.get_search_results())
    print(twittercounts.clean_search_results(twittercounts.get_search_results()))


'''
$ curl --request GET 
 --url 'https://api.twitter.com/1.1/search/tweets.json?q=nasa&result_type=popular' 
 --header 'authorization: OAuth oauth_consumer_key="consumer-key-for-app", 
 oauth_nonce="generated-nonce", oauth_signature="generated-signature", 
 oauth_signature_method="HMAC-SHA1", oauth_timestamp="generated-timestamp", 
 oauth_token="access-token-for-authed-user", oauth_version="1.0"'
 
Thanks to: 
- http://benalexkeen.com/interacting-with-the-twitter-api-using-python/
- https://stackoverflow.com/questions/44301195/twitter-api-count-more-than-100-using-twitter-search-api

According to API:
Specify the parameter max_id to retrieve results from before that.



 '''

