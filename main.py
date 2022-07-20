# from twitter_utils.twitter_utils import *
#
# def main():
#     tweets = 'data/StormFranklin/tweets-labelled.jsonl'
#     places = 'data/StormFranklin/places.jsonl'
#     save_dir = 'plots'
#
#     loader = Loader(tweets, places)
#
#     tweets_df, places_df = loader.load_df()
#
#     processor = Processor(tweets_df, places_df)
#
#     df = processor.extract_features()
#
#     print(df.columns)
#     #
#     # by_date = processor.create_temporal()
#     #
#     # print(by_date.keys())
#     #
#     # splot = StaticPlotter()
#     #
#     # basemap_plots = splot.plot_basemap(df)
#     # freq_plot = splot.plot_frequency(by_date)
#     #
#     # print(basemap_plots)
#     #
#     # tplot = TemporalPlotter()
#     #
#     # basemaps = tplot.temporal_plotter(by_date)
#     # basemaps = tplot.change_structure(basemaps)
#     #
#     #
#     # static_saver = StaticSaver(save_dir, 'franklin')
#     # temporal_saver = TemporalSaver(save_dir, 'franklin')
#     # #
#     # static_saver.create_event_directory()
#     # static_saver.save_plots(basemap_plots)
#     # static_saver.save_plots(freq_plot)
#
#     # temporal_saver.create_event_directory()
#     # temporal_saver.save_all_plots(basemaps)
#
#     meta = MetaData()
#     meta_json = meta.generate_json(tweets_df, places_df)
#
#     meta_saver = MetaSaver(save_dir, 'franklin')
#     meta_saver.create_event_directory()
#
#     meta_saver.save_meta(meta_json)
#
# if __name__ == "__main__":
#     main()

import tkinter as tk
from tkinter import ttk


class MainWindow:
    def __init__(self, main):
        self.main = main
        self.main.title("Twitter Floods")
        # frames and components
        self.options_frame = tk.Frame(self.main, bg="red")

        self.data_frame = tk.Frame(self.options_frame)

        self.data_label = ttk.Label(self.data_frame, text="Add Data:")

        self.labelled_tweets_label = ttk.Label(self.data_frame, text="Labelled-Tweets: ")
        self.labelled_tweets_button = ttk.Button(self.data_frame, text="Browse")

        self.places_label = ttk.Label(self.data_frame, text="Places: ")
        self.places_button = ttk.Button(self.data_frame, text="Browse")

        self.plots_label = ttk.Label(self.data_frame, text="Plots Path: ")
        self.plots_button = ttk.Button(self.data_frame, text="Browse")

        self.submit_button = ttk.Button(self.data_frame, text="Submit")

        self.meta_frame = tk.Frame(self.options_frame)
        self.save_frame = tk.Frame(self.options_frame)

        self.plot_frame = tk.Frame(self.main, bg="green")

        # main layout
        self.options_frame.grid(row=0, column=0)
        self.plot_frame.grid(row=0, column=1)

        # options layout
        self.data_frame.grid(row=0, column=0)
        self.meta_frame.grid(row=1, column=0)
        self.save_frame.grid(row=2, column=0)

        # data frame layout
        self.data_label.grid(row=0, column=0, columnspan=2)
        self.labelled_tweets_label.grid(row=1, column=0)
        self.labelled_tweets_button.grid(row=1, column=1)
        self.places_label.grid(row=2, column=0)
        self.places_button.grid(row=2, column=1)
        self.plots_label.grid(row=3, column=0)
        self.plots_button.grid(row=3, column=1)
        self.submit_button.grid(row=4, column=0, columnspan=2)

def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
