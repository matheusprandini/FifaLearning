import numpy as np
import cv2
import time
from Agent import Agent
from Screen import Screen
from Keys import Keys

if __name__ == '__main__':
    
    agent = Agent('test')
    agent.load_move_model('Models/model1.h5')
    agent.load_action_model('Models/model3.h5')
	
    keys = Keys()
    screen = Screen()

    print('Starting running in...')

	# Countdown to start running the agent  
    for i in list(range(4))[::-1]:
        print(i+1)
        time.sleep(1)
	
    paused = False

    while True:
	
        if not paused:
            new_screen = screen.GrabScreenBGR()
            new_screen = cv2.resize(new_screen, (140,80))
            
            move_prediction = agent.predict_move([new_screen.reshape(1,140,80,3)])
            action_prediction = agent.predict_action([new_screen.reshape(1,140,80,3)])[0]
            moves = list(np.around(move_prediction[0]))
            print(moves)
            print(action_prediction)
			
            if moves == [0,0,0,1]:
                agent.right()
            elif moves == [0,0,1,0]:
                agent.down()
            elif moves == [0,1,0,0]:
                agent.up()
            elif moves == [1,0,0,0]:
                agent.left()

            if action_prediction[0] >= 0.85:
                agent.shoot()
            elif action_prediction[1] >= 0.82:
                agent.pass_defend()
            else:
                agent.release_actions()
        
        keys_pressed = keys.KeyCheck()
		
        if 'T' in keys_pressed:
            if paused:
                paused = False
                print('unpaused!')
                time.sleep(1)
            else:
                print('Pausing!')
                paused = True
                time.sleep(1)