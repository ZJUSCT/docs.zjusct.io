# K8S 调试

当 K8S Pod 中的容器出错进入 Waiting 状态等待重启时，我们无法进入容器调试。此时可以使用 `kubectl debug` 命令拷贝一个新的 Pod，进入调试。

```shell
# Create a copy of mypod changing the command of mycontainer
kubectl debug mypod -it \
    --copy-to=my-debugger --container=mycontainer -- sh
```

这是 `kubectl debug` 自带的示例之一，它将 `mypod` 中的 `mycontainer` 拷贝到一个新的 Pod `my-debugger` 中，并将容器的命令改为 `sh`，以便我们进入调试。新的容器会使用原来容器的镜像和环境变量等配置，但命令被覆盖了。

kubectl debug -n jenkins jenkins-0 -it --copy-to=jenkins-debug --container=jenkins -- sh
