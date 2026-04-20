# 
# Author: Kelvin Kabute
# Last-updated: 2026-04-20

"""Make `scripts` a package so hooks can import modules reliably.

This file is intentionally empty; its presence allows `from scripts...` imports
to succeed when Python's import machinery is invoked from the repository root.
"""

__all__ = []
