#!/bin/bash
#SBATCH --job-name=yamnet
#SBATCH --output=yamnet_%j.out
#SBATCH --error=yamnet_%j.err
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --time=01:00:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1

# Load modules (adjust for your cluster configuration)
# module load cuda/12.0
# module load python/3.10

echo "=========================================="
echo "YAMNet Real-time Sound Detector"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "GPU: $CUDA_VISIBLE_DEVICES"
echo "=========================================="

# Navigate to project directory
cd $SLURM_SUBMIT_DIR || exit 1

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
else
    echo "ERROR: Virtual environment not found!"
    echo "Please run: bash setup.sh"
    exit 1
fi

# Set CUDA paths (adjust for your cluster)
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64

# Configure TensorFlow
export TF_FORCE_GPU_ALLOW_GROWTH=true
export TF_CPP_MIN_LOG_LEVEL=2

# Verify GPU availability
echo "Checking GPU availability..."
python -c "import tensorflow as tf; gpus = tf.config.list_physical_devices('GPU'); print(f'GPUs available: {len(gpus)}')"

# Run YAMNet with GPU acceleration
echo "Starting YAMNet..."
bash run_with_gpu.sh

echo "Job completed!"

