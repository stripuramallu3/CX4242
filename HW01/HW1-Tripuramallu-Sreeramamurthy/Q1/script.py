import csv
import json
import time
import tweepy

# You must use Python 3.0 or above
# For those who have been using python 2.7.x before, here is an article explaining key differences between python 2.7x & 3.x
# http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html

# Rate limit chart for Twitter REST API - https://dev.twitter.com/rest/public/rate-limits

def loadKeys(key_file):
    # TODO: put in your keys and tokens in the keys.json file,
    #       then implement this method for loading access keys and token from keys.json
    # rtype: str <api_key>, str <api_secret>, str <token>, str <token_secret>
    keys = json.load(open("keys.json", "r"))
    return keys["api_key"], keys["api_secret"], keys["token"], keys["token_secret"]

# Q1.b - 5 Marks
def getFollowers(api, root_user, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers of 'root_user'
    # rtype: list containing entries in the form of a tuple (follower, root_user)
    api.wait_on_rate_limit = True
    followers = []
    for follower in tweepy.Cursor(api.followers, screen_name = root_user).items(no_of_followers):
        tempTup = follower.screen_name, root_user
        followers.append(tempTup)
    return followers

# Q1.b - 7 Marks
def getSecondaryFollowers(api, followers_list, no_of_followers):
    # TODO: implement the method for fetching 'no_of_followers' followers for each entry in followers_list
    # rtype: list containing entries in the form of a tuple (follower, followers_list[i])
    api.wait_on_rate_limit = True
    secondary_followers = []
    for follower, root_user in followers_list: 
        for secondary_follower in tweepy.Cursor(api.followers, screen_name = follower).items(no_of_followers): 
            tempTup = secondary_follower.screen_name, follower
            secondary_followers.append(tempTup)
    return secondary_followers

# Q1.c - 5 Marks
def getFriends(api, root_user, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends of 'root_user'
    # rtype: list containing entries in the form of a tuple (root_user, friend)
    api.wait_on_rate_limit = True
    friends = []
    for friend in tweepy.Cursor(api.friends, screen_name = root_user).items(no_of_friends): 
        tempTup = root_user, friend.screen_name
        friends.append(tempTup)
    return friends

# Q1.c - 7 Marks
def getSecondaryFriends(api, friends_list, no_of_friends):
    # TODO: implement the method for fetching 'no_of_friends' friends for each entry in friends_list
    # rtype: list containing entries in the form of a tuple (friends_list[i], friend)
    api.wait_on_rate_limit = True 
    secondary_friends = []
    for root_user, friend in friends_list: 
        for secondary_friend in tweepy.Cursor(api.friends, screen_name = friend).items(no_of_friends): 
            tempTup = friend, secondary_friend.screen_name
            secondary_friends.append(tempTup)
    return secondary_friends

# Q1.b, Q1.c - 6 Marks
def writeToFile(data, output_file):
    # write data to output file
    # rtype: None
    if (output_file == "followers.csv") :
        with open(output_file, "w") as file: 
            writer = csv.writer(file)
            for follower in data: 
                writer.writerow(follower)
            file.close()
    else: 
        with open(output_file, "w") as file: 
            writer = csv.writer(file)
            for friend in data: 
                writer.writerow(friend)
            file.close()






"""
NOTE ON GRADING:

We will import the above functions
and use testSubmission() as below
to automatically grade your code.

You may modify testSubmission()
for your testing purposes
but it will not be graded.

It is highly recommended that
you DO NOT put any code outside testSubmission()
as it will break the auto-grader.

Note that your code should work as expected
for any value of ROOT_USER.
"""

def testSubmission():
    KEY_FILE = 'keys.json'
    OUTPUT_FILE_FOLLOWERS = 'followers.csv'
    OUTPUT_FILE_FRIENDS = 'friends.csv'

    ROOT_USER = 'PoloChau'
    NO_OF_FOLLOWERS = 10
    NO_OF_FRIENDS = 10


    api_key, api_secret, token, token_secret = loadKeys(KEY_FILE)

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(token, token_secret)
    api = tweepy.API(auth)

    primary_followers = getFollowers(api, ROOT_USER, NO_OF_FOLLOWERS)
    secondary_followers = getSecondaryFollowers(api, primary_followers, NO_OF_FOLLOWERS)
    followers = primary_followers + secondary_followers

    primary_friends = getFriends(api, ROOT_USER, NO_OF_FRIENDS)
    secondary_friends = getSecondaryFriends(api, primary_friends, NO_OF_FRIENDS)
    friends = primary_friends + secondary_friends

    writeToFile(followers, OUTPUT_FILE_FOLLOWERS)
    writeToFile(friends, OUTPUT_FILE_FRIENDS)


if __name__ == '__main__':
    testSubmission()

