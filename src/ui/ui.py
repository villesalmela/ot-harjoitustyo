from threading import Thread
from functools import wraps
import tkinter as tk
from tkinter import (
    ttk, filedialog, scrolledtext, PhotoImage,
    messagebox, StringVar, simpledialog, Listbox
)

import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
import matplotlib.dates as mdates

from ui.figure_config import FigureConfig
from utils.utils import check_file


class StorageOverlay:
    def __init__(self, parent, select=False, create=False) -> None:
        self.parent = parent
        self.context = parent.context
        self.overlay = ttk.Frame(parent)
        self.overlay.place(x=1, y=1, relwidth=1, relheight=1)

        self.inner_frame = ttk.Frame(self.overlay)
        self.inner_frame.pack(expand=True)

        self.listbox = Listbox(self.inner_frame, selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)

        self.slot = tk.StringVar()
        self.slots = self.context.list_slots()
        if not self.slots:
            select = False
        self._prepare_listbox()

        if select:
            self.select_button = ttk.Button(
                self.inner_frame,
                text="Select a Slot",
                command=self._on_select,
                state=tk.DISABLED)
            self.select_button.pack(fill=tk.X)

        if create:
            ttk.Button(
                self.inner_frame, text="Create New Slot", command=self._on_new
            ).pack(fill=tk.X)

        ttk.Button(self.inner_frame, text="Cancel", command=self.overlay.destroy).pack(fill=tk.X)

    def _prepare_listbox(self):
        self.listbox.bind('<<ListboxSelect>>', self._on_listbox_select)
        for item in self.slots:
            self.listbox.insert(tk.END, item)

    def _on_select(self):
        selected_slot = self.listbox.get(self.listbox.curselection())
        if selected_slot:
            self.slot.set(selected_slot)
        self.overlay.destroy()

    def _on_new(self):
        if selected_slot := simpledialog.askstring(
                "New Slot", "Enter new slot:", parent=self.inner_frame):
            self.slot.set(selected_slot)
            self.overlay.destroy()

    def _on_listbox_select(self, event):
        if event.widget.curselection():
            self.select_button.config(state=tk.NORMAL, text="Confirm Selection")
        else:
            self.select_button.config(state=tk.DISABLED, text="Select a Slot")

    def ask_slot(self):
        self.overlay.wait_window()
        return self.slot.get()


def with_loading_screen(func):
    "Generated with ChatGPT."

    @wraps(func)
    def wrapper(*args, **kwargs):

        # Function to run in a separate thread
        def run():
            result[0] = func(*args, **kwargs)
            overlay.destroy()

        # Function to stop the thread
        def stop_thread():
            if thread.is_alive():
                # Attempt to join the thread, timing out almost immediately
                thread.join(timeout=0.1)
            overlay.destroy()

        root = args[0]  # Assuming the first argument is always the Tkinter root

        # Create an overlay frame
        overlay = ttk.Frame(root)
        overlay.place(x=1, y=1, relwidth=1, relheight=1)

        # Inner frame to hold widgets
        inner_frame = ttk.Frame(overlay)
        inner_frame.pack(expand=True)

        # Add text
        loading_label = ttk.Label(inner_frame, text="Please wait...")
        loading_label.pack()

        # Button to cancel the operation
        cancel_button = ttk.Button(inner_frame, text="Cancel", command=stop_thread)
        cancel_button.pack()

        # This will store the function's result
        result = [None]

        # Start the thread
        thread = Thread(target=run, daemon=True)
        thread.start()
        overlay.wait_window()

        return result[0]

    return wrapper


class PcapUi(tk.Tk):

    def __init__(self, context, analyze_function):
        super().__init__()
        self.context = context
        self.analyze_function = analyze_function

        self.title('PCAP Analyzer')
        self.geometry('1200x800')
        self.iconphoto(True, PhotoImage(file='assets/icon.png'))

        self.components = {
            "buttons": {},
            "text_areas": {},
            "figures": {},
            "canvases": {},
            "plots": {},
            "indicators": {}
        }

        self.ids = {
            "button": 0,
            "figure": 0,
            "plot": 0,
            "text_area": 0,
            "indicator": 0
        }
        self.map = {}

        self._create_menu()
        self._initialize_ui()

    def _create_menu(self):
        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar, tearoff=0)

        menu_data = [
            ("Add New Capture...", "Ctrl+N", "<Control-n>", self.open_file),
            ("Load Analysis..", "Ctrl+O", "<Control-o>", self.load),
            ("Save Analysis..", "Ctrl+S", "<Control-s>", self.save),
            ("Delete Analysis..", "Ctrl+D", "<Control-d>", self.delete),
            ("Reset", "Ctrl+R", "<Control-r>", self.reset),
            ("Exit", "Ctrl+Q", "<Control-q>", self.close)
        ]

        for item, shortcut_frontend, shortcut_backend, command in menu_data:
            file_menu.add_command(
                label=item, accelerator=shortcut_frontend, command=command)
            self.bind(shortcut_backend, lambda event, cmd=command: cmd())

        menu_bar.add_cascade(label="File", menu=file_menu)

        self.config(menu=menu_bar)

    def _init_buttons(self):
        self.map["button.reset"] = self.create_button(self.frame, "Reset", self.reset, tk.RIGHT)
        self.map["button.load"] = self.create_button(self.frame, "Load", self.load, tk.LEFT)
        self.map["button.save"] = self.create_button(
            self.frame, "Save", self.save, tk.LEFT, state=tk.DISABLED)
        self.map["button.delete"] = self.create_button(self.frame, "Delete", self.delete, tk.LEFT)
        self.map["button.open"] = self.create_button(self.frame, "New Capture", self.open_file, tk.RIGHT)

    def _init_tabs(self):
        # Create the notebook for tabs
        notebook = ttk.Notebook(self)

        # Create frames for tabs
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)
        tab4 = ttk.Frame(notebook)

        # Add tabs to the notebook
        notebook.add(tab1, text='Overview')
        notebook.add(tab2, text='Details')
        notebook.add(tab3, text='DNS')
        notebook.add(tab4, text='DHCP')

        # Pack to make visible
        notebook.pack(expand=True, fill=tk.BOTH)

        return tab1, tab2, tab3, tab4

    def _prepare_tab_1(self, tab1):
        indicators_frame = ttk.Frame(tab1)
        self.map["indicator.packet_count"] = self.create_indicator(
            indicators_frame, 0, "Packet Count", 0, 0)
        self.map["indicator.data_amount"] = self.create_indicator(
            indicators_frame, 0, "Data Amount", 0, 1)
        self.map["indicator.duration"] = self.create_indicator(
            indicators_frame, 0, "Duration", 0, 2)
        self.map["indicator.starttime"] = self.create_indicator(
            indicators_frame, 0, "Start Time", 0, 3)
        self.map["indicator.endtime"] = self.create_indicator(
            indicators_frame, 0, "End Time", 0, 4)
        indicators_frame.pack(expand=True)
        figure_id = self.create_figure_and_canvas(tab1)
        self.map["plot.speed"] = self.create_plot(figure_id, 111, dual=True)

    def _prepare_tab_2(self, tab2):
        self.map["text_area.summary"] = self.create_scrollable_text_area(tab2)

    def _prepare_tab_3(self, tab3):
        figure_id = self.create_figure_and_canvas(tab3)
        self.map["plot.dns_1"] = self.create_plot(figure_id, 211)
        self.map["plot.dns_2"] = self.create_plot(figure_id, 212)

    def _prepare_tab_4(self, tab4):
        figure_id = self.create_figure_and_canvas(tab4)
        self.map["plot.dhcp_1"] = self.create_plot(figure_id, 311)
        self.map["plot.dhcp_2"] = self.create_plot(figure_id, 312)
        self.map["plot.dhcp_3"] = self.create_plot(figure_id, 313)

    def _initialize_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill='x', expand=False)

        self._init_buttons()
        tabs = self._init_tabs()
        preps = [self._prepare_tab_1, self._prepare_tab_2, self._prepare_tab_3, self._prepare_tab_4]
        for tab, prep in zip(tabs, preps):
            prep(tab)

    def create_button(self, container, text, command, side, **kwds):

        # Assigning a unique ID to the button
        button_id = self.ids["button"]
        self.ids["button"] += 1

        # Create the button
        button = ttk.Button(container, text=text, command=command, **kwds)

        # Display the button
        button.pack(padx=10, side=side)

        # Store the button
        self.components["buttons"][button_id] = button
        return button_id

    def create_scrollable_text_area(self, container):

        # Assigning a unique ID to the text area
        text_area_id = self.ids["text_area"]
        self.ids["text_area"] += 1

        # Defining
        text_area = scrolledtext.ScrolledText(container, wrap=tk.WORD)

        # Displaying
        text_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Store the text area
        self.components["text_areas"][text_area_id] = text_area
        return text_area_id

    def create_indicator(self, parent, value, title, row, column):
        "Generated with ChatGPT."

        # Assigning a unique ID to the indicator
        indicator_id = self.ids["indicator"]
        self.ids["indicator"] += 1

        # Create StringVar to hold the value
        value_holder = StringVar(parent, value)

        # Create a new Frame as a child of the specified parent widget
        frame = ttk.Frame(parent, borderwidth=2, relief="groove")

        # Create a Label for the number, large and bold
        number_label = ttk.Label(frame, textvariable=value_holder, font=('Helvetica', 24, 'bold'))
        number_label.pack(pady=(0, 5))  # Add some padding below the number

        # Create a Label for the title, smaller and less prominent
        title_label = ttk.Label(frame, text=title, font=('Helvetica', 14))
        title_label.pack(pady=(5, 0))  # Add some padding above the title

        # Place the frame using the grid layout manager
        frame.grid(row=row, column=column, padx=10, pady=10, sticky='ew')

        # Store the frame
        self.components["indicators"][indicator_id] = value_holder

        return indicator_id

    def create_figure_and_canvas(self, container):

        # Create a figure
        figure = Figure()

        # Assigning a unique ID to the figure
        figure_id = self.ids["figure"]
        self.ids["figure"] += 1

        # Store the figure
        self.components["figures"][figure_id] = figure

        # Create canvas for the figure
        canvas = FigureCanvasTkAgg(figure, container)

        # Display the canvas
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Store the canvas
        self.components["canvases"][figure_id] = canvas

        # Return the ID
        return figure_id

    def create_plot(self, figure_id, position: int, dual=False):

        # Assigning a unique ID to the plot
        plot_id = self.ids["plot"]
        self.ids["plot"] += 1

        # Fetch the parent figure
        figure = self.components["figures"][figure_id]

        # Create the figure
        plot = figure.add_subplot(position)

        # Store the plot and its parent figure
        if dual:
            plot2 = plot.twinx()
            self.components["plots"][plot_id] = (plot, plot2), figure_id
        else:
            self.components["plots"][plot_id] = plot, figure_id

        # Return the ID
        return plot_id

    def open_file(self):

        # Ask the user to select a file
        file_path = filedialog.askopenfilename()

        if file_path:  # file selected
            try:
                check_file(file_path)
            except FileNotFoundError as e:
                messagebox.showerror("Error", str(e))
                return

            self.context.append(file_path)
            self.update()

        else:  # no file selected
            pass

    @with_loading_screen
    def update(self):
        self.reset(keep_context=True)

        details = self.context.df["packet.str"].str.cat(sep="\n")
        result = self.analyze_function(self.context)

        bar_data = {
            "plot.dns_1": result["dns_domains"],
            "plot.dns_2": result["dns_servers"],
            "plot.dhcp_1": result["dhcp_clients"],
            "plot.dhcp_2": result["dhcp_servers"],
            "plot.dhcp_3": result["dhcp_domains"]
        }
        indicators = result["indicators"]
        indicator_data = {
            "indicator.packet_count": indicators["packet_count"],
            "indicator.data_amount": indicators["data_amount"],
            "indicator.duration": indicators["duration"],
            "indicator.starttime": indicators["start_time"],
            "indicator.endtime": indicators["end_time"]
        }

        self.display_text(text_area_id=self.map["text_area.summary"], text=details)
        self.display_timeseries_dual(self.map["plot.speed"], result["speed_config"])
        self._display_bar_graphs(bar_data)
        self._display_indicators(indicator_data)

        if len(self.context) > 0:
            save_button = self.components["buttons"][self.map["button.save"]]
            save_button.config(state=tk.NORMAL)

    def _display_bar_graphs(self, data):
        for name, value in data.items():
            self.display_bar_graph(self.map[name], value)

    def _display_indicators(self, data):
        for name, value in data.items():
            self.display_indicator(self.map[name], value)

    def load(self):
        storage_overlay = StorageOverlay(self, select=True, create=False)
        if name := storage_overlay.ask_slot():
            self.context.load(name)
            self.update()
            messagebox.showinfo("Success", f"Loaded analysis from slot: {name}")

    def save(self):
        storage_overlay = StorageOverlay(self, select=True, create=True)
        if name := storage_overlay.ask_slot():
            self.context.save(name)
            messagebox.showinfo("Success", f"Saved analysis to slot: {name}")

    def delete(self) -> None:
        storage_overlay = StorageOverlay(self, select=True, create=False)
        if name := storage_overlay.ask_slot():
            self.context.del_slot(name)
            messagebox.showinfo("Success", f"Deleted analysis from slot: {name}")

    def display_indicator(self, indicator_id, value):
        self.components["indicators"][indicator_id].set(value)

    def display_text(self, text_area_id, text):

        # Fetch the text area
        text_area = self.components["text_areas"][text_area_id]

        # Make it read-write
        text_area.config(state=tk.NORMAL)

        # Resetting
        text_area.delete('1.0', tk.END)

        # Displaying
        text_area.insert(tk.END, text)

        # Make it read-only
        text_area.config(state=tk.DISABLED)

    def _get_minor_locator(self, duration):
        if duration <= pd.Timedelta(minutes=1):
            minor_locator = mdates.SecondLocator()
        elif duration <= pd.Timedelta(hours=1):
            minor_locator = mdates.MinuteLocator()
        elif duration <= pd.Timedelta(days=1):
            minor_locator = mdates.HourLocator()
        elif duration <= pd.Timedelta(days=30):
            minor_locator = mdates.DayLocator()
        elif duration <= pd.Timedelta(days=365):
            minor_locator = mdates.MonthLocator()
        else:
            minor_locator = mdates.MonthLocator(interval=3)
        return minor_locator

    def _setup_plot_1(self, plot, data1, color1, title, xlabel, y1label):
        plot_color = color1
        plot.set_title(title)
        plot.set_xlabel(xlabel)
        plot_locator = mdates.AutoDateLocator()
        plot_formatter = mdates.ConciseDateFormatter(plot_locator)
        plot.xaxis.set_major_locator(plot_locator)
        plot.xaxis.set_major_formatter(plot_formatter)
        duration = data1.index[-1] - data1.index[0]
        minor_locator = self._get_minor_locator(duration)
        plot.xaxis.set_minor_locator(minor_locator)
        plot.grid(which='minor', linestyle='dashed', linewidth='0.5', color='gray')
        plot.grid(which='major', linestyle='solid', linewidth='1.0', color='black')
        plot.set_ylabel(y1label, color=plot_color)
        plot.fill_between(data1.index, data1, color=plot_color, alpha=0.4)
        plot.yaxis.grid(False)

    def _setup_plot_2(self, plot2, data2, color2, y2label):
        plot2.set_ylabel(y2label, color=color2)
        plot2.plot(data2.index, data2, color=color2, linestyle='none', marker='o', markersize=1.5)
        plot2.yaxis.set_label_position("right")

    def _sync_axes(self, data1, plot, plot2):

        if data1.index.freq == pd.Timedelta('1s'):  # Force same axis for both
            _, ymax = plot2.get_ylim()
            plot2.set_ylim(0, ymax)
            plot.set_ylim(0, ymax)
        else:  # Dynamic, separate, positive axis
            plot2.set_ylim(bottom=0)
            plot.set_ylim(bottom=0)

    def _add_freq_info(self, plot, data1):
        # Info to display in the infobox
        interval_length = data1.index.freqstr
        interval_count = len(data1)

        # Adding an infobox (Generated with ChatGPT)
        info_text = f"Interval length: {interval_length}\nInterval count: {interval_count}"
        plot.text(
            0.05,
            0.95,
            info_text,
            transform=plot.transAxes,
            fontsize=12,
            verticalalignment="top",
            bbox={
                "boxstyle": "round,pad=0.3",
                "facecolor": "white",
                "edgecolor": "black",
                "alpha": 0.5})

    def display_timeseries_dual(self, plot_id, speed_config: FigureConfig):

        # Fetch the plot and its parent figure
        (plot, plot2), figure_id = self.components["plots"][plot_id]

        # Unpacking the configuration
        title = speed_config.title
        data1 = speed_config.data1
        xlabel = speed_config.xlabel
        y1label = speed_config.y1label
        color1 = speed_config.color1
        data2 = speed_config.data2
        y2label = speed_config.y2label
        color2 = speed_config.color2

        # Bail out if there's not enough data
        if len(data1) < 2:

            # Generated with ChatGPT
            plot.text(0.5, 0.5, "Not enough data to plot", horizontalalignment="center",
                      verticalalignment="center", transform=plot.transAxes, fontsize=14)

            # Draw the text
            self.components["canvases"][figure_id].draw()
            return

        self._setup_plot_1(plot, data1, color1, title, xlabel, y1label)
        self._setup_plot_2(plot2, data2, color2, y2label)
        self._sync_axes(data1, plot, plot2)
        self._add_freq_info(plot, data1)

        # Adjust layout to make room for the labels if necessary
        self.components["figures"][figure_id].tight_layout()

        # Refreshing the canvas
        self.components["canvases"][figure_id].draw()

    def display_bar_graph(self, plot_id: int, config: FigureConfig):

        # Fetch the plot and its parent figure
        plot, figure_id = self.components["plots"][plot_id]

        # Unpacking the configuration
        title = config.title
        data = config.data1
        xlabel = config.xlabel
        ylabel = config.y1label
        color = config.color1

        # Creating the horizontal bar graph
        keys, values = data.keys(), data.values()
        bars = plot.barh(range(len(keys)), values, color=color, alpha=0.7)

        # Adding keys as labels on each bar
        for element, key in zip(bars, keys):
            plot.text(0, element.get_y() + element.get_height() / 2, key,
                      va=tk.CENTER, ha=tk.LEFT, color='black')

        # Only keep integer ticks on the x-axis
        plot.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Hide the y-axis labels
        plot.set_yticks([])

        # Adding title and labels
        if title:
            plot.set_title(title)
        if xlabel:
            plot.set_xlabel(xlabel)
        if ylabel:
            plot.set_ylabel(ylabel)

        # Adjust layout to make room for the labels if necessary
        self.components["figures"][figure_id].tight_layout()

        # Refreshing the canvas
        self.components["canvases"][figure_id].draw()

    def close(self):
        self.destroy()

    def reset(self, keep_context=False):

        if not keep_context:
            self.context.reset()
            save_button = self.components["buttons"][self.map["button.save"]]
            save_button.config(state=tk.NORMAL)

        # Resetting the text areas
        for text_area in self.components["text_areas"].values():
            text_area.config(state=tk.NORMAL)
            text_area.delete('1.0', tk.END)
            text_area.config(state=tk.DISABLED)

        # Resetting the plots
        for plot, _ in self.components["plots"].values():
            if isinstance(plot, tuple):
                for p in plot:
                    p.clear()
            else:
                plot.clear()

        # Resetting the indicators
        for indicator in self.components["indicators"].values():
            indicator.set(0)

        # Refreshing the canvas
        for canvas in self.components["canvases"].values():
            canvas.draw()


def start_app(context, analyze_function):
    app = PcapUi(context, analyze_function)
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
