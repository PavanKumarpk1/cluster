pipeline {
    agent any
    
    environment {
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gcp-service-account-key'
        
        HOME               = '/tmp'
        // This maps the Jenkins build number to the variable the compose file expects
        BUILD_TAG          = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                git url: 'https://github.com/PavanKumarpk1/prj1.git', branch: 'main'
            }
        }

        stage('Build & Push with Docker Compose') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, 
                                                 passwordVariable: 'DOCKER_PASS', 
                                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                        
                        dir('Docker') {
                            echo "Building all images with the correct tags..."
                            // This reads the image: definitions we added to the compose file
                            sh "docker-compose build"
                            
                            echo "Pushing all built images to Docker Hub..."
                            sh "docker compose push"
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
