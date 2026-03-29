---
name: postgre-skill
description: |
  這是一個用於生成標準化 PostgreSQL Kubernetes Manifest 的技能。
  它會生成一個名為 'postgre' 的 StatefulSet，並啟用 hostNetwork。
  包含一個名為 'postgre-headless' 的 Headless Service，以及一個名為 'postgre-secret' 並帶有隨機密碼的 Secret。
  它會自動偵測並使用集群中的 StorageClass（如果可用），否則將回退到手動建立的 PersistentVolume。
  它包含處理 PostgreSQL 18+ 版本資料目錄變更的邏輯。
  每當使用者提到 postgre 或需要標準資料庫設定時，務必使用此技能。
---

# PostgreSQL Kubernetes 標準佈署技能

此技能可根據嚴格的命名與網路要求，為 PostgreSQL 佈署生成一整套 Kubernetes Manifest。

## 規格要求
- **命名要求**：StatefulSet 的名稱必須為 `postgre`。
- **網路要求**：Pod spec 中必須設定 `hostNetwork: true`。
- **Service 要求**：必須建立一個名為 `postgre-headless` 的 Headless Service。
- **Secret 要求**：必須建立一個名為 `postgre-secret` 的 Secret，並包含隨機生成的 `POSTGRES_PASSWORD`。
- **儲存要求**：PV/PVC 必須透過 StatefulSet 中的 `volumeClaimTemplates` 進行管理。
  - 如果集群中存在 `StorageClass`，則優先使用。
  - 如果沒有可用的 `StorageClass`，則必須包含一個手動建立的 `PersistentVolume` (PV) 作為 fallback，以供生成的 PVC (`postgre-data-postgre-0`) 使用。
- **資料目錄 (掛載路徑)**：
  - PostgreSQL 17 (含) 以下版本：`/var/lib/postgresql/data`
  - PostgreSQL 18+ 或 `latest` 版本：`/var/lib/postgresql`
  - 產生器會根據映像檔版本自動處理此邏輯。
- **Namespace (命名空間)**：預設為 `postgre`。

## 實作指南
當觸發此技能時：
1. 確認使用者是否有自定義的儲存大小或映像檔偏好 (預設值：100Gi, 映像檔：postgres:16)。
2. 執行產生器腳本：`python ~/.agents/skills/postgre-skill/scripts/generate.py [storage] [image] [namespace]`。
3. 將生成的 YAML 內容提供給使用者。

## 範例請求
**使用者：** "幫我產生一個標準的 postgre 部署設定"
**結果：** 顯示包含 postgre Secret、Service 以及具備 hostNetwork 與版本感知儲存設定的 StatefulSet YAML。
