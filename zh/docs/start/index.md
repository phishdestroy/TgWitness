# 几分钟内即可开始使用

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/start/

首先，请查看一个示例。然后连接您的账户。

## 无需注册即可浏览

下载或克隆该项目，安装 **Python 3.11 或更高版本**，然后运行演示程序。启动器会创建本地环境并安装已标记的依赖项。

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

浏览器将打开一个包含虚构消息的工作区。您可以打开对话、比较编辑内容并检查导出文件。演示模式不会连接到 Telegram。

![TgWitness 对话视图及示例消息](https://phishdestroy.github.io/TgWitness/assets/chats-dark.png)

一个示例工作区。您的日志将单独创建。

## 创建您自己的工作区

关闭演示流程，然后使用常规启动器：

### Windows

```
.\Start.cmd
```

### Linux / macOS

```
sh start.sh
```

打开启动器显示的本地地址。如果系统提示，请输入终端中指定本地文件中的**面板访问令牌**。这将解锁 TgWitness；该操作与 Telegram 登录是分开的。

## 捕获您的第一条消息

1. [连接一个专用的 Telegram 账户。](https://phishdestroy.github.io/TgWitness/zh/docs/accounts/)
2. 选择该账户可访问的群组或频道，然后开始监控。
3. 在您控制的测试群组中发送一条新消息，并确认该消息是否出现在日志中。

如需进行服务器安装，请参阅《[保持运行》](https://phishdestroy.github.io/TgWitness/zh/docs/server/)。
