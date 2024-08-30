import dearpygui.dearpygui as dpg
from loguru import logger

from src.RPE_recording.RPE_live_plot import (
    input_callback,
    toggle_recording,
    update_plot,
)
from src.RPE_recording.select_partecipant_and_session import (
    load_session,
    populate_participants,
    populate_sessions,
)

# Dear PyGui Setup
dpg.create_context()

# Main Window
with dpg.window(label="RPE Recorder", tag="RPE Recorder", width=800, height=800):
    # Section for selecting participant and session
    dpg.add_text("Select Participant and Session")

    dpg.add_combo(
        label="Participant", tag="participant_combo", items=[], callback=populate_sessions
    )
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
with dpg.window(
    label="Input RPE",
    tag="input_window",
    width=300,
    height=100,
    pos=[400, 400],
    no_title_bar=True,
    no_resize=True,
    no_move=True,
    show=False,
):
    dpg.add_text("Waiting for next input", tag="input_text_time")
    dpg.add_input_text(tag="input_text", on_enter=True, decimal=True, callback=input_callback)
    dpg.disable_item("input_text")

populate_participants()


dpg.create_viewport(title="RPE data collection", width=800, height=800)
dpg.setup_dearpygui()
dpg.show_viewport()

logger.info("Application started")

# Main loop
while dpg.is_dearpygui_running():
    update_plot()  # Call update_plot in each frame
    dpg.render_dearpygui_frame()

logger.info("Application closed")
dpg.destroy_context()
