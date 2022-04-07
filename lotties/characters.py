import json
import streamlit as st

class Character():

    def __init__(self, name):
        self.name = name

    def greeting(self):
        return self._getLottie(self.name, 'greeting')
    
    def still(self):
        return self._getLottie(self.name, 'still')
    
    def thinking(self):
        return self._getLottie(self.name, 'thinking')

    def aha(self):
        return self._getLottie(self.name, 'aha')

    def say(self, message):
        return st.info(f"**{self.name.upper()}**  \n" + message)

    def _getLottie(self, name, motion):
        with open(f'lotties/characters/{name}_{motion}.json') as f:
            lottie = json.load(f)
        return lottie


