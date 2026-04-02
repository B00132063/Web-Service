pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                echo 'Using repo from GitHub'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t inventory-api .'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name inventory-container inventory-api'
                sh 'sleep 5'
            }
        }

        stage('Test API') {
            steps {
                sh 'curl http://host.docker.internal:8000/docs'
            }
        }

        stage('Zip Project') {
            steps {
                sh 'zip -r project.zip .'
            }
        }
    }

    post {
        always {
            sh 'docker stop inventory-container || true'
            sh 'docker rm inventory-container || true'
        }
    }
}
