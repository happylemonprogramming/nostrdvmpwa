#!/bin/bash
export STREAMLIT_URL=$(streamlit run Home.py 2>&1 | awk '/Network URL:/ {print $NF}')
gunicorn -w 4 -b 0.0.0.0:$PORT app:app  # Run Flask app with Gunicorn
