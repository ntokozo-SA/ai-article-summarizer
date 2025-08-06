#!/bin/bash

echo "========================================"
echo "AI Article Summarizer Setup Script"
echo "========================================"
echo

echo "Setting up Backend (Flask)..."
cd backend
echo "Installing Python dependencies..."
pip install -r requirements.txt
echo
echo "Backend setup complete!"
echo
echo "Please configure your Gemini API key:"
echo "1. Go to https://makersuite.google.com/app/apikey"
echo "2. Create a new API key"
echo "3. Copy the API key to backend/config.py"
echo
echo "To start the backend server, run:"
echo "python app.py"
echo

cd ..

echo "Setting up Frontend (React Extension)..."
cd extension
echo "Installing Node.js dependencies..."
npm install
echo
echo "Building the extension..."
npm run build
echo
echo "Frontend setup complete!"
echo

cd ..

echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo
echo "Next steps:"
echo "1. Configure your Gemini API key in backend/config.py"
echo "2. Start the backend: cd backend && python app.py"
echo "3. Load the extension in Chrome:"
echo "   - Go to chrome://extensions/"
echo "   - Enable Developer mode"
echo "   - Click 'Load unpacked'"
echo "   - Select the extension/dist folder"
echo
echo "Note: You'll need to replace the icon files with actual PNG icons"
echo 