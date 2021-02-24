# Tronclass CLI

Tronclass CLI 可以让您使用命令行完成 Tronclass 平台有关的各项工作。

支持的平台：

- [学在浙大](http://courses.zju.edu.cn/)

支持的功能：

- 查看待办事项
- 查看课程列表
- 查看课程内容
- 下载课程资料
- 查看课程作业
- *提交课程作业 (WIP)

## 安装

Tronclass CLI 使用 Python 开发，推荐使用 [pipx](https://github.com/pipxproject/pipx#install-pipx) 安装，pipx 可以自动建立独立的 Python 环境，不会干扰您本地的其它 Python 开发环境。当然，您也可以选择使用 `pip` 进行安装。

```
pipx install tronclass-cli
```

安装完成后，可以使用 `tcc -v` 进行测试。

## 快速开始

首先，您可以添加一个配置文件来指定一些常用信息，如用户名等。配置文件默认位于 `~/.tronclass/config.json`，您可以通过修改环境变量 `TRONCLASS_CLI_CONFIG_FILE` 来指定其它地址。

一个典型的配置文件为：

```json
{
    "session": {
        "username": "31xxxxxxxxx", // 您登录时使用的用户名（学号）
        "auth_provider": "zju"
    },
    "api": {
        "api_url": "zju"
    }
}
```

随后，您可以尝试使用 `tcc todo` 命令查看您的待办事项，第一次使用时需要输入您的密码，密码会被安全地保存至您操作系统的凭据管理器中，后续使用时将不会要求输入密码。您可以使用 `tcc -h` 查看可用的命令，使用 `tcc [command] -h` 查看命令的使用方法。