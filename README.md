# Weather Backend

一个基于 FastAPI 的气象数据可视化后端服务，支持实时生成气象预报图片并通过 SSE（Server-Sent Events）流式推送。

## 功能特性

- 🌤️ 实时气象数据可视化
- 📊 温度、风速、降水多要素展示
- 🔄 SSE 流式推送图片
- 🐳 Docker 一键部署
- 🌍 支持任意经纬度坐标

## 快速开始

### 一键部署（推荐）

#### 1. 克隆项目
```bash
git clone https://github.com/hoho2017/weather-backend.git
cd weather-backend
```

#### 2. Docker 一键部署
```bash
# 构建镜像
docker build -t weather-backend .

# 运行容器
docker run -d -p 8000:8000 --name weather-app weather-backend
```

### 本地开发

#### 1. 安装依赖
```bash
pip install -r requirements.txt
```

#### 2. 运行服务
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## API 使用

### 获取气象图片（SSE 流式推送）

**请求：**
```
GET /images?lon=121.47&lat=31.23
```

**参数：**
- `lon`: 经度（必需）
- `lat`: 纬度（必需）

**响应：**
通过 SSE 流式推送图片 URL，每生成一张图片推送一次：

```
event: image
data: /static/lon_121.47_lat_31.23/Forecast - 2025-06-01 08:00.png

event: image
data: /static/lon_121.47_lat_31.23/Forecast - 2025-06-01 09:00.png
...
```

### 前端示例

```javascript
const evtSource = new EventSource("http://localhost:8000/images?lon=121.47&lat=31.23");

evtSource.onmessage = function(event) {
    const imageUrl = event.data;
    console.log("收到图片:", imageUrl);
    // 动态添加到页面
    const img = document.createElement('img');
    img.src = imageUrl;
    document.body.appendChild(img);
};

evtSource.onerror = function(event) {
    console.error("SSE 连接错误:", event);
    evtSource.close();
};
```

## 项目结构

```
weather-backend/
├── app.py              # FastAPI 主应用
├── extract.py          # 气象数据处理和图片生成
├── decompress.py       # 数据解压工具
├── requirements.txt    # Python 依赖
├── Dockerfile         # Docker 配置
├── README.md          # 项目说明
└── images/            # 生成的图片目录
```

## 环境要求

- Python 3.9+
- Docker（可选）
- 网络连接（用于访问气象数据源）

## 配置说明

### 数据源配置

项目默认使用阿里云 OSS 上的气象数据文件。如需修改数据源，请编辑 `extract.py` 中的 `file_path` 变量。

### 端口配置

默认端口为 8000，可通过以下方式修改：

**Docker 方式：**
```bash
docker run -d -p 8080:8000 weather-backend  # 映射到 8080 端口
```

**本地方式：**
```bash
uvicorn app:app --host 0.0.0.0 --port 8080
```
