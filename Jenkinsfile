pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Deploy to Deb-01') {
            steps {
                sshagent(credentials: ['deb01-ssh']) {
                    sh '''
                      ssh -o StrictHostKeyChecking=no ansible@deb-01 "
                        cd ~/fastapi-mysql-demo && \
                        git pull && \
                        docker compose up --build -d
                      "
                    '''
                }
            }
        }
    }
}

