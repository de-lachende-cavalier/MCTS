from math import sqrt
import time
import random
from typing import Callable

from base import BaseState
from tree_node import TreeNode
from policies import random_policy
from selection_strategies import UCB1


class MCTS:
    def __init__(
        self,
        time_limit: int = None,
        iteration_limit: int = None,
        selection_strategy: Callable = UCB1,
        exploration_constant: float = sqrt(2),
        rollout_policy=None,
    ):
        self.root = None
        if time_limit is not None:
            if iteration_limit is not None:
                raise ValueError("Cannot have both a time limit and an iteration limit")
            self.time_limit = time_limit
            self.limit_type = "time"
        else:
            if iteration_limit is None:
                raise ValueError("Must have either a time limit or an iteration limit")
            if iteration_limit < 1:
                raise ValueError("Iteration limit must be greater than one")
            self.search_limit = iteration_limit
            self.limit_type = "iterations"

        self.selection_strategy = selection_strategy
        self.exploration_constant = exploration_constant
        self.rollout_policy = rollout_policy or random_policy

    def search(
        self,
        initial_state: BaseState = None,
        need_details: bool = None,
    ):
        self.root = TreeNode(initial_state, None)

        if self.limit_type == "time":
            time_limit = time.time() + self.time_limit / 1000
            while time.time() < time_limit:
                self.execute_round()
        else:
            for i in range(self.search_limit):
                self.execute_round()

        best_child = self.get_best_child(self.root, 0)
        action = (
            action for action, node in self.root.children.items() if node is best_child
        ).__next__()
        if need_details:
            return action, best_child.total_reward / best_child.num_visits
        else:
            return action

    def execute_round(self):
        """Execute a selection-expansion-simulation-backpropagation round."""
        node = self.select(self.root)
        reward = self.rollout_policy(node.state)
        self.backpropogate(node, reward)

    def select(self, node: TreeNode) -> TreeNode:
        """Select the appropriate node for expansion."""
        while not node.is_terminal:
            if node.is_fully_expanded:
                node = self.get_best_child(node, self.exploration_constant)
            else:
                return self.expand(node)
        return node

    def expand(self, node: TreeNode) -> TreeNode:
        """Expand the given node by creating a new child node."""
        actions = node.state.get_possible_actions()
        for action in actions:
            if action not in node.children:
                new_node = TreeNode(node.state.take_action(action), node)
                node.children[action] = new_node
                if len(actions) == len(node.children):
                    node.is_fully_expanded = True
                return new_node
        raise Exception("Attempted to expand a fully expanded node.")

    def backpropogate(self, node: TreeNode, reward: float):
        """Backpropagate the reward value up the tree to the root."""
        while node is not None:
            node.num_visits += 1
            node.total_reward += reward
            node = node.parent

    def get_best_child(self, node, exploration_value: float) -> TreeNode:
        """Get the best child node for the given node using a specified selection strategy."""
        best_value = float("-inf")
        best_nodes = []
        for child in node.children.values():
            node_value = self.selection_strategy(node, child, exploration_value)
            if node_value > best_value:
                best_value = node_value
                best_nodes = [child]
            elif node_value == best_value:
                best_nodes.append(child)
        return random.choice(best_nodes)
