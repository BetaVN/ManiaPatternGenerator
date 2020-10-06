import math
import random
from AnchorDetection import *

#-------------------------------------------------------------------------------------------------------------
# Parameters

# Pattern parameters
laneNumber = 7 
bpm = 195
beatsnap = 4
noteVariation = [4,2,3,2,3,2,3,2,3,2,3,2,3,2,3,2,4,2,3,2,4,2,3,2,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3]
rowNumberOutput = len(noteVariation) * 1
startingOffset = 126768
fullJacksAllowed = False
startingPattern = [2,3,5,7]
startingPatternToggle = True

# Generation parameters
maxRandomizedRow = 10
anchorCheckRange = 2

#-------------------------------------------------------------------------------------------------------------
# Mania Constants

noteExtension = "1,0,0:0:0:0:"
noteCoordinateY = "192"
maxAnchorScore = 1000000

# Code

noteCountOutput = []
while (len(noteCountOutput) < rowNumberOutput):
    noteCountOutput.extend(noteVariation)

notePatternOutput = [] 
previousPatternVector = []
jackPatternDetected = False
anchorDetection = AnchorDetection(anchorCheckRange, laneNumber)
for noteCount in noteCountOutput:
    if (startingPatternToggle == True):
        anchorDetection.newPattern(startingPattern)
        notePatternOutput.append(startingPattern)
        previousPatternVector = startingPattern
        startingPatternToggle = False
    elif (noteCount == 0):
        notePatternOutput.append(list())
        previousPatternVector = []
        anchorDetection.newPattern(list())
        anchorDetection.updateNoteDistribution()
    else:
        jackPatternDetected = True if (noteCount + len(previousPatternVector) > laneNumber) else False
        availableLane = list(range(1, laneNumber + 1))
        if ((fullJacksAllowed == False) and (jackPatternDetected == False)):
            availableLane = [i for i in availableLane if i not in previousPatternVector]
        anchorScore = maxAnchorScore
        preferredPattern = []
        anchorDetection.updateNoteDistribution()
        for x in range(maxRandomizedRow):
            random.shuffle(availableLane)
            newAnchorScore = anchorDetection.calculateAnchorScore(availableLane[:noteCount])
            if (anchorScore >= newAnchorScore):
                anchorScore = newAnchorScore
                preferredPattern = availableLane[:noteCount]
        anchorDetection.newPattern(preferredPattern)
        previousPatternVector = preferredPattern
        notePatternOutput.append(preferredPattern)

beatsnapDuration = (60000 / bpm) / beatsnap
laneGap = 512 / (laneNumber * 2)
currentTimestamp = startingOffset
currentRowCount = 0
output = open("output.txt", "w")

for notes in notePatternOutput:
    if currentRowCount > rowNumberOutput:
        break
    else:
        for noteLaneID in notes:
            laneID = math.floor((noteLaneID * 2 - 1) * laneGap)
            output.write(str(laneID) + "," + noteCoordinateY + "," +
                  str(round(currentTimestamp)) + "," + noteExtension +  "\n")
        currentRowCount += 1
        currentTimestamp += beatsnapDuration

output.close()
