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
                withCredentials([sshUserPrivateKey(credentialsId: 'deb01-ssh',
                                                  keyFileVariable: 'SSH_KEY',
                                                  usernameVariable: 'SSH_USER')]) {
                    sh '''
                      ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$SSH_USER"@deb-01 "
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


