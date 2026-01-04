# Git安装与环境配置详细指南

## 一、为什么Git命令无法执行？

从你的命令输出可以看到：
```
git : 无法将“git”项识别为 cmdlet、函数、脚本文件或可运行程序的名称。
```

这说明：
1. **Git未安装**：你的电脑上还没有安装Git软件
2. 或**Git未添加到系统路径**：Git已安装但系统无法找到它

## 二、Git安装步骤

### 1. 下载Git安装包

访问Git官方下载页面：
```
https://git-scm.com/download/win
```

页面会自动检测你的Windows版本（32位/64位），并提供下载链接。

### 2. 运行Git安装程序

下载完成后，找到安装文件（通常是`Git-x.y.z-64-bit.exe`），双击运行。

### 3. 安装过程配置

**按照以下步骤进行安装配置**（大部分保持默认即可）：

#### 步骤1：选择安装目录
- 默认安装在 `C:\Program Files\Git\`
- 可以保持默认，点击「Next」

#### 步骤2：选择组件
- 保持所有默认组件勾选，点击「Next」

#### 步骤3：选择开始菜单文件夹
- 保持默认「Git」，点击「Next」

#### 步骤4：选择Git默认编辑器
- 建议选择「Use Visual Studio Code as Git's default editor」
- 如果没有VS Code，保持默认的「Vim」也可以
- 点击「Next」

#### 步骤5：设置Git的初始化分支名称
- 选择「Override the default branch name for new repositories」
- 输入「main」作为默认分支名
- 点击「Next」

#### 步骤6：调整环境变量
- **非常重要！** 选择「Git from the command line and also from 3rd-party software」
- 这个选项会将Git添加到系统环境变量中
- 点击「Next」

#### 步骤7：选择HTTPS传输后端
- 保持默认「Use the OpenSSL library」，点击「Next」

#### 步骤8：配置行结束符转换
- 保持默认「Checkout Windows-style, commit Unix-style line endings」
- 点击「Next」

#### 步骤9：配置终端模拟器
- 选择「Use Windows' default console window」
- 点击「Next」

#### 步骤10：配置额外选项
- 保持默认选项勾选：
  - Enable file system caching
  - Enable Git Credential Manager Core
- 点击「Next」

#### 步骤11：开始安装
- 点击「Install」按钮开始安装
- 安装完成后，点击「Finish」

## 三、验证Git安装

### 1. 打开命令行终端

安装完成后，打开「命令提示符」或「PowerShell」：
- 按 `Win + R` 键，输入 `cmd` 或 `powershell`，按Enter

### 2. 检查Git版本

在终端中输入以下命令并按Enter：
```bash
git --version
```

如果安装成功，会显示Git的版本信息，例如：
```
git version 2.43.0.windows.1
```

## 四、配置Git环境

### 1. 设置用户名和邮箱

在终端中执行以下命令（替换为你的GitHub账户信息）：

```bash
git config --global user.name "你的GitHub用户名"
git config --global user.email "你的GitHub注册邮箱"
```

### 2. 验证配置

输入以下命令查看配置：
```bash
git config --list
```

你应该能看到刚才设置的用户名和邮箱。

## 五、重新执行Git命令

现在你可以重新尝试之前的Git命令了：

1. **进入项目目录**：
   ```bash
   cd f:\2025比赛\2025数据分析省赛\project
   ```

2. **初始化Git仓库**（如果还没有初始化）：
   ```bash
   git init
   ```

3. **关联远程仓库**：
   ```bash
   git remote add origin https://github.com/wang20260103/data-analysis.git
   ```

4. **检查仓库状态**：
   ```bash
   git status
   ```

5. **添加文件**：
   ```bash
   git add .
   ```

6. **提交代码**：
   ```bash
   git commit -m "Initial commit - 数据分析省赛项目"
   ```

7. **推送代码**：
   ```bash
   git push -u origin main
   ```

## 六、常见问题解决

### 1. 安装后仍然无法识别git命令

**解决方法**：
- 关闭并重新打开命令行终端
- 检查系统环境变量是否包含Git路径
- 重启电脑后再次尝试

### 2. 如何检查系统环境变量？

1. 右键点击「此电脑」→「属性」
2. 点击「高级系统设置」→「环境变量」
3. 在「系统变量」中找到「Path」
4. 检查是否包含 `C:\Program Files\Git\cmd`
5. 如果没有，点击「编辑」→「新建」，添加这个路径

### 3. 安装过程中应该选择哪些选项？

关键选项：
- 环境变量：选择「Git from the command line and also from 3rd-party software」
- 默认分支名：设置为「main」
- 终端：选择「Use Windows' default console window」

其他选项可以保持默认。

## 七、继续之前的任务

安装并配置好Git后，你可以继续之前的任务：
1. 将代码提交到本地Git仓库
2. 推送到GitHub远程仓库
3. 部署到Streamlit Cloud

详细步骤可以参考之前创建的指南文件。