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

# gui
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

# plotting
import numpy as np
import matplotlib as mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class DataFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # paths
        self.data_loaded = False
        self.tweets_dir = None
        self.places_dir = None
        self.plots_dir = None

        # data frame elements
        self.data_label = ttk.Label(self, text="Add Data:")

        self.labelled_tweets_label = ttk.Label(self, text="Labelled-Tweets: ")
        self.labelled_tweets_button = ttk.Button(self, text="Browse", command=self.get_labelled_tweets_dir)

        self.places_label = ttk.Label(self, text="Places: ")
        self.places_button = ttk.Button(self, text="Browse", command=self.get_places_dir)

        self.plots_label = ttk.Label(self, text="Plots Path: ")
        self.plots_button = ttk.Button(self, text="Browse", command=self.get_plots_dir)

        self.submit_button = ttk.Button(self, text="Submit", command=self.submit)

        self.confirmation_label = ttk.Label(self, text="")

        # data frame layout
        self.data_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.labelled_tweets_label.grid(row=1, column=0)
        self.labelled_tweets_button.grid(row=1, column=1)
        self.places_label.grid(row=2, column=0)
        self.places_button.grid(row=2, column=1)
        self.plots_label.grid(row=3, column=0)
        self.plots_button.grid(row=3, column=1)
        self.submit_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.confirmation_label.grid(row=5, column=0, columnspan=2)

    def get_labelled_tweets_dir(self):
        tweets_dir = filedialog.askopenfilename(initialdir="data/StormFranklin")
        self.tweets_dir = tweets_dir

    def get_places_dir(self):
        places_dir = filedialog.askopenfilename(initialdir="data/StormFranklin")
        self.places_dir = places_dir

    def get_plots_dir(self):
        plots_dir = filedialog.askdirectory(initialdir="/plots")
        self.plots_dir = plots_dir

    def submit(self):
        dirs = [self.tweets_dir, self.places_dir, self.plots_dir]
        if all(i is not None for i in dirs):
            self.confirmation_label["text"] = "Files Added"
            self.data_loaded = True
            self.master.meta_frame.show_meta()
        else:
            self.confirmation_label["text"] = "Files Missing"
            return False


class MetaFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)

        # meta text content
        self.meta_content = tk.StringVar()

        # meta frame components
        self.meta_label = ttk.Label(self, text="Tweet Metadata")
        self.meta_textbox = ttk.Label(self, textvariable=self.meta_content)
        self.meta_textbox.config(state='disabled')

        # meta frame layout
        self.meta_label.grid(row=0, column=0)
        self.meta_textbox.grid(row=1, column=0)

    def show_meta(self):
        if self.master.data_frame.data_loaded:
            self.meta_content.set("TESTING")


class SaveFrame(ttk.Frame):
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # save frame components
        self.plot_button = ttk.Button(self, text="Plot", command=self.plot)
        self.save_button = ttk.Button(self, text="Save")

        # save frame layout
        self.plot_button.grid(row=0, column=0)
        self.save_button.grid(row=0, column=1)

    def plot(self):
        self.master.master.plot_frame.plot()


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

    def plot(self):
        fig = Figure(figsize=(5, 4))
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=30, pady=30)


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


def main_loop():
    root = MainWindow()

    tweets_dir = None
    places_dir = None
    plots_dir = None

    def get_tweets_dir():
        return root.options_frame.data_frame.tweets_dir

    def get_places_dir():
        return root.options_frame.data_frame.places_dir

    def get_plots_dir():
        return root.options_frame.data_frame.plots_dir

    if root.options_frame.data_frame.data_loaded:
        tweets_dir = get_tweets_dir()
        places_dir = get_places_dir()
        plots_dir = get_plots_dir()

    print(tweets_dir)

    root.mainloop()


if __name__ == '__main__':
    main_loop()
