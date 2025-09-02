# 环境安装

## 第一步：在node安装之前推荐使用mvn去管理node版本，

`不推荐直接安装node，在开发多个项目时可能用到不同的node版本。在此推荐使用mvn管理node版本`


#### 1.删除现有Node版本

如果你的系统已经安装了node，请先卸载它。我的系统已经通过Homebrew安装了node。所以先把它卸载了。如果还没有安装就跳过。

根据你安装方不同去卸载node这里不做说明。


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

- 现在，你可以安装上述输出中列出的任何版本。你也可以使用别名，如node代表最新版本，lts代表最新的LTS版本，等等。

- 安装后，你可以用以下方法来验证所安装的node.js是否安装成功。

- 如果你在系统上安装了多个版本，你可以在任何时候将任何版本设置为默认版本。要设置节点10为默认版本，只需使用。
