
from torch.utils.data import DataLoader
from torchvision.datasets import CIFAR10
from torchvision.transforms import transforms
from torch.autograd import Variable


import torch.nn as nn
import torch.nn.functional as F
import torch

class Block(nn.Module):
    def __init__(self, in_planes, out_planes, expansion, stride):
        super(Block, self).__init__()
        self.stride = stride

        planes = expansion * in_planes
        self.conv1 = nn.Conv2d(in_planes, planes, kernel_size=1, bias=False)
        self.bn1 = nn.BatchNorm2d(planes)
        self.conv2 = nn.Conv2d(planes, planes, kernel_size=3, stride=stride, padding=1, groups=planes, bias=False)
        self.bn2 = nn.BatchNorm2d(planes)
        self.conv3 = nn.Conv2d(planes, out_planes, kernel_size=1, bias=False)
        self.bn3 = nn.BatchNorm2d(out_planes)

        self.shortcut = nn.Sequential()
        if stride == 1 and in_planes != out_planes:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_planes, out_planes, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_planes)
            )

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = F.relu(self.bn2(self.conv2(out)))
        out = self.bn3(self.conv3(out))
        out += self.shortcut(x) if self.stride == 1 else out
        return out


class MobileNetV2(nn.Module):
    def __init__(self, num_classes=10):
        super(MobileNetV2, self).__init__()

        self.cfgs = [
            # t, c, n, s
            [1, 16, 1, 1],
            [6, 24, 2, 1],
            [6, 32, 3, 2],
            [6, 64, 4, 2],
            [6, 96, 3, 1],
            [6, 160, 3, 2],
            [6, 320, 1, 1],
        ]

        self.conv1 = nn.Conv2d(3, 32, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn1 = nn.BatchNorm2d(32)
        self.layers = self._make_layers(in_planes=32)
        self.conv2 = nn.Conv2d(320, 1280, kernel_size=1, bias=False)
        self.bn2 = nn.BatchNorm2d(1280)
        self.linear = nn.Linear(1280, num_classes)

    def _make_layers(self, in_planes):
        layers = []
        for t, c, n, s in self.cfgs:
            for i in range(n):
                stride = s if i == 0 else 1
                layers.append(Block(in_planes, c, t, stride))
                in_planes = c
        return nn.Sequential(*layers)

    def forward(self, x):
        out = F.relu(self.bn1(self.conv1(x)))
        out = self.layers(out)
        out = F.relu(self.bn2(self.conv2(out)))
        out = F.avg_pool2d(out, 4)
        out = out.view(out.size(0), -1)
        out = self.linear(out)
        return out


if __name__ == '__main__':
    train_data = CIFAR10('cifar', download=True, train=True, transform=transforms.ToTensor())
    data = DataLoader(train_data, batch_size=148, shuffle=True)

    device = torch.device("cuda")
    net = MobileNetV2().to(device)
    print(net)
    cross = nn.CrossEntropyLoss().to(device)
    optimizer = torch.optim.Adam(net.parameters(), 0.0001)
    for epoch in range(10):
        for img, label in data:
            img = Variable(img).to(device)
            label = Variable(label).to(device)
            output = net.forward(img)
            loss = cross(output, label)
            loss.backward()
            optimizer.zero_grad()
            optimizer.step()
            pre = torch.argmax(output, 1)
            num = (pre == label).sum().item()
            acc = num / img.shape[0]
        print("epoch:", epoch + 1)
        print("loss:", loss.item())
        print("Accuracy:", acc)

