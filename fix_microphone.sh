#!/bin/bash
# Microphone Fix Script for YAMNet
# Run this if your microphone stops working after a reboot

echo "🔧 Fixing microphone configuration..."

# Restart audio services
echo "Restarting audio services..."
systemctl --user restart pipewire pipewire-pulse wireplumber 2>/dev/null || {
    pulseaudio -k 2>/dev/null
    pulseaudio --start 2>/dev/null
}

# Wait for services to initialize
sleep 3

# Set default source to internal DMIC
echo "Setting default microphone source..."
pactl set-default-source alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source 2>/dev/null

# Set optimal volume levels (130% for good sensitivity)
echo "Setting microphone volumes..."
pactl set-source-volume alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source 130% 2>/dev/null
pactl set-source-volume alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__source 130% 2>/dev/null

# Unmute all microphones
echo "Unmuting microphones..."
pactl set-source-mute alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp_6__source 0 2>/dev/null
pactl set-source-mute alsa_input.pci-0000_00_1f.3-platform-skl_hda_dsp_generic.HiFi__hw_sofhdadsp__source 0 2>/dev/null

echo ""
echo "✅ Microphone configuration complete!"
echo ""
echo "Available microphones:"
pactl list sources short | grep "alsa_input"
echo ""
echo "Default source:"
pactl get-default-source
echo ""
echo "🎤 Your microphone is ready for YAMNet!"

