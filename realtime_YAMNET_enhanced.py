#!/usr/bin/env python3
"""
Enhanced Real-time YAMNet Sound Classifier
with Temporal Smoothing, Confidence Filtering, and Advanced Features
"""

import pyaudio
import librosa
import numpy as np
import keras
from collections import deque
import time

import yamnet.params as params
import yamnet.yamnet as yamnet_model

# ============================================================================
# CONFIGURATION
# ============================================================================
CONFIDENCE_THRESHOLD = 0.15      # Minimum confidence to display
TEMPORAL_WINDOW = 5              # Number of frames to average (smoothing)
MIN_EVENT_DURATION = 2           # Minimum consecutive frames to report event
FRAME_RATE = 1.0                 # Seconds per frame
TOP_K = 5                        # Number of top predictions to show

# ============================================================================
# LOAD MODEL
# ============================================================================
print("🔧 Loading YAMNet model...")
yamnet = yamnet_model.yamnet_frames_model(params)
yamnet.load_weights('yamnet/yamnet.h5')
yamnet_classes = yamnet_model.class_names('yamnet/yamnet_class_map.csv')
print(f"✅ Model loaded! Detecting {len(yamnet_classes)} sound classes\n")

# ============================================================================
# TEMPORAL SMOOTHING BUFFER
# ============================================================================
prediction_history = deque(maxlen=TEMPORAL_WINDOW)
event_duration_counter = {}  # Track how long each event has been detected

# ============================================================================
# AUDIO SETUP
# ============================================================================
frame_len = int(params.SAMPLE_RATE * FRAME_RATE)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=params.SAMPLE_RATE,
    input=True,
    frames_per_buffer=frame_len
)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def apply_temporal_smoothing(current_prediction):
    """Average predictions over temporal window for stability"""
    prediction_history.append(current_prediction)
    if len(prediction_history) < TEMPORAL_WINDOW:
        return current_prediction
    return np.mean(prediction_history, axis=0)


def filter_by_confidence(predictions, threshold=CONFIDENCE_THRESHOLD):
    """Only return predictions above confidence threshold"""
    filtered_indices = np.where(predictions > threshold)[0]
    return filtered_indices


def calculate_audio_energy(audio_data):
    """Calculate RMS energy of audio signal"""
    return np.sqrt(np.mean(audio_data**2))


def is_silence(audio_data, energy_threshold=0.01):
    """Detect if audio is silence using energy threshold"""
    energy = calculate_audio_energy(audio_data)
    return energy < energy_threshold


def update_event_duration(class_idx, is_detected):
    """Track event duration for filtering transient detections"""
    if is_detected:
        event_duration_counter[class_idx] = event_duration_counter.get(class_idx, 0) + 1
    else:
        event_duration_counter[class_idx] = 0
    return event_duration_counter[class_idx]


def get_stable_events(top_indices, smoothed_predictions):
    """Filter events that have been detected for minimum duration"""
    stable_events = []
    for idx in top_indices:
        duration = update_event_duration(idx, True)
        if duration >= MIN_EVENT_DURATION:
            stable_events.append((idx, smoothed_predictions[idx], duration))
    return stable_events


def format_confidence_bar(confidence, width=20):
    """Create ASCII confidence bar"""
    filled = int(confidence * width)
    bar = '█' * filled + '░' * (width - filled)
    return bar


def display_predictions(stable_events, frame_num, energy, processing_time):
    """Enhanced display with bars, duration, and statistics"""
    print("\n" + "="*70)
    print(f"📊 Frame {frame_num:04d} | Energy: {energy:.4f} | "
          f"Processing: {processing_time*1000:.1f}ms")
    print("="*70)
    
    if not stable_events:
        print("🔇 No significant events detected (below threshold)")
    else:
        print(f"\n🎯 Detected Events (confidence > {CONFIDENCE_THRESHOLD}):\n")
        for idx, conf, duration in stable_events:
            bar = format_confidence_bar(conf)
            duration_indicator = "🔥" * min(duration // 2, 5)
            print(f"  {yamnet_classes[idx]:25s} │ {bar} │ {conf:.3f} │ {duration_indicator}")
    
    print("\n" + "-"*70)


# ============================================================================
# MAIN LOOP
# ============================================================================
print("="*70)
print("🎤 Enhanced Real-time YAMNet Sound Classifier")
print("="*70)
print(f"⚙️  Settings:")
print(f"   • Confidence Threshold: {CONFIDENCE_THRESHOLD}")
print(f"   • Temporal Smoothing: {TEMPORAL_WINDOW} frames")
print(f"   • Min Event Duration: {MIN_EVENT_DURATION} frames")
print(f"   • Frame Rate: {FRAME_RATE}s")
print("="*70)
print("🎧 Listening... (Press Ctrl+C to stop)\n")

frame_count = 0

try:
    while True:
        start_time = time.time()
        
        # Capture audio
        data = stream.read(frame_len, exception_on_overflow=False)
        frame_data = librosa.util.buf_to_float(data, n_bytes=2, dtype=np.int16)
        
        # Calculate audio energy
        energy = calculate_audio_energy(frame_data)
        
        # Skip processing if silence (optimization)
        if is_silence(frame_data):
            print(f"\r🔇 Frame {frame_count:04d} - Silence detected (energy: {energy:.4f})", end='')
            frame_count += 1
            time.sleep(0.1)
            continue
        
        # Model prediction
        scores, melspec = yamnet.predict(np.reshape(frame_data, [1, -1]), steps=1)
        current_prediction = np.mean(scores, axis=0)
        
        # Apply temporal smoothing
        smoothed_prediction = apply_temporal_smoothing(current_prediction)
        
        # Filter by confidence
        confident_indices = filter_by_confidence(smoothed_prediction, CONFIDENCE_THRESHOLD)
        
        if len(confident_indices) > 0:
            # Get top K from confident predictions
            top_confident = confident_indices[
                np.argsort(smoothed_prediction[confident_indices])[::-1][:TOP_K]
            ]
            
            # Filter by event duration
            stable_events = get_stable_events(top_confident, smoothed_prediction)
            
            # Display results
            processing_time = time.time() - start_time
            display_predictions(stable_events, frame_count, energy, processing_time)
        else:
            print(f"\r🔇 Frame {frame_count:04d} - Low confidence (energy: {energy:.4f})", end='')
        
        frame_count += 1
        
        # Clear old event counters
        if frame_count % 50 == 0:
            event_duration_counter.clear()

except KeyboardInterrupt:
    print("\n\n" + "="*70)
    print("🛑 Stopped by user")
    print(f"📊 Total frames processed: {frame_count}")
    print(f"⏱️  Average frame rate: {frame_count / (time.time() - start_time):.2f} fps")
    print("="*70)
    
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\n✅ Audio stream closed. Goodbye! 👋\n")

