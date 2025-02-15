#!/bin/bash
# run_project.sh
#
# This script installs and starts both the backend and the frontend.
#
# Usage:
#   ./run_project.sh install   # to install all dependencies
#   ./run_project.sh start     # to start backend and frontend
#   ./run_project.sh all       # to install and then start everything

# Function to install dependencies
install_dependencies() {
    echo "Installing backend dependencies..."
    # Navigate to the backend directory
    cd backend || { echo "Backend directory not found."; exit 1; }
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        python -m venv venv
    fi

    # Activate the virtual environment and install backend packages
    # For Linux/macOS:
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    # For Windows (Git Bash, for instance):
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    fi

    pip install -r requirements.txt
    cd ..

    echo "Installing frontend dependencies..."
    # Navigate to the frontend directory and install npm packages
    cd frontend || { echo "Frontend directory not found."; exit 1; }
    npm install
    cd ..
}

# Function to start backend and frontend services concurrently
start_services() {
    echo "Starting backend..."
    cd backend || { echo "Backend directory not found."; exit 1; }

    # Activate the virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate
    elif [ -f "venv/Scripts/activate" ]; then
        source venv/Scripts/activate
    fi

    # Start the Flask backend (adjust the --app parameter if needed)
    flask --app main run &
    cd ..

    echo "Starting frontend..."
    cd frontend || { echo "Frontend directory not found."; exit 1; }
    npm start &
    cd ..

    # Wait for background processes
    wait
}

# Main logic: check command line argument
case "$1" in
    install)
        install_dependencies
        ;;
    start)
        start_services
        ;;
    all)
        install_dependencies
        start_services
        ;;
    *)
        echo "Usage: $0 {install|start|all}"
        exit 1
        ;;
esac