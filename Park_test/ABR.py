import numpy as np
class Random_ABR(object):
    def __init__(self, state_space, action_space, *args, **kwargs):
        self.state_space = state_space
        self.action_space = action_space

    def get_first_action(self, obs):
        act = 0 #take smallest index
        return act

    def get_action(self, obs, prev_reward, prev_done, prev_info):
        act = np.random.choice(self.action_space)
        return act