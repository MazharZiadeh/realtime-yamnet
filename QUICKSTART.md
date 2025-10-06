# 🎵 Quick Start Guide - Real-time YAMNet Sound Classifier

Get up and running in 2 minutes!

## Quick Setup

```bash
cd realtime_YAMNET
bash setup.sh
```

This will:
- ✅ Create a Python virtual environment
- ✅ Install all required dependencies (TensorFlow, librosa, pyaudio, etc.)
- ✅ Prepare everything for real-time audio classification

## Run the Application

```bash
bash run.sh
```

Or with GPU:
```bash
bash run_with_gpu.sh
```

## What You'll See

1. **Spectrogram Window**: Real-time visualization of audio frequencies (GUI version)
2. **Terminal Output**: Top 5 detected sound events with confidence scores

Example:
```
Current event:
  Speech      : 0.847
  Inside      : 0.523
  Conversation: 0.412
  Music       : 0.234
  Background  : 0.156
```

## Stop the Application

Press `Ctrl+C` in the terminal

## What It Detects

YAMNet can identify **521 different sound events**, including:

- 🗣️ **Speech**: Conversation, laughter, shouting, whispering
- 🎵 **Music**: Instruments, singing, genres
- 🐕 **Animals**: Dogs, cats, birds, insects
- 🚗 **Vehicles**: Cars, trains, airplanes
- 🏠 **Household**: Doors, appliances, tools
- 🌳 **Nature**: Wind, rain, thunder, water
- 🔔 **Alerts**: Alarms, bells, sirens
- And many more!

## Troubleshooting

### "No module named 'pyaudio'"
Run the setup script: `bash setup.sh`

### PyAudio won't install
Install system audio libraries first:
```bash
# Ubuntu/Debian
sudo apt-get install portaudio19-dev python3-dev

# Then run setup again
bash setup.sh
```

### No microphone detected
```bash
bash fix_microphone.sh
```

### Application is slow
- Close other heavy applications
- YAMNet runs on CPU by default (GPU not required but helps)

## System Requirements

- Python 3.8+
- Microphone
- ~500MB disk space (for dependencies)
- Linux, macOS, or Windows

## Ready? Let's Go!

```bash
bash setup.sh    # First time only
bash run.sh      # Start detecting sounds!
```

🎉 Enjoy real-time sound classification!

---
Based on: [SangwonSUH/realtime_YAMNET](https://github.com/SangwonSUH/realtime_YAMNET)

