pipeline {
    agent any
    
    environment {
        // GCP Configurations
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        // Credentials IDs
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gcp-service-account-key'
        
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
                        
                        // Define the full image tag using the current workspace context
                        def fullImage = "${DOCKER_USER}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                        echo "Building and Pushing Single App Image: ${fullImage}"
                        
                        // We build from the current root directory '.' because the Dockerfile is right here!
                        sh "docker build -t ${fullImage} ."
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
                            
                            // Appends deployment.yaml located right at the root
                            sh "kubectl apply -f deployment.yaml"
                            
                            // Dynamically updates the image to the new tag we just pushed
                            // Note: verify that the deployment name inside deployment.yaml matches 'my-web-deployment'
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
