import random
import time

import dearpygui.dearpygui as dpg
from loguru import logger

from src.utils.beep import beep
from src.utils.save_data import save_data
from src.utils.show_error import show_error

# Data storage
data = []  # Store all data points
time_data = []  # Store all time points


user_input = None


# Time tracking
start_time = 0

next_update_time = 0

# Recording state
recording = False


def plot_RPE_graph():
    global data, time_data

    # Check if data and time_data are not empty
    if data and time_data:
        # Filter out None values
        plot_data = [(t, v) for t, v in zip(time_data, data) if v is not None]
        assert plot_data, "No valid data points to plot"

        # Unzip the plot data
        plot_times, plot_values = zip(*plot_data)
        # Update the plot
        dpg.set_value("line_series", [plot_times, plot_values])
        dpg.set_value("scatter_series", [plot_times, plot_values])

        dpg.fit_axis_data("x_axis")
        dpg.fit_axis_data("y_axis")

    elif not data and not time_data:
        # If data and time_data are empty, clear the graph
        dpg.set_value("line_series", [data, time_data])  # Clear line series data
        dpg.set_value("scatter_series", [data, time_data])  # Clear scatter series data
    else:
        logger.error(f"Unexpected condition for data and time_data: {data}, {time_data}")


def update_plot():
    global user_input, next_update_time

    if recording:
        # Update the elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time
        dpg.set_value("timer", f"Elapsed Time: {elapsed_time:.2f}s")

        # Check if it's time for the next input
        if elapsed_time >= next_update_time:

            beep()

            time_data.append(elapsed_time)
            data.append(None)  # Add a placeholder for the next input

            # Update the input window text and enable input
            dpg.set_value(
                "input_text_time", f"Enter RPE value (0-100) for time {elapsed_time:.2f}s:"
            )
            dpg.enable_item("input_text")
            dpg.focus_item("input_text")

            # Set the next update time between 5 and 15 seconds
            next_update_time = elapsed_time + random.uniform(5, 10)


def toggle_recording(sender, app_data, user_data):
    global recording, start_time, next_update_time, data, time_data, user_input

    # Load the selected participant and session
    participant = dpg.get_value("participant_combo")
    session = dpg.get_value("session_combo")

    # Check if a participant and session are selected
    if (
        not participant
        or participant == "No participants found"
        or not session
        or session == "No sessions found"
        or session == "Select a session"
    ):
        error_message = "Please select a valid participant and session before starting recording."
        logger.error(error_message)
        show_error(error_message)
        return

    # Toggle recording state
    recording = not recording

    if recording:
        # Initialize time tracking
        start_time = time.time()
        elapsed_time = 0
        next_update_time = elapsed_time + random.uniform(5, 10)

        # Add initial data point, fatigue is 0 at the start by study design
        time_data.append(0)
        data.append(0)

        # Plot initial graph
        dpg.set_value("line_series", [time_data, data])
        dpg.set_value("scatter_series", [time_data, data])

        # Update button text
        dpg.set_item_label("record_button", "Stop Recording")

        # Show timer
        dpg.configure_item("timer", show=True)

        # Show input window
        dpg.configure_item("input_window", show=True)

        logger.info("Recording started")

        beep()
    else:
        # Update the elapsed time
        current_time = time.time()
        elapsed_time = current_time - start_time

        # Add final data point, fatigue is 100 at the end by study design
        time_data.append(elapsed_time)
        data.append(100.0)

        # Update button text
        dpg.set_item_label("record_button", "Start Recording")

        # Hide timer
        dpg.configure_item("timer", show=False)

        # Hide input window
        dpg.configure_item("input_window", show=False)

        # Update plot with final data point
        plot_RPE_graph()

        # Save data to cvs file
        save_data(data, time_data)

        # Clear data after saving
        data = []
        time_data = []
        user_input = None

        # Clear the plot
        plot_RPE_graph()

        logger.info("Recording stopped")
        beep()


def input_callback(sender, app_data):
    global user_input, data

    value = float(app_data)

    if value < 0 or value > 100:
        logger.warning(f"Input out of range (0-100): {value}")

    # Find the last None value in data and replace it
    for i in range(len(data) - 1, -1, -1):
        if data[i] is None:
            data[i] = value
            logger.debug(f"Added point: Time = {time_data[i]:.2f}, Value = {value:.2f}")
            break

    # Clear the input text, disable it, and update the text
    dpg.set_value("input_text", "")
    dpg.disable_item("input_text")
    dpg.set_value("input_text_time", "Waiting for next input")

    # Update the plot
    plot_RPE_graph()
