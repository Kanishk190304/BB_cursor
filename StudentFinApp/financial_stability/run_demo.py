import os
import webbrowser

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set the path to the demo page
demo_page = os.path.join(current_dir, 'demo_page.html')

print("Opening the Student Financial Stability demo page...")
print(f"Demo page path: {demo_page}")

# Open the demo page in the default browser
webbrowser.open(f'file://{demo_page}')

print("If the browser doesn't open automatically, you can open this file manually:")
print(demo_page) 