import random
import string
import sys
import base64
import subprocess

def generate_password(length=16):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for i in range(length))

def get_default_storage_class():
    try:
        # Try to get the default storage class
        cmd = "kubectl get sc -o jsonpath='{.items[?(@.metadata.annotations.storageclass\\.kubernetes\\.io/is-default-class==\"true\")].metadata.name}'"
        sc = subprocess.check_output(cmd, shell=True).decode().strip()
        if sc:
            return sc

        # If no default, just pick the first one available
        cmd = "kubectl get sc -o jsonpath='{.items[0].metadata.name}'"
        sc = subprocess.check_output(cmd, shell=True).decode().strip()
        return sc
    except Exception:
        return None

def generate_yaml(storage_size="100Gi", image="postgres:16", namespace="postgre"):
    password = generate_password()
    encoded_password = base64.b64encode(password.encode()).decode()

    storage_class = get_default_storage_class()

    # PostgreSQL 18+ (and latest) requires /var/lib/postgresql
    # Older versions use /var/lib/postgresql/data
    mount_path = "/var/lib/postgresql/data"
    if "latest" in image or any(f":{v}" in image for v in range(18, 30)):
        mount_path = "/var/lib/postgresql"

    yaml_content = f"""---
apiVersion: v1
kind: Secret
metadata:
  name: postgre-secret
  namespace: {namespace}
type: Opaque
data:
  POSTGRES_PASSWORD: {encoded_password}
# Note: Raw password for reference: {password}

---
apiVersion: v1
kind: Service
metadata:
  name: postgre-headless
  namespace: {namespace}
  labels:
    app: postgre
spec:
  ports:
  - port: 5432
    name: tcp-postgre
  clusterIP: None
  selector:
    app: postgre
"""

    if not storage_class:
        yaml_content += f"""
---
apiVersion: v1
kind: PersistentVolume
metadata:
  name: postgre-pv-0
spec:
  capacity:
    storage: {storage_size}
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/data/postgre-0
  claimRef:
    name: postgre-data-postgre-0
    namespace: {namespace}
"""

    yaml_content += f"""
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: postgre
  namespace: {namespace}
spec:
  serviceName: "postgre-headless"
  replicas: 1
  selector:
    matchLabels:
      app: postgre
  template:
    metadata:
      labels:
        app: postgre
    spec:
      hostNetwork: true
      containers:
      - name: postgres
        image: {image}
        ports:
        - containerPort: 5432
          name: postgre
        env:
        - name: POSTGRES_PASSWORD
          valueFrom:
            secretKeyRef:
              name: postgre-secret
              key: POSTGRES_PASSWORD
        volumeMounts:
        - name: postgre-data
          mountPath: {mount_path}
  volumeClaimTemplates:
  - metadata:
      name: postgre-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      {f"storageClassName: {storage_class}" if storage_class else ""}
      resources:
        requests:
          storage: {storage_size}
"""
    return yaml_content

if __name__ == "__main__":
    storage = sys.argv[1] if len(sys.argv) > 1 else "100Gi"
    image = sys.argv[2] if len(sys.argv) > 2 else "postgres:16"
    namespace = sys.argv[3] if len(sys.argv) > 3 else "postgre"
    print(generate_yaml(storage, image, namespace))
