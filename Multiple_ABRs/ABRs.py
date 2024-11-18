import numpy as np
import math
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

class ThroughputRule(object):
    def __init__(self, state_space, action_space, *args, **kwargs):
        self.state_space = state_space
        self.action_space = action_space
        self.th_est_sliding = SlidingWindow()
        self.th_est_ewma = Ewma()
        self.safety_factor = 0.9
        self.low_buffer_safety_factor = 0.5
        self.low_buffer_safety_factor_init = 0.9
        self.abandon_multiplier = 1.8
        self.abandon_grace_time = 500

    def get_first_action(self, obs):
        act = 0 #take smallest index
        return act

    def get_action(self, obs, prev_reward, prev_done, prev_info):
        # segment time in milliseconds=4000 in this case
        # bitrates in Kbps
        # tput = Kbps/second
        p = 4000  # ms
        bitrates = [i * 1000 for i in [0.3, 0.75, 1.2, 1.85, 2.85, 4.3]]  # Kbps
        quality = 0
        last_known_throughput = obs[0] * 8 / 1000  # Kbps
        ##for calculating estimated throughput with ewma
        #old_download_time = obs[1]*1000  # past download time in seconds
        #estimated_throughput_ewma = self.th_est_ewma.push(old_download_time, last_known_throughput)

        estimated_throughput = self.th_est_sliding.push(last_known_throughput)
        while (quality + 1 < len(bitrates) and p * bitrates[quality + 1] / estimated_throughput <= p):
            quality += 1
        act = quality
        return act

class ThroughputRuleEWMA(object):
    def __init__(self, state_space, action_space, *args, **kwargs):
        self.state_space = state_space
        self.action_space = action_space
        self.th_est_sliding = SlidingWindow()
        self.th_est_ewma = Ewma()
        self.safety_factor = 0.9
        self.low_buffer_safety_factor = 0.5
        self.low_buffer_safety_factor_init = 0.9
        self.abandon_multiplier = 1.8
        self.abandon_grace_time = 500

    def get_first_action(self, obs):
        act = 0 #take smallest index
        return act

    def get_action(self, obs, prev_reward, prev_done, prev_info):
        # segment time in milliseconds=4000 in this case
        # bitrates in Kbps
        # tput = Kbps/second
        p = 4000  # ms
        bitrates = [i * 1000 for i in [0.3, 0.75, 1.2, 1.85, 2.85, 4.3]]  # Kbps
        quality = 0
        last_known_throughput = obs[0] * 8 / 1000  # Kbps
        old_download_time = obs[1]*1000  # past download time in seconds
        estimated_throughput_ewma = self.th_est_ewma.push(old_download_time, last_known_throughput)
        while (quality + 1 < len(bitrates) and p * bitrates[quality + 1] / estimated_throughput_ewma <= p):
            quality += 1
        act = quality
        return act

class SlidingWindow():
    #tput is the calculated throughput
    #estimated_throughput is the future estimated throughput
    def __init__(self):
        self.window_size = 3
        self.max_store = 20
        self.last_throughputs = []
        self.last_latencies = []
        #self.estimated_latency = None

    def push(self,tput):#(self, time, tput, lat):
        self.last_throughputs += [tput]
        self.last_throughputs = self.last_throughputs[-self.max_store:]
        sample = self.last_throughputs[-self.window_size:]
        estimated_throughput = sum(sample) / len(sample)
        return estimated_throughput

class Ewma():
    #tput is the calculated throughput in Kbps
    #estimated_throughput is the future estimated throughput
    #time is the download time in ms
    def __init__(self):
        self.half_life = [8000, 3000] #in ms
        self.throughput = [0] * len(self.half_life)
        self.weight_throughput = 0

    def push(self, time, tput):
        for i in range(len(self.half_life)):
            alpha = math.pow(0.5, time / self.half_life[i])
            self.throughput[i] = alpha * self.throughput[i] + (1 - alpha) * tput
        self.weight_throughput += time
        tput = None
        for i in range(len(self.half_life)):
            zero_factor = 1 - math.pow(0.5, self.weight_throughput / self.half_life[i])
            t = self.throughput[i] / zero_factor
            tput = t if tput == None else min(tput, t)  # conservative case is min
        estimated_throughput = tput
        return estimated_throughput











