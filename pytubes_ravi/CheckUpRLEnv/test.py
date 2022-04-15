from env import CheckUpEnv
import torch
import numpy as np
from tianshou.policy import DQNPolicy
from tianshou.data import Batch
from checkup_dqn import get_args
from net import MyNet


def load_policy(args, path):
    net = MyNet(input_size=args.state_shape[0]).cuda()

    optim = torch.optim.Adam(net.parameters(), lr=args.lr)
    policy = DQNPolicy(
        net,
        optim,
        args.gamma,
        args.nstep,
        target_update_freq=args.target_update_freq,
    )
    policy.load_state_dict(torch.load(path))
    return policy


def test(policy, env):
    """
    复原policy，实现env
    """
    policy.eval()
    metrics = []

    for groups in env.groups:
        s = groups.reset()
        while True:
            batch = Batch(obs=[s], info={})
            a = policy(batch).act[0]
            s_, r, done, info = groups.step(a)
            if done:
                break
            s = s_
        metrics.append([compute_mean_valid_time_percent(groups.peoples_records),
                        compute_mean_valid_time_percent(groups.queues_records)])
    res = np.mean(np.array(metrics), axis=0)
    print(res, np.mean(res))


if __name__ == '__main__':
    args = get_args()
    env = CheckUpEnv(args.forward, is_train=False)
    args.state_shape = env.observation_space.shape or env.observation_space.n
    args.action_shape = env.action_space.shape or env.action_space.n
    policy = load_policy(args, "models/6_policy.pth")
    test(policy, env)
