import torch

print("PyTorch 버전:", torch.__version__)
print("GPU 사용 가능:", torch.cuda.is_available())
print("PyTorch의 CUDA 버전:", torch.version.cuda)

if torch.cuda.is_available():
    print("GPU 이름:", torch.cuda.get_device_name(0))

device = "cuda" if torch.cuda.is_available() else "cpu"
x = torch.rand(3, 3).to(device)
print("텐서 위치:", x.device)