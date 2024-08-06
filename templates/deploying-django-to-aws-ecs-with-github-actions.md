---
title: Deploying Django Application to AWS ECS Using Github Actions
date: 2024-08-07
tags:
  - python
  - ci/cd
  - aws
  - ecs
---

In this blog I will explain how to deploy a django application using github actions to AWS ECS(container service). Using github actions for your CI/CD pipeline is better than aws’s CI/CD services as it is simpler and very straight forward in my opinion.

### Prerequisites

This blog assumes that you already know Django, AWS. So this blog goes right ahead setting up the services. Although a basic definition will be mentioned before going ahead.

### Why CI/CD pipeline

CI/CD pipeline is a crucial tool in agile development. It’s benefits are:

* Avoids manual deployment and building.
* Without it, you might have to wait for a long time before all the changes are merged to the branch. This leads to slow testing and delayed feedback thus increasing the development cycle.

You can find plenty of CI/CD tools in the market, but 

* Github Actions are simpler and configuring it is very developer friendly. 
* Everything will be at one place, so you don’t have to go between different tools for your code and checking the deployments. 
* It allows us to add checks so that PRs are merged only if all the deploy steps are successful.

### Workflow

![Workflow](/static/images/workflow.png "Workflow")

Before we begin, let’s explain what Github Workflow and AWS ECR are ?

### Github Actions

Github workflow is a set of jobs that gets triggered when an event occurs in your repository. Each job can run sequentially or parallely. Each job is made up of a list of steps. Each step executes an action inside a virtual runner provisioned for the job(github provides or you can also provide this).

Github already provides a list of reusable actions which takes care of most of our needs but if you have a specific scenario which is not covered by any github actions, you can also create one.

### AWS ECS

ECS is a container orchestration service offered by AWS along with EKS, Fargate. ECS is made up of a couple of components. Let's define them before implementing them.

* Cluster: A logical grouping of services and tasks. In case you manage the cluster using EC2(not fargate), it is a grouping of EC2 instances. An EC2 instance becomes part of the cluster by running an ec2-agent in each node. Cluster takes care allocating tasks to appropriate nodes/machines.
* Service: A service manages the group tasks. It takes care of scheduling or maintained of the tasks based on the service configuration(such as maintaining desired number of replicas) Also takes care of scaling the tasks based on metrics. If you are from k8s, this is basically a deployment manifest.
* Task definition: A template for task. If you are from k8s, this is basically a pod manifest.
* Task: A task is a running container based on the configuration provided in the task definition. If you are from k8s, it is the pod.


### Building CI/CD

Any django application works but for this blog we will be using this simple django application which exposes an endpoint which prints current olympic medals. It also has one test case which tests the endpoint. [Code Link](https://github.com/bhimsen92/django-github-actions)

First we will set up a simple workflow which checks out the code, installs the dependencies, tests, adds coverage and annotates the PR or code. We also run on every pull request and block the merge if any test fails.

Go ahead and create a .github/workflows directory inside your repository. This is required by the github. Under workflows directory, create “deploy.yaml” file.


```yaml
name: Deploy to Amazon ECS

on:
  pull_request:
    branches:
      - main

jobs:
  build:
    name: Build & Test
    runs-on: ubuntu-latest
    permissions:
      pull-requests: write
      contents: read
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python 3.12
        uses: actions/setup-python@v2
        with:
          python-version: 3.12
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
          pip install -r requirements.txt
      - name: Test and Coverage
        run: |
          pytest --cache-clear --cov=olympics tests/ > pytest-coverage.txt
      - name: Comment coverage
        uses: MishaKav/pytest-coverage-comment@main
        with:
          pytest-coverage-path: ./pytest-coverage.txt
```

The above workflow should take care of testing the django application. 

### Deploying to AWS

We will deploy the application on ECS(using EC2). We won't be using fargate as there is no free tier available for it. But nothing changes if one chooses to use a fargate. It is just a provisioner. Everything remains the same.

Before we proceed, we need to set up a few things. Head to aws and create the following resources.

* Create an ECR repository. Make a note of the name. This will act as our container registry.
* Create an IAM user which only has image push and task update/execute permissions.
* Store the access key and secret inside github secrets that you created in the previous step.
* Create an ECS cluster. 
* Create a Service and Task definition. Make note of their names(cluster, service, task definition)
* From the task definition panel, take a copy of it’s definition in json form and copy it your repository. Keep it inside “.aws/task-definition.json”.


Ideally this should be behind an application load balancer. But since it costs money, we will make use of “host” networking so that the port is exposed on the host itself. If you can afford a load balancer, keep the tasks in the “bride/awsvpc” networking mode. Create a load balancer and add the service in its target group.

Let’s update the github workflow to include the deployment steps.


```yaml
env:
  AWS_REGION: ap-south-1
  ECR_REPOSITORY: django-ec2
  ECS_SERVICE: django-ec2-service
  ECS_TASK_DEFINITION: .aws/django-task-definition.json
  ECS_CLUSTER: django-ec2-cluster
  CONTAINER_NAME: django-ec2

jobs:
  deploy:
    needs: build
    name: Deploy to AWS ECS
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ env.AWS_REGION }}

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v2

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          IMAGE_TAG: ${{ github.sha }}
        run: |
          # Build a docker container and
          # push it to ECR so that it can
          # be deployed to ECS.
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "image=$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG" >> $GITHUB_OUTPUT

      - name: Fill in the new image ID in the Amazon ECS task definition
        id: task-def
        uses: aws-actions/amazon-ecs-render-task-definition@v1
        with:
          task-definition: ${{ env.ECS_TASK_DEFINITION }}
          container-name: ${{ env.CONTAINER_NAME }}
          image: ${{ steps.build-image.outputs.image }}

      - name: Deploy Amazon ECS task definition
        uses: aws-actions/amazon-ecs-deploy-task-definition@v1
        with:
          task-definition: ${{ steps.task-def.outputs.task-definition }}
          service: ${{ env.ECS_SERVICE }}
          cluster: ${{ env.ECS_CLUSTER }}
          wait-for-service-stability: true
```

Now create a PR request making a change. This should trigger the github actions and deploy your changes to the ECS. 

*Note:*
*To delete the service and ec2 instances, just set the desired capacity of both service and auto scaling group to 0. This should take care of deleting the task and ec2 instances from aws.*
