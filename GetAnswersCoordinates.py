import cv2

blackdot = cv2.imread('/Users/abdallaelattar/PycharmProjects/Image Processing/smallblackdot.png', 0)

print("AnswersCoordinates = [")

for j in range(0, 3):
    for i in range(0, 15):
        crop_ModelAnswer = cv2.imread('/Users/abdallaelattar/PycharmProjects/Image Processing/Model Answer Cropped/model' + str(1 + i + 15*j) + '.png', 0)

        resModelAnswer = cv2.matchTemplate(crop_ModelAnswer, blackdot, cv2.TM_CCOEFF_NORMED)

        min_val_ModelAnswer, max_val_ModelAnswer, min_loc_ModelAnswer, max_loc_ModelAnswer = cv2.minMaxLoc(
        resModelAnswer)

        xModelAnswer, yModelAnswer = max_loc_ModelAnswer
        print("[" + str(xModelAnswer) + "," + str(yModelAnswer) + "], ")

print("]")
