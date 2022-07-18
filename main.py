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

def browse_labelled_tweets():
    filename = filedialog.askopenfilename(initialdir="./data/StormFranklin/",
                                          title="Select file",
                                          filetypes=(("JSON Lines",
                                                     "*.jsonl"),
                                                     ("All files",
                                                      "*.*")))

    just_file = filename.split("/")[-1]
    labelled_tweets_dir_browse["text"] = just_file

def browse_places():
    filename = filedialog.askopenfilename(initialdir="./data/StormFranklin/",
                                          title="Select file",
                                          filetypes=(("JSON Lines",
                                                      "*.jsonl"),
                                                     ("All files",
                                                      "*.*")))

    just_file = filename.split("/")[-1]
    places_dir_browse["text"] = just_file

def browse_plots():
    filename = filedialog.askdirectory(initialdir="./plots",
                                       title="Select directory")

    just_file = filename.split("/")[-1]
    save_dir_browse["text"] = just_file

window = tk.Tk()
window.geometry("1000x600")
window.resizable(False, False)

# Frames for separating columns

options_frame = ttk.Frame(window, padding=(10, 20))
options_frame.grid(row=0, column=0)

main_separator = ttk.Separator(window, orient="horizontal")
main_separator.grid(row=0, column=1)

plot_frame = ttk.Frame(window, padding=(10, 20))
plot_frame.grid(row=0, column=2)

# Filling the option frame

ttk.Label(options_frame, text="Directories: ").grid(row=0, column=0)

# directories frame
dir_frame = ttk.Frame(options_frame, padding=(10, 20))
dir_frame.grid(row=0, column=0)

# labelled tweets
ttk.Label(dir_frame, text="Labelled Tweets: ").grid(row=1, column=0)
labelled_tweets_dir_browse = ttk.Button(dir_frame, command=browse_labelled_tweets)
labelled_tweets_dir_browse.grid(row=1, column=2)

# places
ttk.Label(dir_frame, text="Places: ").grid(row=2, column=0)
places_dir_browse = ttk.Button(dir_frame, command=browse_places)
places_dir_browse.grid(row=2, column=2)

# plots
ttk.Label(dir_frame, text="Save: ").grid(row=3, column=0)
save_dir_browse = ttk.Button(dir_frame, command=browse_plots)
save_dir_browse.grid(row=3, column=2)

ttk.Separator(options_frame, orient="horizontal").grid(row=4, ipadx=200, ipady=10)

### Meta information

meta_frame = ttk.Frame(options_frame)
meta_frame.grid(row=1, column=0)


ttk.Separator(options_frame, orient="horizontal").grid(row=4, ipadx=200, ipady=10)


window.mainloop()
