# Geotagged Tweets Basemap Plotter

A simple GUI application which generates meta-data and basemap plots for tweets queried via the Twitter API.

The application will save the following files to the specified directory

- A time-series plot showing the frequency of tweets within the range of dates of tweets published.
- Basemap plots for the entire period of a tweet data set, as well as individual plots by day (excluding days where no tweets exist)
- A JSON file of the meta-data displayed within the GUI.

## Graphical User Interface
<img src="finished_gui.png" alt="GUI image">
<br>

## Usage Instructions

### Running the application

The project can be cloned directly from this repository. 

To run the project, one should first install all required packages from the provided `requirements.txt` file.

```commandline
    pip install -r requirements.txt
```

Then, run `python main.py` from within the project directory.

### How to use

__Note:__ The application requires a labelled-tweets and places dataset, which at present must be formatted as JSON lines `.jsonl`.

1. Load in the data sets as well as the save location for plots and press the _Submit_ button to generate meta-data. 
2. Press the _Plot_ button to generate all plots and display a plot within the GUI.
3. Press the _Save_ button to save all plots to the specified directory.

## License

This project is licensed under the terms of the `GNU GPL` license. See [LICENSE](https://github.com/jakegodsall/twitter-floods/blob/main/LICENSE.md) for more details.

## TODOs

This is a work in progress and there are a number of tasks to be completed that will make it more generally applicable to the Twitter API.

- Allow for basemaps to be generated anywhere in the world from tweet location, without hard-coding bounding boxes for specific events.
- Allowing for only specific plots to be saved to disk according to user-defined options.