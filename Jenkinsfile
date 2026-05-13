pipeline {
    agent any
    
    environment {
        DOCKER_USER = 'paavan24' 
        DOCKER_PASSWORD = credentials('docker-hub-pass')
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Build & Push') {
    steps {
        // Use this specific block to handle the password safely
        withCredentials([usernamePassword(credentialsId: 'docker-hub-pass', 
                                          passwordVariable: 'DOCKER_PASSWORD', 
                                          usernameVariable: 'DOCKER_USER_VAR')]) {
            script {
                // Use single quotes ('') for the shell command to prevent Groovy interpolation
                sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USER_VAR}" --password-stdin'
                
                def services = ['api_1', 'api_2', 'api_3']
                services.each { name ->
                    sh "docker build -t ${DOCKER_USER}/${name}:${env.BUILD_NUMBER} ./${name}"
                    sh "docker push ${DOCKER_USER}/${name}:${env.BUILD_NUMBER}"
                }
                
                sh "docker build -t ${DOCKER_USER}/frontend:${env.BUILD_NUMBER} ./frontend"
                sh "docker push ${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
            }
        }
    }
}

        stage('Deploy to GKE') {
            steps {
                script {
                    // This updates the cluster to use the new images
                    sh "kubectl set image deployment/store-api-1 api-1=${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-api-2 api-2=${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-api-3 api-3=${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-ui ui=${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
