---
name: bobo-skill
description: |
  A skill for generating standardized Kubernetes manifests for the 'bobo' application. 
  It produces a Deployment named 'bobo' with 2 replicas using image 'quay.io/cooloo9871/bobo:latest', 
  and a ClusterIP Service named 'bobo-svc'. 
  Use this skill whenever the user mentions 'bobo', 'bobo deployment', or 'bobo-svc'.
---

# Bobo Kubernetes Standard Skill

This skill provides a standardized way to generate Kubernetes manifests for the `bobo` application, following strict naming and configuration requirements.

## Specifications
- **Deployment Name**: MUST be `bobo`.
- **Image**: MUST be `quay.io/cooloo9871/bobo:latest`.
- **Replicas**: MUST be `2`.
- **Container Port**: MUST be `3000`.
- **Service Name**: MUST be `bobo-svc`.
- **Service Type**: MUST be `ClusterIP`.
- **Service Port**: MUST be `3000`.

## Implementation Guide
When triggered:
1. Identify if the user wants custom replicas or image (though defaults are standardized).
2. Execute the generator: `python ~/.agents/skills/bobo-skill/scripts/generate_bobo.py [image] [replicas]`.
3. Provide the output YAML to the user.

## Example Request
**User:** "幫我產生一個 bobo 部署設定"
**Result:** Displays the YAML with bobo Deployment (2 pods) and bobo-svc (ClusterIP).
