import random

from mcts.base.base import BaseState


def random_policy(state: BaseState) -> float:
    """
    Execute a random policy rollout for the given state until a terminal state.
    Return the reward of the terminal state.
    """
    while not state.is_terminal():
        try:
            action = random.choice(state.get_possible_actions())
        except IndexError:
            raise Exception(
                "State is not terminal but has no possible actions: " + str(state)
            )
        state = state.take_action(action)
    return state.get_reward()
