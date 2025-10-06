# 🎤 Microphone Troubleshooting Guide

## ✅ Quick Fix

If your microphone isn't working:

```bash
bash fix_microphone.sh
```

## 🔧 What the Script Does

1. Restarts audio services (PipeWire/PulseAudio)
2. Sets the correct default microphone
3. Configures optimal volume levels (130%)
4. Unmutes all microphones
5. Verifies configuration

## 📊 Common Issues

### No Audio Captured

**Symptoms**: YAMNet runs but shows no sound events

**Solution**:
```bash
# Run microphone fix
bash fix_microphone.sh

# Verify microphone
arecord -d 3 test.wav
aplay test.wav
```

### PyAudio Can't Find Device

**Symptoms**: Error about audio device not found

**Solution**:
```bash
# List available devices
python -c "import pyaudio; p = pyaudio.PyAudio(); [print(f'{i}: {p.get_device_info_by_index(i)[\"name\"]}') for i in range(p.get_device_count())]"

# Check PulseAudio sources
pactl list sources short
```

### Volume Too Low

**Symptoms**: Very low confidence scores for all events

**Solution**:
```bash
# Increase microphone volume
pactl set-source-volume @DEFAULT_SOURCE@ 150%

# Verify volume
pactl list sources | grep -A 10 "Name.*input"
```

### Permission Denied

**Symptoms**: Can't access audio device

**Solution**:
```bash
# Add user to audio group
sudo usermod -aG audio $USER

# Log out and log back in
```

## 🎯 Microphone Configuration

### Available Microphones

- **Internal DMIC**: Digital microphone array (recommended for laptops)
- **Headset Mic**: External/analog microphone input

### Set Default Microphone

```bash
# List sources
pactl list sources short

# Set default
pactl set-default-source <SOURCE_NAME>
```

### Test Microphone

```bash
# Record 3 seconds
arecord -d 3 -f cd test.wav

# Play back
aplay test.wav
```

## 🔍 Diagnostic Commands

```bash
# Check audio hardware
arecord -l

# Check PulseAudio/PipeWire
pactl list sources

# Check ALSA mixer
amixer

# Test with Python
python -c "import pyaudio; p = pyaudio.PyAudio(); print('Devices:', p.get_device_count())"
```

## 📞 Still Having Issues?

1. Check hardware connection
2. Restart your computer
3. Update audio drivers
4. Check system audio settings
5. Open a GitHub issue with diagnostic output

---

**Most microphone issues can be fixed by running `bash fix_microphone.sh`**

