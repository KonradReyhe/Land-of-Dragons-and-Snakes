import wave
import struct
import os

def create_placeholder_sound(filename, duration=0.5, frequency=440.0, amplitude=0.5):
    """Create a simple sine wave sound file."""
    # Sound parameters
    sample_rate = 44100
    num_samples = int(duration * sample_rate)
    
    # Create the sound file
    with wave.open(filename, 'w') as wav_file:
        # Set parameters
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 2 bytes per sample
        wav_file.setframerate(sample_rate)
        
        # Generate samples
        for i in range(num_samples):
            t = float(i) / sample_rate
            value = int(32767.0 * amplitude * (i / num_samples))  # Simple fade out
            packed_value = struct.pack('h', value)
            wav_file.writeframes(packed_value)

def main():
    # Ensure the sounds directory exists
    sounds_dir = "assets/sounds"
    os.makedirs(sounds_dir, exist_ok=True)
    
    # Create placeholder sounds
    sounds = [
        "shard_collect",
        "shard_place",
        "serpent_appear",
        "serpent_defeat"
    ]
    
    for sound in sounds:
        filename = os.path.join(sounds_dir, f"{sound}.wav")
        create_placeholder_sound(filename)
        print(f"Created {filename}")

if __name__ == "__main__":
    main() 