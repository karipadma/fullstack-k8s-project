# Employee Management System on AWS EKS

A cloud-native Employee Management application deployed on Amazon EKS.

## Architecture

Browser
↓
Frontend (Nginx + HTML/JS)
↓
AWS Load Balancer
↓
Flask Backend API
↓
Amazon RDS MySQL

Future Enhancement:
Backend → Redis Cache → RDS

---

## Technologies Used

- Docker
- Kubernetes
- Amazon EKS
- Amazon ECR
- Amazon RDS MySQL
- Flask
- HTML
- JavaScript
- AWS Load Balancer

---

## Project Structure

backend/
├── app.py
├── db.py
├── config.py
├── requirements.txt
├── Dockerfile
├── deployment.yaml
└── service.yaml

frontend/
├── index.html
├── Dockerfile
├── deployment.yaml
└── service.yaml

---

# Step 1: Create EKS Cluster

Install eksctl

```bash
curl --silent --location \
"https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" \
| tar xz -C /tmp

sudo mv /tmp/eksctl /usr/local/bin
```

Verify:

```bash
eksctl version
```

Create cluster:

```bash
eksctl create cluster \
--name my-eks-cluster \
--region us-east-1 \
--nodegroup-name linux-nodes \
--node-type t3.medium \
--nodes 2
```

Verify:

```bash
kubectl get nodes
```

---

# Step 2: Create RDS MySQL

Create MySQL database in AWS RDS.

Create database:

```sql
CREATE DATABASE employees;
```

Create table:

```sql
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    role VARCHAR(100)
);
```

Insert sample data:

```sql
INSERT INTO employees (name, role)
VALUES
('John','Developer'),
('Mary','Manager'),
('David','Tester');
```

---

# Step 3: Backend Docker Image

Backend Dockerfile:

```dockerfile
FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python","app.py"]
```

Build image:

```bash
docker build -t backend:v1 .
```

Run locally:

```bash
docker run -p 5000:5000 backend:v1
```

---

# Step 4: Create ECR Repository

Create repository:

```bash
aws ecr create-repository \
--repository-name backend \
--region us-east-1
```

Login:

```bash
aws ecr get-login-password --region us-east-1 \
| docker login \
--username AWS \
--password-stdin ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

Tag image:

```bash
docker tag backend:v1 \
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend:v1
```

Push image:

```bash
docker push \
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend:v1
```

---

# Step 5: Backend Deployment

deployment.yaml

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: backend-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: backend

  template:
    metadata:
      labels:
        app: backend

    spec:
      containers:
      - name: backend

        image: ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend:v1

        ports:
        - containerPort: 5000
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

Verify:

```bash
kubectl get pods
```

---

# Step 6: Backend Service

service.yaml

```yaml
apiVersion: v1
kind: Service

metadata:
  name: backend-service

spec:
  type: LoadBalancer

  selector:
    app: backend

  ports:
  - port: 80
    targetPort: 5000
```

Deploy:

```bash
kubectl apply -f service.yaml
```

Verify:

```bash
kubectl get svc
```

Copy backend LoadBalancer URL.

---

# Step 7: Test Backend

Get employees:

```bash
curl http://BACKEND-LB/api/employees
```

Add employee:

```bash
curl -X POST \
-H "Content-Type: application/json" \
-d '{"name":"Alex","role":"Developer"}' \
http://BACKEND-LB/api/employees
```

---

# Step 8: Frontend Docker Image

Frontend Dockerfile:

```dockerfile
FROM nginx

COPY index.html /usr/share/nginx/html/index.html
```

Build image:

```bash
docker build -t frontend:v1 .
```

---

# Step 9: Push Frontend Image

Create repository:

```bash
aws ecr create-repository \
--repository-name frontend \
--region us-east-1
```

Tag image:

```bash
docker tag frontend:v1 \
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/frontend:v1
```

Push image:

```bash
docker push \
ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/frontend:v1
```

---

# Step 10: Frontend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment

metadata:
  name: frontend-deployment

spec:
  replicas: 2

  selector:
    matchLabels:
      app: frontend

  template:
    metadata:
      labels:
        app: frontend

    spec:
      containers:
      - name: frontend

        image: ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/frontend:v1

        ports:
        - containerPort: 80
```

Deploy:

```bash
kubectl apply -f deployment.yaml
```

---

# Step 11: Frontend Service

```yaml
apiVersion: v1
kind: Service

metadata:
  name: frontend-service

spec:
  type: LoadBalancer

  selector:
    app: frontend

  ports:
  - port: 80
    targetPort: 80
```

Deploy:

```bash
kubectl apply -f service.yaml
```

Verify:

```bash
kubectl get svc
```

Copy frontend LoadBalancer URL.

---

# Step 12: Enable CORS

Install:

```bash
pip install flask-cors
```

Update app.py:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
```

Rebuild image.

Push new version.

Update deployment:

```bash
kubectl set image deployment/backend-deployment \
backend=ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/backend:v2
```

---

# Step 13: Verify Application

Open:

```text
http://FRONTEND-LB
```

Features:

- Add Employee
- Get Employees

Verify data is stored in RDS.

---

# Kubernetes Commands

```bash
kubectl get pods
kubectl get svc
kubectl get deployments
kubectl logs deployment/backend-deployment
kubectl describe pod <pod-name>
```

---

# Future Enhancements

- Redis Cache (ElastiCache)
- Kubernetes Secrets
- Ingress Controller
- Route53
- HTTPS with ACM
- CI/CD using GitHub Actions
- Monitoring using Prometheus & Grafana
- Horizontal Pod Autoscaler

---

# Author

Padma

AWS | Docker | Kubernetes | EKS | Flask | RDS
