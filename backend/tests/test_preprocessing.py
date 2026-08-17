"""
测试不同模型的预处理是否正确
"""
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

import numpy as np
from PIL import Image
from src.ml.image_preprocess import preprocess_for_shape

# 创建测试图像 (100x100 RGB, 所有像素值为128)
test_img = Image.new('RGB', (100, 100), color=(128, 128, 128))

print("测试图像: 100x100 RGB, 所有像素值为128\n")

# 1. Simple mode (0-1 归一化)
simple_arr = preprocess_for_shape(test_img, (100, 100, 3), mode='simple')
print("Simple mode (0-1):")
print(f"  Shape: {simple_arr.shape}")
print(f"  Expected: (1, 100, 100, 3)")
print(f"  Value range: [{simple_arr.min():.4f}, {simple_arr.max():.4f}]")
print(f"  Expected: [0.5020, 0.5020] (128/255)")
print(f"  Sample pixel: {simple_arr[0, 50, 50, :]}")
print()

# 2. VGG mode (Caffe, BGR mean subtraction)
vgg_arr = preprocess_for_shape(test_img, (100, 100, 3), mode='vgg')
print("VGG mode (Caffe):")
print(f"  Shape: {vgg_arr.shape}")
print(f"  Expected: (1, 100, 100, 3)")
print(f"  Sample pixel (BGR): {vgg_arr[0, 50, 50, :]}")
print(f"  Expected: [128-103.939, 128-116.779, 128-123.68] = [24.061, 11.221, 4.32]")
print()

# 3. EfficientNet mode (Torch, -1 to 1)
effnet_arr = preprocess_for_shape(test_img, (100, 100, 3), mode='efficientnet')
print("EfficientNet mode (Torch):")
print(f"  Shape: {effnet_arr.shape}")
print(f"  Expected: (1, 100, 100, 3)")
print(f"  Value range: [{effnet_arr.min():.4f}, {effnet_arr.max():.4f}]")
print(f"  Expected: [0.0039, 0.0039] ((128/255 - 0.5) * 2)")
print(f"  Sample pixel: {effnet_arr[0, 50, 50, :]}")
print()

# 验证
print("=" * 60)
print("验证结果:")
print("=" * 60)

# Simple mode 检查
simple_correct = np.allclose(simple_arr[0, 50, 50, :], [128/255] * 3, atol=0.001)
print(f"✓ Simple mode: {'PASS' if simple_correct else 'FAIL'}")

# VGG mode 检查 (BGR order + mean subtraction)
vgg_expected = np.array([128 - 103.939, 128 - 116.779, 128 - 123.68])
vgg_correct = np.allclose(vgg_arr[0, 50, 50, :], vgg_expected, atol=0.1)
print(f"✓ VGG mode: {'PASS' if vgg_correct else 'FAIL'}")

# EfficientNet mode 检查
effnet_expected = (128/255 - 0.5) * 2
effnet_correct = np.allclose(effnet_arr[0, 50, 50, :], [effnet_expected] * 3, atol=0.001)
print(f"✓ EfficientNet mode: {'PASS' if effnet_correct else 'FAIL'}")

if simple_correct and vgg_correct and effnet_correct:
    print("\n✅ 所有预处理模式工作正常!")
else:
    print("\n❌ 部分预处理模式存在问题!")
