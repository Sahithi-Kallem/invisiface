#!/bin/bash

echo "🚀 Starting InvisiFace: Face Anonymizer and Digital Identity Protection System"
echo "================================================================"

# Function to handle cleanup on exit
cleanup() {
    echo -e "\n🛑 Shutting down InvisiFace..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM

echo "📦 Setting up backend..."
cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install dependencies
source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

echo "🔧 Starting FastAPI backend on http://localhost:8000"
python main.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "🎨 Setting up frontend..."
cd ../frontend

# Install npm dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing npm dependencies..."
    npm install > /dev/null 2>&1
fi

echo "⚛️  Starting React frontend on http://localhost:3000"
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ InvisiFace is now running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both services"

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID