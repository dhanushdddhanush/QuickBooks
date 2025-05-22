#!/bin/bash
gunicorn -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0 --port=8000
