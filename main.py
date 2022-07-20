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
from tkinter import filedialog


class DataFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # data frame elements
        self.data_label = ttk.Label(self, text="Add Data:")

        self.labelled_tweets_label = ttk.Label(self, text="Labelled-Tweets: ")
        self.labelled_tweets_button = ttk.Button(self, text="Browse", command=self.load_labelled)

        self.places_label = ttk.Label(self, text="Places: ")
        self.places_button = ttk.Button(self, text="Browse", command=self.load_places)

        self.plots_label = ttk.Label(self, text="Plots Path: ")
        self.plots_button = ttk.Button(self, text="Browse", command=self.ask_dir)

        self.submit_button = ttk.Button(self, text="Submit")

        # data frame layout
        self.data_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.labelled_tweets_label.grid(row=1, column=0)
        self.labelled_tweets_button.grid(row=1, column=1)
        self.places_label.grid(row=2, column=0)
        self.places_button.grid(row=2, column=1)
        self.plots_label.grid(row=3, column=0)
        self.plots_button.grid(row=3, column=1)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def load_labelled(self):
        global tweet_dir
        tweet_dir = filedialog.askopenfilename(initialdir="/home/jake/Documents/twitter-floods-root/twitter-floods/data/StormFranklin")

    def load_places(self):
        ...

    def ask_dir(self):
        ...


class MetaFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
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
        self.save_button.grid(row=0, column=1)


class OptionsFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # options frame components
        self.data_frame = DataFrame(self)
        self.horiz1 = ttk.Separator(self, orient="horizontal")
        self.meta_frame = MetaFrame(self)
        self.horiz2 = ttk.Separator(self, orient="horizontal")
        self.save_frame = SaveFrame(self)

        # options frame layout
        self.data_frame.grid(row=0, column=0)
        self.horiz1.grid(row=1, column=0, sticky="ew", pady=30)
        self.meta_frame.grid(row=2, column=0)
        self.horiz2.grid(row=3, column=0, sticky="ew", pady=30)
        self.save_frame.grid(row=4, column=0, sticky="s")


class PlotFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Twitter Floods")
        self.geometry("800x600")
        self.resizable(False, False)

        # configuration
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=2)

        # main frames
        self.options_frame = OptionsFrame(self, width=400, height=600, borderwidth=1)
        self.vert = ttk.Separator(self, orient="vertical")
        self.plot_frame = PlotFrame(self, width=400, height=600, borderwidth=1)
        # main layout

        self.options_frame.grid(row=0, column=0)
        self.vert.grid(row=0, column=1, sticky="ns")
        self.plot_frame.grid(row=0, column=2)

def main():
    root = MainWindow()

    tweets_dir = tk.StringVar()
    places_dir = tk.StringVar()
    save_dir = tk.StringVar()

    print(tweet_dir)

    root.mainloop()


if __name__ == '__main__':
    main()
