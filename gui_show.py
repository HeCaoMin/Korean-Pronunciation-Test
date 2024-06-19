import random
import tkinter as tk
from tkinter import filedialog
import os
import pyaudio
import wave
import threading

from PIL import Image, ImageTk
from predict_single_test_korea_wavs import Model


is_playing = False
my_thread = None
on_hit = False
tmp_file_path = 'tmp_wav'

model = Model()

class Speech_recongnize():
    def __init__(self):

        # GUI工具包的接口

        self.window1 = tk.Tk()
        self.window1.title('Korean Spoken Pronunciation Correction Software Serving the Acquired Deafness')
        self.window1.geometry('650x500')



        self.var = tk.StringVar()
        # 新建Label标签控件，显示一行或多行文本且不允许用户修改，relief参数指定边框样式，anchor参数控制文本在 Label 中显示的位置
        label_ = tk.Label(self.window1, textvariable=self.var, borderwidth=1, relief="sunken", font=('宋体', 12),
                          width=25, height=7, anchor='nw', justify='left', bg="#FFFFFF",wraplength=400)
        label_.place(x=320, y=350)

        self.result_label = tk.Label(self.window1, text="")
        self.result_label.place(x=10, y=340)


        # img_gif = tk.PhotoImage(file='pic/stop.gif')
        # self.label_img = tk.Label(self.window1, image=img_gif)
        # self.label_img.place(x=20, y=370)

        image_path = "pic/stop.gif"
        # image_on_display = ImageTk.PhotoImage(file=image_path)
        # self.label_img = tk.Label(self.window1, image=image_on_display)
        # self.label_img.place(x=20, y=370)

        img = Image.open(image_path)
        img = img.resize((100, 100))  # 调整图片大小
        photo = ImageTk.PhotoImage(img)
        self.label_img = tk.Label(self.window1)
        self.label_img.config(image=photo)
        self.label_img.image = photo
        self.label_img.place(x=20, y=370)

        # self.recommendation_label = tk.Label(self.window1, text="1111111")
        # self.recommendation_label.place(x=400, y=340)




        # 结果输出内容
        self.string_list = []

        # 查询结果输出内容
        self.string_list_chaxun = []

        # 判断tmp_file_path路径是否存在，不存在创建路径
        if not os.path.exists(tmp_file_path):
            os.mkdir(tmp_file_path)
        # 新建Button控件
        self.b = tk.Button(self.window1, text='hit me', borderwidth=0, command=self.hit_me)
        # 定义录音按钮图片
        self.img_start = tk.PhotoImage(file="pic/record.gif")
        # 定义录音停止按钮图片
        self.img_stop = tk.PhotoImage(file="pic/stop.gif")
        # 设置按钮图片
        self.b.config(image=self.img_start)
        self.b.place(x=530, y=360)

        label1_1 = tk.Label(self.window1, text="ㅏ")
        label1_1.place(x=20, y=5)
        label1_2 = tk.Label(self.window1, text="ㅑ")
        label1_2.place(x=60, y=5)
        label1_3 = tk.Label(self.window1, text="ㅓ")
        label1_3.place(x=100, y=5)
        label1_4 = tk.Label(self.window1, text="ㅕ")
        label1_4.place(x=140, y=5)
        label1_5 = tk.Label(self.window1, text="ㅗ")
        label1_5.place(x=180, y=5)
        label1_6 = tk.Label(self.window1, text="ㅛ")
        label1_6.place(x=220, y=5)
        label1_7 = tk.Label(self.window1, text="ㅜ")
        label1_7.place(x=260, y=5)
        label1_8 = tk.Label(self.window1, text="ㅠ")
        label1_8.place(x=300, y=5)
        label1_9 = tk.Label(self.window1, text="ㅡ")
        label1_9.place(x=340, y=5)
        label1_10 = tk.Label(self.window1, text="ㅣ")
        label1_10.place(x=380, y=5)


        label2_1 = tk.Label(self.window1, text="ㄱ")
        label2_1.place(x=5, y=25)
        label2_2 = tk.Label(self.window1, text="ㄴ")
        label2_2.place(x=5, y=45)
        label2_3 = tk.Label(self.window1, text="ㄷ")
        label2_3.place(x=5, y=65)
        label2_4 = tk.Label(self.window1, text="ㄹ")
        label2_4.place(x=5, y=85)
        label2_5 = tk.Label(self.window1, text="ㅁ")
        label2_5.place(x=5, y=105)
        label2_6 = tk.Label(self.window1, text="ㅂ")
        label2_6.place(x=5, y=125)
        label2_7 = tk.Label(self.window1, text="ㅅ")
        label2_7.place(x=5, y=145)
        label2_8 = tk.Label(self.window1, text="ㅇ")
        label2_8.place(x=5, y=165)
        label2_9 = tk.Label(self.window1, text="ㅈ")
        label2_9.place(x=5, y=185)
        label2_10 = tk.Label(self.window1, text="ㅊ")
        label2_10.place(x=5, y=205)
        label2_11 = tk.Label(self.window1, text="ㅋ")
        label2_11.place(x=5, y=225)
        label2_12 = tk.Label(self.window1, text="ㅌ")
        label2_12.place(x=5, y=245)
        label2_13 = tk.Label(self.window1, text="ㅍ")
        label2_13.place(x=5, y=265)
        label2_14 = tk.Label(self.window1, text="ㅎ")
        label2_14.place(x=5, y=285)







        self.k = tk.IntVar()
        ra1 = tk.Radiobutton(self.window1, text="가", variable=self.k, value=1)
        ra2 = tk.Radiobutton(self.window1, text="갸", variable=self.k, value=2)
        ra3 = tk.Radiobutton(self.window1, text="거", variable=self.k, value=3)
        ra4 = tk.Radiobutton(self.window1, text="겨", variable=self.k, value=4)
        ra5 = tk.Radiobutton(self.window1, text="고", variable=self.k, value=5)
        ra6 = tk.Radiobutton(self.window1, text="교", variable=self.k, value=6)
        ra7 = tk.Radiobutton(self.window1, text="구", variable=self.k, value=7)
        ra8 = tk.Radiobutton(self.window1, text="규", variable=self.k, value=8)
        ra9 = tk.Radiobutton(self.window1, text="그", variable=self.k, value=9)
        ra10 = tk.Radiobutton(self.window1, text="기", variable=self.k, value=10)
        ra1.place(x=20, y=25)
        ra2.place(x=60, y=25)
        ra3.place(x=100, y=25)
        ra4.place(x=140, y=25)
        ra5.place(x=180, y=25)
        ra6.place(x=220, y=25)
        ra7.place(x=260, y=25)
        ra8.place(x=300, y=25)
        ra9.place(x=340, y=25)
        ra10.place(x=380, y=25)


        ra11 = tk.Radiobutton(self.window1, text="나", variable=self.k, value=11)
        ra12 = tk.Radiobutton(self.window1, text="냐", variable=self.k, value=12)
        ra13 = tk.Radiobutton(self.window1, text="너", variable=self.k, value=13)
        ra14 = tk.Radiobutton(self.window1, text="녀", variable=self.k, value=14)
        ra15 = tk.Radiobutton(self.window1, text="노", variable=self.k, value=15)
        ra16 = tk.Radiobutton(self.window1, text="뇨", variable=self.k, value=16)
        ra17 = tk.Radiobutton(self.window1, text="누", variable=self.k, value=17)
        ra18 = tk.Radiobutton(self.window1, text="뉴", variable=self.k, value=18)
        ra19 = tk.Radiobutton(self.window1, text="느", variable=self.k, value=19)
        ra20 = tk.Radiobutton(self.window1, text="니", variable=self.k, value=20)
        ra11.place(x=20, y=45)
        ra12.place(x=60, y=45)
        ra13.place(x=100, y=45)
        ra14.place(x=140, y=45)
        ra15.place(x=180, y=45)
        ra16.place(x=220, y=45)
        ra17.place(x=260, y=45)
        ra18.place(x=300, y=45)
        ra19.place(x=340, y=45)
        ra20.place(x=380, y=45)


        ra21 = tk.Radiobutton(self.window1, text="다", variable=self.k, value=21)
        ra22 = tk.Radiobutton(self.window1, text="댜", variable=self.k, value=22)
        ra23 = tk.Radiobutton(self.window1, text="더", variable=self.k, value=23)
        ra24 = tk.Radiobutton(self.window1, text="뎌", variable=self.k, value=24)
        ra25 = tk.Radiobutton(self.window1, text="도", variable=self.k, value=25)
        ra26 = tk.Radiobutton(self.window1, text="됴", variable=self.k, value=26)
        ra27 = tk.Radiobutton(self.window1, text="두", variable=self.k, value=27)
        ra28 = tk.Radiobutton(self.window1, text="듀", variable=self.k, value=28)
        ra29 = tk.Radiobutton(self.window1, text="드", variable=self.k, value=29)
        ra30 = tk.Radiobutton(self.window1, text="디", variable=self.k, value=30)
        ra21.place(x=20,  y=65)
        ra22.place(x=60,  y=65)
        ra23.place(x=100, y=65)
        ra24.place(x=140, y=65)
        ra25.place(x=180, y=65)
        ra26.place(x=220, y=65)
        ra27.place(x=260, y=65)
        ra28.place(x=300, y=65)
        ra29.place(x=340, y=65)
        ra30.place(x=380, y=65)

        ra31 = tk.Radiobutton(self.window1, text="라", variable=self.k, value=31)
        ra32 = tk.Radiobutton(self.window1, text="랴", variable=self.k, value=32)
        ra33 = tk.Radiobutton(self.window1, text="러", variable=self.k, value=33)
        ra34 = tk.Radiobutton(self.window1, text="려", variable=self.k, value=34)
        ra35 = tk.Radiobutton(self.window1, text="로", variable=self.k, value=35)
        ra36 = tk.Radiobutton(self.window1, text="료", variable=self.k, value=36)
        ra37 = tk.Radiobutton(self.window1, text="루", variable=self.k, value=37)
        ra38 = tk.Radiobutton(self.window1, text="류", variable=self.k, value=38)
        ra39 = tk.Radiobutton(self.window1, text="르", variable=self.k, value=39)
        ra40 = tk.Radiobutton(self.window1, text="리", variable=self.k, value=40)
        ra31.place(x=20,  y=85)
        ra32.place(x=60,  y=85)
        ra33.place(x=100, y=85)
        ra34.place(x=140, y=85)
        ra35.place(x=180, y=85)
        ra36.place(x=220, y=85)
        ra37.place(x=260, y=85)
        ra38.place(x=300, y=85)
        ra39.place(x=340, y=85)
        ra40.place(x=380, y=85)

        ra41 = tk.Radiobutton(self.window1, text="마", variable=self.k, value=41)
        ra42 = tk.Radiobutton(self.window1, text="먀", variable=self.k, value=42)
        ra43 = tk.Radiobutton(self.window1, text="머", variable=self.k, value=43)
        ra44 = tk.Radiobutton(self.window1, text="며", variable=self.k, value=44)
        ra45 = tk.Radiobutton(self.window1, text="모", variable=self.k, value=45)
        ra46 = tk.Radiobutton(self.window1, text="묘", variable=self.k, value=46)
        ra47 = tk.Radiobutton(self.window1, text="무", variable=self.k, value=47)
        ra48 = tk.Radiobutton(self.window1, text="뮤", variable=self.k, value=48)
        ra49 = tk.Radiobutton(self.window1, text="므", variable=self.k, value=49)
        ra50 = tk.Radiobutton(self.window1, text="미", variable=self.k, value=50)
        ra41.place(x=20,  y=105)
        ra42.place(x=60,  y=105)
        ra43.place(x=100, y=105)
        ra44.place(x=140, y=105)
        ra45.place(x=180, y=105)
        ra46.place(x=220, y=105)
        ra47.place(x=260, y=105)
        ra48.place(x=300, y=105)
        ra49.place(x=340, y=105)
        ra50.place(x=380, y=105)

        ra51 = tk.Radiobutton(self.window1, text="바", variable=self.k, value=51)
        ra52 = tk.Radiobutton(self.window1, text="뱌", variable=self.k, value=52)
        ra53 = tk.Radiobutton(self.window1, text="버", variable=self.k, value=53)
        ra54 = tk.Radiobutton(self.window1, text="벼", variable=self.k, value=54)
        ra55 = tk.Radiobutton(self.window1, text="보", variable=self.k, value=55)
        ra56 = tk.Radiobutton(self.window1, text="뵤", variable=self.k, value=56)
        ra57 = tk.Radiobutton(self.window1, text="부", variable=self.k, value=57)
        ra58 = tk.Radiobutton(self.window1, text="뷰", variable=self.k, value=58)
        ra59 = tk.Radiobutton(self.window1, text="브", variable=self.k, value=59)
        ra60 = tk.Radiobutton(self.window1, text="비", variable=self.k, value=60)
        ra51.place(x=20,  y=125)
        ra52.place(x=60,  y=125)
        ra53.place(x=100, y=125)
        ra54.place(x=140, y=125)
        ra55.place(x=180, y=125)
        ra56.place(x=220, y=125)
        ra57.place(x=260, y=125)
        ra58.place(x=300, y=125)
        ra59.place(x=340, y=125)
        ra60.place(x=380, y=125)

        ra61 = tk.Radiobutton(self.window1, text="사", variable=self.k, value=61)
        ra62 = tk.Radiobutton(self.window1, text="샤", variable=self.k, value=62)
        ra63 = tk.Radiobutton(self.window1, text="서", variable=self.k, value=63)
        ra64 = tk.Radiobutton(self.window1, text="셔", variable=self.k, value=64)
        ra65 = tk.Radiobutton(self.window1, text="소", variable=self.k, value=65)
        ra66 = tk.Radiobutton(self.window1, text="쇼", variable=self.k, value=66)
        ra67 = tk.Radiobutton(self.window1, text="수", variable=self.k, value=67)
        ra68 = tk.Radiobutton(self.window1, text="슈", variable=self.k, value=68)
        ra69 = tk.Radiobutton(self.window1, text="스", variable=self.k, value=69)
        ra70 = tk.Radiobutton(self.window1, text="시", variable=self.k, value=70)
        ra61.place(x=20,  y=145)
        ra62.place(x=60,  y=145)
        ra63.place(x=100, y=145)
        ra64.place(x=140, y=145)
        ra65.place(x=180, y=145)
        ra66.place(x=220, y=145)
        ra67.place(x=260, y=145)
        ra68.place(x=300, y=145)
        ra69.place(x=340, y=145)
        ra70.place(x=380, y=145)

        ra71 = tk.Radiobutton(self.window1, text="아", variable=self.k, value=71)
        ra72 = tk.Radiobutton(self.window1, text="야", variable=self.k, value=72)
        ra73 = tk.Radiobutton(self.window1, text="어", variable=self.k, value=73)
        ra74 = tk.Radiobutton(self.window1, text="여", variable=self.k, value=74)
        ra75 = tk.Radiobutton(self.window1, text="오", variable=self.k, value=75)
        ra76 = tk.Radiobutton(self.window1, text="요", variable=self.k, value=76)
        ra77 = tk.Radiobutton(self.window1, text="우", variable=self.k, value=77)
        ra78 = tk.Radiobutton(self.window1, text="유", variable=self.k, value=78)
        ra79 = tk.Radiobutton(self.window1, text="으", variable=self.k, value=79)
        ra80 = tk.Radiobutton(self.window1, text="이", variable=self.k, value=80)
        ra71.place(x=20,  y=165)
        ra72.place(x=60,  y=165)
        ra73.place(x=100, y=165)
        ra74.place(x=140, y=165)
        ra75.place(x=180, y=165)
        ra76.place(x=220, y=165)
        ra77.place(x=260, y=165)
        ra78.place(x=300, y=165)
        ra79.place(x=340, y=165)
        ra80.place(x=380, y=165)


        ra81 = tk.Radiobutton(self.window1, text="자", variable=self.k, value=81)
        ra82 = tk.Radiobutton(self.window1, text="쟈", variable=self.k, value=82)
        ra83 = tk.Radiobutton(self.window1, text="저", variable=self.k, value=83)
        ra84 = tk.Radiobutton(self.window1, text="져", variable=self.k, value=84)
        ra85 = tk.Radiobutton(self.window1, text="조", variable=self.k, value=85)
        ra86 = tk.Radiobutton(self.window1, text="죠", variable=self.k, value=86)
        ra87 = tk.Radiobutton(self.window1, text="주", variable=self.k, value=87)
        ra88 = tk.Radiobutton(self.window1, text="쥬", variable=self.k, value=88)
        ra89 = tk.Radiobutton(self.window1, text="즈", variable=self.k, value=89)
        ra90 = tk.Radiobutton(self.window1, text="지", variable=self.k, value=90)
        ra81.place(x=20,  y=185)
        ra82.place(x=60,  y=185)
        ra83.place(x=100, y=185)
        ra84.place(x=140, y=185)
        ra85.place(x=180, y=185)
        ra86.place(x=220, y=185)
        ra87.place(x=260, y=185)
        ra88.place(x=300, y=185)
        ra89.place(x=340, y=185)
        ra90.place(x=380, y=185)

        ra91 = tk.Radiobutton(self.window1, text="차", variable=self.k, value=91)
        ra92 = tk.Radiobutton(self.window1, text="챠", variable=self.k, value=92)
        ra93 = tk.Radiobutton(self.window1, text="처", variable=self.k, value=93)
        ra94 = tk.Radiobutton(self.window1, text="쳐", variable=self.k, value=94)
        ra95 = tk.Radiobutton(self.window1, text="초", variable=self.k, value=95)
        ra96 = tk.Radiobutton(self.window1, text="쵸", variable=self.k, value=96)
        ra97 = tk.Radiobutton(self.window1, text="추", variable=self.k, value=97)
        ra98 = tk.Radiobutton(self.window1, text="츄", variable=self.k, value=98)
        ra99 = tk.Radiobutton(self.window1, text="츠", variable=self.k, value=99)
        ra100 = tk.Radiobutton(self.window1,text="치", variable=self.k, value=100)
        ra91.place(x=20,  y=205)
        ra92.place(x=60,  y=205)
        ra93.place(x=100, y=205)
        ra94.place(x=140, y=205)
        ra95.place(x=180, y=205)
        ra96.place(x=220, y=205)
        ra97.place(x=260, y=205)
        ra98.place(x=300, y=205)
        ra99.place(x=340, y=205)
        ra100.place(x=380,y=205)

        ra101 = tk.Radiobutton(self.window1, text="카", variable=self.k, value=101)
        ra102 = tk.Radiobutton(self.window1, text="캬", variable=self.k, value=102)
        ra103 = tk.Radiobutton(self.window1, text="커", variable=self.k, value=103)
        ra104 = tk.Radiobutton(self.window1, text="켜", variable=self.k, value=104)
        ra105 = tk.Radiobutton(self.window1, text="코", variable=self.k, value=105)
        ra106 = tk.Radiobutton(self.window1, text="쿄", variable=self.k, value=106)
        ra107 = tk.Radiobutton(self.window1, text="쿠", variable=self.k, value=107)
        ra108 = tk.Radiobutton(self.window1, text="큐", variable=self.k, value=108)
        ra109 = tk.Radiobutton(self.window1, text="크", variable=self.k, value=109)
        ra110 = tk.Radiobutton(self.window1, text="키", variable=self.k, value=110)
        ra101.place(x=20,  y=225)
        ra102.place(x=60,  y=225)
        ra103.place(x=100, y=225)
        ra104.place(x=140, y=225)
        ra105.place(x=180, y=225)
        ra106.place(x=220, y=225)
        ra107.place(x=260, y=225)
        ra108.place(x=300, y=225)
        ra109.place(x=340, y=225)
        ra110.place(x=380, y=225)


        ra111 = tk.Radiobutton(self.window1, text="타", variable=self.k, value=111)
        ra112 = tk.Radiobutton(self.window1, text="탸", variable=self.k, value=112)
        ra113 = tk.Radiobutton(self.window1, text="터", variable=self.k, value=113)
        ra114 = tk.Radiobutton(self.window1, text="텨", variable=self.k, value=114)
        ra115 = tk.Radiobutton(self.window1, text="토", variable=self.k, value=115)
        ra116 = tk.Radiobutton(self.window1, text="툐", variable=self.k, value=116)
        ra117 = tk.Radiobutton(self.window1, text="투", variable=self.k, value=117)
        ra118 = tk.Radiobutton(self.window1, text="튜", variable=self.k, value=118)
        ra119 = tk.Radiobutton(self.window1, text="트", variable=self.k, value=119)
        ra120 = tk.Radiobutton(self.window1, text="티", variable=self.k, value=120)
        ra111.place(x=20,  y=245)
        ra112.place(x=60,  y=245)
        ra113.place(x=100, y=245)
        ra114.place(x=140, y=245)
        ra115.place(x=180, y=245)
        ra116.place(x=220, y=245)
        ra117.place(x=260, y=245)
        ra118.place(x=300, y=245)
        ra119.place(x=340, y=245)
        ra120.place(x=380, y=245)

        ra121 = tk.Radiobutton(self.window1, text="파", variable=self.k, value=121)
        ra122 = tk.Radiobutton(self.window1, text="퍄", variable=self.k, value=122)
        ra123 = tk.Radiobutton(self.window1, text="퍼", variable=self.k, value=123)
        ra124 = tk.Radiobutton(self.window1, text="펴", variable=self.k, value=124)
        ra125 = tk.Radiobutton(self.window1, text="포", variable=self.k, value=125)
        ra126 = tk.Radiobutton(self.window1, text="표", variable=self.k, value=126)
        ra127 = tk.Radiobutton(self.window1, text="푸", variable=self.k, value=127)
        ra128 = tk.Radiobutton(self.window1, text="퓨", variable=self.k, value=128)
        ra129 = tk.Radiobutton(self.window1, text="프", variable=self.k, value=129)
        ra130 = tk.Radiobutton(self.window1, text="피", variable=self.k, value=130)
        ra121.place(x=20,  y=265)
        ra122.place(x=60,  y=265)
        ra123.place(x=100, y=265)
        ra124.place(x=140, y=265)
        ra125.place(x=180, y=265)
        ra126.place(x=220, y=265)
        ra127.place(x=260, y=265)
        ra128.place(x=300, y=265)
        ra129.place(x=340, y=265)
        ra130.place(x=380, y=265)

        ra131 = tk.Radiobutton(self.window1, text="하", variable=self.k, value=131)
        ra132 = tk.Radiobutton(self.window1, text="햐", variable=self.k, value=132)
        ra133 = tk.Radiobutton(self.window1, text="허", variable=self.k, value=133)
        ra134 = tk.Radiobutton(self.window1, text="혀", variable=self.k, value=134)
        ra135 = tk.Radiobutton(self.window1, text="호", variable=self.k, value=135)
        ra136 = tk.Radiobutton(self.window1, text="효", variable=self.k, value=136)
        ra137 = tk.Radiobutton(self.window1, text="후", variable=self.k, value=137)
        ra138 = tk.Radiobutton(self.window1, text="휴", variable=self.k, value=138)
        ra139 = tk.Radiobutton(self.window1, text="흐", variable=self.k, value=139)
        ra140 = tk.Radiobutton(self.window1, text="히", variable=self.k, value=140)
        ra131.place(x=20,  y=285)
        ra132.place(x=60,  y=285)
        ra133.place(x=100, y=285)
        ra134.place(x=140, y=285)
        ra135.place(x=180, y=285)
        ra136.place(x=220, y=285)
        ra137.place(x=260, y=285)
        ra138.place(x=300, y=285)
        ra139.place(x=340, y=285)
        ra140.place(x=380, y=285)

        self.Wav_Random_Button = tk.Button(self.window1, text="무작위 단어", command=self.random_wav)
        self.Wav_Random_Button.place(x=450, y=50)

        self.Remove_Button = tk.Button(self.window1, text="취소", command=self.remove_wav)
        self.Remove_Button.place(x=570, y=50)



        self.select_random_wav = tk.StringVar()
        self.Random_Wav_Entry = tk.Entry(self.window1, textvariable=self.select_random_wav)
        self.Random_Wav_Entry.place(x=450, y=100)




        self.Wav_Label = tk.Label(self.window1, text="오디오 선택：")
        self.Wav_Label.place(x=10, y=310)

        self.select_path_wav = tk.StringVar()
        self.Wav_Entry = tk.Entry(self.window1, textvariable=self.select_path_wav)
        self.Wav_Entry.place(x=100, y=310)

        self.Wav_Select_Button = tk.Button(self.window1, text="검색", command=self.select_file_wav)
        self.Wav_Select_Button.place(x=300, y=310)

        self.Wav_Asr_Button = tk.Button(self.window1, text="시작", command=self.wav_asr)
        self.Wav_Asr_Button.place(x=520, y=310)


        self.korea_words_list = ["가을", "메기", "김기", "온갖", "공기",
                                 "각도", "추억담", "옥수수", "거울", "사막",
                                 "저녁", "비록", "고양이", "구름", "기침",
                                 "아가", "악어", "수고", "고구마", "다람쥐",
                                 "아들", "감독", "대문", "디귿", "도자기",
                                 "두부", "수달", "마대", "마디", "파도",
                                 "솓가락"
                                 ]

        self.korea_word = ""
        # 加载窗口，一次又一次地循环
        self.window1.mainloop()

    def remove_wav(self):
        self.select_random_wav.set("")



    def random_wav(self):
        korea_words = []

        for i in os.listdir("korea_words/"):
            print(i)
            korea_words.append(i.split(".wav")[0])
        # korea_words = [ i.split(".")[0] for i in os.listdir("kerea_words/")]
        random_int = random.randint(0, len(korea_words))

        self.korea_word = korea_words[random_int]

        self.select_random_wav.set(self.korea_words_list[random_int])

    def select_file_wav(self):
        # 单个文件选择

        selected_file_path = filedialog.askopenfilename()  # 使用askopenfilename函数选择单个文件
        self.select_path_wav.set(selected_file_path)

    def wav_asr(self):

        print(self.select_random_wav.get())
        if self.select_random_wav.get() != "":
            wavpath1 = "korea_words/" + self.korea_word + ".wav"
        else:
            wavpath1 = "reduce_frenquency/"+str(self.k.get())+".WAV"
        wavpath2 = self.select_path_wav.get()

        similarity = model.predict_result(wavpath1, wavpath2)
        print(similarity)
        if similarity >= 0.75:
            self.result_label["text"] = "○，당신의 발음이 맞습니다"
            self.result_label["foreground"] = "green"

            image_path = "pic/stop.gif"
            img = Image.open(image_path)
            img = img.resize((100, 100))  # 调整图片大小
            photo = ImageTk.PhotoImage(img)
            self.label_img = tk.Label(self.window1)
            self.label_img.config(image=photo)
            self.label_img.image = photo
            self.label_img.place(x=20, y=370)

            self.var.set("")
        else:
            self.result_label["text"] = "X,당신의 발음은 표준이 아닙니다"
            self.result_label["foreground"] = "red"


            image_path = "pic/record.gif"
            img = Image.open(image_path)
            img = img.resize((100, 100))  # 调整图片大小
            photo = ImageTk.PhotoImage(img)
            self.label_img = tk.Label(self.window1)
            self.label_img.config(image=photo)
            self.label_img.image = photo
            self.label_img.place(x=20, y=370)



            self.var.set("Wrong pronunciation.")









    def hit_me(self):
        # 按钮操作，按一下开启录音，再按一下暂停，如此循环
        # #用global使用定义在函数外的变量的值
        global on_hit
        global wave_name

        # 开启录音
        if on_hit == False:
            self.b.config(image=self.img_stop)
            # 构成完整文件存储路径
            self.var.set("Recording...")

            wav_length = str(len(os.listdir("tmp_wav/"))+1)
            wave_name = 'tmp_wav/'+ wav_length+ '.wav'

            self.press_button_record(wave_name)
            on_hit = True
        # 结束录音并调用模型进行语音识别
        else:
            self.b.config(image=self.img_start)
            self.press_button_stop()
            self.var.set("结束录音...")

            if self.select_random_wav.get() != "":
                wavpath1 = "korea_words/" + self.korea_word + ".wav"
            else:
                wavpath1 = "reduce_frenquency/" + str(self.k.get()) + ".WAV"


            # wavpath1 = self.select_path_Standard_wav.get()

            similarity = model.predict_result(wavpath1, wave_name)
            print(similarity)
            if similarity >= 0.75:

                self.result_label["text"] = "○，당신의 발음이 맞습니다"
                self.result_label["foreground"] = "green"
                image_path = "pic/stop.gif"
                img = Image.open(image_path)
                img = img.resize((100, 100))  # 调整图片大小
                photo = ImageTk.PhotoImage(img)
                self.label_img = tk.Label(self.window1)
                self.label_img.config(image=photo)
                self.label_img.image = photo
                self.label_img.place(x=20, y=370)

                self.var.set("")
            else:
                self.result_label["text"] = "X,당신의 발음은 표준이 아닙니다"
                self.result_label["foreground"] = "red"

                

                image_path = "pic/record.gif"
                img = Image.open(image_path)
                img = img.resize((100, 100))  # 调整图片大小
                photo = ImageTk.PhotoImage(img)
                self.label_img = tk.Label(self.window1)
                self.label_img.config(image=photo)
                self.label_img.image = photo
                self.label_img.place(x=20, y=370)

                self.var.set("Wrong pronunciation.")
            on_hit = False



    def press_button_stop(self):
        global is_playing
        global my_thread

        # 如正is_playing为True, 结束录音
        if is_playing:
            is_playing = False
            my_thread.join()

    def press_button_record(self, wave_name):
        global is_playing
        global my_thread
        # 如果is_playing为False，则建立线程开始录音
        if not is_playing:
            is_playing = True
            my_thread = threading.Thread(target=self.input_voice_recording, args=(wave_name,))
            my_thread.start()

    def input_voice_recording(self, wave_name):
        global is_playing
        # 设置默认参数
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)
        # print("Recording...")
        frames = []

        # 录音中
        while is_playing:
            data = stream.read(CHUNK)
            frames.append(data)
        # print("录音完成!")

        # 结束录音
        stream.stop_stream()
        stream.close()
        p.terminate()

        # 保存录音文件
        wf = wave.open(wave_name, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

        wf.close()

    def save_audio_to_wav(self, filename, data):
        # wb只写二进制
        wf = wave.open(filename, 'wb')
        # 设置通道数
        wf.setnchannels(1)
        # 比特宽度 每一帧的字节数
        wf.setsampwidth(2)
        # 帧率  每秒有多少帧
        wf.setframerate(2000)
        # 连接读取进来的文字
        wf.writeframes(b"".join(data))
        # 关闭文件
        wf.close()





if __name__ == "__main__":
    Speech_recongnize()



