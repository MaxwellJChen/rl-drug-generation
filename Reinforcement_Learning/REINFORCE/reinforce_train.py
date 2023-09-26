import torch
from torch.optim import Adam
from SURGE import SURGE
from Reinforcement_Learning.mol_env import vectorized_mol_env
from graph_embedding import batch_from_states

model = SURGE()
max_steps = 100
num_envs = 2
env = vectorized_mol_env(num_envs = num_envs, max_steps = max_steps)
optimizer = Adam(params = model.parameters())

# Training loop
saved_actions = {'t': [], 'nmol': [], 'nfull': [], 'b': []}
saved_log_probs = {'t': [], 'nmol': [], 'nfull': [], 'b': []}
saved_rewards = []

def select_action(states):
    batch = batch_from_states(states)
    actions, log_probs = model.act(batch, return_log_probs = True)
    for key in ['t', 'nmol', 'nfull', 'b']:
        saved_actions[key].append(actions[key])
        saved_log_probs[key].append(log_probs[key])

    return actions

states = env.reset()
for i in range(max_steps):
    actions = select_action(states)
    states, rewards, valids, timestep = env.step(actions['t'], actions['nmol'], actions['nfull'], actions['b'])
