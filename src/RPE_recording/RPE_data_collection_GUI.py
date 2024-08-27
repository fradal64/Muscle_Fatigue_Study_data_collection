import dearpygui.dearpygui as dpg
from pathlib import Path
import sys
import time
from loguru import logger
import threading
from playsound import playsound
import csv
from datetime import datetime
import random
sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.config import PROJ_ROOT

from src.RPE_recording.select_partecipant_and_session import populate_participants, populate_sessions, load_session



# Dear PyGui Setup
dpg.create_context()

# Data storage
data = []  # Store all data points
time_data = []  # Store all time points
recording = False
start_time = 0
last_update_time = 0
user_input = None
participant = None
session = None
next_update_time = 0

# Beep function
def beep(sound_file=PROJ_ROOT / 'sounds' / 'beep.wav'):
    def _beep():
        try:
            playsound(sound_file)
        except Exception as e:
            logger.warning(f"Failed to play sound: {e}")
    
    # Run the beep in a separate thread
    threading.Thread(target=_beep, daemon=True).start()

def update_plot():
    global last_update_time, user_input, next_update_time
    if recording:
        current_time = time.time()
        elapsed_time = current_time - start_time
        dpg.set_value("timer", f"Elapsed Time: {elapsed_time:.2f}s")
        
        if current_time >= next_update_time:
            beep()

            time_data.append(elapsed_time)
            data.append(None)  # Add a placeholder for the next input
            
            # Update the plot (only plot non-None values)
            plot_data = [(t, v) for t, v in zip(time_data, data) if v is not None]
            if plot_data:
                plot_times, plot_values = zip(*plot_data)
                dpg.set_value('line_series', [plot_times, plot_values])
                dpg.set_value('scatter_series', [plot_times, plot_values])
                dpg.fit_axis_data('x_axis')
                dpg.fit_axis_data('y_axis')
            
            last_update_time = current_time
            
            # Set the next update time between 5 and 15 seconds
            next_update_time = current_time + random.uniform(5, 15)
            
            # Update the input window text and enable input
            dpg.set_value("input_text_time", f"Enter RPE value (0-100) for time {elapsed_time:.2f}s:")
            dpg.enable_item("input_text")
            dpg.focus_item("input_text")

def save_data():
    global participant, session, data, time_data
    if not participant or not session:
        logger.warning("Participant or session not selected. Data not saved.")
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"RPE_data_{participant}_{session}_{timestamp}.csv"
    filepath = PROJ_ROOT / filename

    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Time (s)', 'RPE Value'])
        for t, v in zip(time_data, data):
            if v is not None:
                writer.writerow([f"{t:.2f}", v])

    logger.info(f"Data saved to {filepath}")

def toggle_recording(sender, app_data, user_data):
    global recording, start_time, last_update_time, data, time_data, user_input, participant, session
    recording = not recording
    if recording:
        participant = dpg.get_value("participant_combo")
        session = dpg.get_value("session_combo")
        if not participant or not session:
            logger.warning("Please select a participant and session before starting recording.")
            recording = False
            return

        start_time = time.time()
        last_update_time = start_time
    
        dpg.set_value('line_series', [time_data, data])
        dpg.set_value('scatter_series', [time_data, data])
        dpg.set_item_label("record_button", "Stop Recording")
        dpg.configure_item("input_window", show=True)
        dpg.configure_item("timer", show=True)
        dpg.focus_item("input_text")
        logger.info("Recording started")
        beep()
    else:
        current_time = time.time()
        elapsed_time = current_time - start_time
        time_data.append(elapsed_time)
        data.append(100.0)
        logger.debug(f"Added final point: Time = {elapsed_time:.2f}, Value = 100.0")

        dpg.set_item_label("record_button", "Start Recording")
        dpg.configure_item("input_window", show=False)
        dpg.configure_item("timer", show=False)
        save_data()  # Save data when stopping recording
        # Update plot with final data point
        plot_data = [(t, v) for t, v in zip(time_data, data) if v is not None]
        if plot_data:
            plot_times, plot_values = zip(*plot_data)
            dpg.set_value('line_series', [plot_times, plot_values])
            dpg.set_value('scatter_series', [plot_times, plot_values])
            dpg.fit_axis_data('x_axis')
            dpg.fit_axis_data('y_axis')
        # Clear data after saving
        data = []
        time_data = []
        user_input = None
        dpg.set_value('line_series', [[], []])
        dpg.set_value('scatter_series', [[], []])
        logger.info("Recording stopped")
        beep()

def input_callback(sender, app_data):
    global user_input, data
    try:
        value = float(app_data)
        if 0 <= value <= 100:
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
            plot_data = [(t, v) for t, v in zip(time_data, data) if v is not None]
            if plot_data:
                plot_times, plot_values = zip(*plot_data)
                dpg.set_value('line_series', [plot_times, plot_values])
                dpg.set_value('scatter_series', [plot_times, plot_values])
                dpg.fit_axis_data('x_axis')
                dpg.fit_axis_data('y_axis')
        else:
            logger.warning(f"Input out of range (0-100): {value}")
    except ValueError:
        logger.warning(f"Invalid input: {app_data}")

# Main Window
with dpg.window(label="RPE Recorder", tag="RPE Recorder", width=800, height=800):
    # Section for selecting participant and session
    dpg.add_text("Select Participant and Session")
    
    dpg.add_combo(label="Participant", tag="participant_combo", items=[], callback=populate_sessions)
    dpg.add_combo(label="Session", tag="session_combo", items=[], callback=load_session)
    
    # Section for recording
    dpg.add_separator()
    dpg.add_text("Recording Section")
    
    # Add timer
    dpg.add_text("Elapsed Time: 0.00s", tag="timer", show=False)
    
    # Add plot
    with dpg.plot(label="RPE Data", height=300, width=-1):
        dpg.add_plot_legend()
        x_axis = dpg.add_plot_axis(dpg.mvXAxis, label="Time (s)", tag="x_axis")
        y_axis = dpg.add_plot_axis(dpg.mvYAxis, label="RPE Value", tag="y_axis")
        dpg.set_axis_limits(y_axis, ymin=0, ymax=100)
        dpg.add_line_series([], [], label="RPE", parent=y_axis, tag="line_series")
        dpg.add_scatter_series([], [], label="Data Points", parent=y_axis, tag="scatter_series")

    dpg.add_button(label="Start Recording", callback=toggle_recording, tag="record_button")

# Input Window
with dpg.window(label="Input RPE", tag="input_window", width=300, height=100, pos=[400, 400], no_title_bar=True, no_resize=True, no_move=True, show=False):
    dpg.add_text("Enter RPE value (0-100) for time 0.00s:", tag="input_text_time")
    dpg.add_input_text(tag="input_text", on_enter=True, callback=input_callback)

populate_participants()

dpg.create_viewport(title='RPE data collection', width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

logger.info("Application started")

# Main loop
while dpg.is_dearpygui_running():
    update_plot()  # Call update_plot in each frame
    dpg.render_dearpygui_frame()

logger.info("Application closed")
dpg.destroy_context()