import math


def UCB1(node, child, c: float = math.sqrt(2)):
    """UCB1 selection strategy."""
    node_value = (
        node.state.get_current_player() * child.total_reward / child.num_visits
        + c * math.sqrt(math.log(node.num_visits) / child.num_visits)
    )
    return node_value
