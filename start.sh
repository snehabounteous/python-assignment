#!/bin/bash

# Optional: install any runtime dependencies that may be missing
pip install email-validator

# Start your FastAPI app
uvicorn app.main:app --host 0.0.0.0 --port 10000
