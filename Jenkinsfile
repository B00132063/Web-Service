pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-container"
        ZIP_NAME = "complete-${new Date().format('yyyy-MM-dd-HH-mm-ss')}.zip"
    }

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Repository pulled from GitHub by Jenkins SCM settings'
            }
        }

        stage('Generate README') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root'
                }
            }
            steps {
                sh 'python scripts/generate_readme.py'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME'
                sh 'sleep 8'
            }
        }

        stage('Run Unit Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root:root'
                }
            }
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest tests/'
            }
        }

        stage('Create Zip File') {
            agent {
                docker {
                    image 'ubuntu:22.04'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    apt-get update
                    apt-get install -y zip
                    zip -r $ZIP_NAME . -x "venv/*" ".git/*" "__pycache__/*" "*.pyc"
                '''
            }
        }
    }

    post {
        always {
            sh 'docker stop $CONTAINER_NAME || true'
            sh 'docker rm $CONTAINER_NAME || true'
        }
    }
}