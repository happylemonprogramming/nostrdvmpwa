#!/bin/bash
streamlit run Home.py &  # Run Streamlit app in the background
gunicorn -w 4 -b 0.0.0.0:$PORT app:app  # Run Flask app with Gunicorn
