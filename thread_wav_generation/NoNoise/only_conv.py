import os
import numpy as np
import time
from extraLib import strcmp
from  getACECorpusData import getACECorpusData
from  readInT60DRRSubband import readInT60DRRSubband
from  genCorpusStdOut import genCorpusStdOut
import librosa

import soundfile as sf
import datetime
import glob
import random
from option import args
import sys
sys.path.append('../')
from utils import *

random.seed(1234)

def genACECorpusDataset(params):
    ACECorpusData = getACECorpusData(params.readFromServer)
    #funciton logic
    nRoomMicDists = len(params.roomMicDistRange)
    
    nMicConfigs = params.micConfigRange

    nSNRs = len(params.snrRange)
    nNoises = len(params.noiseRange)
    nTalkers = len(params.talkerRange)
    nUtterTypes = len(params.utterRange)

    #T60DRRresultsFile = "/data2/cql/code/augu_data/test_icothief/test_icothief.csv"


    # REVIEW  读取T60_file



    a = params.corpusOutputFolderRoot
    b = params.datasetName
    c = ACECorpusData.ACE_DATA_EXT_SPEECH
    # corpusFolder = os.path.join(params.corpusOutputFolderRoot,params.datasetName,ACECorpusData.ACE_DATA_EXT_SPEECH)
    #corpusFolder = params.corpusOutputFolderRoot+params.datasetName+'/'+ACECorpusData.ACE_DATA_EXT_SPEECH
    corpusFolder = params.corpusOutputFolderRoot
    if not os.path.exists(corpusFolder):

        os.makedirs(corpusFolder)

    #Do the convolving of the files
    results = {} #是为test_id创建一个字典

    for micConfigInd in range(params.micConfigRange):
        #Load the mic config parameters
        
        params.corpusMicConfig = ACECorpusData.MIC_CONFIGs[micConfigInd]
        if "_" in params.corpusMicConfig:
            raise ValueError("命名不允许包含下划线")
        
        if params.corpusMicConfig != args.need_config:
            continue
        if params.corpusMicConfig == ACECorpusData.REC_CONFIG_SINGLE:
            # DO nothing
            params.micConfigGT = params.singleMicConfigGT #赋予它Linch的设备
        else:
            params.micConfigGT = params.corpusMicConfig
        #Generate the output folder mic config name
        micConfigCorpusFolder = os.path.join(corpusFolder , params.corpusMicConfig)

        if not os.path.exists(micConfigCorpusFolder):
            os.makedirs(micConfigCorpusFolder)
            # raise  ValueError('Corpus mic config root folder %s does not exist.  Creating.', micConfigCorpusFolder)


        #Open the output file containing the meta data for each data set
        #还不清楚它为什么要创建一个这样的列表
        #表明测试了多少次吧
        results["testID"]= 1
        #Open an output file.  Deal with the condition where the job is being
        #restarted

        rirFolder = str(params.corpusInputFolderRoot)
        #rirFolder = os.path.join(str(params.corpusInputFolderRoot),str(params.corpusMicConfig))
        #print("rirFolder:",rirFolder)
        time_rir = time.time()
        
        for sourceRIRFileName in glob.glob(rirFolder+"/*.wav"):

            params.Room = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            rir_audio , rir_sr = librosa.load(sourceRIRFileName, sr = params.fs,mono=False)
            rir_audio = rir_audio.T
            print("加载一条rir的时间是:{}".format(time.time()-time_rir))

            #提取不同场景下相应的rir
            source_wav = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            
            #Get the T60 and DRR information
            if rir_audio.ndim == 1:
                params.nChannels = 1
            else:

                _, params.nChannels = rir_audio.shape
            #-------------------------------------------------------这里插入噪音信号-----------------------------------------------------
            dict_noise = {}

            #for chanInd in range(0,params.nChannels):
            #升到只有1到9
            if rir_audio.ndim != 1:
                nChannels = rir_audio.shape[1]
            else:
                nChannels = 1
            for chanInd in range(1, nChannels+1):
                #% Use the original channel from the appropriate mic config from
                # the ground truth data
                # if strcmp(params.corpusMicConfig, ACECorpusData.REC_CONFIG_SINGLE):
                if params.corpusMicConfig == ACECorpusData.REC_CONFIG_SINGLE:
                    channelGT = params.singleMicConfigGTChan
                else:
                    channelGT = chanInd
                    #nChannels = h.shape[1]
                #T60DRRData是从表格读出来的数据
                #TODO 这里需要确认是否要对rowIndex等相应参数进行+-1操作,row_Index是逻辑值二维的，不能用于对list使用，这个还没考虑清楚

            #我将TIMIT数据保存为了一个train.txt/test.txt，我只需遍历这个文件就行了啊！
            with open(ACECorpusData.TIMIT_TRAIN_TXT,encoding = 'gb2312') as read:
                line2 = [lines for lines in read.readlines()]
                if args.speaker_choose_num is not None:
                    line2 = random.sample(line2,args.speaker_choose_num)
                
            # TODO
            # line2 = random.sample(line2, 20)
            for f2 in line2:
                time_timit = time.time()
                wave_file = f2.split("\n")[0]
                
                speaker_root = args.speaker_root
                wave_file = os.path.join(speaker_root, wave_file)
                
                y, sr = librosa.load(wave_file, sr = params.fs,mono=False)
                print("加载timit时间{}".format(time.time()-time_timit))
                rir_audio_int = rir_audio * 32768
                rir_audio_int = rir_audio_int.astype(dtype=np.int16)

                if rir_audio.ndim != 1:
                    revUtter = np.zeros([y.shape[0], rir_audio.shape[1]])
                    for i in range(rir_audio.shape[1]):
                        hh = rir_audio[:, i]
                        data = np.convolve(y, hh)
                        revUtter[:, i] = data[:y.shape[0]]
                else:
                    print("ndim")
                    if args.cut_direct is True: #切除直达声
                        spl_list = SPLCal_List(rir_audio_int, frame_len=args.spl_window)
                        max_spl_idx = np.argmax(spl_list) * args.spl_window
                        new_start_idx = max_spl_idx + 500  # 切除直达声之后的起始位置
                        rir_audio = rir_audio[new_start_idx:]
                        
                    if args.time_disturb == True: # 扰动
                        revUtter = time_disturb(y, rir_audio, args)
                    else: #
                        revUtter = np.convolve(y, rir_audio)[:y.shape[0]]
                        revUtter = np.expand_dims(revUtter, axis=1)

                save_name_list = wave_file.split("/")[-1]
                save_name = save_name_list.split(".")[0]

                params.talkerCodeName = save_name
                if "_" in params.talkerCodeName:
                        raise ValueError("speech命名不允许包含下划线")
                
                results["fullUtterOutFileName"] = os.path.join(micConfigCorpusFolder, '%s_%s_%s_N_NdB.wav'%(
                        params.corpusMicConfig,
                        params.Room,
                        params.talkerCodeName,
                        ))
                time_write = time.time()
                sf.write(results["fullUtterOutFileName"],revUtter,params.fs)
                print("写入文件用时：{}".format(time.time()-time_write))


    print("finishing saving")

