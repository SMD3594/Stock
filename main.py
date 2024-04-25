import requests
import tkinter as ttk
import json
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)


class Variables:
    api = "https://api.twelvedata.com/time_series?apikey=06ca6c5f49b1426091c20825d922e503&format=JSON"
    ticker = "&symbol="
    interval = "&interval="
    stock = "&stock="
    grain = "&dp="
    size = "&outputsize="
    open = {}
    close = {}
    high = {}
    low = {}
    date_time = {}


def plot():
    for k, v in Variables.close.items():
        Variables.close[k] = float(v)

    for k, v in Variables.open.items():
        Variables.open[k] = float(v)

    for k, v in Variables.high.items():
        Variables.high[k] = float(v)

    for k, v in Variables.low.items():
        Variables.low[k] = float(v)

    lists_date_time_reversed = dict(reversed(list(Variables.date_time.items())))
    lists_date_time = lists_date_time_reversed.values()
    lists_close_reverse = dict(reversed(list(Variables.close.items())))
    lists_close = lists_close_reverse.values()
    lists_open_reverse = dict(reversed(list(Variables.open.items())))
    lists_open = lists_open_reverse.values()
    lists_high_reverse = dict(reversed(list(Variables.high.items())))
    lists_high = lists_high_reverse.values()
    lists_low_reverse = dict(reversed(list(Variables.low.items())))
    lists_low = lists_low_reverse.values()

    # the figure that will contain the plot
    fig = Figure(figsize=(10, 6), dpi=150)
    # adding the subplot
    plot1 = fig.add_subplot()
    fig.autofmt_xdate(rotation=45)
    # plotting the graph
    plot1.plot(lists_date_time, lists_close, color='black')

    # creating the Tkinter canvas containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=mainframe)

    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().pack(side=ttk.BOTTOM)
    # creating the Matplotlib toolbar
    toolbar = NavigationToolbar2Tk(canvas, mainframe)
    toolbar.update()
    plot1.set_title(t.get().upper())

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().pack(side=ttk.BOTTOM)


def calculate(event):
    try:
        response = requests.get(
            Variables.api + Variables.ticker + t.get() + Variables.interval +
            drop_interval.get() + Variables.grain + drop_grain.get() +
            Variables.size + "10")
        x = json.loads(response.text)
        print(x)
        num_open = 0
        num_high = 0
        num_low = 0
        num_close = 0
        num_datetime = 0
        for close_val in x['values']:
            output.set(close_val['close'])
            Variables.close[num_close] = close_val['close']
            num_close += 1

        for open_val in x['values']:
            Variables.open[num_open] = open_val['open']
            num_open += 1

        for high_val in x['values']:
            Variables.high[num_high] = high_val['high']
            num_high += 1

        for low_val in x['values']:
            Variables.low[num_low] = low_val['low']
            num_low += 1

        for time in x['values']:
            Variables.date_time[num_datetime] = time['datetime']
            num_datetime += 1

        print("OPEN: ", Variables.open)
        print("HIGH: ", Variables.high)
        print("LOW: ", Variables.low)
        print("CLOSE: ", Variables.close)
        print("Datetime: ", Variables.date_time)
        plot()

    except ValueError:
        pass


root = ttk.Tk()
root.title("Price Checker")

mainframe = ttk.Frame(root)
mainframe.pack(fill=ttk.BOTH, expand=ttk.TRUE)

ticker_label = ttk.Label(mainframe, text="Ticker:", font=('Gothic', 14))
ticker_label.pack(side=ttk.TOP)


t = ttk.StringVar()
t_entry = ttk.Entry(mainframe, width=7, textvariable=t, font=('Gothic', 14))
t_entry.pack(side=ttk.TOP)

interval_options = [
    "1min",
    "5min",
    "15min",
    "30min",
    "45min",
    "1h",
    "2h",
    "4h",
    "1day",
    "1week",
    "1month"
]

drop_interval = ttk.StringVar()

drop_interval.set("1min")

drop = ttk.OptionMenu(root, drop_interval, *interval_options)
drop.pack(side=ttk.TOP)

grain_options = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11"
]

drop_grain = ttk.StringVar()
drop_grain.set("2")
drop_g = ttk.OptionMenu(root, drop_grain, *grain_options)
drop_g.pack(side=ttk.TOP)

price_label = ttk.Label(mainframe, text="Price:", font=('Gothic', 14))
price_label.pack(side=ttk.TOP)

output = ttk.StringVar()
output_label = ttk.Label(mainframe, textvariable=output, font=('Gothic', 14, 'bold'))
output_label.pack(side=ttk.TOP)

fetch_button = ttk.Button(master=mainframe, height=2, width=10, text="Fetch")
fetch_button.bind('<Button-1>', calculate)
fetch_button.pack(side=ttk.TOP)

root.bind('<Return>', calculate)

t_entry.focus()

root.mainloop()
