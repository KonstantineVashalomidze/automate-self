import time
import re
import pyautogui
from pynput.keyboard import Key

def parse_log_line(line):
    pattern = r"Time since last event: (\d+\.\d+)s - (.+)"
    match = re.match(pattern, line)
    if match:
        time_diff, event = match.groups()
        return float(time_diff), event

def simulate_events_from_file(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            time_diff, event = parse_log_line(line)
            time.sleep(time_diff)

            if "Mouse moved to" in event:
                x, y = re.findall(r'\d+', event)
                pyautogui.moveTo(int(x), int(y))
            elif "Mouse clicked" in event:
                x, y, button = re.findall(r'\d+|left|middle|right', event)
                pyautogui.click(int(x), int(y), button=button)
            elif "Mouse released" in event:
                pass  # No need to simulate mouse release events
            elif "Mouse scrolled" in event:
                x, y, dx, dy = re.findall(r'-?\d+', event)
                pyautogui.scroll(int(dy), x=int(x), y=int(y))
            elif "Key Pressed" in event:
                key = re.search(r'Key Pressed: (.+)', event).group(1)
                if key.startswith('Key.'):
                    key = getattr(Key, key.split('.')[1])
                pyautogui.press(key)

# Read and simulate events from the log file
simulate_events_from_file('recordsOfTheKeyLog.txt')
