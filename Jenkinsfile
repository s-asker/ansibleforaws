pipeline {
    agent any

    environment {
        PLAYBOOK_DIR = '/var/lib/jenkins/shared_workspace/CICD'
    }

    stages {
        stage('CI/CD Playbook Execution') {
            steps {
                script {
                    def COLOR_MAP = [
                        'SUCCESS': 'good',
                        'FAILURE': 'danger',
                    ]

                    withCredentials([aws(credentialsId: "aws_credentials_id")]) {
                        ansiblePlaybook(
                            playbook: "${PLAYBOOK_DIR}/update-servers.yml",
                            become: true,
                            becomeUser: 'root'
                        )
                    }
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
