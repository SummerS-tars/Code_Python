# 移动应用 UI 数据集构建指南

## 1. 项目目标

本项目旨在通过自动化工具采集 Android 应用的 **GUI 截图** 及其对应的 **XML 结构树 (View Hierarchy)**，用于构建 UI 理解或多智能体操作的数据集。

## 2. 环境准备 (Windows/Mac)

在开始之前，请确保你的电脑上配置了以下两样东西：**ADB 工具包** 和 **Python 环境**。

### 2.1 安装 ADB (Android Debug Bridge)

ADB 是电脑与安卓手机通信的桥梁。

**Windows 用户：**

1. 下载 SDK Platform Tools：[官方下载链接](https://developer.android.com/studio/releases/platform-tools)
2. 解压压缩包（建议解压到 `C:\platform-tools` 或 `D:\adb` 这种简单路径）。
3. **配置环境变量** (关键步骤)：
   - 右键“此电脑” -> 属性 -> 高级系统设置 -> 环境变量。
   - 在“系统变量”中找到 `Path`，点击编辑。
   - 新建一行，填入你刚才解压的文件夹路径（例如 `C:\platform-tools`）。
4. **验证安装**：
   - 打开 VS Code 终端或 CMD，输入 `adb version`。
   - 如果显示版本号，即为安装成功。

**Mac 用户：**

```bash
brew install android-platform-tools
```

### 2.2 安装 Python 依赖库

我们需要以下 Python 库：

```bash
# 核心依赖
pip install uiautomator2

# 图像处理和可视化
pip install opencv-python pillow numpy

# 可选：matplotlib（用于更美观的可视化，已包含在代码中但非必需）
# pip install matplotlib
```

或者一次性安装所有依赖：

```bash
pip install uiautomator2 opencv-python pillow numpy
```

> 注意：`xml.etree.ElementTree` 是 Python 标准库，无需额外安装。

------



## 3. 连接 STF 远程真机

我们将使用 STF 平台上的远程设备进行采集。

1. **占用设备**：在 STF 网页上找到空闲手机，点击 **"Use"**。
2. **获取连接码**：
   - 在控制页面的 "Remote Debugging" 区域，找到连接命令。
   - 格式如：`adb connect 10.176.xx.xx:74xx`。
3. **执行连接**： 在终端输入上述命令。
4. **⚠️ 关键授权步骤**：
   - 输入 `adb devices`，如果状态显示 `unauthorized`。
   - **立刻去看 STF 网页上的手机屏幕**。
   - 手动点击弹窗中的 **"Always allow" (始终允许)** -> **"Allow"**。
   - 再次输入 `adb devices`，直到状态变为 `device`。

---

## 4. 数据采集

### 4.1 .apk文件下载

由于没有手机应用助手，需要直接下载.apk文件，然后直接运行传输到远程真机上（adb install ".apk下载地址"）

.apk下载网址推荐：豌豆荚 (https://www.google.com/search?q=wandoujia.com)

### 4.2 配置设备地址

在开始采集之前，需要修改 `capture.py` 文件中的设备地址：

```python
# 在 capture.py 中找到这一行，替换为你的设备地址
DEVICE_ADDR = "10.176.65.211:7429"  # 改为你的设备地址
```

### 4.3 运行采集脚本

在终端中运行采集脚本：

```bash
python capture.py
```

### 4.4 采集数据

1. **连接成功后**，脚本会提示你按 Enter 键进行采集。
2. **在手机上操作**：打开目标应用，导航到你想要采集的页面。
3. **采集数据**：
   - 直接按 Enter：使用默认文件名（`unknown_app_时间戳`）
   - 输入自定义名称后按 Enter：例如输入 `wechat_login`，会生成 `wechat_login_时间戳.xml` 和 `wechat_login_时间戳.jpg`
4. **重复采集**：继续在手机上操作，按 Enter 采集更多页面。
5. **退出**：输入 `q` 退出采集脚本。

采集的数据会保存在 `./data_collection` 目录中，每个页面会生成两个文件：
- `文件名.xml`：UI 结构树
- `文件名.jpg`：屏幕截图

---

## 5. 数据处理：生成 YOLO 数据集

### 5.1 标注方案说明

本项目使用**三类标注方案**（`three_class`），将 UI 组件分为：

- **类别 0 - 文字**：包含文本内容的组件（TextView、Button 等）
- **类别 1 - 图片**：图片组件（ImageView 等）
- **类别 2 - 可点击**：可交互的组件（Button、可点击的 View 等）

> 注意：一个组件可能同时属于多个类别。例如，一个可点击的按钮会同时标注为"文字(0)"和"可点击(2)"。

### 5.2 批量处理数据

采集完成后，使用 `generate_yolo_data.py` 批量处理所有数据：

```bash
python generate_yolo_data.py
```

**默认行为**：
- 从 `./data_collection` 目录读取所有 XML 和图片文件
- 使用 `three_class` 标注方案
- 输出到 `./dataset` 目录

**自定义参数**：

```bash
# 指定数据目录和输出目录
python generate_yolo_data.py --data_dir ./data_collection --output_dir ./dataset

# 使用其他标注方案（不推荐，已确定使用 three_class）
python generate_yolo_data.py --scheme two_class
```

### 5.3 单文件处理（测试用）

如果需要测试单个文件：

```bash
python generate_yolo_data.py --xml ./data_collection/app_20231126_120000.xml --image ./data_collection/app_20231126_120000.jpg
```

### 5.4 输出结果

处理完成后，`./dataset` 目录中会包含：

1. **图片文件**：`.jpg` 或 `.png` 格式
   - 例如：`app_20231126_120000.jpg`

2. **标注文件**：`.txt` 格式（YOLO 格式）
   - 例如：`app_20231126_120000.txt`
   - **重要**：标注文件名与图片文件名（不含扩展名）完全一致

3. **可视化文件**（可选）：`_visualized.jpg`
   - 例如：`app_20231126_120000_visualized.jpg`
   - 用于验证标注质量，可以看到标注框和类别标签

**数据集结构示例**：

```
dataset/
├── app_20231126_120000.jpg          # 图片
├── app_20231126_120000.txt          # 标注（与图片同名）
├── app_20231126_120000_visualized.jpg  # 可视化结果
├── wechat_login_20231126_120100.jpg
├── wechat_login_20231126_120100.txt
└── wechat_login_20231126_120100_visualized.jpg
```

### 5.5 验证数据集

检查数据集是否正确生成：

1. **文件配对检查**：确保每个 `.jpg`/`.png` 文件都有对应的 `.txt` 文件（文件名相同）。
2. **查看可视化结果**：打开 `_visualized.jpg` 文件，检查标注框是否正确。
3. **检查标注文件**：打开 `.txt` 文件，每行格式应为：
   ```
   类别ID x_center y_center width height
   ```
   例如：`0 0.5 0.3 0.2 0.1` 表示一个文字组件。

---

## 6. 常见问题

### Q1: 采集时提示连接失败？

- 检查 `adb devices` 是否显示 `device` 状态
- 确认 `capture.py` 中的设备地址是否正确
- 检查 STF 设备是否仍然在线

### Q2: 处理数据时提示找不到图片文件？

- 确保 XML 和图片文件在同一目录（`./data_collection`）
- 检查文件名是否匹配（除了扩展名外应该完全相同）

### Q3: 生成的标注文件为空？

- 检查 XML 文件是否包含有效的 UI 组件信息
- 尝试降低 `--min_size` 参数（默认 10 像素）

