import numpy as np
import cv2
import time
import os
from Screen import Screen
from Keys import Keys

class Data():

    def __init__(self, file_name='training_data.npy'):
        self.file_name = file_name
        self.path_file = 'Data/' + file_name
        self.training_data = self.InitializeTrainingData()        

    def InitializeTrainingData(self):
        if os.path.isfile(self.path_file):
            print('File exists, loading previous data!')
            return list(np.load(self.path_file))
        print('File does not exist, creating file!')
        return []

    def CreateTrainingData(self):
        keys = Keys()
        screen = Screen()
        print('Starting Training in...')

        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False
        last_time = time.time()
        while True:
	
            if not paused:
                grabbed_screen = screen.GrabScreenBGR()
                new_screen = cv2.resize(grabbed_screen, (140,80))
                keys_pressed = keys.KeyCheck()
                output_move = keys.KeysMovementOutput(keys_pressed)
                output_action = keys.KeysActionOutput(keys_pressed)
                self.training_data.append([new_screen,output_move,output_action])
                #print('Frame took {} seconds'.format(time.time()-last_time))
                #last_time = time.time()
            
            if len(self.training_data) % 1000 == 0:
                print(len(self.training_data))
                
            keys_pressed = keys.KeyCheck()
            if 'T' in keys_pressed:
                if paused:
                    paused = False
                    print('Unpausing training...')
                    time.sleep(2)
                else:
                    print('Pausing training!')
                    paused = True
                    time.sleep(1)
            if 'P' in keys_pressed:
                np.save(self.path_file,self.training_data)	

if __name__ == '__main__':
    data = Data()
    data.CreateTrainingData()