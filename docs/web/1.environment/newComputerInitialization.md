# 环境安装

## 第一步：在node安装之前推荐使用mvn去管理node版本，

`不推荐直接安装node，在开发多个项目时可能用到不同的node版本。在此推荐使用mvn管理node版本`

<font style="color:#DF2A3F;">⚠如果你的系统已经安装了node，请先卸载它。根据你安装方不同去卸载node这里不做说明.</font>


### windows 安装

在window中直接下载nvm安装包安装即可，安装完成后重启命令行
[github](https://github.com/coreybutler/nvm-windows)

### MAC & Linux


#### 安装NVM

- 确定电脑是否有`homebrew` 没有执行下面命令安装

```bash
/bin/bash -c "$(curl -fsSL https:/raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

- 现在，你的系统已经准备好了，可以进行安装。更新Homebrew软件包列表并安装NVM。

```bash
brew update 
brew install nvm
```

- 接下来，在home目录中为NVM创建一个文件夹。

```bash
mkdir ~/.nvm 
```

- mac可能需要配环境变量。在你的home中编辑以下配置文件，在 `~/.bash_profile`（或`~/.zshrc`，用于macOS Catalina或更高版本）中添加以下几行
```bash
export NVM_DIR=~/.nvm
source$(brew --prefix nvm)/nvm.sh
```

- 按ESC + `:wq` 保存并关闭你的文件。

```bash
source ~/.bash_profile
```

- 接下来，将该变量加载到当前的shell环境中。在下一次登录，它将自动加载。

NVM已经安装在你的macOS/Linux系统上。

- 验证安装

```bash
nvm -v
```


## 第二步 : 如何使用NVM  且用NVM安装Node.js

- 首先，看看有哪些Node版本可以安装。要查看可用的版本，请输入。

```bash
nvm list available
```

- 现在，你可以安装上述输出中列出的任何版本。你也可以使用别名，如node代表最新版本，lts代表最新的LTS版本，等等。

例子：

|   CURRENT    |     LTS      |  OLD STABLE  | OLD UNSTABLE |
|--------------|--------------|--------------|--------------|
|    24.7.0    |   22.19.0    |   0.12.18    |   0.11.16    |
|    24.6.0    |   22.18.0    |   0.12.17    |   0.11.15    |
|    24.5.0    |   22.17.1    |   0.12.16    |   0.11.14    |
|    24.4.1    |   22.17.0    |   0.12.15    |   0.11.13    |
|    24.4.0    |   22.16.0    |   0.12.14    |   0.11.12    |
|    24.3.0    |   22.15.1    |   0.12.13    |   0.11.11    |
|    24.2.0    |   22.15.0    |   0.12.12    |   0.11.10    |
|    24.1.0    |   22.14.0    |   0.12.11    |    0.11.9    |

这里安装例子中最新的LTS
```bash
 nvm install 22.19.0 #安装
 nvm use 22.19.0 # 使用
```
- 安装后，你可以用以下方法来验证所安装的node.js是否安装成功。
```bash
node -v
```

