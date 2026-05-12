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
                    // Use the ID 'docker-hub-credentials' we are creating in Step 2
                    docker.withRegistry('https://index.docker.io/v1/', 'docker-hub-credentials') {
                        
                        echo 'Building & Pushing API 1...'
                        docker.build("${DOCKER_USER}/api_1:${env.BUILD_NUMBER}", "./api_1").push()

                        echo 'Building & Pushing API 2...'
                        docker.build("${DOCKER_USER}/api_2:${env.BUILD_NUMBER}", "./api_2").push()

                        echo 'Building & Pushing API 3...'
                        docker.build("${DOCKER_USER}/api_3:${env.BUILD_NUMBER}", "./api_3").push()

                        echo 'Building & Pushing UI...'
                        docker.build("${DOCKER_USER}/frontend:${env.BUILD_NUMBER}", "./frontend").push()
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
