#!/bin/bash
export JAVA_HOME="/opt/homebrew/opt/openjdk@17"

echo "Starting Real-Time Recommendation Engine Background Infrastructure..."
cd /Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine
docker compose up -d

echo "Starting Recommendation Engine API (Port 8000)..."
source venv/bin/activate

echo "Waiting for Kafka to be ready..."
sleep 8
docker exec real-time-recommendation-engine-kafka-1 kafka-topics --create --topic user_interactions --bootstrap-server localhost:9092 --if-not-exists || true

export MLFLOW_TRACKING_URI="http://localhost:5005"
uvicorn src.api.recommendation_api:app --host 0.0.0.0 --port 8000 > backend_api.log 2>&1 &
API_PID=$!

echo "Starting Real-Time Streaming Processor..."
export MLFLOW_TRACKING_URI="http://localhost:5005"
python src/streaming/feature_processor.py > backend_stream.log 2>&1 &
STREAM_PID=$!

echo "Starting Internal API Bridge (Port 8001)..."
export REDIS_HOST="localhost"
export REDIS_PORT=6379 
export KAFKA_BROKER="localhost:9092"
uvicorn api.main:app --port 8001 > cppe_api.log 2>&1 &
CPPE_API_PID=$!

echo "Starting Hybrid Recommendation Engine Worker..."
export PYTHONPATH="/Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine"
python recommendation_engine/worker.py > worker.log 2>&1 &
WORKER_PID=$!

echo "Starting Premium E-Commerce UI (Port 3001)..."
cd /Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine/frontend
export VITE_API_URL="http://localhost:8001"
npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!

echo "Starting Admin Dashboard (Port 8501)..."
cd /Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine/dashboard
export API_URL="http://localhost:8001"
export STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
streamlit run app.py --server.port 8501 --server.headless true > dashboard.log 2>&1 &
DASHBOARD_PID=$!

echo ""
echo "✅===============================================================✅"
echo "All systems are running smoothly in the background!"
echo "E-Commerce Website (React): http://localhost:3001"
echo "Admin Dashboard (Streamlit): http://localhost:8501"
echo "Recommendation API (Docs): http://localhost:8000/docs"
echo "✅===============================================================✅"
echo ""
echo "To shut everything down when you are completely finished, run:"
echo "kill $API_PID $STREAM_PID $CPPE_API_PID $FRONTEND_PID $DASHBOARD_PID && cd /Users/rishi/Desktop/Real-Time-Recommendation-Engine/Real-Time-Recommendation-Engine && docker compose down"



#./start_all.sh
