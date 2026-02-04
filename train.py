import gym
import register_env  # Import the registration file
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import DummyVecEnv

from gym.envs.registration import register

register(
    id="Origins-v0",  # Unique name for the environment
    entry_point="origins_env:OriginsEnv",  # Path to the class
)



# Create the environment
env = gym.make("Origins-v0")
env = DummyVecEnv([lambda: env])  # Vectorized wrapper for PPO

# Define the PPO model
model = PPO(
    "MlpPolicy",  
    env,
    learning_rate=0.0003,
    n_steps=2048,
    batch_size=64,
    n_epochs=10,
    gamma=0.99,
    gae_lambda=0.95,
    clip_range=0.2,
    verbose=1,
    tensorboard_log="./ppo_origins_tensorboard/"
)

# Train the model
model.learn(total_timesteps=100000)

# Save the trained model
model.save("ppo_origins")

# Test the model
obs = env.reset()
for _ in range(10):
    action, _states = model.predict(obs)  # Get action from trained model
    obs, reward, done, info = env.step(action)
    if done:
        obs = env.reset()
