#标准化wav
import os
import librosa
import soundfile as sf

# 定义文件夹路径
folder_path = "/data1/zdm/RIR/clap_val/HDY1/135DGNT"

# 获取文件夹下所有的wav文件
file_list = [file for file in os.listdir(folder_path) if file.endswith(".wav")]

# 遍历每个文件
for file_name in file_list:
    # 拼接文件路径
    file_path = os.path.join(folder_path, file_name)

    # 读取音频文件
    audio, sr = librosa.load(file_path)

    # 标准化音频
    normalized_audio = librosa.util.normalize(audio)

    # 删除原始文件
    os.remove(file_path)

    # 保存标准化后的音频，使用相同的文件名
    sf.write(file_path, normalized_audio, sr)
