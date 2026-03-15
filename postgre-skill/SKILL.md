---
name: postgre-skill
description: |
  A skill for generating standardized PostgreSQL Kubernetes manifests.
  It produces a StatefulSet named 'postgre' with hostNetwork enabled,
  a headless service named 'postgre-headless', and a secret 'postgre-secret'
  with a randomly generated password. This skill handles both MySQL (as requested by naming conventions)
  and PostgreSQL deployments following the exact naming structure provided by the user.
  Make sure to use this skill whenever the user mentions postgre or standardized db setup.
---

# PostgreSQL Kubernetes Standard Skill

This skill generates a complete set of Kubernetes manifests for a PostgreSQL deployment, following strict naming and network requirements.

## Specifications
- **Name Requirement**: StatefulSet MUST be named `postgre`.
- **Network Requirement**: `hostNetwork: true` MUST be set in the Pod spec.
- **Service Requirement**: A headless service named `postgre-headless` MUST be created.
- **Secret Requirement**: A secret named `postgre-secret` MUST be created with a random `POSTGRES_PASSWORD`.
- **Storage Requirement**: PV/PVC MUST be managed via `volumeClaimTemplates` in the StatefulSet. A default `PersistentVolume` (PV) of 100Gi MUST be included as a fallback for the generated PVC (`postgre-data-postgre-0`).
- **Namespace**: Default to `postgre`.

## Implementation Guide
When triggered:
1. Determine if the user has custom storage size or image preferences (Default: 100Gi).
2. Execute the generator: `python ~/.agents/skills/postgre-skill/scripts/generate.py [storage] [image] [namespace]`.
3. Provide the output YAML to the user.

## Example Request
**User:** "幫我產生一個標準的 postgre 部署設定"
**Result:** Displays the YAML with postgre Secret, Service, and StatefulSet with hostNetwork.
