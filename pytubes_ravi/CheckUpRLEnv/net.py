import numpy
import torch
import torch.nn as nn
from utils import np2tensor


class MyNet(torch.nn.Module):
    def __init__(self, input_size, output_size):
        """input size = forward * len(room_list)"""
        super(MyNet, self).__init__()
        self.projection = nn.Sequential(
            torch.nn.Linear(input_size, 1024),
            torch.nn.ReLU(),
            torch.nn.Linear(1024, 512),
            torch.nn.ReLU(),
            torch.nn.Linear(512, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, output_size),
            torch.nn.Softmax()
        )
        self._initialize_weights()

    def _initialize_weights(self):
        for m in self.projection.modules():
            if isinstance(m, nn.Linear):
                nn.init.uniform_(m.weight - 0.05, 0.05)
                if m.bias is not None:
                    nn.init.constant_(m.bias, 0)
            elif isinstance(m, nn.BatchNorm1d):
                nn.init.constant_(m.weight, 1)
                nn.init.constant_(m.bias, 0)

    def forward(self, s, state=None, info={}):

        if type(s) == numpy.ndarray:
            s = np2tensor(s)
        return self.projection(s), state
