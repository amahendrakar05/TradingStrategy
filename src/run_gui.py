"""
GUI Launcher - Yahoo Finance Technical Analysis
Run this script to launch the interactive GUI application
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == '__main__':
    try:
        from gui_analysis import main
        main()
    except ImportError as e:
        print(f"Error: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
