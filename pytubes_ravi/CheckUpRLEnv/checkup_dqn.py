import argparse
import random
from env import CheckUpEnv
import torch
from tianshou.env import DummyVectorEnv
import numpy as np
from tianshou.policy import DQNPolicy
from tianshou.data import VectorReplayBuffer, Collector
from tianshou.trainer import offpolicy_trainer
from net import MyNet
import os


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('--seed', type=int, default=100)

    parser.add_argument('--eps-test', type=float, default=0.05)
    parser.add_argument('--eps-train', type=float, default=0.1)

    parser.add_argument('--buffer-size', type=int, default=1000)

    # forward表示状态看了多少步，这里表示看前7步和当前步共8步
    parser.add_argument('--forward', type=int, default=8)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--gamma', type=float, default=0.95)

    parser.add_argument('--target-update-freq', type=int, default=200)
    parser.add_argument('--update-per-step', type=float, default=0.9)

    parser.add_argument('--epoch', type=int, default=200)

    parser.add_argument('--step-per-epoch', type=int, default=10000)
    parser.add_argument('--step-per-collect', type=int, default=20)

    parser.add_argument('--nstep', type=int, default=3)
    parser.add_argument('--batch-size', type=int, default=64)

    parser.add_argument('--training-num', type=int, default=10)
    parser.add_argument('--test-num', type=int, default=1)

    parser.add_argument(
        '--device', type=str, default='cuda' if torch.cuda.is_available() else 'cpu'
    )
    args = parser.parse_known_args()[0]
    return args


def train_dqn(args=get_args()):
    env = CheckUpEnv(args.forward, is_train=True)

    args.state_shape = env.observation_space.shape or env.observation_space.n
    args.action_shape = env.action_space.shape or env.action_space.n

    print(args.state_shape, args.action_shape)
    # train_envs创建了10个
    train_envs = DummyVectorEnv(
        [lambda: CheckUpEnv(args.forward, is_train=True) for _ in range(args.training_num)]
    )
    # val_envs创建了1个
    val_envs = DummyVectorEnv(
        [lambda: CheckUpEnv(args.forward, is_train=False) for _ in range(args.test_num)]
    )
    # 设置随机种子，使得随机数生成结果每次一致
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    train_envs.seed(args.seed)
    val_envs.seed(args.seed)
    # build net
    net = MyNet(input_size=args.state_shape[0]).to(args.device)
    # setup optim
    optim = torch.optim.Adam(net.parameters(), lr=args.lr)
    # setup policy
    policy = DQNPolicy(
        net,
        optim,
        discount_factor=args.gamma,
        estimation_step=args.nstep,
        target_update_freq=args.target_update_freq,
    )
    # 负责存储数据和采样出来数据用于policy的训练
    buf = VectorReplayBuffer(args.buffer_size, buffer_num=len(train_envs))
    """
    采集器(Collector)是天授中的一个关键概念。它定义了策略与不同环境交互的逻辑。
    在每一回合(step)中, 采集器会让策略与环境交互指定数目(至少)的步数或者轮数,并且会将产生的数据存储在重放缓冲区中。
    """
    train_collector = Collector(policy, train_envs, buf, exploration_noise=True)
    test_collector = Collector(policy, val_envs, exploration_noise=True)

    train_collector.collect(n_step=args.batch_size * args.training_num)

    def test_fn(epoch, env_step):
        policy.set_eps(args.eps_test)
        torch.save(policy.state_dict(), os.path.join("models", str(epoch) + '_policy.pth'))

    def train_fn(epoch, env_step):
        if env_step <= 10000:
            policy.set_eps(args.eps_train)
        elif env_step <= 50000:
            eps = args.eps_train - (env_step - 10000) / \
                  40000 * (0.9 * args.eps_train)
            policy.set_eps(eps)
        else:
            policy.set_eps(0.1 * args.eps_train)

    result = offpolicy_trainer(
        policy,
        train_collector,
        test_collector,
        args.epoch,
        args.step_per_epoch,
        args.step_per_collect,
        args.test_num,
        args.batch_size,
        update_per_step=args.update_per_step,
        train_fn=train_fn,
        test_fn=test_fn,
    )


if __name__ == '__main__':
    train_dqn(get_args())
