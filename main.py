import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from twitter_utils.twitter_utils import *


class DataFrame(ttk.Frame):
    """
        This frame represents the first row of the first column of the GUI.
        The purpose of this frame is to allow the user to set the variables
        for labelled tweets file, places file and plots directory.
    """
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)
        # paths
        self.data_loaded = False  # Boolean of whether the data has been loaded
        self.tweets_dir = None  # store the tweets directory as a string
        self.places_dir = None  # store the places directory as a string
        self.plots_dir = None  # store the plots directory as a string
        self.dirs = tk.StringVar()

        # components
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
        """
            Return the tweets path from the filedialog to the instance variable.
        """
        tweets_dir = filedialog.askopenfilename(initialdir="data/StormFranklin")
        self.tweets_dir = tweets_dir

    def get_places_dir(self):
        """
            Return the places path from the filedialog to the instance variable.
        """
        places_dir = filedialog.askopenfilename(initialdir="data/StormFranklin")
        self.places_dir = places_dir

    def get_plots_dir(self):
        """
            Return the plots directory from the filedialog to the instance variable.
        """
        plots_dir = filedialog.askdirectory(initialdir="/plots")
        self.plots_dir = plots_dir
        print(self.plots_dir)

    def submit(self):
        """
            Submit the directories to store in the instance variables.
            Includes some basic validation.
        """
        dirs = [self.tweets_dir, self.places_dir, self.plots_dir]
        if all(i is not None for i in dirs):
            self.confirmation_label["text"] = "Files Added"
            self.data_loaded = True
            self.master.meta_frame.show_meta()
        else:
            self.confirmation_label["text"] = "Files Missing"


class MetaFrame(ttk.Frame):
    """
        This frame represents the second row of the first column of the GUI.
        The purpose of this frame is to show the meta data of the dataset provided.
    """
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
        """
            Show the meta data in the meta textbox.
        """
        tweets = self.master.data_frame.tweets_dir
        places = self.master.data_frame.places_dir

        loader = Loader(tweets, places)
        tweets_df, places_df = loader.load_df()
        meta = MetaData(tweets_df, places_df)

        meta_data = meta.generate_for_gui()

        self.meta_content.set(meta_data)


class SaveFrame(ttk.Frame):
    """
        This frame represents the final row of the first column of the GUI.
        The purpose of this frame is provide an interface by which the user can
        make a plot to be visualised within the GUI, as well as save the plots
        generated.
    """
    def __init__(self, main, *args, **kwargs):
        # super the ttk.Frame object
        super().__init__(main, *args, **kwargs)

        self.event_name = None # event name of directory creation
        self.static_plots = None  # dictionary of static plots
        self.freq_plot = None  # variable of frequency plot
        self.temporal_plots = None  # dictionary of temporal plots
        self.meta_json = None  # variable for meta data JSON


        # save frame components
        self.plot_button = ttk.Button(self, text="Plot", command=self.plot)
        self.save_button = ttk.Button(self, text="Save", command=self.save)

        # save frame layout
        self.plot_button.grid(row=0, column=0)
        self.save_button.grid(row=0, column=1)

    def generate_plots(self):
        """
            Generates all plots (static and temporal)
            for the data set provided. Also generates meta
            data.
        """
        # get the dataset files
        tweets = self.master.data_frame.tweets_dir
        places = self.master.data_frame.places_dir

        # get the event name to create a directory for the event
        self.event_name = tweets.split("/")[-2]

        # load the datasets using Loader to get pandas.DataFrame objects
        loader = Loader(tweets, places)
        tweets_df, places_df = loader.load_df()

        # process the dataframes using Processor
        processor = Processor(tweets_df, places_df)
        df = processor.extract_features()
        by_date = processor.create_temporal()

        # plot the static plots using StaticPlotter and store in self.static_plots
        splot = StaticPlotter()
        self.static_plots = splot.plot_basemap(df)
        # plot the frequency plot using StaticPlotter and store in self.freq_plot
        self.freq_plot = splot.plot_frequency(by_date)

        # plot the temporal plots using TemporalPlotter and store in self.temporal_plots
        tplot = TemporalPlotter()
        self.temporal_plots = tplot.temporal_plotter(by_date)
        self.temporal_plots = tplot.change_structure(self.temporal_plots)

        # get the meta data using MetaData and store in self.meta_json
        meta = MetaData(tweets_df, places_df)
        self.meta_json = meta.generate_json()

    def plot(self):
        """
            Plot the static plot generated by self.generate_plots()
            on the TkCanvas in the PlotFrame.
        """
        self.generate_plots()
        self.master.master.plot_frame.plot()

    def save(self):
        """
            Saves the static plots, temporal plots and meta data to disk.
        """
        # get the save directory
        save_dir = self.master.data_frame.plots_dir

        # save the static plots
        static_saver = StaticSaver(save_dir, self.event_name)
        static_saver.create_event_directory()
        static_saver.save_plots(self.static_plots)
        static_saver.save_plots(self.freq_plot)

        # save the temporal plots
        temporal_saver = TemporalSaver(save_dir, self.event_name)
        temporal_saver.create_event_directory()
        temporal_saver.save_all_plots(self.temporal_plots)

        # save the meta data
        meta_saver = MetaSaver(save_dir, 'franklin')
        meta_saver.create_event_directory()
        meta_saver.save_meta(self.meta_json)


class OptionsFrame(ttk.Frame):
    """
        This is the first column of the GUI, which
        includes the DataFrame, the MetaFrame and the SaveFrame.
    """
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
    """
        This is the second column of the GUI where the plot will
        be displayed.
    """
    def __init__(self, main, *args, **kwargs):
        super().__init__(main, *args, **kwargs)

    def plot(self):
        """
            Render the plot generated earlier to the Tk Canvas.
        """
        fig = self.master.options_frame.save_frame.static_plots['density']

        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, padx=30, pady=30)


class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Twitter Floods")
        self.geometry("1200x600")

        # configuration
        self.columnconfigure(index=0, weight=2)
        self.columnconfigure(index=2, weight=3)

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
    root.mainloop()


if __name__ == '__main__':
    main_loop()
