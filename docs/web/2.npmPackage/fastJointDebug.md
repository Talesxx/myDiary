# 在npm包开发中如何快速联调

`在包开发中，常常需要与使用的仓库进行联调以确定问题所在`


## 针对两独立仓库情况下
### 对于无对等依赖的npm包 


使用以下操作进行

#### 第一步 软连接方式使用npm包
```bash
D:\path\you-package> npm link  # 在you-package包目录下运行
D:\path\you-app> npm link  <you-package>  # //在使用了you-package项目中运行
```


#### 第二步 配置webpack 使得可以监听变更<font style="color:#DF2A3F;">（如果你的项目是其他脚手架请参考你的脚手架配置）</font>
这种方式可以让你在dev模式下监听 npm包内容变更时自动重新编译

```typescript
  webpack:(webpackConfig) => {
    let modifiedConfig = webpackConfig;
    if (modifiedConfig.watchOptions) {
      modifiedConfig.watchOptions.ignored = ['**/node_modules/(?!you-package)/**', '**/.git/**']
    }
    return modifiedConfig;
  },
```




### <font style="color:#DF2A3F;">特殊情况</font> 对于使用了peerDependencies（对等依赖）的包使用一下教程
以you-package为例，本文介绍如何在you-app工程通过硬链接的方式联编you-package


#### 修改包的依赖方式(或者手动修改对应依赖格式为 file:xxx/xx)

在package.json中修改对应依赖

```json5
{
    ...
    "dependencies": {
    "you-package": "file:xxx/xx", // 可以是相对也，可以是绝对路径
      },
    ...
}
```

#### 删除node_modules 使用pnpm i安装依赖


```bash
rm -f /node_modules
pnpm i
```
#### 同理 配置webpack 使得可以监听变更 同上

## 在Monorepo中使用 workspace:* （使用pnpm）


```json5
 // root/apps/you-app/package.json
{
    ...
    "dependencies": {
    "you-package": "workspace:*", 
      },
    ...
}
```

####  <font style="color:#DF2A3F;">特殊情况</font> 对于使用了peerDependencies（对等依赖）可能会出现npm包和使用包的app的对等依赖安装的版本不同问题

使用依赖覆盖方式解决

```json5
  // root/package.json
    {
      "name": "monorepo",
      "version": "1.0.0",
      "dependencies": {
        // ...其他依赖
      },
      "pnpm": {
        "overrides": {
          "lodash": "4.18.0" // 比如说lodash是npm包的对等依赖  
          // "react": "18.2.0"
        }
      }
    }
```

#### 同理 配置webpack 使得可以监听变更 同上