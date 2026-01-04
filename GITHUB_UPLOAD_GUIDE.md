# 将代码上传到GitHub的详细步骤

## 一、安装Git

### Windows系统
1. 访问Git官网：https://git-scm.com/download/win
2. 下载适合你系统的Git安装包
3. 双击安装包，按照默认选项进行安装
4. 安装完成后，打开命令提示符（cmd）或PowerShell，输入以下命令验证安装：
   ```bash
   git --version
   ```

## 二、配置Git环境

### 1. 设置用户名和邮箱
这些信息将显示在你的GitHub提交记录中：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
```

### 2. 配置SSH密钥（可选但推荐）
使用SSH可以避免每次推送时都输入密码：

1. 生成SSH密钥：
   ```bash
   ssh-keygen -t ed25519 -C "你的GitHub注册邮箱"
   ```

2. 按Enter键接受默认路径和空密码

3. 启动SSH代理：
   ```bash
   eval $(ssh-agent -s)
   ```

4. 添加SSH密钥到代理：
   ```bash
   ssh-add ~/.ssh/id_ed25519
   ```

5. 复制SSH公钥内容：
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

6. 登录GitHub，进入"Settings" → "SSH and GPG keys" → "New SSH key"
7. 粘贴公钥内容，设置标题，点击"Add SSH key"

## 三、初始化本地Git仓库

1. 进入项目目录：
   ```bash
   cd f:\2025比赛\2025数据分析省赛\project
   ```

2. 初始化Git仓库：
   ```bash
   git init
   ```

## 四、创建.gitignore文件

创建.gitignore文件来排除不需要上传的文件：

```bash
# 打开记事本创建.gitignore
notepad .gitignore
```

在记事本中添加以下内容：
```
# Python文件
__pycache__/
*.py[cod]
*$py.class

# 数据文件（根据需要决定是否上传）
# data/

# 环境文件
.env
venv/
*.venv/
env/

# IDE配置
.idea/
.vscode/
*.swp
*.swo
*~

# 日志文件
*.log

# 操作系统文件
.DS_Store
Thumbs.db

# 临时文件
*.tmp
*.temp
```

保存并关闭记事本。

## 五、提交本地代码

1. 查看当前仓库状态：
   ```bash
   git status
   ```

2. 添加所有文件到暂存区：
   ```bash
   git add .
   ```

3. 提交代码到本地仓库：
   ```bash
   git commit -m "Initial commit - 数据分析省赛项目"
   ```

## 六、在GitHub创建远程仓库

1. 登录GitHub：https://github.com/
2. 点击右上角的"+"号，选择"New repository"
3. 填写仓库信息：
   - Repository name：输入仓库名称（如：data-analysis-competition）
   - Description：可选，输入项目描述
   - Repository type：选择"Public"（公开）或"Private"（私有）
   - Initialize this repository with：不要勾选任何选项
4. 点击"Create repository"

## 七、关联本地仓库和远程仓库

### 方法1：使用HTTPS（简单但每次推送需要输入密码）

在GitHub仓库页面复制HTTPS地址（如：https://github.com/你的用户名/仓库名.git）

```bash
git remote add origin https://github.com/你的用户名/仓库名.git
```

### 方法2：使用SSH（推荐，需要已配置SSH密钥）

在GitHub仓库页面复制SSH地址（如：git@github.com:你的用户名/仓库名.git）

```bash
git remote add origin git@github.com:你的用户名/仓库名.git
```

## 八、推送代码到GitHub

1. 推送代码：
   ```bash
   git push -u origin main
   ```

   如果使用HTTPS方式，会提示输入GitHub用户名和密码（或个人访问令牌）

2. 验证推送结果：
   - 刷新GitHub仓库页面
   - 查看代码是否已成功上传

## 九、后续代码更新步骤

当你修改了代码后，重复以下步骤：

1. 查看修改状态：
   ```bash
   git status
   ```

2. 添加修改的文件：
   ```bash
   git add .
   ```

3. 提交修改：
   ```bash
   git commit -m "描述你的修改内容"
   ```

4. 推送更新：
   ```bash
   git push
   ```

## 十、常见问题解决

### 1. 推送失败：fatal: unable to access 'https://github.com/...'
- 检查网络连接
- 确认GitHub用户名和密码是否正确
- 如果使用HTTPS，尝试使用个人访问令牌代替密码

### 2. SSH连接失败：Permission denied (publickey)
- 检查SSH密钥是否正确生成
- 确认SSH密钥已添加到GitHub账户
- 验证SSH连接：`ssh -T git@github.com`

### 3. 本地分支与远程分支不同步
- 先拉取远程更新：`git pull origin main`
- 解决冲突后再推送：`git push origin main`

## 十一、GitHub Desktop（图形界面可选）

如果你不习惯命令行，也可以使用GitHub Desktop：

1. 下载安装：https://desktop.github.com/
2. 使用GitHub账户登录
3. 点击"Add" → "Add Existing Repository"
4. 选择项目目录
5. 点击"Publish Repository"推送到GitHub

---

完成以上步骤后，你的代码就成功上传到GitHub了！你可以在GitHub仓库页面查看和管理你的代码。