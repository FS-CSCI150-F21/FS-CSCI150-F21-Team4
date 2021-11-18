from twitterScrapeV1 import twitterMentionFunct, tweetFormatJson
import json
import re
import pickle

def tweetSentimentAnalyzer(userName, totalTweets):
    scrapeSuccess = False
    tweetData, scrapeSuccess = twitterMentionFunct(userName=userName, tweetAmount=totalTweets)
    if scrapeSuccess is False:
        return {} , scrapeSuccess
    else:
        scrapeSuccess = True

    tweetFormatJson("tweetText.json",tweetData)
    with open("vectorizer.pickle", "rb") as pickle_in:
        processedVector = pickle.load(pickle_in)

    with open("LogisticRegClass.pickle", "rb") as pickle_in:
        logicRegClass = pickle.load(pickle_in)

    with open('tweetText.json', encoding='utf-8') as infile:
        tweetJson = json.load(infile)

    testEntries = tweetJson['data']
    testProcessed = []
    for sentence in testEntries:
        sentence = sentence['text']
        # Remove all the special characters
        processed_feature = re.sub(r'\W', ' ', sentence)

        # remove all single characters
        processed_feature= re.sub(r'\s+[a-zA-Z]\s+', ' ', processed_feature)

        # Remove single characters from the start
        processed_feature = re.sub(r'\^[a-zA-Z]\s+', ' ', processed_feature) 

        # Substituting multiple spaces with single space
        processed_feature = re.sub(r'\s+', ' ', processed_feature, flags=re.I)

        # Removing prefixed 'b'
        processed_feature = re.sub(r'^b\s+', '', processed_feature)

        # Converting to Lowercase
        processed_feature = processed_feature.lower()

        testProcessed.append(processed_feature)

    processed_features = processedVector.transform(testProcessed).toarray()
    prediction = logicRegClass.predict(processed_features)
    print(processed_features.shape)
    print(prediction)
    predictionList= prediction.tolist()
    possitiveTweetsTot = predictionList.count('4')
    negativeTweetsTot = predictionList.count('0')
    print(f"Number of Positive tweets: {possitiveTweetsTot}")
    print(f"Number of Negative tweets: {negativeTweetsTot}")
    return {"tweet_postive": possitiveTweetsTot, "tweet_negative": negativeTweetsTot}, scrapeSuccess