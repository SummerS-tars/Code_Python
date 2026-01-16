import torch
from torchvision import models, transforms
from PIL import Image
import json
import urllib.request

# 1. 准备图像预处理步骤
# 预训练模型通常需要特定的输入格式：
# - 调整大小到 256x256
# - 中心裁剪出 224x224
# - 转换为 Tensor 格式
# - 标准化（使用 ImageNet 的均值和标准差）
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def load_labels():
    """下载并加载 ImageNet 的 1000 个类别标签，这样我们能看到文字而不是数字 ID"""
    url = "https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json"
    try:
        with urllib.request.urlopen(url) as f:
            labels = json.load(f)
        return labels
    except Exception as e:
        print("无法下载标签，将直接显示类别ID。")
        return None

def identify_image(image_path):
    print(f"正在分析图片: {image_path} ...")
    
    # 2. 加载图像
    try:
        input_image = Image.open(image_path)
        # 确保图片是 RGB 模式（防止输入灰度图或透明图报错）
        if input_image.mode != 'RGB':
            input_image = input_image.convert('RGB')
    except FileNotFoundError:
        print("错误：找不到文件，请检查路径。")
        return

    # 3. 预处理图像并增加一个维度 (Batch Size)
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(0) # 形状变为 [1, 3, 224, 224]

    # 4. 加载预训练的 ResNet50 模型
    # weights='DEFAULT' 会自动下载在大规模数据集上训练好的权重
    model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
    model.eval() # 设置为评估模式

    # 5. 进行预测
    if torch.cuda.is_available():
        input_batch = input_batch.to('cuda')
        model.to('cuda')

    with torch.no_grad(): # 推理时不需要计算梯度，节省内存
        output = model(input_batch)

    # 6. 获取结果
    # Softmax 将输出转换为概率分布
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    
    # 获取概率最高的前 3 个结果
    top3_prob, top3_catid = torch.topk(probabilities, 3)
    
    labels = load_labels()

    print("\n=== 识别结果 ===")
    for i in range(top3_prob.size(0)):
        class_id = top3_catid[i].item()
        score = top3_prob[i].item() * 100
        
        if labels:
            print(f"排名 {i+1}: {labels[class_id]} (置信度: {score:.2f}%)")
        else:
            print(f"排名 {i+1}: 类别ID {class_id} (置信度: {score:.2f}%)")

# --- 使用示例 ---
# 请将 'test_image.jpg' 替换为你本地的图片路径
# identify_image('test_image.jpg')