# 对象存储：RadosGW

## Rook

具体内容请阅读官方文档 [Object Storage (RGW) - Rook Ceph Documentation](https://rook.io/docs/rook/latest-release/Storage-Configuration/Object-Storage-RGW)，本节只做简要记录。

使用 Rook Ceph 管理 Ceph 对象存储，需要经过下面几个步骤：

- 创建 `CephObjectStore`。创建后，Ceph RGW pod 就会启动。

    - **Helm Chart**：如果使用 Helm Chart，那么为 `rook-ceph-cluster` 配置好 `cephObjectStores` 就会自动创建一个名为 `default` 的该 CRD，无须再创建。
    - **访问**：在 K8S 内，通过 `rook-ceph-rgw-<objectStoreName>.<objectStoreNamespace>.svc` 访问。

- 创建 `ObjectBucketClaim`。这与 `PersistentVolumeClaim` 类似。创建该 CRD 后，Ceph 中就会创建对应的 bucket，并在 K8S 中创建一个 Secret 和 ConfigMap，包含访问该 bucket 的必要信息。




