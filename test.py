import os

words_dict ={"left": 0, "eight": 1, "nine":2, "bed":3, "cat": 4,
             "tree": 5, "up":6, "dog":7, "four":8, "off":9, "on":10,
             "five": 11, "two": 12, "marvin":13, "stop":14, "bird":15,
             "happy":16, "three":17, "no":18, "six":19, "wow":20,
             "yes":21, "go":22, "zero":23, "down":24, "house":25,
             "one":26, "right":27, "seven":28, "sheila":29}
file = open("train1.txt", encoding="utf-8-sig", mode="w")
num = 0

for i in os.listdir(r"C:\Users\hewan\Downloads\speech_commands_v0.01\speech_commands_v0.01\\"):
    # print(i)
    for j in os.listdir(r"C:\Users\hewan\Downloads\speech_commands_v0.01\speech_commands_v0.01\\"+i+"\\"):

        if j.endswith(".wav") or j.endswith(".WAV"):
            # print(i+j)
            filepath = r"C:\Users\hewan\Downloads\speech_commands_v0.01\speech_commands_v0.01\\"+i+"\\"+j
            file.write(filepath+" "+str(num)+"\n")
    num =num +1

file.close()