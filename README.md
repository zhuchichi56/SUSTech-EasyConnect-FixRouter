# SUSTech-EasyConnect-FixRouter(mac)

**解决SUSTecher在家连接学校VPN导致无法使用Git等问题**

当在家连接学校VPN时，EasyConnect的客户端默认做全局代理，可能导致某些应用程序（如Git）无法正常工作。然而，EasyConnect客户端没有提供查看和更改选项，而服务端的访问IP权限和IP映射由服务端细致定义。

为了解决这个问题，我们可以尝试通过修改路由表来实现部分流量走VPN，而其他流量绕过VPN，直接访问本地网络，从而保证只有在需要访问知网或校园网资源时才使用EasyConnect的代理功能，不影响其他应用的速度。

具体操作步骤如下：

1. 首先，连接EasyConnect VPN，并确保VPN连接成功。

2. 打开终端（Terminal）应用程序。

3. 使用以下命令查看当前的路由表：

   ```bash
   netstat -rn
   ```

   这将显示当前的路由表，包含目标地址、网关、标志和接口等信息。

4. 根据你想要访问的资源，找到相应的目标地址和网关。通常来说，知网或校园网资源的目标地址可能是以特定IP段开头的，例如以10开头的IP地址。记录下相关的目标地址和网关信息。

5. 使用以下命令来删除所有使用特定网关的路由表项：

   ```bash
   sudo route delete <网关地址>
   ```

   例如，如果网关地址是10.21.144.10，那么命令将是：

   ```bash
   sudo route delete 10.21.144.10
   ```

   重复执行上述命令，删除所有使用特定网关的路由表项。

6. 最后，添加一个路由表项，让你希望通过EasyConnect访问的资源走VPN。例如，如果你想要访问的资源是以10开头的IP段，可以使用以下命令添加路由表项：

   ```bash
   sudo route -n add -net 10.0.0.0/8 <网关地址>
   ```

   例如，如果网关地址是10.21.144.10，那么命令将是：

   ```bash
   sudo route -n add -net 10.0.0.0/8 10.21.144.10
   ```

   这样，所有以10开头的IP地址的流量将通过EasyConnect VPN进行访问。

通过上述步骤，你可以实现在使用EasyConnect访问知网或校园网资源时启用代理功能，而其他应用程序将直接访问本地网络，不会被代理拖慢速度。请注意，由于EasyConnect客户端的限制，这只是一种临时解决方案，随着VPN断开和重新连接，可能需要重新执行这些操作。
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
