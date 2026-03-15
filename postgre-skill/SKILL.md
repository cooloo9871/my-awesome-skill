---
name: postgre-skill
description: |
  A skill for generating standardized PostgreSQL Kubernetes manifests.
  It produces a StatefulSet named 'postgre' with hostNetwork enabled,
  a headless service named 'postgre-headless', and a secret 'postgre-secret'
  with a randomly generated password.
  It automatically detects and uses the cluster's StorageClass if available,
  otherwise it falls back to a manual PersistentVolume.
  It includes logic to handle PostgreSQL 18+ data directory changes.
  Make sure to use this skill whenever the user mentions postgre or standardized db setup.
---

# PostgreSQL Kubernetes Standard Skill

This skill generates a complete set of Kubernetes manifests for a PostgreSQL deployment, following strict naming and network requirements.

## Specifications
- **Name Requirement**: StatefulSet MUST be named `postgre`.
- **Network Requirement**: `hostNetwork: true` MUST be set in the Pod spec.
- **Service Requirement**: A headless service named `postgre-headless` MUST be created.
- **Secret Requirement**: A secret named `postgre-secret` MUST be created with a random `POSTGRES_PASSWORD`.
- **Storage Requirement**: PV/PVC MUST be managed via `volumeClaimTemplates` in the StatefulSet.
  - If a `StorageClass` exists in the cluster, it will be used.
  - If NO `StorageClass` is available, a manual `PersistentVolume` (PV) of the requested size MUST be included as a fallback for the generated PVC (`postgre-data-postgre-0`).
- **Data Directory (Mount Path)**:
  - For PostgreSQL 17 and below: `/var/lib/postgresql/data`
  - For PostgreSQL 18+ and `latest`: `/var/lib/postgresql`
  - The generator handles this logic automatically based on the image version.
- **Namespace**: Default to `postgre`.

## Implementation Guide
When triggered:
1. Determine if the user has custom storage size or image preferences (Default: 100Gi, Image: postgres:16).
2. Execute the generator: `python ~/.agents/skills/postgre-skill/scripts/generate.py [storage] [image] [namespace]`.
3. Provide the output YAML to the user.

## Example Request
**User:** "幫我產生一個標準的 postgre 部署設定"
**Result:** Displays the YAML with postgre Secret, Service, and StatefulSet with hostNetwork and version-aware storage configuration.
