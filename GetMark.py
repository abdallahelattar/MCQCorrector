import cv2
import numpy
import math
import sys
import xlrd
from xlutils.copy import copy

AnswersCoordinates = [[120, 4], [161, 4], [80, 5], [80, 6], [203, 7], [80, 8], [161, 9], [161, 9], [80, 10], [162, 10],
                      [80, 10],
                      [121, 13], [162, 13], [162, 13], [121, 14], [66, 5], [188, 6], [106, 6], [147, 7], [106, 8],
                      [188, 9],
                      [147, 10], [188, 10], [106, 10], [188, 11], [147, 11], [188, 12], [188, 13], [106, 13], [147, 14],
                      [118, 7],
                      [118, 7], [199, 9], [158, 9], [117, 10], [158, 10], [117, 10], [158, 11], [158, 11], [76, 11],
                      [117, 11],
                      [117, 12], [158, 13], [158, 13], [117, 14]]


def GetBigBlackDots(image):
    bigblackdot = cv2.imread('/Users/abdallaelattar/PycharmProjects/Image Processing/bigblackdot.png', 0)
    ret, threshold = cv2.threshold(image, 200, 255, cv2.THRESH_BINARY)

    FirstDot = [0, 0]
    SecondDot = [0, 0]
    FirstCount = 0
    SecondCount = 0

    result = cv2.matchTemplate(threshold, bigblackdot, cv2.TM_CCOEFF_NORMED)

    threshold = 0.9
    loc = numpy.where(result >= threshold)
    for point in zip(*loc[::-1]):
        x, y = point
        if x < 500:
            FirstCount += 1
            FirstDot[0] += x
            FirstDot[1] += y
        else:
            SecondCount += 1
            SecondDot[0] += x
            SecondDot[1] += y

    FirstDot[0] = FirstDot[0] / FirstCount
    FirstDot[1] = FirstDot[1] / FirstCount
    SecondDot[0] = SecondDot[0] / SecondCount
    SecondDot[1] = SecondDot[1] / SecondCount
    return (FirstDot, SecondDot)


def RotateImage(image, FirstDot, SecondDot):
    Angle = math.atan(float((SecondDot[1] - FirstDot[1])) / float((SecondDot[0] - FirstDot[0])))
    cols, rows = image.shape

    M = cv2.getRotationMatrix2D((rows / 2, cols / 2), math.degrees(Angle), 1)
    rotated = cv2.warpAffine(image, M, (rows, cols))
    ret, RotatedImage = cv2.threshold(rotated, 200, 255, cv2.THRESH_BINARY)
    return RotatedImage


def GetMark(StudentAnswer):
    blackdot = cv2.imread('/Users/abdallaelattar/PycharmProjects/Image Processing/smallblackdot.png', 0)
    Mark = 0
    threshold = 0
    FirstDotStudent, SecondDotStudent = GetBigBlackDots(StudentAnswer)

    FirstColXPositionStudent = FirstDotStudent[0] + 75
    FirstColYPositionStudent = FirstDotStudent[1] - 730

    for i in range(0, 15):
        crop_StudentAnswer = StudentAnswer[FirstColYPositionStudent + i * 40: FirstColYPositionStudent + 40 + i * 40,
                             FirstColXPositionStudent - 120: FirstColXPositionStudent + 120]

        resStudentAnswer = cv2.matchTemplate(crop_StudentAnswer, blackdot, cv2.TM_CCOEFF_NORMED)
        min_val_StudentAnswer, max_val_StudentAnswer, min_loc_StudentAnswer, max_loc_StudentAnswer = cv2.minMaxLoc(
            resStudentAnswer)

        xStudentAnswer, yStudentAnswer = max_loc_StudentAnswer
        print('for student answer:' + str(i + 1) + "    " + str(xStudentAnswer), str(yStudentAnswer))
        xModelAnswer, yModelAnswer = AnswersCoordinates[i]
        print('for model answer:' + str(i + 1) + "    " + str(xModelAnswer), str(yModelAnswer))

        print('val : ' + str(max_val_StudentAnswer))

        cv2.imwrite('/Users/abdallaelattar/PycharmProjects/Image Processing/temp/student' + str(i + 1) + '.png',
                    crop_StudentAnswer)

        if max_val_StudentAnswer > threshold:
            if math.fabs(xModelAnswer - xStudentAnswer) <= 15 and math.fabs(yModelAnswer - yStudentAnswer) <= 15:
                Mark += 1
                print('grade = 1\n')

    SecondColXPositionStudent = (FirstDotStudent[0] + SecondDotStudent[0]) / 2 + 50
    SecondColYPositionStudent = FirstDotStudent[1] - 730

    for i in range(0, 15):
        crop_StudentAnswer = StudentAnswer[SecondColYPositionStudent + i * 40: SecondColYPositionStudent + 40 + i * 40,
                             SecondColXPositionStudent - 120: SecondColXPositionStudent + 120]

        resStudentAnswer = cv2.matchTemplate(crop_StudentAnswer, blackdot, cv2.TM_CCOEFF_NORMED)
        min_val_StudentAnswer, max_val_StudentAnswer, min_loc_StudentAnswer, max_loc_StudentAnswer = cv2.minMaxLoc(
            resStudentAnswer)

        xStudentAnswer, yStudentAnswer = max_loc_StudentAnswer
        print('for student answer:' + str(i + 16) + "    " + str(xStudentAnswer), str(yStudentAnswer))
        xModelAnswer, yModelAnswer = AnswersCoordinates[i + 15]
        print('for model answer:' + str(i + 16) + "    " + str(xModelAnswer), str(yModelAnswer))

        print('val : ' + str(max_val_StudentAnswer))

        cv2.imwrite('/Users/abdallaelattar/PycharmProjects/Image Processing/temp/student' + str(i + 16) + '.png',
                    crop_StudentAnswer)

        if max_val_StudentAnswer > threshold:
            if math.fabs(xModelAnswer - xStudentAnswer) <= 15 and math.fabs(yModelAnswer - yStudentAnswer) <= 15:
                Mark += 1
                print('grade = 1\n')

    ThirdColXPositionStudent = SecondDotStudent[0]
    ThirdColYPositionStudent = SecondDotStudent[1] - 730

    for i in range(0, 15):
        crop_StudentAnswer = StudentAnswer[ThirdColYPositionStudent + i * 40: ThirdColYPositionStudent + 40 + i * 40,
                             ThirdColXPositionStudent - 120: ThirdColXPositionStudent + 120]

        resStudentAnswer = cv2.matchTemplate(crop_StudentAnswer, blackdot, cv2.TM_CCOEFF_NORMED)
        min_val_StudentAnswer, max_val_StudentAnswer, min_loc_StudentAnswer, max_loc_StudentAnswer = cv2.minMaxLoc(
            resStudentAnswer)

        xStudentAnswer, yStudentAnswer = max_loc_StudentAnswer
        print('for student answer:' + str(i + 31) + "    " + str(xStudentAnswer), str(yStudentAnswer))
        xModelAnswer, yModelAnswer = AnswersCoordinates[i + 30]
        print('for model answer:' + str(i + 31) + "    " + str(xModelAnswer), str(yModelAnswer))

        print('val : ' + str(max_val_StudentAnswer))

        cv2.imwrite('/Users/abdallaelattar/PycharmProjects/Image Processing/temp/student' + str(i + 31) + '.png',
                    crop_StudentAnswer)

        if max_val_StudentAnswer > threshold:
            if math.fabs(xModelAnswer - xStudentAnswer) <= 15 and math.fabs(yModelAnswer - yStudentAnswer) <= 15:
                Mark += 1
                print('grade = 1\n')

    return Mark


image = cv2.imread(sys.argv[1], 0)

FirstDot, SecondDot = GetBigBlackDots(image)
RotatedImage = RotateImage(image, FirstDot, SecondDot)

cv2.imwrite('/Users/abdallaelattar/PycharmProjects/Image Processing/rotated.png', RotatedImage)

Mark = GetMark(RotatedImage)

print('\n\n Mark = ' + str(Mark))

rb = xlrd.open_workbook('markss.xls')
r_sheet = rb.sheet_by_index(0)

max_nb_row = 0
for r_sheet in rb.sheets():
    max_nb_row = max(max_nb_row, r_sheet.nrows)

wb = copy(rb)
sheet = wb.get_sheet(0)
sheet.write(max_nb_row, 0, sys.argv[1])
sheet.write(max_nb_row, 1, str(Mark))
wb.save('markss.xls')
