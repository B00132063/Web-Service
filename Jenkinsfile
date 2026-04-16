pipeline {
    agent any

    environment {
        IMAGE_NAME = "inventory-api"
        CONTAINER_NAME = "inventory-container"
    }

    stages {
        stage('Checkout Code') {
            steps {
                // If Jenkins is configured with Pipeline from SCM,
                // this checks out the repository automatically
                checkout scm
            }
        }

        stage('Clean Old Container') {
            steps {
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                    docker run -d -p 8000:8000 --name $CONTAINER_NAME $IMAGE_NAME
                    sleep 10
                '''
            }
        }

        stage('Check API is Up') {
            steps {
                sh 'curl http://localhost:8000/docs'
            }
        }

        stage('Run Python Tests') {
            steps {
                sh 'pytest tests/test_api.py'
            }
        }

        stage('Generate README') {
            steps {
                sh 'python3 scripts/generate_readme.py > README.txt'
            }
        }

        stage('Create Zip File') {
            steps {
                sh '''
                    ZIP_NAME="complete-$(date +%Y-%m-%d-%H-%M-%S).zip"
                    zip -r $ZIP_NAME . -x "venv/*" "*.git*" "__pycache__/*"
                '''
            }
        }

        // Only use this stage if you have a Postman collection JSON file
        stage('Run Newman Tests') {
            when {
                expression { fileExists('postman_collection.json') }
            }
            steps {
                sh 'newman run postman_collection.json'
            }
        }
    }

    post {
        always {
            sh '''
                docker stop $CONTAINER_NAME || true
                docker rm $CONTAINER_NAME || true
            '''
        }
    }
}