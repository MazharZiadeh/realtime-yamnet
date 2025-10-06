#!/bin/bash
# Setup script for Real-time YAMNet

echo "=========================================="
echo "  Real-time YAMNet Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version || { echo "ERROR: Python 3 not found!"; exit 1; }

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
else
    echo "Virtual environment already exists."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing dependencies..."
pip install -r requirements.txt

# Check if yamnet.h5 exists
if [ ! -f "yamnet/yamnet.h5" ]; then
    echo ""
    echo "⚠️  WARNING: Model weights not found!"
    echo "Downloading YAMNet model weights..."
    mkdir -p yamnet
    wget -O yamnet/yamnet.h5 https://storage.googleapis.com/audioset/yamnet.h5
else
    echo "✓ Model weights found"
fi

echo ""
echo "=========================================="
echo "  ✅ Setup Complete!"
echo "=========================================="
echo ""
echo "To run the application:"
echo "  bash run.sh          # CPU mode"
echo "  bash run_with_gpu.sh # GPU mode (if available)"
echo ""
echo "If microphone issues occur, run:"
echo "  bash fix_microphone.sh"
echo ""

