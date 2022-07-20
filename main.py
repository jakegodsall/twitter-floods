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


class DataFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # data frame elements
        self.data_label = ttk.Label(self, text="Add Data:")

        self.labelled_tweets_label = ttk.Label(self, text="Labelled-Tweets: ")
        self.labelled_tweets_button = ttk.Button(self, text="Browse")

        self.places_label = ttk.Label(self, text="Places: ")
        self.places_button = ttk.Button(self, text="Browse")

        self.plots_label = ttk.Label(self, text="Plots Path: ")
        self.plots_button = ttk.Button(self, text="Browse")

        self.submit_button = ttk.Button(self, text="Submit")

        # data frame layout
        self.data_label.grid(row=0, column=0, columnspan=2)
        self.labelled_tweets_label.grid(row=1, column=0)
        self.labelled_tweets_button.grid(row=1, column=1)
        self.places_label.grid(row=2, column=0)
        self.places_button.grid(row=2, column=1)
        self.plots_label.grid(row=3, column=0)
        self.plots_button.grid(row=3, column=1)
        self.submit_button.grid(row=4, column=0, columnspan=2)


class MetaFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # meta frame components
        self.meta_label = ttk.Label(self, text="Tweet Metadata")
        self.meta_textbox = ttk.Entry(self)

        # meta frame layout
        self.meta_label.grid(row=0, column=0)
        self.meta_textbox.grid(row=1, column=0)

class SaveFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # save frame components
        self.plot_button = ttk.Button(self, text="Plot")
        self.save_button = ttk.Button(self, text="Save")

        # save frame layout
        self.plot_button.grid(row=0, column=0)
        self.save_button.grid(row=1, column=0)

class OptionsFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # options frame components
        self.data_frame = DataFrame(self)
        self.meta_frame = MetaFrame(self)
        self.save_frame = SaveFrame(self)

        # options frame layout
        self.data_frame.grid(row=0, column=0)
        self.meta_frame.grid(row=1, column=0)
        self.save_frame.grid(row=2, column=0)

class MainWindow:
    def __init__(self, main):
        self.main = main
        self.main.title("Twitter Floods")
        # frames and components
        self.options_frame = OptionsFrame(self.main)
        self.plot_frame = tk.Frame(self.main, bg="green")

        # main layout
        self.options_frame.grid(row=0, column=0)
        self.plot_frame.grid(row=0, column=1)




def main():
    root = tk.Tk()
    root.geometry("800x600")
    root.resizable(False, False)
    MainWindow(root)
    root.mainloop()


if __name__ == '__main__':
    main()
