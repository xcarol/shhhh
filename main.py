import pyaudio
import wave
from pydub import AudioSegment

def record_audio(filename, duration, channels=1, rate=44100, frames_per_buffer=1024):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=channels,
                    rate=rate,
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    
    frames = []
    print("Recording...")
    for _ in range(0, int(rate / frames_per_buffer * duration)):
        data = stream.read(frames_per_buffer)
        frames.append(data)
    print("Recording finished.")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()

def play_audio(filename):
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)
    
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)
    
    stream.stop_stream()
    stream.close()
    p.terminate()

def analyze_audio(filename, threshold_db=-30.0, min_duration=2000, max_duration=3000):
    audio = AudioSegment.from_wav(filename)
    loud_chunks = [chunk for chunk in audio[::1000] if chunk.dBFS > threshold_db]

    for chunk in audio[::1000]:
        print(f"Detected a loud chunk at {chunk.dBFS} dB.")
            
    if len(loud_chunks) * 1000 >= min_duration and len(loud_chunks) * 1000 <= max_duration:
        print(f"There are between {min_duration/1000} and {max_duration/1000} seconds where the volume is above {threshold_db} dB.")
    else:
        print(f"The volume does not meet the criteria.")

if __name__ == "__main__":
    record_audio("shhhh.wav", 5)
    analyze_audio("shhhh.wav")
    