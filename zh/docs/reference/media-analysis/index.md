# 本地 OCR 和转录

Canonical page: https://phishdestroy.github.io/TgWitness/zh/docs/reference/media-analysis/

通过本地工作进程识别捕获的图像和音频；将生成的文本与源文件保持关联。

[工作流指南](https://phishdestroy.github.io/TgWitness/docs/archive/) · [维基](https://github.com/phishdestroy/TgWitness/blob/main/docs/wiki/Archive-and-Integrations.md)

打开`media.saved`日志记录，选择**“识别附件**”，然后在**“查询存档**”下选择 OCR或转录。处理过程为手动且在本地进行。 不支持云端媒体模式或自动上传。原始附件字节和 `media_sha256`保持不变；识别出的文本会被明确标记为机器 识别结果，并单独存储，同时包含源文件哈希值、引擎/模型版本、 语言、参数及完成时间。转录文本保留返回的时间戳。

请使用**“搜索已识别文本**”功能及 OCR/转录 过滤器来检索这些结果。这是一项独立的衍生数据搜索；它不会在后台将机器 识别结果转换为原始 Telegram 文本，也不会将其添加到已签名的事件中。

## 配置可选的工作进程

第 1 版需要配备本地 Docker 守护进程的 Linux 主机。Windows 系统 可在配备独立本地守护进程的 Linux 虚拟机/WSL 环境中运行 TgWitness。 该面板绝不会自行解码任何不可信的附件。

```
docker build -f deploy/media-worker/Dockerfile -t tgwitness-media:local .
export TGWITNESS_MEDIA_IMAGE=tgwitness-media:local
```

在 TgWitness 服务环境中设置这些变量并重启服务。 守护进程套接字默认值为 `/var/run/docker.sock`；无 root 权限的部署可设置为 `TGWITNESS_DOCKER_SOCKET`。工作进程会明确使用该 Unix 套接字， 而非远程 Docker 上下文。请勿向控制面板用户暴露 Docker API，也请勿将 其套接字挂载到识别容器内。

若需进行转录，请单独安装一个与 CTranslate2 兼容的 Whisper 模型， 然后将 `TGWITNESS_WHISPER_MODEL_DIR` 设置为其目录。工作节点将通过 `local_files_only=True` 加载该模型；所选模型和输入数据将以只读方式挂载。 请参阅引擎的[模型加载文档](https://github.com/SYSTRAN/faster-whisper)。 随附的 OCR 镜像包含英语和俄语的训练数据。如有需要，可将其他 语言构建到您的镜像中；语言代码遵循 [Tesseract 的 CLI 规范](https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html)。

处理过程中不会加载任何模型。构建/下载安装程序可能会使用网络； 每个实际的识别容器均已禁用网络功能。请在启用网络功能前安装镜像； 运行时使用 `--pull=never`。

## 限制与恢复

该容器以无特权用户身份运行，具有只读根目录、已撤销 权限、`no-new-privileges` 配置、1 个 CPU、2 GiB 内存、PID 限制以及受限的 临时文件系统。仅挂载所选文件的经过验证的副本以及可选的 模型目录。 收集器的数据库、存储库和会话均 未挂载。[Docker 运行时](https://docs.docker.com/reference/cli/docker/container/run/) 标志强制执行这些限制；这仍属于容器边界，而非硬件安全区。

文件大小上限为 50 MiB，图像分辨率上限为 2000 万像素，音频时长上限为 30 分钟（ 且时长已知），处理时长上限为 5 分钟。每次仅有一个工作进程运行， 每个工作区最多可有 20 个排队/正在运行的任务，并保留 100 个任务。 “取消”将停止容器；“重试”将创建一个与先前尝试相关联的新任务。 中断的任务在重启后会被标记。当模型 无法适应配置的限制时，处理可能会失败；若未进行隔离，系统不会静默运行。
