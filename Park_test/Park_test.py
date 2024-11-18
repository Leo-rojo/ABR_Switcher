import park
from ABR import Random_ABR
import numpy as np

#import environment
env = park.make('abr_sim')
conta_action = 0
obs = env.reset()
actions = np.arange(env.action_space.n)
Random_ABR = Random_ABR(obs, actions)
done = False
print('step 0, no action done')
#start the simulation
#first action
act = Random_ABR.get_first_action(obs)
obs, reward, done, info = env.step(act)
prev_obs, prev_reward, prev_done, prev_info = obs, reward, done, info
conta_action += 1
print('step 1, first action done')

while not done:
    act = Random_ABR.get_action(prev_obs, prev_reward, prev_done, prev_info)
    conta_action += 1
    obs, reward, done, info = env.step(act)
    print('step', str(conta_action), 'action', act)
    prev_obs, prev_reward, prev_done, prev_info = obs, reward, done, info
