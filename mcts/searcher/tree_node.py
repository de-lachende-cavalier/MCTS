from mcts.base.base import BaseState


class TreeNode:
    def __init__(self, state: BaseState, parent: "TreeNode"):
        self.state = state
        self.is_terminal = state.is_terminal()
        self.is_fully_expanded = self.is_terminal
        self.parent = parent
        self.num_visits = 0
        self.total_reward = 0
        self.children = {}

    def __str__(self):
        s = [
            "total_reward: %s" % self.total_reward,
            "num_visits: %d" % self.num_visits,
            "is_terminal: %s" % self.is_terminal,
            "possible_actions: %s" % (self.children.keys()),
        ]
        return "%s: {%s}" % (self.__class__.__name__, ", ".join(s))
