# Real-time YAMNet Sound Event Detector - Setup Guide

This project performs real-time sound classification using YAMNet, detecting 521 different audio events from your microphone feed.

## What's Included

✅ YAMNet model weights (yamnet.h5)
✅ YAMNet implementation files
✅ Real-time audio capture and classification script

## Installation

### 1. Install System Dependencies (if needed)

**On Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio
```

**On macOS:**
```bash
brew install portaudio
```

**On Windows:**
PyAudio should install directly from pip.

### 2. Install Python Dependencies

```bash
bash setup.sh
```

Or install manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Running the Application

Simply run:
```bash
bash run.sh
```

Or with GPU:
```bash
bash run_with_gpu.sh
```

## What It Does

- 🎤 Captures audio from your microphone in real-time (1-second chunks)
- 🧠 Analyzes audio using the YAMNet neural network
- 📊 Shows a spectrogram visualization of the audio
- 🏆 Displays the top 5 detected sound events with confidence scores
- 🔄 Updates continuously every second

## Troubleshooting

### PyAudio Installation Issues

**Linux:**
```bash
sudo apt-get install portaudio19-dev
pip install pyaudio
```

**macOS:**
```bash
brew install portaudio
pip install pyaudio
```

**Windows:**
```bash
pip install pipwin
pipwin install pyaudio
```

### No Microphone Detected

Make sure your microphone is properly connected and not being used by another application.

Run the microphone fix script:
```bash
bash fix_microphone.sh
```

### Performance Issues

If the application is slow, consider using GPU acceleration or close other resource-intensive applications.

## Credits

- Original project: [SangwonSUH/realtime_YAMNET](https://github.com/SangwonSUH/realtime_YAMNET)
- YAMNet model: [Google Research](https://github.com/tensorflow/models/tree/master/research/audioset/yamnet)

## License

MIT License - See LICENSE file for details

---

**Ready to go!** Just run `bash setup.sh` then `bash run.sh` to start detecting sounds! 🎵

