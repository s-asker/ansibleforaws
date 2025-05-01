def COLOR_MAP = [
    'SUCCESS': 'good',
    'FAILURE': 'danger',
]
pipeline {
    agent any
    environment {
        PLAYBOOK_DIR = '/var/lib/jenkins/shared_workspace/CICD'  // Change this if your deploy path is different
    }

   stages {
           stage('CI/CD Playbook Execution') {
                steps {
                    withCredentials([aws(credentialsId: "aws_credentials_id")]) {
                    ansiblePlaybook(
                    playbook: "${PLAYBOOK_DIR}/update-servers.yml",
                    become: true,
                    becomeUser: 'root' // Enables become/sudo
                    )
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
