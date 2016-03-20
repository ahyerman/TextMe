#!/bin/bash

# TUESDAY
# Run tuesday morning for commute to North (Hutchins stop)
echo "python stop_info.py 149" | at 0745 tuesday
# Run tuesday morning for commute to Central (cooley stop)
echo "python stop_info.py 88" | at 1025 tuesday
# Run tuesday afternoon for back to North (power center)
echo "python stop_info.py 43" | at 1255 tuesday

# THURSDAY
# Run thursday morning for commute to North (Hutchins stop)
echo "python stop_info.py 149" | at 0745 thursday
# Run thursday morning for commute to Central (cooley stop)
echo "python stop_info.py 88" | at 1025 thursday
# Run thursday afternoon for back to North (power center)
echo "python stop_info.py 43" | at 1255 thursday

# Rerun shell
echo "source weekly.sh" | at now + 7 days
