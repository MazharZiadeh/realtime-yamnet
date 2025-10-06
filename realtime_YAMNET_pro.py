#!/usr/bin/env python3
"""
PRO Real-time YAMNet with Advanced Features:
- VAD (Voice Activity Detection)
- Multi-resolution analysis
- Confidence calibration
- Event history logging
"""

import pyaudio
import librosa
import numpy as np
import keras
from collections import deque, defaultdict
import time
from datetime import datetime

import yamnet.params as params
import yamnet.yamnet as yamnet_model

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================
class Config:
    # Thresholds
    CONFIDENCE_THRESHOLD = 0.12
    VAD_ENERGY_THRESHOLD = 0.008
    MIN_EVENT_DURATION = 3
    
    # Temporal processing
    TEMPORAL_WINDOW = 7
    WEIGHTED_AVERAGE = True
    WEIGHT_DECAY = 0.85  # Exponential decay for older predictions
    
    # Display
    TOP_K = 5
    SHOW_ENERGY = True
    SHOW_DURATION = True
    SHOW_TREND = True
    
    # Logging
    LOG_EVENTS = True
    LOG_FILE = "yamnet_events.log"
    
    # Performance
    FRAME_RATE = 1.0
    SKIP_SILENCE = True


config = Config()

# ============================================================================
# LOAD MODEL
# ============================================================================
print("🔧 Loading YAMNet PRO model...")
yamnet = yamnet_model.yamnet_frames_model(params)
yamnet.load_weights('yamnet/yamnet.h5')
yamnet_classes = yamnet_model.class_names('yamnet/yamnet_class_map.csv')
print(f"✅ Model loaded! {len(yamnet_classes)} classes ready\n")

# ============================================================================
# STATE TRACKING
# ============================================================================
prediction_history = deque(maxlen=config.TEMPORAL_WINDOW)
event_duration = defaultdict(int)
event_history = []
previous_top_class = None
frame_stats = {'total': 0, 'active': 0, 'silent': 0}

# ============================================================================
# AUDIO SETUP
# ============================================================================
frame_len = int(params.SAMPLE_RATE * config.FRAME_RATE)
p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=params.SAMPLE_RATE,
    input=True,
    frames_per_buffer=frame_len
)

# ============================================================================
# ADVANCED PROCESSING FUNCTIONS
# ============================================================================

def weighted_temporal_smoothing(current_prediction):
    """Exponentially weighted moving average for temporal smoothing"""
    prediction_history.append(current_prediction)
    
    if len(prediction_history) < 2:
        return current_prediction
    
    if config.WEIGHTED_AVERAGE:
        # Apply exponential weights (recent = more weight)
        weights = np.array([config.WEIGHT_DECAY ** i 
                           for i in range(len(prediction_history)-1, -1, -1)])
        weights /= weights.sum()
        
        smoothed = np.average(prediction_history, axis=0, weights=weights)
    else:
        smoothed = np.mean(prediction_history, axis=0)
    
    return smoothed


def vad_energy_based(audio_data):
    """Voice Activity Detection using energy threshold"""
    rms_energy = np.sqrt(np.mean(audio_data**2))
    zero_crossing_rate = np.mean(np.abs(np.diff(np.sign(audio_data)))) / 2
    
    # Combine energy and ZCR for better VAD
    is_active = (rms_energy > config.VAD_ENERGY_THRESHOLD) or (zero_crossing_rate > 0.1)
    
    return is_active, rms_energy, zero_crossing_rate


def calculate_spectral_features(audio_data):
    """Extract additional spectral features"""
    spectral_centroid = np.mean(librosa.feature.spectral_centroid(y=audio_data, sr=params.SAMPLE_RATE))
    spectral_rolloff = np.mean(librosa.feature.spectral_rolloff(y=audio_data, sr=params.SAMPLE_RATE))
    
    return {
        'centroid': spectral_centroid,
        'rolloff': spectral_rolloff
    }


def calibrate_confidence(predictions, alpha=0.5):
    """Simple confidence calibration using temperature scaling"""
    # Sharpen or soften probability distribution
    calibrated = predictions ** (1.0 / (1.0 + alpha))
    return calibrated / calibrated.sum()


def update_event_tracking(class_idx, confidence, is_present):
    """Track event duration and trends"""
    global previous_top_class
    
    if is_present:
        event_duration[class_idx] += 1
        
        # Detect event transitions
        trend = "🔺"  # New or rising
        if previous_top_class == class_idx:
            trend = "▶️"  # Continuing
        elif previous_top_class is not None:
            trend = "🔄"  # Transitioning
        
        previous_top_class = class_idx
    else:
        event_duration[class_idx] = 0
    
    return event_duration[class_idx], trend if is_present else ""


def log_event(class_name, confidence, duration):
    """Log detected events to file"""
    if not config.LOG_EVENTS:
        return
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {class_name:30s} | Conf: {confidence:.3f} | Duration: {duration}s\n"
    
    with open(config.LOG_FILE, 'a') as f:
        f.write(log_entry)


def format_display(events, frame_num, vad_info, spectral_info, proc_time):
    """Rich formatted display"""
    energy, zcr = vad_info['energy'], vad_info['zcr']
    
    print("\n" + "╔" + "="*68 + "╗")
    print(f"║ 📊 Frame {frame_num:04d} │ ⚡ {energy:.4f} │ "
          f"🌊 ZCR: {zcr:.3f} │ ⏱️  {proc_time*1000:.1f}ms" + " " * 8 + "║")
    print("╠" + "="*68 + "╣")
    
    if not events:
        print("║ 🔇 No significant events detected" + " " * 38 + "║")
    else:
        print(f"║ 🎯 Top {len(events)} Detected Events:" + " " * 45 + "║")
        print("╟" + "─"*68 + "╢")
        
        for idx, conf, duration, trend in events:
            bar_width = int(conf * 30)
            bar = "█" * bar_width + "░" * (30 - bar_width)
            
            duration_str = f"[{duration}s]" if config.SHOW_DURATION else ""
            trend_str = trend if config.SHOW_TREND else ""
            
            print(f"║ {yamnet_classes[idx]:20s} │{bar}│ {conf:.3f} {duration_str:6s} {trend_str:3s}║")
    
    print("╚" + "="*68 + "╝")


# ============================================================================
# MAIN PROCESSING LOOP
# ============================================================================
print("╔" + "="*68 + "╗")
print("║" + " "*20 + "🚀 YAMNet PRO Edition" + " "*27 + "║")
print("╠" + "="*68 + "╣")
print(f"║ Confidence Threshold: {config.CONFIDENCE_THRESHOLD:5.2f} │ "
      f"Temporal Window: {config.TEMPORAL_WINDOW:2d} frames" + " " * 18 + "║")
print(f"║ Min Event Duration:   {config.MIN_EVENT_DURATION:5d}s │ "
      f"VAD Threshold:   {config.VAD_ENERGY_THRESHOLD:.4f}" + " " * 19 + "║")
print("╠" + "="*68 + "╣")
print("║ 🎧 Listening for sounds... (Ctrl+C to stop)" + " " * 24 + "║")
print("╚" + "="*68 + "╝\n")

frame_count = 0
start_session = time.time()

try:
    while True:
        start_time = time.time()
        
        # Capture audio
        data = stream.read(frame_len, exception_on_overflow=False)
        frame_data = librosa.util.buf_to_float(data, n_bytes=2, dtype=np.int16)
        
        # VAD - Voice/Audio Activity Detection
        is_active, energy, zcr = vad_energy_based(frame_data)
        frame_stats['total'] += 1
        
        if not is_active and config.SKIP_SILENCE:
            frame_stats['silent'] += 1
            print(f"\r🔇 Frame {frame_count:04d} - Silence (E:{energy:.4f}, ZCR:{zcr:.3f})" + " "*20, end='')
            frame_count += 1
            continue
        
        frame_stats['active'] += 1
        
        # Extract spectral features
        spectral_features = calculate_spectral_features(frame_data)
        
        # Model prediction
        scores, melspec = yamnet.predict(np.reshape(frame_data, [1, -1]), steps=1)
        current_prediction = np.mean(scores, axis=0)
        
        # Calibrate confidence
        calibrated_prediction = calibrate_confidence(current_prediction)
        
        # Temporal smoothing
        smoothed_prediction = weighted_temporal_smoothing(calibrated_prediction)
        
        # Get top predictions
        top_indices = np.argsort(smoothed_prediction)[::-1][:config.TOP_K]
        
        # Filter and track events
        detected_events = []
        for idx in top_indices:
            conf = smoothed_prediction[idx]
            if conf > config.CONFIDENCE_THRESHOLD:
                duration, trend = update_event_tracking(idx, conf, True)
                
                if duration >= config.MIN_EVENT_DURATION:
                    detected_events.append((idx, conf, duration, trend))
                    
                    # Log significant events
                    if duration == config.MIN_EVENT_DURATION:
                        log_event(yamnet_classes[idx], conf, duration)
        
        # Display results
        processing_time = time.time() - start_time
        vad_info = {'energy': energy, 'zcr': zcr}
        
        format_display(detected_events, frame_count, vad_info, spectral_features, processing_time)
        
        frame_count += 1

except KeyboardInterrupt:
    elapsed_time = time.time() - start_session
    
    print("\n\n╔" + "="*68 + "╗")
    print("║ 🛑 Session Ended" + " " * 50 + "║")
    print("╠" + "="*68 + "╣")
    print(f"║ Total Frames:  {frame_stats['total']:6d} │ "
          f"Active: {frame_stats['active']:6d} │ Silent: {frame_stats['silent']:6d}" + " " * 13 + "║")
    print(f"║ Duration:      {elapsed_time:6.1f}s │ "
          f"Avg FPS: {frame_stats['total']/elapsed_time:5.2f}" + " " * 31 + "║")
    if config.LOG_EVENTS:
        print(f"║ Events logged to: {config.LOG_FILE}" + " " * 38 + "║")
    print("╚" + "="*68 + "╝")
    
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    print("\n✅ YAMNet PRO session closed. Goodbye! 👋\n")

