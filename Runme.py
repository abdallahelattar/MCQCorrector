import os

for soln in os.listdir("/Users/abdallaelattar/PycharmProjects/Image Processing/test/"):
    if soln.endswith(".png"):
        print(soln)
        #raw_input('press enter to continue...')
        os.system("python getmark.py" + " \"/Users/abdallaelattar/PycharmProjects/Image Processing/test/" + soln + "\"")
