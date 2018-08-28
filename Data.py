import numpy as np
import pandas as pd
import cv2
import time
import os
from Screen import Screen
from Keys import Keys
from collections import Counter
from random import shuffle

class Data():

    def __init__(self, file_name='training_data.npy'):
        self.file_name = file_name
        self.path_file = 'Data/' + file_name
        self.training_data = self.InitializeTrainingData()        

	# Load training data if exists, else return an empty list
    def InitializeTrainingData(self):
        if os.path.isfile(self.path_file):
            print('File exists, loading previous data!')
            return list(np.load(self.path_file))
        print('File does not exist, creating file!')
        return []
	
	# Show all data in training data (image, output_move, output_action)
    def validate_data():
        for data in train_data:
            img = data[0]
            output_move = data[1]
            output_action = data[2]
            cv2.imshow('test', img)
            print(output_move, ' ', output_action)
            if cv2.waitKey(25) & 0xFF == ord('q'): # Destroy all images when close the script
                cv2.destroyAllWindows()
                break

	# Create training data
    def CreateTrainingData(self):
        keys = Keys()
        screen = Screen()
        print('Starting Training in...')

		# Countdown to start the training
        for i in list(range(4))[::-1]:
            print(i+1)
            time.sleep(1)
        
        paused = False
        last_time = time.time()
		
        while True:
	
            if not paused:
                grabbed_screen = screen.GrabScreenBGR() # Get actual frame
                new_screen = cv2.resize(grabbed_screen, (140,80)) # Resize frame
                keys_pressed = keys.KeyCheck() # Check for pressed keys
                output_move = keys.KeysMovementOutput(keys_pressed) # Verifies if one move key was pressed
                output_action = keys.KeysActionOutput(keys_pressed) # Verifies if one action key was pressed
                self.training_data.append([new_screen,output_move,output_action]) # Create an instance of training data
            
            if len(self.training_data) % 1000 == 0:
                print(len(self.training_data))
                
            keys_pressed = keys.KeyCheck()
			
			# Pausing or Unpausing training
            if 'T' in keys_pressed:
                if paused:
                    paused = False
                    print('Unpausing training...')
                    time.sleep(2)
                else:
                    print('Pausing training!')
                    paused = True
                    time.sleep(1)
			
			# Saving Data
            if 'P' in keys_pressed:
                np.save(self.path_file,self.training_data)
				
    def BalanceData(self):
        train_data = np.load(self.path_file)
		
		# Convert numpy 'train_data' array to a pandas Dataframe
        df = pd.DataFrame(train_data)

		# Initialize examples
        lefts = []
        rights = []
        forwards = []
        backwards = []
        no_moves = []

        shoots = []
        passes = []
        defend = []
        no_actions = []

		# Randomize instances positions
        shuffle(train_data)

        for data in train_data:
            img = data[0]
            choice_move = data[1]
            choice_action = data[2]

            ## Complete Movement examples
            if choice_move == [1,0,0,0]:
                lefts.append([img,choice_move])
            elif choice_move == [0,1,0,0]:
                forwards.append([img,choice_move])
            elif choice_move == [0,0,1,0]:
                backwards.append([img,choice_move])
            elif choice_move == [0,0,0,1]:
                rights.append([img,choice_move])
            elif choice_move == [0,0,0,0]:
                no_moves.append([img,choice_move])
            else:
                print('No matches corresponding to a movement')
        
            ## Complete Action examples
            if choice_action == [1,0,0]:
                shoots.append([img,choice_action])
            elif choice_action == [0,1,0]:
                passes.append([img,choice_action])
            elif choice_action == [0,0,1]:
                defend.append([img,choice_action])
            elif choice_action == [0,0,0]:
                no_actions.append([img,choice_action])
            else:
                print('No matches corresponding to an action')

		# Balancing movement data examples
        forwards = forwards[:len(lefts)][:len(rights)][:len(backwards)]
        lefts = lefts[:len(forwards)]
        rights = rights[:len(forwards)]
        backwards = backwards[:len(forwards)]

        final_data = forwards + backwards + lefts + rights
        shuffle(final_data)

        print(len(shoots))
        print(len(passes))
        print(len(defend))
        print(len(no_actions))

		# Balancing action data examples
        shoots = shoots[:len(passes)][:len(defend)][:len(no_actions)]
        passes = passes[:len(shoots)]
        defend = defend[:len(shoots)]
        no_actions = no_actions[:len(shoots)]
        final_data_actions = shoots + passes + defend + no_actions
        shuffle(final_data_actions)

        print(len(final_data))
        print(len(final_data_actions))
		
		# Saving balancing data
        np.save('Data/training_move_data.npy', final_data)
        np.save('Data/training_action_data.npy', final_data_actions)

if __name__ == '__main__':
    data = Data()
    #data.CreateTrainingData()
    data.BalanceData()