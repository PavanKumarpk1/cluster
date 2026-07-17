pipeline {
    agent any
    
    environment {
        // GCP Configurations
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        // Credentials IDs
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gke-deploy-key'  // 1st FIX: Updated to your exact credential ID
        
        HOME               = '/tmp'
        IMAGE_NAME         = 'my-test-app'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                git url: 'https://github.com/PavanKumarpk1/prj1.git', branch: 'main'
            }
        }

        stage('Build & Push Image') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, 
                                                 passwordVariable: 'DOCKER_PASS', 
                                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                        
                        def fullImage = "${DOCKER_USER}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                        
                        // 2nd FIX: Added verbose logging to clearly track the push process
                        echo "=========================================="
                        echo "TARGET IMAGE URL: https://hub.docker.com/r/${DOCKER_USER}/${env.IMAGE_NAME}"
                        echo "BUILDING: ${fullImage}"
                        echo "=========================================="
                        
                        sh "docker build -t ${fullImage} ."
                        
                        echo "=========================================="
                        echo "PUSHING TO DOCKER HUB..."
                        echo "=========================================="
                        sh "docker push ${fullImage}"
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
                            sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                            sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                            
                            sh "kubectl apply -f deployment.yaml"
                            
                            // Note: verify that the deployment container configuration names match inside deployment.yaml
                            sh "kubectl set image deployment/my-web-deployment web-container=\${DOCKER_USER}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
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
