"""
Backward compatibility wrapper for main.py.

This file maintains backward compatibility with the old structure.
For new installations, use: python -m system_architect.cli
Or install the package and use: system-architect
"""

from src.system_architect.cli import main

if __name__ == "__main__":
    main()
