# Third Party
import librosa
import numpy as np

# ===============================================
#       code from Arsha for loading data.
# ===============================================
def load_wav(vid_path, sr, mode='train'):
    wav, sr_ret = librosa.load(vid_path, sr=sr)
    assert sr_ret == sr
    if mode == 'train':
        extended_wav = np.append(wav, wav)
        if np.random.random() < 0.3:
            extended_wav = extended_wav[::-1]
        return extended_wav
    else:
        extended_wav = np.append(wav, wav[::-1])
        return extended_wav



def lin_spectogram_from_wav(wav, hop_length, win_length, n_fft=1024):
    linear = librosa.stft(wav, n_fft=n_fft, win_length=win_length, hop_length=hop_length) # linear spectrogram
    return linear.T


def load_data(path, win_length=400, sr=16000, hop_length=160, n_fft=512, spec_len=250, mode='train'):
    '''
    提取语音特征
    :param path:
    :param win_length:
    :param sr:
    :param hop_length:
    :param n_fft:
    :param spec_len:
    :param mode:
    :return:
    '''
    wav = load_wav(path, sr=sr, mode=mode)
    linear_spect = lin_spectogram_from_wav(wav, hop_length, win_length, n_fft)
    mag, _ = librosa.magphase(linear_spect)  # magnitude
    mag_T = mag.T
    freq, time = mag_T.shape
    if mode == 'train':
        # print("time=")
        # print(time)
        # print("spec_len")
        # print(spec_len)
        '''
        你来自哪里
        1 2 3 4 5 1 2 3 4 5
        1234
        2345
        4512哪里你来
        '''

        # randtime = np.random.randint(0, time-spec_len)
        randtime = np.random.randint(0, np.absolute(time - spec_len))
        spec_mag = mag_T[:, randtime:randtime+spec_len]
    else:
        spec_mag = mag_T
    # preprocessing, subtract mean, divided by time-wise var
    mu = np.mean(spec_mag, 0, keepdims=True)
    std = np.std(spec_mag, 0, keepdims=True)
    return (spec_mag - mu) / (std + 1e-5)


if __name__=="__main__":
    a = 1
    data = load_data("media/datasets/voxceleb1/wav/deqing-20200220-zdq/wav/qing1.wav")