pipeline {
    agent any
    
    environment {
        DOCKER_USER = 'paavan24' 
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
        script {
            // Using shell commands instead of the 'docker' property
            sh "echo ${DOCKER_PASSWORD} | docker login -u ${DOCKER_USER} --password-stdin"
            
            echo 'Building API 1...'
            sh "docker build -t ${DOCKER_USER}/api_1:${env.BUILD_NUMBER} ./api_1"
            sh "docker push ${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"

            echo 'Building API 2...'
            sh "docker build -t ${DOCKER_USER}/api_2:${env.BUILD_NUMBER} ./api_2"
            sh "docker push ${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"

            echo 'Building API 3...'
            sh "docker build -t ${DOCKER_USER}/api_3:${env.BUILD_NUMBER} ./api_3"
            sh "docker push ${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"

            echo 'Building UI...'
            sh "docker build -t ${DOCKER_USER}/frontend:${env.BUILD_NUMBER} ./frontend"
            sh "docker push ${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
            
            // Add your other APIs here...
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
