from threading import Thread
from functools import wraps
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, PhotoImage

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator



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
    def __init__(self, analyze_function):
        super().__init__()
        self.analyze_function = analyze_function

        self.title('PCAP Analyzer')
        self.geometry('800x600')
        icon = PhotoImage(file='assets/icon.png')
        self.iconphoto(True, icon)

        self.text_areas = {}
        self.figures = {}
        self.canvases = {}
        self.plots = {}

        self.figure_id = 0
        self.plot_id = 0
        self.text_area_id = 0

        self.create_menu()
        self.initialize_ui()

    def create_menu(self):
        self.menu_bar = tk.Menu(self)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)

        menu_data = [
            ("Open File...", "Ctrl+O", "<Control-o>", self.open_file),
            ("Reset", "Ctrl+R", "<Control-r>", self.reset),
            ("Exit", "Ctrl+Q", "<Control-q>", self.close)
        ]

        for item, shortcut_frontend, shortcut_backend, command in menu_data:
            self.file_menu.add_command(
                label=item, accelerator=shortcut_frontend, command=command)
            self.bind(shortcut_backend, lambda event, cmd=command: cmd())

        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        self.config(menu=self.menu_bar)

    def initialize_ui(self):
        self.frame = ttk.Frame(self)
        self.frame.pack(padx=10, pady=10, fill='x', expand=False)

        self.reset_button = ttk.Button(self.frame, text="Reset", command=self.reset)
        self.reset_button.pack(side='right')

        # Create the notebook for tabs
        self.notebook = ttk.Notebook(self)

        # Create frames for tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)

        # Add tabs to the notebook
        self.notebook.add(self.tab1, text='Details')
        self.notebook.add(self.tab2, text='DNS')

        # Pack to make visible
        self.notebook.pack(expand=True, fill=tk.BOTH)

        # Prepare tab 1
        self.summary_text_area_id = self.create_scrollable_text_area(self.tab1)

        # Prepare tab 2
        figure_id = self.create_figure_and_canvas(self.tab2)

        self.dns_plot_id_1 = self.create_plot(figure_id, 211)
        self.dns_plot_id_2 = self.create_plot(figure_id, 212)

    def create_scrollable_text_area(self, container):

        # Assigning a unique ID to the text area
        text_area_id = self.text_area_id
        self.text_area_id += 1

        # Defining
        text_area = scrolledtext.ScrolledText(container, wrap=tk.WORD)

        # Store the text area
        self.text_areas[text_area_id] = text_area

        # Displaying
        self.text_areas[text_area_id].pack(
            padx=10, pady=10, fill=tk.BOTH, expand=True)

        return text_area_id

    def create_figure_and_canvas(self, container):

        # Create a figure
        figure = plt.Figure()

        # Assigning a unique ID to the figure
        figure_id = self.figure_id
        self.figure_id += 1

        # Store the figure
        self.figures[figure_id] = figure

        # Create canvas for the figure
        canvas = FigureCanvasTkAgg(figure, container)

        # Store the canvas
        self.canvases[figure_id] = canvas

        # Display the canvas
        canvas_widget = self.canvases[figure_id].get_tk_widget()
        canvas_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

        # Return the ID
        return figure_id

    def create_plot(self, figure_id, position: int):

        # Assigning a unique ID to the plot
        plot_id = self.plot_id
        self.plot_id += 1

        # Fetch the parent figure
        figure = self.figures[figure_id]

        # Create the figure
        plot = figure.add_subplot(position)

        # Store the plot and its parent figure
        self.plots[plot_id] = plot, figure_id

        # Return the ID
        return plot_id

    def open_file(self):

        # Ask the user to select a file
        file_path = filedialog.askopenfilename()

        if file_path:  # file selected
            result = self.process_file(file_path)
            if result is None:  # User cancelled the operation
                return
            produced_text, dns_most_queried_domains, dns_most_common_servers, speed_config = result
            self.display_text(
                text_area_id=self.summary_text_area_id, text=produced_text)
            self.display_bar_graph(
                plot_id=self.dns_plot_id_1,
                data=dns_most_queried_domains,
                title="Most queried domains (grouped by 2LD)",
                xlabel="Count",
                ylabel="Domain")
            self.display_bar_graph(plot_id=self.dns_plot_id_2, data=dns_most_common_servers,
                                   title="Most used DNS servers", xlabel="Count", ylabel="Server")
        else:  # no file selected
            pass

    @with_loading_screen
    def process_file(self, file_path):
        return self.analyze_function(file_path)

    def display_text(self, text_area_id, text):

        # Fetch the text area
        text_area = self.text_areas[text_area_id]

        # Resetting
        text_area.delete('1.0', tk.END)

        # Displaying
        text_area.insert(tk.END, text)

    def display_bar_graph(
        self,
        plot_id: int,
        data: dict[str, int],
        title: str | None = None,
        xlabel: str | None = None,
        ylabel: str | None = None
    ):

        # Fetch the plot and its parent figure
        plot, figure_id = self.plots[plot_id]

        # Creating the horizontal bar graph
        keys = list(data.keys())
        values = list(data.values())
        bars = plot.barh(range(len(keys)), values, color='skyblue', alpha=0.7)

        # Adding keys as labels on each bar
        for bar, key in zip(bars, keys):
            plot.text(0, bar.get_y() + bar.get_height() / 2, key,
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
        self.figures[figure_id].tight_layout()

        # Refreshing the canvas
        self.canvases[figure_id].draw()

    def close(self):
        self.destroy()

    def reset(self):
        # Resetting the text areas
        for text_area in self.text_areas.values():
            text_area.delete('1.0', tk.END)

        # Resetting the plots
        for plot, _ in self.plots.values():
            plot.clear()

        # Refreshing the canvas
        for canvas in self.canvases.values():
            canvas.draw()


def start_app(analyze_function):
    app = PcapUi(analyze_function)
    app.mainloop()
