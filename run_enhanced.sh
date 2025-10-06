#!/bin/bash
# Run Enhanced YAMNet with temporal smoothing and confidence filtering

cd /tmp/realtime_YAMNET

# Check and fix microphone if needed
if [ -f "fix_microphone.sh" ]; then
    echo "🔍 Verifying microphone..."
    bash fix_microphone.sh > /dev/null 2>&1
fi

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

echo "🚀 Starting Enhanced YAMNet..."
echo "   ✨ Features: Temporal smoothing, confidence filtering, event tracking"
echo ""
python realtime_YAMNET_enhanced.py 2>&1 | grep -v "ALSA\|jack\|Cannot connect\|JackShm\|Unknown PCM\|pcm_\|oneDNN\|AVX\|I tensorflow\|I external"

