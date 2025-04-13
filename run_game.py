"""
Run Game Script
Starts the game from the command line.
"""

import sys
import os

# Add the project root directory to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.game.main import main

if __name__ == "__main__":
    main() 