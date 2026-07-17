pipeline {
    agent any
    
    environment {
        // GCP Configurations
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        // Jenkins Credentials IDs
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gcp-service-account-key'
        
        HOME               = '/tmp'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                git url: 'https://github.com/PavanKumarpk1/prj1.git', branch: 'main'
            }
        }

        stage('Build with Docker Compose & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, 
                                                 passwordVariable: 'DOCKER_PASS', 
                                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                        
                        // Move into the Docker folder where docker-compose.yml lives
                        dir('Docker') {
                            echo "Building all services using Docker Compose..."
                            sh "docker compose build"
                            
                            echo "Tagging and Pushing services to Docker Hub..."
                            // Because docker compose builds them locally, we tag them with the build number and push
                            sh "docker tag docker-api_1:latest \${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                            sh "docker tag docker-api_2:latest \${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                            sh "docker tag docker-api_3:latest \${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                            sh "docker tag docker-ui:latest    \${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                            
                            sh "docker push \${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                            sh "docker push \${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                            sh "docker push \${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                            sh "docker push \${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                        }
                    }
                }
            }
        }

        stage('Deploy to GKE Cluster') {
            steps {
                withCredentials([file(credentialsId: env.GCP_KEY_CREDS_ID, variable: 'GKE_KEY')]) {
                    withEnv([
                        'KUBERNETES_SERVICE_HOST=', 
                        'KUBERNETES_SERVICE_PORT='
                    ]) {
                        script {
                            dir('Docker') {
                                sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                                sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                                
                                sh "kubectl apply -f k8s-deploy.yaml"
                                
                                sh "kubectl set image deployment/store-api-1 api-1=\${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                                sh "kubectl set image deployment/store-api-2 api-2=\${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                                sh "kubectl set image deployment/store-api-3 api-3=\${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                                sh "kubectl set image deployment/store-ui ui=\${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                            }
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh 'docker logout || true'
        }
    }
}
