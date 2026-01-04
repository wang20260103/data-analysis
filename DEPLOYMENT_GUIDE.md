# Streamlit项目部署指南

本指南将帮助你部署Streamlit项目，使其可以通过浏览器正常访问。

## 一、本地部署与测试

### 1. 确保依赖已安装
```bash
# 安装项目所需依赖
pip install -r requirements.txt
```

### 2. 本地启动应用
```bash
# 运行Streamlit应用
python -m streamlit run web_app.py
```

应用将在浏览器中自动打开，访问地址通常为：`http://localhost:8501`

### 3. 本地测试要点
- 检查所有功能是否正常工作
- 确保data文件夹下的Excel文件能被正确读取
- 测试不同页面的切换和数据加载

## 二、创建requirements.txt文件

部署前需创建`requirements.txt`文件，列出所有项目依赖：

```bash
# 生成requirements.txt
pip freeze > requirements.txt
```

然后根据实际使用的包进行精简，以下是示例：
```txt
streamlit
pandas
openpyxl  # Excel文件读取
matplotlib
seaborn
scikit-learn  # 若使用了机器学习功能
```

## 三、云平台部署

### 1. Streamlit Cloud（推荐）

**优点**：专为Streamlit设计，部署简单，集成GitHub

**步骤**：
1. **创建GitHub仓库**
   - 将项目代码上传到GitHub仓库
   - 确保包含`requirements.txt`和`data`文件夹

2. **注册Streamlit Cloud账户**
   - 访问：https://streamlit.io/cloud
   - 使用GitHub账户登录

3. **部署应用**
   - 点击"New app"
   - 选择你的GitHub仓库
   - 选择主分支
   - 指定启动文件：`web_app.py`
   - 点击"Deploy"

4. **配置设置**
   - 在"Settings"中可配置环境变量
   - 确保`data`文件夹被正确包含在仓库中

**注意**：Streamlit Cloud的免费版有资源限制，适合小型应用。

### 2. Docker部署

**优点**：跨平台，环境一致性好

**步骤**：

1. **创建Dockerfile**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   
   # 安装依赖
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   # 复制项目文件
   COPY . .
   
   # 暴露端口
   EXPOSE 8501
   
   # 启动命令
   CMD ["streamlit", "run", "web_app.py"]
   ```

2. **构建Docker镜像**
   ```bash
   docker build -t streamlit-app .
   ```

3. **运行Docker容器**
   ```bash
   docker run -p 8501:8501 streamlit-app
   ```

4. **访问应用**
   - 本地访问：`http://localhost:8501`
   - 若部署在服务器，需配置防火墙和端口转发

### 3. Heroku部署

**优点**：免费套餐可用，支持自动部署

**步骤**：

1. **安装Heroku CLI**
   - 下载地址：https://devcenter.heroku.com/articles/heroku-cli

2. **创建Heroku应用**
   ```bash
   heroku create your-app-name
   ```

3. **创建Procfile**
   ```
   web: sh setup.sh && streamlit run web_app.py
   ```

4. **创建setup.sh文件**
   ```bash
   mkdir -p ~/.streamlit/echo "[server]\nheadless = true\nport = \$PORT\nenableCORS = false\n" > ~/.streamlit/config.toml
   ```

5. **部署应用**
   ```bash
   git push heroku main
   ```

## 四、部署注意事项

### 1. 数据文件管理
- 确保`data`文件夹中的Excel文件被包含在部署中
- 若文件较大，考虑使用外部存储（如AWS S3、Google Cloud Storage）

### 2. 依赖管理
- 确保`requirements.txt`包含所有必需的包
- 指定包的版本以避免兼容性问题

### 3. 配置文件
- 可使用`.streamlit/config.toml`配置应用设置
- 如端口、主题、缓存设置等

### 4. 安全设置
- 避免在代码中硬编码敏感信息
- 使用环境变量存储配置信息

### 5. 性能优化
- 对大型数据集使用Streamlit缓存
- 优化图表渲染性能

## 五、常见问题排查

1. **应用无法启动**
   - 检查依赖是否正确安装
   - 查看日志中的错误信息

2. **数据文件无法读取**
   - 确认文件路径是否正确
   - 检查文件权限

3. **页面加载缓慢**
   - 优化数据加载和处理逻辑
   - 使用Streamlit缓存

4. **部署平台错误**
   - 查看平台提供的日志
   - 确保配置文件正确

## 六、访问方式

部署成功后，你可以通过以下方式访问应用：
- **Streamlit Cloud**：`https://your-app-name.streamlit.app`
- **Docker**：`http://your-server-ip:8501`
- **Heroku**：`https://your-app-name.herokuapp.com`

根据选择的部署方式，访问地址会有所不同。