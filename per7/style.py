import time

def get_theme():
    hour = time.localtime().tm_hour
    return "dark" if hour < 6 or hour > 18 else "light"

def get_colors(theme):
    if theme == "dark":
        return {
            "bg": "#2c3e50",
            "fg": "#ecf0f1",
            "entry_bg": "#34495e",
            "button_bg": "#1abc9c"
        }
    else:
        return {
            "bg": "#ecf0f1",
            "fg": "#2c3e50",
            "entry_bg": "#ffffff",
            "button_bg": "#3498db"
        }
