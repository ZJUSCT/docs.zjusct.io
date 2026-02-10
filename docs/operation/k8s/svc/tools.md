# 服务部署工具

## [kubectl](https://kubernetes.io/docs/reference/kubectl/)

kubectl 已经在 K8S 管理篇中介绍过，这里不再赘述。

## [Helm](https://helm.sh/)

kubectl 是最底层的工具，能够直接操作 Kubernetes API 来管理资源。如果将 kubectl 看作从源码构建应用并安装，那么 Helm 就对应包管理器。

Helm 通过 Chart 来定义一个应用的资源，Chart 中的模板可以使用 Go 模板语法来动态生成 YAML 文件。

## [Kustomize](https://kustomize.io/)

Helm 有时无法满足我们的需求：

- 部分服务没有现成的 Helm Chart。
- 常常需要手动创建一些资源（如 ConfigMap、Secret 等），而现成的 Helm Chart 中没有提供相关模板。

Kustomize 能够使用 Helm Chart，并且能够管理其他更多的资源。

一个具有 `kustomization.yaml` 的目录就是一个 Kustomize 应用。

Kustomize 内建在 kubectl 中，两条常用命令：

- `kubectl kustomize [path]`：渲染 Kustomize 应用，输出 YAML。
- `kubectl apply -k [path]`：渲染并应用 Kustomize 应用。

## [Argo](https://argo-cd.readthedocs.io/en/stable/)

Kustomize + Helm 让我们能够**系统地用文件管理所有 K8S 资源**。于是我们又想：如果能**自动化地将这些资源部署**到集群中就好了。Argo CD 就是一个 GitOps 工具，能够监视 Git 仓库中的 Kustomize、Helm 项目，并自动将其部署到集群中。

Argo 的组成部分：

- API Server
- Repository Server：保存 Git 仓库和应用 manifest 的本地缓存。
- Application Controller：监视应用的运行状态，和预期状态进行对比，并执行所需的同步操作。

### Argo 部署单个服务

Argo 提供下列 CRD：

- `Application`：一个要部署的应用实例
    - `source`：应用的源代码位置（Git 仓库、Helm Chart 等）
    - `destination`：应用要部署到哪个集群和命名空间
- `AppProject`：一组 application
    - `sourceRepos`：允许从哪些 Git 仓库部署应用
    - `destinations`：允许将应用部署到哪些集群和命名空间

### Argo ApplicationSet 批量部署服务

!!! quote

    - [How to create ArgoCD Applications Automatically using ApplicationSet? “Automation of GitOps” | by AmrAlaaYassen | Medium](https://amralaayassen.medium.com/how-to-create-argocd-applications-automatically-using-applicationset-automation-of-the-gitops-59455eaf4f72)

### Argo 维护

#### 强制刷新 ApplicationSet

在 K8S 中，资源出了可以进行标准的 CRUD 操作，往往还能通过 Annotation 和 Label 进行操作。Argo 也不例外，见 [Annotations and Labels used by Argo CD - Argo CD - Declarative GitOps CD for Kubernetes](https://argo-cd.readthedocs.io/en/stable/user-guide/annotations-and-labels/)

- `argocd.argoproj.io/application-set-refresh`：强制刷新 ApplicationSet，重新生成 Application。

#### 暂停应用同步

在 WebUI 进入 Application 详情页，找到你要暂停同步的资源，点击 Pause

#### 部署 Helm 和 Kustomize 应用

https://github.com/argoproj/argo-cd/issues/11564
