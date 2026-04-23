#!/bin/bash

echo "🛑 Stopping Python & Node Servers..."
# Kill the FastAPI Recommendation Engine
pkill -f "uvicorn src.api.recommendation_api"

# Kill the Real-Time Streaming Processor
pkill -f "python src/streaming/feature_processor"

# Kill the CPPE Internal API
pkill -f "uvicorn api.main:app"

# Kill the React Frontend
pkill -f "vite"

# Kill the Streamlit Dashboard
pkill -f "streamlit run app.py"

echo "🛑 Stopping Docker Infrastructure..."
# Stop Recommendation Engine Docker
cd /Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine
docker compose down

# MongoDB is automatically stopped via local docker compose down

echo "✅ Everything has been completely shut down!"
