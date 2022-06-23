from pathlib import Path

import numpy as np
import pandas as pd
import datetime

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


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

        df = self.tweets_df.copy(deep=True)

        end_date = df.created_at.max()
        start_date = df.created_at.min()

        days = [(start_date.date() + datetime.timedelta(day)).isoformat()
                for day in range((end_date.date() - start_date.date()).days + 1)]

        df['created_at'] = df['created_at'].apply(lambda date: date.date().isoformat())
        df_by_date = {}

        for day in days:
            df_by_date[day] = df[df.created_at == day]

        return df_by_date

class Plotter():
    def __init__(self):
        ...

    def plot_basemap(self, df, region='UK', size=5):
        # creating a list of options for plots
        density = ["normal", "density"]

        # creating a dictionary for storing plots
        plots = {}

        # iterating through options
        for option in density:

            fig, ax = plt.subplots(figsize=(8, 8))

            bbox = [0, 0, 0, 0]
            if region == 'UK':
                loc = 'upper right'
                bbox = [-10.5, 49.5, 3.5, 59.5, 4.36, 54.7]
            elif region == 'Australia':
                loc = 'lower left'
                bbox = [100.338953078, -43.6345972634, 153.569469029, -2.6681857235, 133.8807, -26.6980]

            m = Basemap(llcrnrlon=bbox[0], llcrnrlat=bbox[1], urcrnrlon=bbox[2], urcrnrlat=bbox[3],
                        resolution='i', projection='tmerc', lon_0=bbox[4], lat_0=bbox[5], ax=ax)
            m.drawlsmask(land_color='#00883D', ocean_color='#23C7CD', lakes=True)
            m.drawcoastlines(color='#012C00')
            m.drawcountries(color='white')

            s = [size, size]

            if option == 'density':
                s = [2 * df.counts * size]

            colours = df.label.astype('category').cat.codes
            scatter = m.scatter(df.longitude_to_use, df.latitude_to_use,
                                latlon=True, alpha=1, s=s[0], c=colours)

            plt.legend(handles=scatter.legend_elements()[0], title='Sentiment', labels=['Negative', 'Positive'])

            plots[f'{option}'] = fig

        return plots

    def change_structure(self, plots_by_day):
        k = list(plots_by_day.values())[0].keys()
        return {inner: {outer: plots_by_day[outer][inner] for outer in plots_by_day} for inner in k}


class StaticPlotter:
    def __init__(self):
        pass

    def show_options(self):
        ...

    def plot_basemap(self, df, region='UK', size=5):

        # creating a list of options for plots
        density = ["normal", "density"]

        # creating a dictionary for storing plots
        plots = {}

        # iterating through options
        for option in density:

            fig, ax = plt.subplots(figsize=(8, 8))

            bbox = [0, 0, 0, 0]
            if region == 'UK':
                loc = 'upper right'
                bbox = [-10.5, 49.5, 3.5, 59.5, 4.36, 54.7]
            elif region == 'Australia':
                loc = 'lower left'
                bbox = [100.338953078, -43.6345972634, 153.569469029, -2.6681857235, 133.8807, -26.6980]

            m = Basemap(llcrnrlon=bbox[0], llcrnrlat=bbox[1], urcrnrlon=bbox[2], urcrnrlat=bbox[3],
                        resolution='i', projection='tmerc', lon_0=bbox[4], lat_0=bbox[5], ax=ax)
            m.drawlsmask(land_color='#00883D', ocean_color='#23C7CD', lakes=True)
            m.drawcoastlines(color='#012C00')
            m.drawcountries(color='white')

            s = [size, size]

            if option == 'density':
                s = [2 * df.counts * size]

            colours = df.label.astype('category').cat.codes
            scatter = m.scatter(df.longitude_to_use, df.latitude_to_use,
                                latlon=True, alpha=1, s=s[0], c=colours)

            plt.legend(handles=scatter.legend_elements()[0], title='Sentiment', labels=['Negative', 'Positive'])

            plots[f'{option}'] = fig

        return plots


class TemporalPlotter(StaticPlotter):
    def __init__(self):
        pass

    def temporal_plotter(self, df_by_day):
        temporal_basemaps = {}
        for k, v in df_by_day.items():
            if v.shape[0] > 0:
                temporal_basemaps[k] = self.plot_basemap(v)
        return temporal_basemaps

    def change_structure(self, plots_by_day):
        k = list(plots_by_day.values())[0].keys()
        return {inner: {outer: plots_by_day[outer][inner] for outer in plots_by_day} for inner in k}


class Saver:
    def __init__(self, plots_dir):
        self.plots_dir = Path(plots_dir)
        self.event_dir = None

    def create_event_directory(self, event_name):
        (self.plots_dir / event_name).mkdir(exist_ok=True)
        self.event_dir = self.plots_dir / event_name
        print(self.event_dir)

    def save_all_plots(self, plots):
        for plot_type, dates in plots.items():
            (self.event_dir / plot_type).mkdir(exist_ok=True)
            new_dir = self.event_dir / plot_type
            for date, plot in dates.items():
                plot.savefig(new_dir / date)