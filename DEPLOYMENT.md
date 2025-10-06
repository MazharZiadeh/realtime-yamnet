# 🚀 Deployment Guide - Real-time YAMNet

Complete guide for deploying YAMNet on various platforms.

## 📋 Quick Deployment

```bash
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
bash setup.sh && bash run.sh
```

## 💻 Local Machine

### Linux
```bash
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-dev python3-venv
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
bash setup.sh
bash run.sh
```

### macOS
```bash
brew install portaudio python3
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
bash setup.sh
bash run.sh
```

### Windows
```powershell
# Install Python 3.8+ from python.org
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
python -m venv venv
venv\Scripts\activate
pip install pipwin
pipwin install pyaudio
pip install -r requirements.txt
python realtime_YAMNET.py
```

## 🖥️ Remote Server

```bash
# Copy to server
scp -r realtime_YAMNET user@server:/home/user/

# SSH and setup
ssh user@server
cd realtime_YAMNET
bash setup.sh

# Run in background
nohup bash run_with_gpu.sh > output.log 2>&1 &
```

## 🎮 GPU Cluster (SLURM)

```bash
cd realtime_YAMNET
sbatch deploy/slurm_job.sh
squeue -u $USER
```

## 🐳 Docker

```bash
# Build
docker build -t realtime-yamnet .

# Run
docker run -it --rm \
  --device /dev/snd \
  -e PULSE_SERVER=unix:/run/user/1000/pulse/native \
  -v /run/user/1000/pulse:/run/user/1000/pulse \
  realtime-yamnet

# GPU version
docker run -it --rm --gpus all \
  --device /dev/snd \
  realtime-yamnet:gpu
```

## ☁️ Cloud Platforms

### AWS EC2
```bash
# Launch GPU instance (g4dn.xlarge)
ssh -i key.pem ubuntu@instance
sudo apt-get install -y portaudio19-dev nvidia-driver-525
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
bash setup.sh
bash run_with_gpu.sh
```

### Google Cloud Platform
```bash
gcloud compute ssh instance-name
git clone https://github.com/MazharZiadeh/realtime_YAMNET.git
cd realtime_YAMNET
bash setup.sh
bash run_with_gpu.sh
```

## 🔧 Troubleshooting

### Microphone Issues
```bash
bash fix_microphone.sh
```

### GPU Not Available
```bash
nvidia-smi
python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"
```

## 📊 Deployment Checklist

- [ ] System dependencies installed
- [ ] Python environment configured
- [ ] Model weights downloaded
- [ ] Microphone tested
- [ ] GPU drivers installed (if using GPU)
- [ ] Audio routing configured

---

**For detailed deployment instructions, see each platform's section above.**

