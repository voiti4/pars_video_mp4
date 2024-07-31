# This file contains utilits for finding particular qualities in video frame

def devide_keyframe(arrOfSize):
    maxSize = minSize = arrOfSize[0]
    for el in  arrOfSize:
        if el / minSize > 5:
            maxSize = el
            break
        elif el / minSize < 0.2:
            minSize = el
            break
    else:
        return [minSize, maxSize]
    countMin = countMax = sumMin = sumMax = 0
    for el in arrOfSize:
        if el / maxSize > 0.33:
            sumMax += el
            countMax += 1
        else:
            sumMin += el
            countMin += 1
    return [sumMin / countMin, sumMax / countMax]






# print(devide_keyframe([1, 1, 1, 3, 1, 1.1, 4, 3.5]))