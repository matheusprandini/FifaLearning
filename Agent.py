import numpy as np
import cv2
import time
from Screen import Screen
from Model import Model
from Keys import Keys, W, A, S, D, L, SPACE

class Agent():

    def __init__(self, name):
	    self.name = name
	    self.keyboard = Keys()
	    self.move_model = None
	    self.action_model = None

    def right(self):
        self.keyboard.PressKey(D)
        self.keyboard.ReleaseKey(W)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(S)

    def left(self):
        self.keyboard.PressKey(A)
        self.keyboard.ReleaseKey(W)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(S)

    def up(self):
        self.keyboard.PressKey(W)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(S)

    def down(self):
        self.keyboard.PressKey(S)
        self.keyboard.ReleaseKey(A)
        self.keyboard.ReleaseKey(D)
        self.keyboard.ReleaseKey(W)
    
    def shoot(self):
        self.keyboard.ReleaseKey(L)
        self.keyboard.PressKey(SPACE)
        time.sleep(0.22)
        self.keyboard.ReleaseKey(SPACE)
    
    def pass_defend(self):
        self.keyboard.PressKey(L)
        self.keyboard.ReleaseKey(SPACE)

    def release_actions(self):
        self.keyboard.ReleaseKey(L)
        self.keyboard.ReleaseKey(SPACE)
	
    def load_move_model(self, path_file):
        self.move_model = Model.LoadModel(path_file)
		
    def load_action_model(self, path_file):
        self.action_model = Model.LoadModel(path_file)
	
    def predict_move(self, image):
        return self.move_model.predict(image)
	
    def predict_action(self, image):
        return self.action_model.predict(image)
		
if __name__ == '__main__':
    agent = Agent('test')
    agent.left()
    agent.right()
    agent.up()
    agent.down()
    agent.shoot()
    agent.pass_defend()
    agent.release_actions()