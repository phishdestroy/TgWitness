# 几分钟内即可开始使用

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/start/

先在演示中随便看看，再连接您自己的账户。

## 无需注册即可浏览

获取项目，准备好 **Python 3.11 或更高版本**，运行演示。其余的由启动器完成。

```
git clone https://github.com/phishdestroy/TgWitness.git
cd TgWitness
```

### Windows

```
.\scripts\Demo.cmd
```

### Linux / macOS

```
sh start.sh --demo
```

浏览器中会打开一个包含虚构消息的工作区。打开聊天，对比一次编辑，查看一份导出。不涉及 Telegram。

![TgWitness 对话视图及示例消息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

一个示例工作区。您的日志将单独创建。

## 创建您自己的工作区

关闭演示，然后：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

打开启动器显示的地址，粘贴它所指文件中的**面板访问令牌**。这是 TgWitness 的令牌，不是 Telegram 的。

## 捕获您的第一条消息

1. [连接一个专用的 Telegram 账户。](https://phishdestroy.github.io/TgWitness/zh/docs/accounts/)
2. 选择一个群组或频道，开始观察。
3. 在测试群组中发送一条消息，看着它出现在日志中。

如需进行服务器安装，请参阅《[保持运行》](https://phishdestroy.github.io/TgWitness/zh/docs/server/)。
