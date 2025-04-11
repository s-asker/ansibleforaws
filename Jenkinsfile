pipeline {
    agent any

    environment {
        DEPLOY_DIR = '/var/www/html'  // Change this if your deploy path is different
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'website', url: 'https://github.com/s-asker/ansibleforaws.git'
            }
        }

        stage('Deploy') {
            steps {
                script {
                    echo "Deploying static website to ${DEPLOY_DIR}..."
                    sh """
                        rm -rf ${DEPLOY_DIR}/*
                        cp -r * ${DEPLOY_DIR}/
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Deployment successful!'
        }
        failure {
            echo 'Deployment failed!'
        }
    }
}
