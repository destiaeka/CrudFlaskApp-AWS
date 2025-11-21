# Flask CRUD Deployment on AWS (S3, RDS, ECR, EKS, Helm)

## About
This project deploys a Flask CRUD application using AWS cloud-native services. It uses **AWS S3** for file storage, **AWS RDS** for the database, **AWS ECR** for container images, and **Amazon EKS** for Kubernetes orchestration. Deployment is automated using **Helm** and **GitHub Actions CI/CD**.

## Architecture
- **Flask API** (CRUD)
- **AWS S3** – Media/Object storage  
- **AWS RDS** – MySQL/PostgreSQL database  
- **AWS ECR** – Container registry  
- **Amazon EKS** – Kubernetes cluster  
- **Helm** – Deployment management  
- **GitHub Actions** – CI/CD pipeline  

## Features
- CRUD API using Flask  
- Cloud storage via S3  
- Managed relational database (RDS)  
- Dockerized app pushed to ECR  
- Helm chart for Kubernetes deployment  
- Autoscaling via HPA

## How to Deploy
1. Build & push image to ECR (automated via GitHub Actions)  
2. Apply Helm chart:
   ```
   helm install crudapp ./helm
   ```
3. Show Running POD
   ```
   ~ $ kubectl get all
    NAME                                   READY   STATUS    RESTARTS      AGE
    pod/crudapp-crudapp-6f6d5885b8-5rj7w   1/1     Running   1 (57m ago)   97m
    pod/crudapp-crudapp-6f6d5885b8-cw96q   1/1     Running   1 (57m ago)   97m
    pod/crudapp-crudapp-6f6d5885b8-v2cb6   1/1     Running   0             97m
    
    NAME                      TYPE           CLUSTER-IP      EXTERNAL-IP                                                              PORT(S)          AGE
    service/crudapp-crudapp   LoadBalancer   10.100.135.35   ab00e39714c6740109c870969b7ffe8f-567022461.us-east-1.elb.amazonaws.com   5000:32650/TCP   92m
    service/kubernetes        ClusterIP      10.100.0.1      <none>                                                                   443/TCP          145m
    
    NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
    deployment.apps/crudapp-crudapp   3/3     3            3           97m
    
    NAME                                         DESIRED   CURRENT   READY   AGE
    replicaset.apps/crudapp-crudapp-6f6d5885b8   3         3         3       97m
    
    NAME                                                  REFERENCE                    TARGETS           MINPODS   MAXPODS   REPLICAS   AGE
    horizontalpodautoscaler.autoscaling/crudapp-crudapp   Deployment/crudapp-crudapp   memory: 42%/50%   3         10        3          97m
   ```

## CI/CD
Push to main → Build Docker → Push to ECR → Deploy to EKS automatically.

## Tech Stack
Flask • Docker • Kubernetes • AWS S3 • AWS RDS • AWS ECR • EKS • Helm • GitHub Actions
