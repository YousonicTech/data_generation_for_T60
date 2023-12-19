import wave
import splweighting 
from gen_specgram import Filter_Downsample_Spec
import numpy as np
import matplotlib.pyplot as plt
path = "/data1/zdm/clap/wav/1K/NoNoise/HYBL_1K/five-twelve/five-twelve_five-twelve-ch2_Recording-10-01_N_NdB.wav"
f = wave.open(path, "rb")
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data = f.readframes(nframes)
wave_data = np.frombuffer(str_data, dtype=np.int16)
wave_data.shape = -1, nchannels
wave_data = wave_data.T

for audio_samples_np in wave_data:
    audio_chunk = audio_samples_np[8000:27000]
    
    # chunk_a_weighting = splweighting.weight_signal(audio_chunk, framerate)

    chunk_result, _, _ = Filter_Downsample_Spec(audio_chunk, framerate)
    image = chunk_result[3]
    
    plt.imshow(image,aspect='auto')
    plt.savefig("image4.png")
#plt.plot(clean)
    


