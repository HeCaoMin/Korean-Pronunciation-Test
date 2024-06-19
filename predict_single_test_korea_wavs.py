from __future__ import absolute_import
from __future__ import print_function
import os
import sys
import numpy as np


import toolkits
import model
import utils as ut
# ===========================================
#        Parse the argument
# ===========================================
import argparse

parser = argparse.ArgumentParser()
# set up training configuration.设置训练配置。
parser.add_argument('--gpu', default='', type=str)
parser.add_argument('--resume',
                    # default='model/gvlad_softmax/resnet34_vlad8_ghost2_bdim512_deploy/weights.h5',
                    default='model/weights-40-0.968.h5',
                    type=str)
parser.add_argument('--batch_size', default=2, type=int)
parser.add_argument('--data_path', default='../data', type=str)
# set up network configuration. 设置网络配置
parser.add_argument('--net', default='resnet34s', choices=['resnet34s', 'resnet34l'], type=str)
parser.add_argument('--ghost_cluster', default=2, type=int)
parser.add_argument('--vlad_cluster', default=32, type=int)
parser.add_argument('--bottleneck_dim', default=512, type=int)
parser.add_argument('--aggregation_mode', default='gvlad', choices=['avg', 'vlad', 'gvlad'], type=str)
# set up learning rate, training loss and optimizer. 设置学习率、训练损失和优化器
parser.add_argument('--loss', default='softmax', choices=['softmax', 'amsoftmax'], type=str)
parser.add_argument('--test_type', default='normal', choices=['normal', 'hard', 'extend'], type=str)

global args
args = parser.parse_args()


class Model():

    def __init__(self):
        toolkits.initialize_GPU(args)

        self.params = {'dim': (257, None, 1),
                  'nfft': 512,
                  'spec_len': 250,
                  'win_length': 400,
                  'hop_length': 160,
                  'n_classes': 5994,
                  'sampling_rate': 16000,
                  'normalize': True,
                  }

        self.network_eval = model.vggvox_resnet2d_icassp(input_dim=self.params['dim'],
                                                    num_class=self.params['n_classes'],
                                                    mode='eval', args=args)
        # ==> load pre-trained model ???
        if args.resume:
            # ==> get real_model from arguments input,
            # load the model if the imag_model == real_model.
            if os.path.isfile(args.resume):
                self.network_eval.load_weights(os.path.join(args.resume), by_name=True)
                # self.result_path = set_result_path(args)
                # print('==> successfully loading model {}.'.format(args.resume))
            else:
                raise IOError("==> no checkpoint found at '{}'".format(args.resume))
        else:
            raise IOError('==> please type in the model to load')

    def predict_result(self, wav1path, wav2path):
        wav1_specs = ut.load_data(wav1path, win_length=self.params['win_length'], sr=self.params['sampling_rate'],
                             hop_length=self.params['hop_length'], n_fft=self.params['nfft'],
                             spec_len=self.params['spec_len'], mode='eval')
        wav1_specs = np.expand_dims(np.expand_dims(wav1_specs, 0), -1)
        v1 = self.network_eval.predict(wav1_specs)[0]# [] 512个数的数组

        wav2_specs = ut.load_data(wav2path, win_length=self.params['win_length'], sr=self.params['sampling_rate'],
                                  hop_length=self.params['hop_length'], n_fft=self.params['nfft'],
                                  spec_len=self.params['spec_len'], mode='eval')
        wav2_specs = np.expand_dims(np.expand_dims(wav2_specs, 0), -1)
        v2 = self.network_eval.predict(wav2_specs)[0]
        result = []
        '''
        v1 = [x1, x2,x3... x512]
        v2 = [y1, y2, y3... y512]
        result = [x1*y1,x2*y2]
        x1*y1+x2*y2+...+x512*y512=1
        '''
        result += [np.sum(v1 * v2)]
        return result[0]




def set_result_path(args):
    model_path = args.resume
    exp_path = model_path.split(os.altsep)
    result_path = os.path.join('result', exp_path[2], exp_path[3])
    if not os.path.exists(result_path): os.makedirs(result_path)
    return result_path




if __name__ == "__main__":

    model = Model()
    print("同一个音素对比")
    result = model.predict_result("reduce_frenquency/1.WAV", "reduce_frenquency/1_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1.wav", "reduce_frenquency/1_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1_2.wav", "reduce_frenquency/1_3.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/2.WAV", "reduce_frenquency/2_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/2.wav", "reduce_frenquency/2_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/2_2.wav", "reduce_frenquency/2_3.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/3.WAV", "reduce_frenquency/3_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/3.wav", "reduce_frenquency/3_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/3_2.wav", "reduce_frenquency/3_3.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/4.WAV", "reduce_frenquency/4_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/4.wav", "reduce_frenquency/4_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/4_2.wav", "reduce_frenquency/4_3.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/5.WAV", "reduce_frenquency/5_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/5.wav", "reduce_frenquency/5_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/5_2.wav", "reduce_frenquency/5_3.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/6.WAV", "reduce_frenquency/6_2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/6.wav", "reduce_frenquency/6_3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/6_2.wav", "reduce_frenquency/6_3.WAV")
    print(result)
    print("不同一个音素对比")
    result = model.predict_result("reduce_frenquency/1.WAV", "reduce_frenquency/2.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1.wav", "reduce_frenquency/3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1.wav", "reduce_frenquency/4.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1.wav", "reduce_frenquency/5.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/1.wav", "reduce_frenquency/6.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/2.wav", "reduce_frenquency/3.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/2.wav", "reduce_frenquency/4.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/2.wav", "reduce_frenquency/5.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/2.wav", "reduce_frenquency/6.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/3.wav", "reduce_frenquency/4.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/3.wav", "reduce_frenquency/5.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/3.wav", "reduce_frenquency/6.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/4.wav", "reduce_frenquency/5.WAV")
    print(result)
    result = model.predict_result("reduce_frenquency/4.wav", "reduce_frenquency/6.WAV")
    print(result)
    print()
    result = model.predict_result("reduce_frenquency/5.wav", "reduce_frenquency/6.WAV")
    print(result)
    # result = model.predict_result("data/yuan2.wav", "data/zhu7.wav")
    # print(result)
    # result = model.predict_result("data/wav/zhushao-20200220-zsc/wav/zhu6.wav", "data/wav/zhushao-20200220-zsc/wav/zhu7.wav")
    # print(result)
    # result = model.predict_result("data/wav/zhushao-20200220-zsc/wav/zhu6.wav","data/wav/zhushao-20200220-zsc/wav/zhu6.wav")
    # print(result)
    # result = model.predict_result("data/wav/deqing-20200220-zdq/wav/qing6.wav", "data/wav/ruicheng-20200220-zrc/wav/rui6.wav")
    # print(result)
    # result = model.predict_result("data/wav/deqing-20200220-zdq/wav/qing8.wav", "data/wav/deqing-20200220-zdq/wav/qing7.wav")
    # print(result)
    # result = model.predict_most_like(wav1path="data/yuan2.wav", wav2path="data/yuan6.wav",
    #                                  unknownwavpath="data/yuan6.wav")


