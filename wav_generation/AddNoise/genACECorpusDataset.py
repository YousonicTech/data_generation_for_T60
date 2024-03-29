import os
import numpy as np
import time
from extraLib import strcmp,judgeList,v_addnoise
import wave
import scipy.signal as sg
from  getACECorpusData import getACECorpusData
from  readInT60DRRSubband import readInT60DRRSubband
from  genCorpusStdOut import genCorpusStdOut
import librosa
import csv
from scipy import signal
import soundfile as sf
import datetime
import csv
import glob
import random
from option import args

random.seed(1234)
def genACECorpusDataset(params):
    ACECorpusData = getACECorpusData(params.readFromServer)
    #funciton logic


    nRoomMicDists = len(params.roomMicDistRange)


    nMicConfigs = params.micConfigRange

    nSNRs = args.SNR
    params.snrRange=nSNRs
    # nSNRs = len(params.snrRange)
    nNoises = len(params.noiseRange)
    nTalkers = len(params.talkerRange)
    nUtterTypes = len(params.utterRange)

    #T60DRRresultsFile = "/data2/cql/code/augu_data/test_icothief/test_icothief.csv"

    T60DRRresultsFile = args.T60DRRresultsFile


    # REVIEW  读取T60_file

    T60DRRData = readInT60DRRSubband(T60DRRresultsFile)


    freqBands = np.unique(T60DRRData["freqBand"])

    nFreqBands = len(freqBands)

    speechFolder = os.path.join(params.corpusInputFolderRoot,ACECorpusData.ACE_DATA_EXT_SPEECH)
    

    # Generate the output folder root name
    # corpusFolder = [params.corpusOutputFolderRoot,params.datasetName, '/', ACECorpusData.ACE_DATA_EXT_SPEECH]
    # outptFolder/Dev/Speech
    # corpusFolder = os.path.join(params.corpusOutputFolderRoot,params.datasetName,ACECorpusData.ACE_DATA_EXT_SPEECH)
    
    corpusFolder = params.corpusOutputFolderRoot
    
    #corpusFolder = params.corpusOutputFolderRoot+params.datasetName+'/'+ACECorpusData.ACE_DATA_EXT_SPEECH
    if not os.path.exists(corpusFolder):
        # raise ValueEroor('Corpus root folder %s does not exist.  Creating.'%corpusFolder)
        os.makedirs(corpusFolder)

    #Do the convolving of the files
    results = {} #是为test_id创建一个字典



    for micConfigInd in range(params.micConfigRange):
        #Load the mic config parameters
        params.corpusMicConfig = ACECorpusData.MIC_CONFIGs[micConfigInd]
        if "_" in params.corpusMicConfig:
            raise ValueError("ROOM 名称不允许包含下划线！")
        
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
        results["testID"] = 1
        
        #Open an output file.  Deal with the condition where the job is being
        #restarted
        if params.startOffset == 0:
            #time.strftime("%d:%m:%Y")
            #resultsFileName = micConfigCorpusFolder+'_'+params.testName +'_results.txt'
            dt = datetime.datetime.now()
            resultsFileName = os.path.join(micConfigCorpusFolder,"results.csv")
            print("resultFilename:",resultsFileName)
            resultsHandle = open(resultsFileName, "a", newline="")
            csv_writer = csv.writer(resultsHandle)

                #resultsHandle = csv.writer(csvfile)
        else:
            if strcmp(params.startOffsetDate, ''):
                print('Timestamp for existing file to append not specified.  Should be in format yyyymmddThhmmss')
                # raise ValueEroor('Timestamp for existing file to append not specified.  Should be in format yyyymmddThhmmss')
            resultsFileName = os.path.join(micConfigCorpusFolder,"results.csv")
            print("resultFilename:",resultsFileName)

            resultsHandle = open(resultsFileName, "w", newline="")
            csv_writer = csv.writer(resultsHandle)
            results["testID"] = results["testID"] + params.startOffset
        params.rowsTotal = nRoomMicDists * nMicConfigs * nTalkers * nUtterTypes * nNoises * nSNRs

        rirFolder = str(params.corpusInputFolderRoot)
        print("rirFolder:",rirFolder)
        time_rir = time.time()
        for sourceRIRFileName in glob.glob(rirFolder+"/*.wav"):

            params.Room = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            # print(" params.Room",params.Room)
            h, rir_sr = librosa.load(sourceRIRFileName, sr=params.fs, mono=False)
            h = librosa.util.normalize(h)
            h = h.T
            print("加载一条rir的时间是:{}".format(time.time()-time_rir))

            #提取不同场景下相应的rir
            source_wav = (sourceRIRFileName.split("/")[-1]).split(".")[0]
            utterCsvFileName = "Unknown" + "_" +params.corpusMicConfig+ "_" + source_wav+"_<talker>_<utter>_<noise>_<SNR>dB.wav"
            #Get the T60 and DRR information
            if h.ndim == 1:
                params.nChannels = 1
            else:

                _, params.nChannels = h.shape
            #-------------------------------------------------------这里插入噪音信号-----------------------------------------------------
            dict_noise = {}
            # path = "/data2/TEAM/Noise_TUT/TUT-acoustic-scenes-2017-development/evaluation_setup"
            # audio_root = "/data2/TEAM/Noise_TUT/TUT-acoustic-scenes-2017-development/audio"
            # txt_file = '/data2/cql/code/augu_data/get_data/noise.txt'
            # # with open(txt_file) as f:
            # # 因为噪音文件太多了，一次性生成这么多噪音文件吗
            # with open(txt_file) as read:
            #     line1 = [lines for lines in read.readlines()]
            #----我应该从15个txt文件中生成15个语音-----之后在下面中进行加载
            time_noise = time.time()
            line1 = []
            
            # 15种噪音，每种抽取一个噪音
            for txt_file in glob.glob(args.noise_dir + "/*.txt"):
                # 之后从这个txt_file中随机选择一条
                with open(txt_file) as read:
                    wave_list = [lines for lines in read.readlines()]
                length = len(wave_list)
                num_line = random.randint(0, length-1)
                line1.append(wave_list[num_line])
                
            print("line1:",line1)

            for f1 in line1:

                noiseFileName = f1.split('\n')[0]
                noise, noiseFs = librosa.load(noiseFileName, sr=params.fs, mono=False)
                noise = librosa.util.normalize(noise)
                # Acccount for the noises in Meeting_Room_2 (611)-1 which only have
                # 4 channels for the noise recordings
                noise = noise.T
                if noise.ndim == 1:
                    noiseChannels = 1
                    noise = np.expand_dims(noise, axis=1)
                else:
                    _, noiseChannels = noise.shape

                if noiseChannels != params.nChannels:
                    #通道数不相等，我们可以构造相等的通道数

                    delt_channels = params.nChannels - noiseChannels
                    if delt_channels > 0:
                        new_noise = np.zeros((noise.shape[0],params.nChannels))
                        new_noise[:,:noiseChannels] = noise
                        for i in range(noiseChannels,delt_channels):
                            new_noise[:,i]=noise[:,0]
                    else:

                        new_noise = noise[:,params.nChannels]
                        new_noise = np.expand_dims(new_noise,axis=1)
                    noiseChannels = params.nChannels
                    noise = new_noise



                dict_noise[noiseFileName] = [noise, noiseFs, noiseChannels]
            print("读取15条噪音的时间是:{}".format(time.time() - time_noise))
            #for chanInd in range(0,params.nChannels):
            #升到只有1到9
            if h.ndim != 1:
                nChannels = h.shape[1]
            else:
                nChannels = 1
            for chanInd in range(1,nChannels+1):
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

                for freqBandInd in range(nFreqBands):
                    #因为matlab可以直接判断[1,2,3]==1 -> [1,0,0],而python却不能，所以这里也要做相应的处理

                    # rowIndex = T60DRRData.channel == channelGT & T60DRRData.sessionID == params.sessionID & \
                    #            strcmp(T60DRRData.config, params.micConfigGT) &\
                    #            strcmp(T60DRRData.freqBand, num2str(freqBandInd))
                    judge1 = T60DRRData["channel"]==np.array([channelGT])

                    judge2 = T60DRRData["room"]==np.array(params.Room)
                    judge3 = np.array([T60DRRData["config"][i]==params.micConfigGT for i in range(len(T60DRRData["config"]))])#T60DRRData["config"]== np.array(params.micConfigGT)
                    judge4 = T60DRRData["freqBand"] == np.array([freqBandInd+1])

                    rowIndex = judge1 & judge3 & judge4 & judge2

                    if sum(rowIndex) == 0:
                        print("HEAT")
                        if sum(judge1) == 0:
                            print("HEAT judge1")
                        if sum(judge2) ==0 :
                            print("HEAT judge2")
                        if sum(judge3) == 0:
                            print("HEAT judge3")
                        if sum(judge4) == 0:
                            print("HEAT judge4")
                        continue
                    else:
                        print("PASS")
                    #results.testID already assigned
                    results["channel"] = chanInd
                    #str2double because it is saved as a silly string by mistake
                    # a = T60DRRData["freqBand"]
                    # b = a[rowIndex]
                    # print("T60DRRData:",T60DRRData)

                    results["freqBand"] = T60DRRData["freqBand"][rowIndex]# 11
                    # print("freqBand:",results["freqBand"],"rowindex:",rowIndex)


                    results["centreFreq"] = T60DRRData["centreFreq"][rowIndex]#12
                    results["DRR"] = T60DRRData["DRR"][rowIndex]# 14
                    results["DRRMean"] = T60DRRData["DRRMean"][rowIndex]#15
                    results["T60"] = T60DRRData["T60AHM"][rowIndex]#16
                    results["T60Mean"] = T60DRRData["T60AHMMean"][rowIndex]# 19
                    #Fullband for this channel
                    results["DRRFullband"] = T60DRRData["DRRFullband"][rowIndex]# 22
                    results["T60Fullband"] = T60DRRData["T60AHMFullband"][rowIndex]#24
                    #If single channel, then the fullband mean across all channels is the same
                    # as for this channel
                    if strcmp(params.corpusMicConfig, ACECorpusData.REC_CONFIG_SINGLE):
                        results["DRRFullbandMean"] = T60DRRData["DRRFullband"][rowIndex]#23
                        results["T60FullbandMean"] = T60DRRData["T60AHMFullband"][rowIndex]#27
                    else:

                        results["DRRFullbandMean"] = T60DRRData["DRRFullbandMean"][rowIndex]#23
                        results["T60FullbandMean"] = T60DRRData["T60AHMFullbandMean"][rowIndex]#27
                    results["fileName"] = utterCsvFileName

                    params.roomCodeName =  params.Room
                    if "_" in params.roomCodeName:
                        raise ValueError("具体的rir wav名称不允许包含下划线！")

                    params.roomConfig = params.corpusMicConfig
                    Head,outputLine = genCorpusStdOut(results, params)
                    if Head is not None:
                        csv_writer.writerow(Head)
                    if outputLine is not None:
                        csv_writer.writerow(outputLine)
                    print('%s'%outputLine)
                    print(resultsHandle, '%s'%outputLine)
                    results["testID"] = results["testID"] + 1


            #我将TIMIT数据保存为了一个train.txt/test.txt，我只需遍历这个文件就行了啊！
            with open(ACECorpusData.TIMIT_TRAIN_TXT,encoding = 'gb2312') as read:
                line2 = [lines for lines in read.readlines()]

            for f2 in line2:
                time_timit = time.time()
                wave_file = f2.split("\n")[0]

                Speaker_root = args.Speaker_root
                wave_file = os.path.join(Speaker_root, wave_file)

                y, sr = librosa.load(wave_file, sr = params.fs,mono=False)
                y = librosa.util.normalize(y)
                print("加载timit时间{}".format(time.time()-time_timit))
                if h.ndim != 1:
                    revUtter = np.zeros([y.shape[0], h.shape[1]])
                    for i in range(h.shape[1]):
                        hh = h[:, i]
                        data = np.convolve(y, hh)
                        revUtter[:, i] = data[:y.shape[0]]
                else:
                    revUtter = np.convolve(y, h)[:y.shape[0]]
                    revUtter = np.expand_dims(revUtter, axis=1)
                save_name_list = wave_file.split("/")[-1]
                save_name = save_name_list.split(".")[0]
                params.talkerCodeName = save_name
                if "_" in params.talkerCodeName:
                    raise ValueError("干语料speech名称不允许包含下划线！")
                params.talkerName = save_name


                for f3 in line1:

                    noiseFileName =  f3.split('\n')[0]

                    params.noise = (noiseFileName.split("/")[-1]).split(".")[0]
                    if "_" in params.noise:
                        raise ValueError("noise名称不允许包含下划线！")
                    
                    [noise, noiseFs, noiseChannels] = dict_noise[noiseFileName]
                    for snrInd in range(0,len(params.snrRange)):
                        params.SNR = params.snrRange[snrInd]

                        results["fullUtterOutFileName"] = os.path.join(micConfigCorpusFolder, '%s_%s_%s_%s_%ddB.wav'%(
                        params.corpusMicConfig,
                        params.roomCodeName,
                        params.talkerCodeName,
                        params.noise,
                        params.SNR))

                        if not os.path.exists(results["fullUtterOutFileName"]) or params.overwriteWavFiles:

                            if not params.noWriteMode:

                                noisyRevUtter = np.zeros([len(revUtter), params.nChannels])
                                # Process each channel of the signal separately
                                for chanInd in range(params.nChannels):
                                    #For 611-1 which only has 4 channels in the Lin8Ch noises, use the last existing
                                    # % noise channel.  Since v_addnoise selects a random excerpt of the
                                    #% noise, the noise will not be correlated with the other channels
                                    lastExistingChannel = noiseChannels
                                    begin = time.time()
                                    if chanInd > noiseChannels:

                                        noisyRevUtter[:, chanInd]= v_addnoise(
                                        revUtter[:, chanInd], params.fs, params.SNR, '', noise[:, lastExistingChannel], params.fs)
                                    else:
                                        noisyRevUtter[:, chanInd]= v_addnoise(
                                        revUtter[:, chanInd],noise[:, chanInd], params.SNR)
                                    print("all use time:",time.time() - begin)


                            #Normalise the data to +/- 1.0
                            noisyRevUtter = noisyRevUtter / np.max(np.abs(noisyRevUtter))
                            #Write out the .wav file containing the speech

                            time_write = time.time()
                            
                            
                            sf.write(results["fullUtterOutFileName"],noisyRevUtter,params.fs)
                            print("写入文件用时：{}".format(time.time()-time_write))
        resultsHandle.close()

    print("finishing saving")








