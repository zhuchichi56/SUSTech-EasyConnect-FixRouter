# SUSTech-EasyConnect-FixRouter(mac)

**解决SUSTecher在家连接学校VPN导致无法使用Git等问题**

当在家连接学校VPN时，EasyConnect的客户端默认做全局代理，可能导致某些应用程序（如Git）无法正常工作。然而，EasyConnect客户端没有提供查看和更改选项，而服务端的访问IP权限和IP映射由服务端细致定义。

为了解决这个问题，我们可以尝试通过修改路由表来实现部分流量走VPN，而其他流量绕过VPN，直接访问本地网络，从而保证只有在需要访问知网或校园网资源时才使用EasyConnect的代理功能，不影响其他应用的速度。


## 使用说明

1. 首先将两个文件 `fixRouter.py` 和 `EasyConnect.sh` 放在同一目录下。

2. 打开 `fixRouter.py` 文件，更改 `gateway_to_delete` 变量的值，将其中的 IP 地址改成你在内网中 VPN 的 gateway 地址。

3. 在 `fixRouter.py` 文件中找到如下部分：

   ```python
   # 增加对应vpn的路由，本人要访问的机器是10.xxx.xxx.xxx，所以能访问了
   subprocess.run(['sudo', 'route', '-n', 'add', '-net', '10.0.0.0/8', '10.21.144.10'])
   ```

   将其中的 `10.0.0.0/8` 改成你想要加密的目标网段，`10.21.144.10` 改成上一步中删除的那个 gateway。

4. 运行 `EasyConnect.sh` 脚本：

   ```bash
   ./EasyConnect.sh
   ```

   脚本将会自动执行 `fixRouter.py` 并输入密码，等待脚本执行完成即可。

注意：确保在运行 `EasyConnect.sh` 之前已经安装了 `expect` 工具，它用于自动输入密码。如果你没有安装 `expect`，可以通过以下命令进行安装：

```bash
brew install expect
```

请确保你有权限运行这些脚本，否则可能需要使用 `chmod` 命令给脚本添加执行权限。


