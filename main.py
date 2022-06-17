from twitter_utils.twitter_utils import Loader, Processor, StaticPlotter, TemporalPlotter, Saver


def main():
    tweets = '/Users/jakegodsall/Google Drive/My Drive/Dev/twitter-floods/data/StormFranklin/tweets-labelled.jsonl'
    places = '/Users/jakegodsall/Google Drive/My Drive/Dev/twitter-floods/data/StormFranklin/places.jsonl'

    loader = Loader(tweets, places)

    tweets_df, places_df = loader.load_df()

    processor = Processor(tweets_df, places_df)

    print(tweets_df)

    df = processor.extract_features()

    print(df.columns)

    by_date = processor.create_temporal()

    print(by_date.keys())

    splot = StaticPlotter()

    # basemap_plots = splot.plot_basemap()
    #
    # print(basemap_plots)

    tplot = TemporalPlotter()

    basemaps = tplot.temporal_plotter(by_date)
    basemaps = tplot.change_structure(basemaps)
    print(basemaps.keys())

    saver = Saver('/Users/jakegodsall/Google Drive/My Drive/Dev/twitter-floods/plots')

    saver.create_event_directory('franklin')

    saver.save_all_plots(basemaps)


if __name__ == "__main__":
    main()