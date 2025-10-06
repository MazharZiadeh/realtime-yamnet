#!/bin/bash
# Quick run script for real-time YAMNet

# Check and fix microphone if needed
if [ -f "fix_microphone.sh" ]; then
    echo "🔍 Verifying microphone..."
    bash fix_microphone.sh > /dev/null 2>&1
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Run the application
echo "🎤 Starting real-time YAMNet sound classifier..."
echo "Press Ctrl+C to stop"
echo ""
python realtime_YAMNET.py 2>&1 | grep -v "ALSA\|jack\|Cannot connect\|JackShm\|Unknown PCM\|pcm_"

