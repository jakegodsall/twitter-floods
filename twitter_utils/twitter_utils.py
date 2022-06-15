from pathlib import Path

import numpy as np
import pandas as pd


class Loader:
    def __init__(self, tweet_dir, places_dir):
        """Loads the tweet and places files."""
        self.root_dir = Path("./")
        self.tweet_dir = Path(tweet_dir)
        self.places_dir = Path(places_dir)

    def load_df(self):
        """Read the files into dataframes"""
        tweet_df = pd.read_json(self.tweet_dir, lines=True)
        places_df = pd.read_json(self.places_dir, lines=True)

        return tweet_df, places_df


class Processor:
    def __init__(self, tweets_df, places_df):
        self.tweets_df = tweets_df
        self.places_df = places_df

    def filter_geo(self):
        self.tweets_df = self.tweets_df[self.tweets_df.geo.notnull()]

    def extract_coords(self):
        # extract dictionary in geo feature
        expanded_geo = self.tweets_df.geo.apply(lambda s: pd.Series(s))
        # concatenate the new df to the original df
        self.tweets_df = pd.concat([self.tweets_df, expanded_geo], axis=1)

        # flatten dictionary in coordinates feature
        expanded_coords = self.tweets_df.coordinates.apply(lambda s: pd.Series(s))
        # rename new features from dictionary
        expanded_coords.columns = [0, 'type', 'gt_coordinates']
        # concatenate the new df to the original df
        self.tweets_df = pd.concat([self.tweets_df, expanded_coords], axis=1)

        # flatten longitude and latitude
        lonlat = self.tweets_df.gt_coordinates.apply(lambda s: pd.Series(s))
        # rename new features from dictionary
        lonlat.columns = ['gt_longitude', 'gt_latitude']
        # concatenate the new df to the original df
        self.tweets_df = pd.concat([self.tweets_df, lonlat], axis=1)

    def _get_centre(self, row):
        """
            Calculates and returns the central coordinate for the bounding
            box

            Args:
                param1: row of the dataframe

            Returns:
                central coordinates (list)

        """
        return [(row[0] + row[2]) / 2, (row[1] + row[3]) / 2]

    def extract_bbox(self):
        places_df = self.places_df[['id', 'geo']]
        places_df = pd.concat([places_df, places_df.geo.apply(lambda s: pd.Series(s))['bbox']], axis=1)
        places_df = places_df.drop('geo', axis=1)
        self.tweets_df = pd.merge(self.tweets_df, places_df,
                                  left_on='place_id',
                                  right_on='id')
        self.tweets_df['bbox_centre'] = self.tweets_df.bbox.apply(self._get_centre)
        self.tweets_df['bbox_longitude'] = self.tweets_df.bbox_centre.apply(lambda s: s[0])
        self.tweets_df['bbox_latitude'] = self.tweets_df.bbox_centre.apply(lambda s: s[1])

    def determine_coords_to_use(self):
        """
            Determines which coordinates to use from the original coordinates
            and those generated from the bounding box of the places.jsonl file.

        """
        self.tweets_df['has_coords'] = self.tweets_df.coordinates.notnull()
        self.tweets_df['longitude_to_use'] = np.where(self.tweets_df['has_coords'],
                                                      self.tweets_df['gt_longitude'],
                                                      self.tweets_df['bbox_longitude'])
        self.tweets_df['latitude_to_use'] = np.where(self.tweets_df['has_coords'],
                                                     self.tweets_df['gt_latitude'],
                                                     self.tweets_df['bbox_latitude'])

    def add_coordinate_counts(self):
        """
            FOR INTERNAL USE
            Returns a nx4 dataframe with columns longitude, latitude, label
            and counts for plotting
            Here 'counts' is the number of times those coordinates appear in the sample
            Returns:
                augmented dataframe (pandas.DataFrame)

        """
        self.tweets_df['counts'] = self.tweets_df.groupby('longitude_to_use')['longitude_to_use'].transform('count')

    def extract_features(self):
        self.filter_geo()
        self.extract_coords()
        self.extract_bbox()
        self.determine_coords_to_use()
        self.add_coordinate_counts()

        return self.tweets_df.loc[:, ['created_at', 'label',
                                      'longitude_to_use',
                                      'latitude_to_use',
                                      'counts']]

    def create_temporal(self):
        ...


class StaticPlotter:
    def __init__(self):
        ...

    def show_options(self):
        ...

    def plot_basemap(self):
        ...




