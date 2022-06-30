from pathlib import Path

import numpy as np
import pandas as pd
import datetime
import json

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

from textwrap import dedent

class Loader:
    """
        Used to load data from the Tweet object and the Places object
        from the Twitter API.

        Inputs:
            tweet_dir (str) - absolute or relative path to the tweets_labelled.jsonl file
            places_dir (str) - absolute or relative path to the places.jsonl file
    """
    def __init__(self, tweet_dir, places_dir):
        """Creates a number of useful Path objects for the class"""
        self.root_dir = Path("./")
        self.tweet_dir = Path(tweet_dir)
        self.places_dir = Path(places_dir)

    def load_df(self):
        """
            Read the files into pandas data frames.

            Inputs:
                None
            Outputs:
                tweet_df (pandas.DataFrame)
                places_df (pandas.DataFrame)
        """
        tweet_df = pd.read_json(self.tweet_dir, lines=True)
        places_df = pd.read_json(self.places_dir, lines=True)

        return tweet_df, places_df


class Processor:
    """
        Processes the data frame objects to extract useful
        features and create new features for samples without
        exact coordinate data.
    """
    def __init__(self, tweets_df, places_df):
        """
            Inputs:
                tweets_df (pandas.DataFrame)
                places_df (pandas.DataFrame)
        """
        self.tweets_df = tweets_df
        self.places_df = places_df

    def filter_geo(self):
        """
            Filter rows of the tweets_df dataframe
            for those with any kind of geospatial information.
        """
        self.tweets_df = self.tweets_df[self.tweets_df.geo.notnull()]

    def extract_coords(self):
        """
            Extract the coordinates from the geo feature.
        """
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
        # rename new features from dictionary to gt for ground truth
        lonlat.columns = ['gt_longitude', 'gt_latitude']
        # concatenate the new df to the original df
        self.tweets_df = pd.concat([self.tweets_df, lonlat], axis=1)

    def get_centre(self, row):
        """
            Calculates and returns the central coordinate for the bounding
            box

            Inputs:
                row of the dataframe

            Returns:
                central coordinates (list)

        """
        return [(row[0] + row[2]) / 2, (row[1] + row[3]) / 2]

    def extract_bbox(self):
        """
            Extracts the bounding box from the places_df data frame and
            concatenates the value to the tweets_df data frame.
        """
        places_df = self.places_df[['id', 'geo']]
        places_df = pd.concat([places_df, places_df.geo.apply(lambda s: pd.Series(s))['bbox']], axis=1)
        places_df = places_df.drop('geo', axis=1)
        self.tweets_df = pd.merge(self.tweets_df, places_df,
                                  left_on='place_id',
                                  right_on='id')
        self.tweets_df['bbox_centre'] = self.tweets_df.bbox.apply(self.get_centre)
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
            Adds a counts feature which represents the number of times samples
            are found with the same coordinate (from taking the centre of the bounding box)
        """
        self.tweets_df['counts'] = self.tweets_df.groupby('longitude_to_use')['longitude_to_use'].transform('count')

    def extract_features(self):
        """
            Groups the Processor methods and returns a tweets_df dataframe
            consisting of only those features which are used for geospatial
            analysis.

            Returns:
                    tweets_df (pandas.DataFrame)
        """
        self.filter_geo()
        self.extract_coords()
        self.extract_bbox()
        self.determine_coords_to_use()
        self.add_coordinate_counts()

        return self.tweets_df.loc[:, ['created_at', 'label',
                                      'longitude_to_use',
                                      'latitude_to_use',
                                      'has_coords',
                                      'counts']]

    def create_temporal(self):
        """
            Creates a dictionary of pandas.DataFrame's of the form
                dy_by_date[date] = dataframe of samples where created_at == date

            Returns:
                df_by_date (dictionary)
        """

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
    """
        Abstract base class for plotting.
    """
    def __init__(self,
                 figsize=(8, 8),
                 land_color='#00883D',
                 ocean_color='#23C7CD',
                 coastline_color='#012C00',
                 country_color='white'):
        """
            All parameters for styling basemap plots
        """
        self.figsize = figsize
        self.land_color = land_color
        self.ocean_color = ocean_color
        self.coastline_color = coastline_color
        self.country_color = country_color



    def plot_basemap(self, df, region='UK', size=5):
        """
            Creates a basemap plot for a given Processor data frame.

            Inputs:
                df (pandas.DataFrame)
                region (str) either 'UK' or 'Australia' for determining
                    bounding box of the plot

            Returns:
                plots (dictionary) - a dictionary of basemap plots
        """
        # creating a list of options for plots
        density = ["normal", "density"]

        # creating a dictionary for storing plots
        plots = {}

        # iterating through options
        for option in density:
            fig, ax = plt.subplots(figsize=self.figsize)

            bbox = [0, 0, 0, 0]
            if region == 'UK':
                loc = 'upper right'
                bbox = [-10.5, 49.5, 3.5, 59.5, 4.36, 54.7]
            elif region == 'Australia':
                loc = 'lower left'
                bbox = [100.338953078, -43.6345972634, 153.569469029, -2.6681857235, 133.8807, -26.6980]

            m = Basemap(llcrnrlon=bbox[0], llcrnrlat=bbox[1], urcrnrlon=bbox[2], urcrnrlat=bbox[3],
                        resolution='i', projection='tmerc', lon_0=bbox[4], lat_0=bbox[5], ax=ax)
            m.drawlsmask(land_color=self.land_color, ocean_color=self.ocean_color, lakes=True)
            m.drawcoastlines(color=self.coastline_color)
            m.drawcountries(color=self.country_color)

            s = [size, size]

            if option == 'density':
                s = [2 * df.counts * size]

            colours = df.label.astype('category').cat.codes
            scatter = m.scatter(df.longitude_to_use, df.latitude_to_use,
                                latlon=True, alpha=1, s=s[0], c=colours)

            plt.legend(handles=scatter.legend_elements()[0], title='Sentiment', labels=['Negative', 'Positive'])

            plots[f'{option}'] = fig

        return plots


class StaticPlotter(Plotter):
    """
        Plotter class for plotting the static plot,
        that is, where all points are plotted regardless of date.
    """
    def __init__(self,
                 figsize=(8, 8),
                 land_color='#00883D',
                 ocean_color='#23C7CD',
                 coastline_color='#012C00',
                 country_color='white'):
        super().__init__(figsize, land_color, ocean_color,
                         coastline_color, country_color)

    def show_options(self):
        ...

    def plot_frequency(self, df_by_day):
        freq_by_date = {date: df.shape[0] for date, df in df_by_day.items()}
        fig, ax = plt.subplots(figsize=(4, 4))
        ax.plot(freq_by_date.keys(), freq_by_date.values())
        ax.set_xlabel("Date")
        dates = [l.set_visible(False) for (i, l) in enumerate(ax.xaxis.get_ticklabels()) if i % 2 != 0]
        ax.set_xticklabels(freq_by_date.keys(), rotation=45)
        ax.set_ylabel("Number of tweets")

        return {"freq_plot": fig}


class TemporalPlotter(Plotter):
    def __init__(self,
                 figsize=(8, 8),
                 land_color='#00883D',
                 ocean_color='#23C7CD',
                 coastline_color='#012C00',
                 country_color='white'):
        super().__init__(figsize, land_color, ocean_color,
                         coastline_color, country_color)

    def temporal_plotter(self, df_by_day):
        temporal_basemaps = {}
        for k, v in df_by_day.items():
            if v.shape[0] > 0:
                temporal_basemaps[k] = self.plot_basemap(v)
        return temporal_basemaps

    def change_structure(self, plots_by_day):
        k = list(plots_by_day.values())[0].keys()
        return {inner: {outer: plots_by_day[outer][inner] for outer in plots_by_day} for inner in k}


class MetaData:
    def __init__(self, tweets_df, places_df):
        extracted_df = Processor(tweets_df, places_df).extract_features()

        self.total_tweets = tweets_df.shape[0]
        self.total_tweets_with_geo = extracted_df.shape[0]
        self.total_tweets_precise_geo = extracted_df[extracted_df.has_coords].shape[0]
        self.positive_with_geo = extracted_df[extracted_df.label == 'positive'].shape[0]
        self.negative_with_geo = extracted_df[extracted_df.label == 'negative'].shape[0]

    def generate_json(self):
        meta = {
            "Total tweets": self.total_tweets,
            "Total tweets with geo": self.total_tweets_with_geo,
            "Total tweets with precise geo": self.total_tweets_precise_geo,
            "Positive tweets with geo": self.positive_with_geo,
            "Negative tweets with geo": self.negative_with_geo,
        }

        return meta

    def generate_for_gui(self):
        return dedent(f"""Total tweets: {self.total_tweets}
        Number of tweets with geo-info: {self.total_tweets_with_geo}
        Number of tweets with precise geo-info: {self.total_tweets_precise_geo}
        Number of positive tweets (geo): {self.positive_with_geo}
        Number of negative tweets (geo): {self.negative_with_geo}""")

class Saver:
    def __init__(self, plots_dir, event_name):
        self.plots_dir = Path(plots_dir)
        self.event_name = event_name
        self.event_dir = None

    def create_event_directory(self):
        (self.plots_dir / self.event_name).mkdir(exist_ok=True)
        self.event_dir = self.plots_dir / self.event_name
        print(self.event_dir)


class StaticSaver(Saver):
    def __init__(self, plots_dir, event_name):
        super().__init__(plots_dir, event_name)

    def save_plots(self, plots):
        for plot_type, plot in plots.items():
            (self.event_dir / plot_type).mkdir(exist_ok=True)
            new_dir = self.event_dir / plot_type
            plot.savefig(new_dir / self.event_name, bbox_inches="tight")

class TemporalSaver(Saver):
    def __init__(self, plots_dir, event_name):
        super().__init__(plots_dir, event_name)

    def save_all_plots(self, plots):
        for plot_type, dates in plots.items():
            (self.event_dir / plot_type).mkdir(exist_ok=True)
            new_dir = self.event_dir / plot_type
            for date, plot in dates.items():
                plot.savefig(new_dir / date)


class MetaSaver(Saver):
    def __init__(self, plots_dir, event_name):
        super().__init__(plots_dir, event_name)

    def save_meta(self, meta_json):
        with open(self.event_dir / "meta.json", "w") as json_file:
            json.dump(meta_json, json_file)