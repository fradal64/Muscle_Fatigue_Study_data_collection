import dearpygui.dearpygui as dpg


def show_error(message):
    width = 400
    height = 100
    with dpg.window(
        label="Error",
        modal=True,
        no_close=True,
        autosize=True,
        pos=(dpg.get_viewport_width() // 2 - width // 2, dpg.get_viewport_height() // 2 - height),
        no_move=True,
        width=width,
        height=height,
    ) as modal_id:
        dpg.add_text(message)
        dpg.add_button(label="OK", width=75, callback=lambda: dpg.delete_item(modal_id))
