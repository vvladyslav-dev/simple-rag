#!/bin/bash
# Get the port from environment variable (Azure App Service sets this)
PORT=${PORT:-8501}

# Run Streamlit on the specified port
streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true

