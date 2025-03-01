import numpy as np
import random
import pygame


# game setting
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_SPEED = 5
BULLET_SPEED = 5
GHOST_SPEED = 10
COIN_SPEED = 10

# Q-Learning parametres
LEARNING_RATE = 0.3
DISCOUNT_FACTOR = 0.99
EXPLORATION_RATE = 1.0
MIN_EXPLORATION_RATE = 0.05
EXPLORATION_DECAY_RATE = 0.995

# actions：0=moving left，1=moving right，2=shoot
ACTIONS = [0, 1, 2]

# initialize q table
STATE_SPACE = [(x, y, c_x, c_y) for x in range(300, 601, 5) for y in range(240, 641, 10) for c_x in range(320, 581, 5) for c_y in range(50, 641, 10)]
Q_TABLE = np.zeros((len(STATE_SPACE), len(ACTIONS)))
state_dict = {}
state_index = 0

def get_state(player_x, ghost_x, ghost_y, coin_x, coin_y):
    player_x = round(player_x / 50) * 50
    ghost_x = round(ghost_x / 50) * 50
    ghost_y = round(ghost_y / 50) * 50
    coin_x = round(coin_x / 50) * 50
    coin_y = round(coin_y / 50) * 50
    return (player_x, ghost_x, ghost_y, coin_x, coin_y)

def get_state_index(state):
    global state_index
    if state not in state_dict:
        state_dict[state] = state_index
        state_index += 1
    return state_dict[state]

def choose_action(state_index):
    if random.uniform(0, 1) < EXPLORATION_RATE:
        return random.choice(ACTIONS)
    else:
        return np.argmax(Q_TABLE[state_index])

def update_q_table(state_index, action, reward, next_state_index):
    best_next_action = np.argmax(Q_TABLE[next_state_index])
    td_target = reward + DISCOUNT_FACTOR * Q_TABLE[next_state_index][best_next_action]
    td_error = td_target - Q_TABLE[state_index][action]
    Q_TABLE[state_index][action] += LEARNING_RATE * td_error

def train_q_learning(episodes):
    global EXPLORATION_RATE
    state_dict.clear()
    state_index = 0

    for episode in range(episodes):
        # initializing
        player_x = 640
        ghost_x, ghost_y = 240, 50
        coin_x, coin_y = random.randint(320, 580), 640

        state = get_state(player_x, ghost_x, ghost_y, coin_x, coin_y)
        state_index = get_state_index(state)

        done = False
        total_reward = 0
        start_time = pygame.time.get_ticks()

        while not done:
            # decide which action to use
            action = choose_action(state_index)
            reward = -1
            # react and get reward
            if action == 0:
                player_x = max(300, player_x - PLAYER_SPEED)
            elif action == 1:
                player_x = min(600, player_x + PLAYER_SPEED)
            elif action == 2:
                if abs(player_x - ghost_x) < 50 and abs(player_x - ghost_y) < 50:
                    reward = 100
                    done = True
                else:
                    reward = -20
            else:
                reward = -1
            #coin collection reward
            if abs(player_x - coin_x) < 50 and abs(player_x - coin_y) < 50:
                reward += 700
                coin_x, coin_y = random.randint(320, 580), 640

            ghost_y += GHOST_SPEED
            coin_y -= COIN_SPEED

            # check the condition that the game ends
            current_time = pygame.time.get_ticks()
            if ghost_y > 640 or current_time - start_time >= 30 * 1000:
                done = True

            # calculate next state
            next_state = get_state(player_x, ghost_x, ghost_y, coin_x, coin_y)
            next_state_index = get_state_index(next_state)

            # update  q table
            update_q_table(state_index, action, reward, next_state_index)

            # update state index
            state_index = next_state_index
            total_reward += reward

        # update exploration rate
        EXPLORATION_RATE = max(MIN_EXPLORATION_RATE, EXPLORATION_RATE * EXPLORATION_DECAY_RATE)
        print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}, Exploration Rate: {EXPLORATION_RATE}")

    print("Training complete. Q-Table:")
    print(Q_TABLE)
    np.save("q_table.npy", Q_TABLE)

# 训练 Q-Learning 智能体
train_q_learning(episodes=1000)