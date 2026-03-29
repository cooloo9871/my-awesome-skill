---
name: cnpg-skill
description: 專用於在 Kubernetes 上安裝與部署 CloudNativePG (CNPG) 的技能。當使用者需要安裝 CloudNativePG Operator 或建立 PostgreSQL 叢集時，請務必使用此技能。
---

# CloudNativePG (CNPG) 部署技能

本技能提供在 Kubernetes 上部署 CloudNativePG (CNPG) 的標準化流程與最佳實作。CloudNativePG 是一個開源的 Postgres Operator，旨在管理 Kubernetes 上的 PostgreSQL 負載。

## 核心流程

### 1. 安裝 CloudNativePG Operator

當需要安裝 Operator 時，請執行以下步驟：

1.  建立 `cnpg-system` 命名空間（如果不存在）。
2.  部署 CloudNativePG Operator 的官方 YAML。

**推薦指令：**
```bash
kubectl apply -f https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/main/releases/cnpg-1.24.0.yaml
```
*(注意：版本號應根據目前的最新穩定版進行調整。)*

### 2. 驗證 Operator 狀態

在建立 Cluster 之前，必須確認 Operator 已正確執行：
```bash
kubectl get deployment -n cnpg-system cnpg-controller-manager
```

### 3. 部署 CloudNativePG Cluster (最佳實作)

根據使用者的需求，建立名為 `mycnpg` 的叢集。此配置包含 2 個執行個體（1 Primary + 1 Replica）以提供基本的高可用性，並使用叢集內的 `storageClass` 建立 50Gi 的磁碟。

#### Cluster Manifest Template:
```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: mycnpg
spec:
  instances: 2
  imageName: ghcr.io/cloudnative-pg/postgresql:16
  storage:
    size: 50Gi
  bootstrap:
    initdb:
      database: cnpg
      owner: bigred
      secret:
        name: cnpg-bigred
```

## 使用指南

- **安裝 Operator**：當使用者要求「安裝 cnpg」、「安裝 operator」時，請執行步驟 1。
- **建立 Cluster**：當使用者要求「建立 cluster」、「部署 postgres」時，請先確認步驟 2 已通過，再執行步驟 3。
- **命名規範**：叢集名稱預設為 `mycnpg`，執行個體數量為 2。
- **存儲配置**：自動使用叢集預設的 `storageClass`，大小設定為 50Gi。
- **資料庫初始化**：資料庫為 `cnpg`，擁有者為 `bigred`，密鑰名稱為 `cnpg-bigred`。

## 檢查點
- 確認 `cnpg-system` namespace 存在。
- 確認 `cnpg-controller-manager` pod 狀態為 Running。
- 確認 `cnpg-bigred` secret 在部署 Cluster 前已存在或已規劃建立。
