#!/bin/bash

cd /tmp/realtime_YAMNET

# Check and fix microphone if needed
if [ -f "fix_microphone.sh" ]; then
    bash fix_microphone.sh > /dev/null 2>&1
fi

source venv/bin/activate

# Set up CUDA library paths for GPU acceleration
export LD_LIBRARY_PATH=/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cuda_runtime/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cudnn/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cublas/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cuda_nvrtc/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cufft/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/curand/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cusolver/lib:/tmp/realtime_YAMNET/venv/lib/python3.12/site-packages/nvidia/cusparse/lib:$LD_LIBRARY_PATH

# Enable TensorFlow GPU memory growth to avoid OOM
export TF_FORCE_GPU_ALLOW_GROWTH=true

echo "========================================================================"
echo "  🚀 GPU-Accelerated YAMNet - RTX 4070 Max-Q Edition"
echo "========================================================================"
echo ""
echo "Checking GPU availability..."
python << 'EOF' 2>&1 | grep -v "oneDNN\|AVX\|I tensorflow"
import tensorflow as tf
gpus = tf.config.list_physical_devices('GPU')
print(f"✓ GPUs detected: {len(gpus)}")
for gpu in gpus:
    print(f"  🎮 {gpu.name} - {gpu.device_type}")
if gpus:
    # Enable memory growth
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)
    print("\n✓ GPU memory growth enabled")
    print("✓ Ready for real-time inference!")
EOF

echo ""
echo "========================================================================"
echo "  🎤 Starting microphone capture with GPU acceleration..."
echo "  Your RTX 4070 will process the audio in real-time!"
echo "  Press Ctrl+C to stop"
echo "========================================================================"
echo ""
sleep 2

# Run with GPU
python realtime_YAMNET_text.py 2>&1 | grep -v "ALSA\|jack\|Cannot connect\|JackShm\|Unknown PCM\|pcm_\|oneDNN\|AVX\|I tensorflow\|I external"

