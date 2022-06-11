from twitter_utils.twitter_utils import Loader, Processor

def main():
    tweets = '/Users/jakegodsall/Google Drive/My Drive/Dev/twitter-floods/data/StormFranklin/tweets-labelled.jsonl'
    places = '/Users/jakegodsall/Google Drive/My Drive/Dev/twitter-floods/data/StormFranklin/places.jsonl'

    loader = Loader(tweets, places)

    tweets_df, places_df = loader.load_df()

    processor = Processor(tweets_df, places_df)

    print(tweets_df)

    df = processor.extract_features()

    print(df.columns)


if __name__ == "__main__":
    main()