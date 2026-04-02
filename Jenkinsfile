pipeline {
    agent any

    stages {

        stage('Clone Repo') {
            steps {
                echo 'Using existing repo'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install -r requirements.txt'
                sh 'pip3 install pytest'
            }
        }

        stage('Generate README') {
            steps {
                sh 'python3 scripts/generate_readme.py'
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

        stage('Run Tests') {
            steps {
                sh 'pytest tests/'
            }
        }

        stage('Zip Project') {
            steps {
                sh 'zip -r complete.zip .'
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