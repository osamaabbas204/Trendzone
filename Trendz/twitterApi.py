import tweepy
from textblob import TextBlob
from datetime import date, timedelta
from .models import MObiletrend, Laptoptrend
tweets = []
# function to calculate percentage


def percentage(reaction, nooftweet):
    temp = 100 * float(reaction) / float(nooftweet)
    return format(temp, '.2f')


def runtime(searchTerm):
    # authenticating
    consumerKey = "veDhmVUkFY7o6FHnIrnQw0Z9s"
    consumerSecret = "FBu9JvIb5uiQiYZlDBrq1uxhfgOsElyrarlRF9UozOdQmQI04D"
    accessToken = "847364064581894147-3JnskoJO1hCoqe1uYz1xnuNoEv81MZz"
    accessTokenSecret = "e8KuDHXRgl8N6TK73Hdpfx6ZL6OyVqKA3Nijp7TczH9h6"
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # input for term to be searched and how many tweets to search
    NoOfTerms = 10
    # searching for tweets
    for search in searchTerm:
        tweets = tweepy.Cursor(api.search, q=search,
                               lang="en").items(NoOfTerms)
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
    # iterating through tweets1 fetched
        for tweet in tweets:
            # tweet's text
            analysis = TextBlob(tweet.text)
            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0.00):
                positive += 1
            elif (analysis.sentiment.polarity < 0.00):
                negative += 1

        # finding average of how people are reacting
        positive = percentage(positive, NoOfTerms)
        negative = percentage(negative, NoOfTerms)
        neutral = percentage(neutral, NoOfTerms)

        # Data dictionary for each brand
        if(search == '#oppo'):
            oppo = {'positive': positive,
                    'negative': negative, 'neutral': neutral}
        elif(search == '#vivo'):
            vivo = {'positive': positive,
                    'negative': negative, 'neutral': neutral}
        elif(search == '#samsung'):
            samsung = {'positive': positive,
                       'negative': negative, 'neutral': neutral}
        elif(search == '#xiaomi'):
            xiaomi = {'positive': positive,
                      'negative': negative, 'neutral': neutral}
        elif(search == 'Apple iphone'):
            apple = {'positive': positive,
                     'negative': negative, 'neutral': neutral}
        elif(search == '#huawei'):
            huawei = {'positive': positive,
                      'negative': negative, 'neutral': neutral}
        elif(search == '#teampixel'):
            googlepixel = {'positive': positive,
                           'negative': negative, 'neutral': neutral}
        elif(search == '#OnePlus'):
            oneplus = {'positive': positive,
                       'negative': negative, 'neutral': neutral}
        elif(search == '#dell'):
            oppo = {'positive': positive,
                    'negative': negative, 'neutral': neutral}
        elif(search == 'lenovo laptop'):
            vivo = {'positive': positive,
                    'negative': negative, 'neutral': neutral}
        elif(search == 'macbook'):
            samsung = {'positive': positive,
                       'negative': negative, 'neutral': neutral}
        elif(search == '#hplaptop'):
            xiaomi = {'positive': positive,
                      'negative': negative, 'neutral': neutral}
        elif(search == '#microsoft #laptop'):
            apple = {'positive': positive,
                     'negative': negative, 'neutral': neutral}
        elif(search == 'acer laptop'):
            huawei = {'positive': positive,
                      'negative': negative, 'neutral': neutral}
        elif(search == 'asus laptop'):
            googlepixel = {'positive': positive,
                           'negative': negative, 'neutral': neutral}
        elif(search == 'Msi laptop'):
            oneplus = {'positive': positive,
                       'negative': negative, 'neutral': neutral}
        # printing out data tweets
        print("Daily public reaction on " + search)
        print()
        print()
        print("Detailed Report: " + search)
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

    context = {"oppo": oppo, "vivo": vivo, "xiaomi": xiaomi, "apple": apple,
               "huawei": huawei, "googlepixel": googlepixel, "oneplus": oneplus, "samsung": samsung}
    return context


# -----------------------------------------------------------------------------------------------------------------
def runtime_productgraph(name):
    # authenticating
    consumerKey = "veDhmVUkFY7o6FHnIrnQw0Z9s"
    consumerSecret = "FBu9JvIb5uiQiYZlDBrq1uxhfgOsElyrarlRF9UozOdQmQI04D"
    accessToken = "847364064581894147-3JnskoJO1hCoqe1uYz1xnuNoEv81MZz"
    accessTokenSecret = "e8KuDHXRgl8N6TK73Hdpfx6ZL6OyVqKA3Nijp7TczH9h6"
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # name assignment to tweepy cursor for searching relevant tweets
    search = name
    NoOfTerms = 10
    i = 0
    # searching for tweets
    tweets = tweepy.Cursor(api.search, q=search, lang="en").items(NoOfTerms)
    polarity = 0
    positive = 0
    negative = 0
    neutral = 0
    # iterating through tweets1 fetched
    for tweet in tweets:
        # tweet's text
        analysis = TextBlob(tweet.text)
        # adding up polarities to find the average later
        polarity += analysis.sentiment.polarity
        # adding reaction of how people are reacting to find average later
        if (analysis.sentiment.polarity == 0):
            neutral += 1
        elif (analysis.sentiment.polarity > 0.00):
            positive += 1
        elif (analysis.sentiment.polarity < 0.00):
            negative += 1
    # finding average of how people are reacting
    positive = percentage(positive, NoOfTerms)
    negative = percentage(negative, NoOfTerms)
    neutral = percentage(neutral, NoOfTerms)
    # finding average reaction
    polarity = polarity / NoOfTerms
    # Data dictionary for each brand
    Pname = {'positive': positive, 'negative': negative, 'neutral': neutral}
    # printing out data tweets
    print("Reviews of " + name)
    print(str(positive) + "% people thought it was positive")
    print(str(negative) + "% people thought it was negative")
    print(str(neutral) + "% people thought it was neutral")
    return Pname
# -----------------------------------------------------------------------------------------------------------------


def dailytrends(device_name):
    # setting date
    today = date.today()
    start = today - timedelta(days=today.weekday())
    # authenticating
    consumerKey = "veDhmVUkFY7o6FHnIrnQw0Z9s"
    consumerSecret = "FBu9JvIb5uiQiYZlDBrq1uxhfgOsElyrarlRF9UozOdQmQI04D"
    accessToken = "847364064581894147-3JnskoJO1hCoqe1uYz1xnuNoEv81MZz"
    accessTokenSecret = "e8KuDHXRgl8N6TK73Hdpfx6ZL6OyVqKA3Nijp7TczH9h6"
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # input for term to be searched and how many tweets to search
    if device_name == "Mobile":
        searchTerm = ['#oppo', '#vivo', '#xiaomi', '#Apple',
                      '#huawei', '#teampixel', '#OnePlus', 'smartphone #samsung']
    else:
        searchTerm = ['#dell', 'lenovo laptop', 'macbook', '#hplaptop',
                      '#microsoft #laptop', 'acer laptop', 'asus laptop', 'Msi laptop']

    NoOfTerms = 50

    # searching for tweets
    for search in searchTerm:
        tweets = tweepy.Cursor(api.search, q=search,
                               since=start, lang="en").items(NoOfTerms)
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
    # iterating through tweets1 fetched
        for tweet in tweets:
            # tweet's text
            analysis = TextBlob(tweet.text)
            # adding up polarities to find the average later
            polarity += analysis.sentiment.polarity
            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0.00):
                positive += 1
            elif (analysis.sentiment.polarity < 0.00):
                negative += 1

        # finding average of how people are reacting
        positive = percentage(positive, NoOfTerms)
        negative = percentage(negative, NoOfTerms)
        neutral = percentage(neutral, NoOfTerms)
        # finding average reaction
        polarity = polarity / NoOfTerms
        # Data dictionary for each brand
        # if(searchTerm[i] == '#oppo'):
        #     oppo = {'positive': positive,
        #             'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#vivo'):
        #     vivo = {'positive': positive,
        #             'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == 'smartphone #samsung'):
        #     samsung = {'positive': positive,
        #                'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#xiaomi'):
        #     xiaomi = {'positive': positive,
        #               'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#Apple'):
        #     apple = {'positive': positive,
        #              'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#huawei'):
        #     huawei = {'positive': positive,
        #               'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#teampixel'):
        #     googlepixel = {'positive': positive,
        #                    'negative': negative, 'neutral': neutral}
        # elif(searchTerm[i] == '#OnePlus'):
        #     oneplus = {'positive': positive,
        #                'negative': negative, 'neutral': neutral}
        # printing out data tweets
        print("Daily public reaction on " + search)
        print()
        print()
        print("Detailed Report: " + search)
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

        if device_name == "Mobile":
            if MObiletrend.objects.filter(brandName=search, status="daily"):
                MObiletrend.objects.filter(brandName=search, status="daily").update(
                    positive=positive, negative=negative, neutral=neutral)

            else:
                trend = MObiletrend(
                    brandName=searchTerm[i], status="daily", positive=positive, negative=negative, neutral=neutral)
                trend.save()
        else:
            if Laptoptrend.objects.filter(brandName=search, status="daily"):
                Laptoptrend.objects.filter(brandName=search, status="daily").update(
                    positive=positive, negative=negative, neutral=neutral)

            else:
                trend = Laptoptrend(
                    brandName=search, status="daily", positive=positive, negative=negative, neutral=neutral)
                trend.save()

    return None


# -----------------------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------
def weeklytrends(device_name):
    # setting date
    today = date.today()
    start = today - timedelta(days=today.weekday())
    end = start + timedelta(days=6)
    print("Today: " + str(today))
    print("Start: " + str(start))
    print("End: " + str(end))
    # authenticating
    consumerKey = "veDhmVUkFY7o6FHnIrnQw0Z9s"
    consumerSecret = "FBu9JvIb5uiQiYZlDBrq1uxhfgOsElyrarlRF9UozOdQmQI04D"
    accessToken = "847364064581894147-3JnskoJO1hCoqe1uYz1xnuNoEv81MZz"
    accessTokenSecret = "e8KuDHXRgl8N6TK73Hdpfx6ZL6OyVqKA3Nijp7TczH9h6"
    auth = tweepy.OAuthHandler(consumerKey, consumerSecret)
    auth.set_access_token(accessToken, accessTokenSecret)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    # input for term to be searched and how many tweets to search
    if device_name == "Mobile":
        searchTerm = ['#oppo', '#vivo', '#xiaomi', '#Apple',
                      '#huawei', '#teampixel', '#OnePlus', '#samsung']
    else:
        searchTerm = ['#dell', 'lenovo laptop', 'macbook', '#hplaptop',
                      '#surfacebook', 'acer laptop', 'asus laptop', 'Msi laptop']

    NoOfTerms = 200
    # searching for tweets
    for search in searchTerm:
        tweets = tweepy.Cursor(
            api.search, q=search, since=start, count=NoOfTerms, until=end, lang="en").items(NoOfTerms)
        polarity = 0
        positive = 0
        negative = 0
        neutral = 0
    # iterating through tweets1 fetched
        for tweet in tweets:
            # tweet's text
            analysis = TextBlob(tweet.text)
            # adding up polarities to find the average later
            polarity += analysis.sentiment.polarity
            # adding reaction of how people are reacting to find average later
            if (analysis.sentiment.polarity == 0):
                neutral += 1
            elif (analysis.sentiment.polarity > 0.00):
                positive += 1
            elif (analysis.sentiment.polarity < 0.00):
                negative += 1

        # finding average of how people are reacting
        positive = percentage(positive, NoOfTerms)
        negative = percentage(negative, NoOfTerms)
        neutral = percentage(neutral, NoOfTerms)
        # finding average reaction
        polarity = polarity / NoOfTerms
        # Data dictionary for each brand

        # printing out data tweets
        print("Daily public reaction on " + search)
        print()
        print()
        print("Detailed Report: " + search)
        print(str(positive) + "% people thought it was positive")
        print(str(negative) + "% people thought it was negative")
        print(str(neutral) + "% people thought it was neutral")

        if device_name == "Mobile":
            if MObiletrend.objects.filter(brandName=search, status="weekly"):
                MObiletrend.objects.filter(brandName=search, status="weekly").update(
                    positive=positive, negative=negative, neutral=neutral)

            else:
                trend = MObiletrend(
                    brandName=search, status="weekly", positive=positive, negative=negative, neutral=neutral)
                trend.save()
        else:
            if Laptoptrend.objects.filter(brandName=search, status="weekly"):
                Laptoptrend.objects.filter(brandName=search, status="weekly").update(
                    positive=positive, negative=negative, neutral=neutral)

            else:
                trend = Laptoptrend(
                    brandName=search, status="weekly", positive=positive, negative=negative, neutral=neutral)
                trend.save()
    return None

# ----------------------------------------------------------------------------------------------------

# -----------------------------------------------------------------------------------------------------------------


# -----------------------------------------------------------------------------------------------------------------
#

    # runtime()
    # dailytrends()
    # weeklytrends( searchTerm = ['#oppo', '#vivo', '#xiaomi', '#Apple', '#huawei', '#teampixel', '#OnePlus', '#samsung'])
    # name="iphone 12"
    # runtime_productgraph(name)

def mobileweekly_trend():
    weeklytrends("Mobile")
    pass


def mobiledaily_trend():
    dailytrends("Mobile")
    pass


def laptopweekly_trend():
    weeklytrends("Laptop")
    pass


def Laptopdaily_trend():
    dailytrends("Laptop")
    pass
