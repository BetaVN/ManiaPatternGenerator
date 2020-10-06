import math
from collections import deque

class AnchorDetection:
    def __init__(self, anchorCheckRange, laneNumber):
        self.anchorLimit = anchorCheckRange
        self.queueLimit = anchorCheckRange * 2 + 1
        self.laneNumber = laneNumber
        self.noteDistribution = []
        self.patternQueue = deque()
        for x in range(self.queueLimit):
            self.patternQueue.append(list())

    def newPattern(self, pattern):
        if (len(self.patternQueue) > self.queueLimit - 1):
            self.patternQueue.popleft()
        self.patternQueue.append(pattern)

    def updateNoteDistribution(self):
        self.noteDistribution = [0] * self.laneNumber
        for x in range(self.anchorLimit):
            for y in self.patternQueue[x * 2 + 1]:
                self.noteDistribution[y - 1] += 1

    def calculateAnchorScore(self, pattern):
        resultScore = 0
        for note in pattern:
            resultScore += self.noteDistribution[note - 1]
        if (len(set(pattern) - set(self.patternQueue[self.queueLimit - 2])) == 0):
            resultScore += 2
        return resultScore
            

                    

