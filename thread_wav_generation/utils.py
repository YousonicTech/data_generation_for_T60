import numpy as np

def SPLCal(x):
    Leng = len(x)
    pa = np.sqrt(np.sum(np.power(x, 2))/Leng)
    p0 = 2e-5
    spl = 20 * np.log10(pa / p0)
    return spl

def SPLCal_List(audio,frame_len=100):
    # 分帧计算SPL
    N = len(audio) // frame_len  # 分帧数

    spl = np.zeros(N)
    for k in range(N):
        frame = audio[k*frame_len: (k+1)*frame_len]
        spl[k] = SPLCal(frame)
    return spl

# 用于RIR扰动
def adjust_values(arr, start_idx, end_idx , percent , amplitude_percent):
    # 获取需要调整的元素位置
    indices = np.arange(start_idx, end_idx)
    
    # 计算需要调整的元素个数
    num_adjust = int(len(indices) * percent)
    # 在需要调整的元素中随机选择要增加或减少的值的索引
    adjust_indices = np.random.choice(indices, size=num_adjust, replace=False)
    # 随机生成要增加或减少的百分比
    percentages = np.random.choice([-amplitude_percent, amplitude_percent], size=num_adjust)
    # 根据索引和百分比调整数组的元素
    arr[adjust_indices] = arr[adjust_indices]+arr[adjust_indices] * percentages
    
    return arr

def time_disturb(speech,rir_audio,args):
    N = len(speech) // int(args.time_disturb_window_len)
    revUtter = np.array([])
    for i in range(N):
        start_idx = i * int(args.time_disturb_window_len)
        end_idx = (i + 1) * int(args.time_disturb_window_len)
        temp = speech[start_idx:end_idx]
        rir_audio = adjust_values(rir_audio,0,len(rir_audio)-1,args.time_disturb_percent,args.time_disturb_amplitude_percent)
        temp = np.convolve(temp, rir_audio)[:temp.shape[0]]
        revUtter = np.append(revUtter, temp)
    revUtter = np.expand_dims(revUtter, axis=1)
    return revUtter