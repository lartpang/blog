---
title: "【译】使用便携模式的VSCode"
date: 2024-07-30 07:17:42
tags: ["tool"]
---
> 原始文档：https://code.visualstudio.com/docs/editor/portable#_migrate-to-portable-mode

Visual Studio Code 支持[便携模式](https://en.wikipedia.org/wiki/Portable_application)。此模式使 VS Code 创建和维护的所有数据都位于自身附近，因此可以在环境中移动。

此模式还提供了一种设置 VS Code 扩展的安装文件夹位置的方法，这对于阻止在 Windows AppData 文件夹中安装扩展的企业环境非常有用。

便携模式支持 Windows 的 ZIP 下载，Linux 的 TAR.GZ 下载，以及 macOS 的常规应用程序下载。请参阅[下载页面](https://code.visualstudio.com/download)以查找适合您平台的正确文件。

> [!note]
> 请勿尝试在从 Windows User or System installers 进行安装时配置便携模式。便携模式仅在 Windows ZIP 存档上受支持。另请注意，Windows ZIP压缩包不支持自动更新。

## 启用便携模式

### Windows、Linux

解压缩 VS Code 下载后，在 VS Code 的文件夹中创建一个文件夹：`data`

```
|- VSCode-win32-x64-1.84.2
|   |- Code.exe (or code executable)
|   |- data
|   |- bin
|   |  |- code
|   |  |- ...
|   |- ...
```
从那时起，该文件夹将用于包含所有 VS Code 数据，包括会话状态、首选项、扩展等。

> [!note]
> 该文件夹将覆盖 `--user-data-dir` 和 `--extensions-dir` 这两个[命令行](https://code.visualstudio.com/docs/editor/command-line#_advanced-cli-options)选项。

`data` 文件夹可以移动到其他 VS Code 安装中。这对于更新可移植的 VS Code 版本非常有用，在这种情况下，您可以将文件夹移动到较新的 VS Code 提取版本。

### macOS

在 macOS 上，您需要将数据文件夹作为应用程序本身的同级文件夹。由于该文件夹将与应用程序并列，因此您需要专门命名它，以便 VS Code 可以找到它。默认文件夹名称为：`code-portable-data`。

```
|- Visual Studio Code.app
|- code-portable-data
```

如果您的应用程序处于[隔离状态](https://apple.stackexchange.com/a/104875)，则便携模式将不起作用，如果您刚刚下载了 VS Code，则默认情况下会发生这种情况。如果便携模式似乎不起作用，请确保删除隔离属性：

```
xattr -dr com.apple.quarantine Visual\ Studio\ Code.app
```

> [!note]
> 在预览体验成员上，文件夹应命名为 `code-insiders-portable-data`。

## 更新便携式 VS Code

- 在 Windows 和 Linux 上，可以通过将 `data` 文件夹复制到 VS Code 的最新版本来更新 VS Code。

- 在 macOS 上，自动更新应一如既往地工作，无需额外工作。

## 迁移到便携模式

您还可以将现有安装迁移到便携模式。

### Windows、Linux

1. 下载适用于您的平台的 [VS Code](https://code.visualstudio.com/download)（或 [VS Code Insiders](https://code.visualstudio.com/insiders)）ZIP 分发。

2. 如上所述创建 `data` 文件夹。
3. 将用户数据目录 `Code` 复制到 `data` 中，并重命名为 `user-data`。
    - Windows `%APPDATA%\Code`
    - Linux `$HOME/.config/Code`
4. 将扩展目录复制到 `data`。
    - Windows `%USERPROFILE%\.vscode\extensions`
    - Linux `~/.vscode/extensions`

例如，以下是 Windows 上的预期结果：

```
|- VSCode-win32-x64-1.84.2
|   |- Code.exe (or code executable)
|   |- data
|   |   |- user-data
|   |   |   |- ...
|   |   |- extensions
|   |   |   |- ...
|   |- ...
```

### macOS

下载适用于 macOS 的 [VS Code](https://code.visualstudio.com/download)（或 [VS Code Insiders](https://code.visualstudio.com/insiders)）。

1. 如上所述创建文件夹 `code-portable-data`。
2. 将用户数据目录 `$HOME/Library/Application Support/Code` 复制到 `code-portable-data` 并重命名为 `user-data`。
3. 将扩展目录 `~/.vscode/extensions` 复制到 `code-portable-data
`。

## TMP 目录

默认情况下，即使在便携模式下，默认的 `TMP` 目录仍然是系统目录，因为那里没有保留任何状态。如果您还希望将 TMP 目录放在可移植目录中，则可以在 `data` 文件夹内创建一个空目录 `tmp`。只要目录存在，它就会用于 TMP 数据。