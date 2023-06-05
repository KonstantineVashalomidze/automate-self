import time
from pynput import mouse, keyboard

def custom_print(msg, file):
    print(msg, file=file)
    file.flush()

def listen_input_events():
    prev_event_time = time.time()

    def log_event_time():
        nonlocal prev_event_time
        current_time = time.time()
        time_diff = current_time - prev_event_time
        prev_event_time = current_time
        return f"Time since last event: {time_diff:.4f}s"

    def on_mouse_click(x, y, button, pressed):
        if pressed:
            custom_print(f"{log_event_time()} - Mouse clicked at ({x}, {y}) with {button}", log_file)
        else:
            custom_print(f"{log_event_time()} - Mouse released at ({x}, {y}) with {button}", log_file)

    def on_mouse_scroll(x, y, dx, dy):
        custom_print(f"{log_event_time()} - Mouse scrolled at ({x}, {y})({dx}, {dy})", log_file)

    def on_key_press(key):
        try:
            custom_print(f"{log_event_time()} - Key Pressed: {key.char}", log_file)
        except AttributeError:
            custom_print(f"{log_event_time()} - Key Pressed: {key.name}", log_file)

        if key == keyboard.Key.esc:
            # Stop the program if the "esc" key is pressed
            return False

    # Create mouse listener
    mouse_listener = mouse.Listener(
        on_click=on_mouse_click,
        on_scroll=on_mouse_scroll
    )
    mouse_listener.start()

    # Create keyboard listener
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press
    )
    keyboard_listener.start()

    # Wait for the listeners to stop (until the "esc" key is pressed)
    keyboard_listener.join()
    mouse_listener.join()

# Open the log file and call the function to start listening for input events
with open('recordsOfTheKeyLog.txt', 'w') as log_file:
    listen_input_events()