import torch

# 当前安装的 PyTorch 库的版本
print(torch.__version__)
# 检查 CUDA 是否可用，即你的系统有 NVIDIA 的 GPU
print(torch.cuda.is_available())
# 创建一个 5x3 随机张量
x = torch.rand(5, 3)
print(x)

