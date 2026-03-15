import sys

def generate_yaml(image="quay.io/cooloo9871/bobo:latest", replicas=2):
    yaml_content = f"""---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: bobo
  labels:
    app: bobo
spec:
  replicas: {replicas}
  selector:
    matchLabels:
      app: bobo
  template:
    metadata:
      labels:
        app: bobo
    spec:
      containers:
      - name: bobo
        image: {image}
        ports:
        - containerPort: 80
          name: http

---
apiVersion: v1
kind: Service
metadata:
  name: bobo-svc
  labels:
    app: bobo
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: 80
    protocol: TCP
    name: http
  selector:
    app: bobo
"""
    return yaml_content

if __name__ == "__main__":
    # Allow overriding through arguments if needed
    image = sys.argv[1] if len(sys.argv) > 1 else "quay.io/cooloo9871/bobo:latest"
    replicas = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    print(generate_yaml(image, replicas))
