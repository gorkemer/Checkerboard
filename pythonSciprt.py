"""
Flickering checker board annuli, nTrials with each having 2 condition (stimulus and blank) within each 'trial', and the size of the stimulus block alternates between 'large' and 'small' sizes.

# Make two wedges (in opposite contrast) and alternate (flash) them. THere is fixation task, where the observers were asked to respond the color of changes of the fixation square. The color of the fixation square changes from its original color to either 'yellow' or 'red' randomly for the duration of 3 frames (16x3 ms). Users were asked to press '1' for red, and '4' for yellow, and the responses are saved to the response list variable. 


    run it with practice: 0, if you write '1' on there it will wait for key press '6', then initiates 24 seconds long blank block period. This is implemented for the purpose of conducting experiment in fMRI, 6 denotes the trigger box's command.)

"""
from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
from random import choice, randrange, shuffle
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import time
from psychopy.tools.filetools import fromFile, toFile
import csv
#Data Handling


try: #try to get a previous parameters file
    expInfo = fromFile('lastParams.pickle')
except:#if not there then use a default set
    expInfo = {'observer':'','practice': 1} #add more if you want # 'InitialPosition':0
expInfo['dateStr']= data.getDateStr() #add the current time
#present a dialogue to change params
dlg = gui.DlgFromDict(expInfo, title='Gabor', fixed=['dateStr'])

#make a text file to save data
fileName = expInfo['observer'] + expInfo['dateStr']


#initializing windows and experiment parameters
win = visual.Window([1920,1080], units = 'deg', monitor = 'Umram', color = 'gray',fullscr=True)
win.setRecordFrameIntervals(True)
globalClock = core.Clock()

refRate = 60  # 1 second
nTrials = 12
stimDur = refRate * 12 # 12 seconds stimulus presentation duration

largeStim = 8.05  #stimulus size by degree
smallStim = 1.67

t = 0

flashPeriod = 0.1  # seconds for one B-W cycle (i.e. 0.01 = 1/Hz)
responses = []
colorlist = []
trialList = []
keyList = []
response = None


#defining colors with RGB protocol
yellow = [1,1,-1]
black = [-1,-1,-1]
red = [1,-1,-1]

# Make two wedges (in opposite contrast) and alternate them for flashing
wedge1 = visual.RadialStim(win, tex='sqrXsqr', color=1, size=largeStim, pos = (-9.06,0),
    visibleWedge=[0, 360], radialCycles=2, angularCycles=5, interpolate=False,
    autoLog=False)  # this stim changes too much for autologging to be useful
wedge2 = visual.RadialStim(win, tex='sqrXsqr', color=-1, size=largeStim, pos = (-9.06,0),
    visibleWedge=[0, 360], radialCycles=2, angularCycles=5, interpolate=False,
    autoLog=False)  # this stim changes too much for autologging to be useful
wedge3 = visual.RadialStim(win, tex='sqrXsqr', color=1, size=largeStim, pos = (9.06,0),
    visibleWedge=[0, 360], radialCycles=2, angularCycles=5, interpolate=False,
    autoLog=False)  # this stim changes too much for autologging to be useful
wedge4 = visual.RadialStim(win, tex='sqrXsqr', color=-1, size=largeStim, pos = (9.06,0),
    visibleWedge=[0, 360], radialCycles=2, angularCycles=5, interpolate=False,
    autoLog=False)  # this stim changes too much for autologging to be useful

fixationColored = visual.GratingStim(win, size=0.5, pos=[0,0], sf=0,color = red, colorSpace = 'rgb')
fixationRegular = visual.GratingStim(win, size=0.5, pos=[0,0], sf=0,color = black,colorSpace = 'rgb')


def pickingTheNew(magicFrame):
    '''' randomly decides on the 'magic' frame from a l
        ist of 0 to 30 frames, where the fixation color changes '''

    NewMagicFrame = choice(range(0,30))
    return NewMagicFrame



##TRIGGER BOX
if expInfo['practice'] == 0:
    event.waitKeys(keyList = ['6'])

    ##24 sec wait
    for times in range(durInitialBlank):
        fixation.draw()
        win.flip()


for trials in range(nTrials):
    print trials
    if trials % 2 == 0: # during the even numbered trials wedges become large
        wedge1.size = largeStim
        wedge2.size = largeStim
        wedge3.size = largeStim
        wedge4.size = largeStim
    else:
        wedge1.size = smallStim
        wedge2.size = smallStim
        wedge3.size = smallStim
        wedge4.size = smallStim
    
    trialList.append(trials)
    responses = []
    colorlist = []
    respWindowEnded = None
    
    for times in range(2): # in each trial there are two conditions: a stimulus presentation block, and a blank block.
        t0 = time.time()
        
        ## initializing important parameters before the frame loop ##
        frameCount = -1  # -1 because first frame should count as 0 in this program
        doThreeTimes = 0
        magicFrame = choice(range(0, 30)) #initial random magic frame
        colorChoice = choice(['yellow', 'red'])
        fixationColored.color = colorChoice
        colorlist.append(colorChoice)
        
        
        ##### Frame Loop ######
        for frames in range(stimDur):
            keys = event.getKeys(keyList=["1", "4", "escape"] )
            if times == 0:
            ###### GABOR PERIOD #######
                t = globalClock.getTime()
                
                if frameCount == magicFrame-1:
                    respWindowEnded = True
                else:
                    respWindowEnded = False
                if t % flashPeriod < flashPeriod / 2.0:  #diving with 2 makes the flashperiod equal to 50ms which is 0.05# more accurate to count frames 
                    stim = wedge1
                    stim2 = wedge3
                    #check if it is magicFrame, if so change the color for three frame long.
                    if frameCount >= magicFrame and doThreeTimes < 3: # 0 , 1 , 2 =  3 times
                        fixa = fixationColored
                        doThreeTimes += 1
                        if doThreeTimes == 3:
                            Color_started = True
                    else:
                        fixa = fixationRegular
                else:
                    stim = wedge2
                    stim2 = wedge4
                    if frameCount >= magicFrame and doThreeTimes < 3: 
                        fixa = fixationColored
                        doThreeTimes += 1
                        if doThreeTimes == 3:
                            Color_started = True
                    else:
                        fixa = fixationRegular
                stim.draw()
                stim2.draw()
                fixa.draw()

                
            ######### BLANK PERIOD ###### 
            
            else:
                if frameCount >= magicFrame and doThreeTimes < 3: # 0 , 1 , 2 =  3 times
                        fixa = fixationColored
                        doThreeTimes += 1
                        if doThreeTimes == 3:
                            Color_started = True
                else:
                   fixa = fixationRegular


            for key in keys:
                if key == '1' and Color_started:  #
                    if colorChoice == 'red':
                        response = 1
                    elif colorChoice =='yellow':
                        response = -1
                    responses.append(response)
                    keyList.append(key)
                elif key == '4' and Color_started:
                    if colorChoice == 'yellow':
                        response = 1
                    elif colorChoice == 'red':
                        response = -1
                    responses.append(response)
                    keyList.append(key)
                elif key == 'escape':
                       win.close()
                       core.quit()
                else:
                    response = None
                    responses.append(response)
            
            fixa.draw()
            ## end of the frame ##
            win.flip()
            frameCount += 1
            
            if frameCount >= 60: # One second/round has elapsed, time to reset some stuff
                frameCount = 0
                doThreeTimes = 0
                colorChoice = choice(['yellow','red'])
                fixationColored.color = colorChoice
                pickingTheNew(magicFrame)
                colorlist.append(colorChoice)


        print colorlist
        print responses
        
        t1 = time.time()
        timesTime = t1-t0
        print timesTime
    
    
rows = zip(colorlist,responses,keyList)
with open(fileName+'Checkerboard.csv', 'wb') as f:
    writer = csv.writer(f)
    for row in rows:
        writer.writerow(row)

win.close()
core.quit()
