import os
import sys

"""
This code finds the main folder of your project by going up one level from the current file's location. It then adds that main folder to the beginning of Python's search path, which is the list of places Python looks when you try to import modules. This allows you to import files from anywhere in your project without Python throwing "module not found" errors. The print statements just show you what folder was found and what the full search path looks like.
"""


project_root = os.path.join(os.path.dirname(__file__), '..')
print(f"Project root: {project_root}")

sys.path.insert(0, project_root)
print(sys.path)