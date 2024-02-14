import gym
import numpy
import random
import os
import Enviroment
from gym import spaces

from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv
from stable_baselines3.common.evaluation import evaluate_policy


class Agent:
    def __init__(self):
        self.log_path = os.path.join('Training', 'Logs')
        self.save_path = os.path.join('Training', 'Model', 'Snake_Model')
        self.env = Enviroment.SnakeEnv()
        self.env.snake.create_game_field()
        self.model = None

    def learn(self, time_steps=100000):
        self.model = PPO("MlpPolicy", self.env, verbose=1, tensorboard_log=self.log_path)
        self.model.learn(total_timesteps=time_steps)
        self.model.save(self.save_path)

    def learn_with_saved_mode(self, time_steps=100000):
        self.load_model()
        self.model.learn(total_timesteps=time_steps)
        self.model.save(self.save_path)

    def load_model(self):
        self.model = PPO.load(self.save_path, env=self.env)

    def evaluate_model(self):
        self.load_model()
        print(evaluate_policy(self.model, self.env, n_eval_episodes=10, render=False))

    def start_agent(self):
        self.load_model()
        epis = 10
        for episode in range(1, epis + 1):
            obs = self.env.reset()
            done = False
            score = 0

            while not done:
                action, _ = self.model.predict(obs)
                obs, reward, done, info = self.env.step(action=action, slow=True)
                score += reward
            print("episode:{} Score:{}".format(episode, score))
        self.env.close()
