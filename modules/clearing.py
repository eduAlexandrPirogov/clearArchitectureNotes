class clearing:
    def __init__(self):
        self.isClearing = False
        self.states = ["water", "soap", "brush"]
        self.currentState = self.states[0]

    def start(self):
        self.isClearing = True

    def stop(self):
        self.isClearing = False

    def set(self, state):
        self.currentState = state
