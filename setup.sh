#!/bin/bash
streamlit run Home.py --server.host 0.0.0.0 --server.port 8501 &  # Run Streamlit app in the background
gunicorn -w 4 -b 0.0.0.0:$PORT app:app --preload  # Run Flask app with Gunicorn
