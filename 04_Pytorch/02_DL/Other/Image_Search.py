import torch
import torch.nn as nn
from torchvision import models, transforms
from PIL import Image
import numpy as np

# 定义与上面相同的预处理
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

class FeatureExtractor:
    def __init__(self):
        # 加载 ResNet50
        base_model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        
        # ★关键步骤★：去掉最后一层分类层 (Fully Connected Layer)
        # 我们只需要卷积层提取出的特征，不需要它告诉我们需要分到哪一类
        self.feature_layer = torch.nn.Sequential(*list(base_model.children())[:-1])
        self.feature_layer.eval()

    def get_vector(self, image_path):
        """将图片转换为特征向量"""
        try:
            img = Image.open(image_path).convert('RGB')
            img_tensor = preprocess(img).unsqueeze(0)
            
            with torch.no_grad():
                # 输出形状通常是 [1, 2048, 1, 1]
                feature_vector = self.feature_layer(img_tensor)
            
            # 展平为一维向量 [2048]
            return feature_vector.flatten().numpy()
        except Exception as e:
            print(f"处理图片 {image_path} 时出错: {e}")
            return None

def calculate_similarity(vector1, vector2):
    """计算余弦相似度 (Cosine Similarity)"""
    # 相似度公式：(A . B) / (||A|| * ||B||)
    dot_product = np.dot(vector1, vector2)
    norm_a = np.linalg.norm(vector1)
    norm_b = np.linalg.norm(vector2)
    return dot_product / (norm_a * norm_b)

# --- 模拟电商以图搜图流程 ---
def demo_image_search():
    extractor = FeatureExtractor()
    
    print("正在初始化以图搜图系统...")
    
    # 假设这是你的本地图片路径 (请确保这些文件存在)
    # image_a: 用户上传的图片 (比如一只金毛狗)
    # image_b: 数据库里的图片1 (另一只金毛狗)
    # image_c: 数据库里的图片2 (一辆汽车)
    
    # 为了演示，你需要准备三张真实的图片路径
    # 这里只是逻辑演示
    print("请设置真实的图片路径来运行此演示。")
    
    # 示例逻辑：
    # vec_a = extractor.get_vector('dog1.jpg')
    # vec_b = extractor.get_vector('dog2.jpg')
    # vec_c = extractor.get_vector('car.jpg')
    
    # if vec_a is not None and vec_b is not None:
    #     sim_ab = calculate_similarity(vec_a, vec_b)
    #     print(f"图片A与图片B的相似度: {sim_ab:.4f} (越高越相似)")
    #     # 通常同类物体相似度 > 0.6 或 0.7
        
    # if vec_a is not None and vec_c is not None:
    #     sim_ac = calculate_similarity(vec_a, vec_c)
    #     print(f"图片A与图片C的相似度: {sim_ac:.4f}")

# 运行演示
# demo_image_search()