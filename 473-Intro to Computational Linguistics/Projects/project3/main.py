import os
import sys

class FSM:
    def __init__(self):
        self.handlers = {}
        self.stateStart = None
        self.endStates = []

    def add_state(self, name, handler, end_state=0):
        name = name.upper()
        self.handlers[name] = handler
        if end_state:
            sel.endStates.append(name)
    def set_start(self, name):
        self.startState = name.upper()

    def run(self, cargo):
         try:
             handler = self.handlers[self.startState]
        
