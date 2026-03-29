---
name: bobo-skill
description: |
  這是一個用於為 'bobo' 應用程式生成標準化 Kubernetes Manifest 的技能。
  它會生成一個名為 'bobo' 的 Deployment（包含 2 個副本），使用 'quay.io/cooloo9871/bobo:latest' 映像檔，
  以及一個名為 'bobo-svc' 的 ClusterIP Service。
  每當使用者提到 'bobo'、'bobo 部署' 或 'bobo-svc' 時，務必使用此技能。
---

# Bobo Kubernetes 標準佈署技能

此技能可根據嚴格的命名與設定要求，為 `bobo` 應用程式生成標準化 Kubernetes Manifest。

## 規格要求
- **Deployment 名稱**：必須為 `bobo`。
- **映像檔 (Image)**：必須為 `quay.io/cooloo9871/bobo:latest`。
- **副本數 (Replicas)**：必須為 `2`。
- **容器埠號 (Container Port)**：必須為 `3000`。
- **Service 名稱**：必須為 `bobo-svc`。
- **Service 類型**：必須為 `ClusterIP`。
- **Service 埠號**：必須為 `3000`。

## 實作指南
當觸發此技能時：
1. 確認使用者是否需要自定義副本數或映像檔 (雖然預設值為標準配置)。
2. 執行產生器腳本：`python ~/.agents/skills/bobo-skill/scripts/generate_bobo.py [image] [replicas]`。
3. 將生成的 YAML 內容提供給使用者。

## 範例請求
**使用者：** "幫我產生一個 bobo 部署設定"
**結果：** 顯示包含 bobo Deployment (2 個 pod) 與 bobo-svc (ClusterIP) 的 YAML。
