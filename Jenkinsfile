pipeline {
    agent any
    
    environment {
        // GCP Project and Cluster Configurations
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        // Credentials IDs configured in your Jenkins Global Dashboard
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gcp-service-account-key' // Jenkins Secret File ID
        
        // Forces commands to write tracking configurations to a writable path
        HOME               = '/tmp'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                // Pull down your application source tree
                git url: 'https://github.com/PavanKumarpk1/prj1.git', branch: 'main'
            }
        }

        stage('Build & Push Images') {
            steps {
                // Safely extract Docker credentials out of memory
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, 
                                                 passwordVariable: 'DOCKER_PASS', 
                                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        // Securely pass the docker password via standard input pipeline
                        sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                        
                        // Map each of your service directories from the architecture blueprint
                        def services = ['api_1', 'api_2', 'api_3', 'frontend']
                        
                        services.each { name ->
                            def imageName = "${DOCKER_USER}/${name}:${env.BUILD_NUMBER}"
                            echo "=========================================="
                            echo "Building and Pushing Image: ${imageName}"
                            echo "=========================================="
                            
                            sh "docker build -t ${imageName} ./${name}"
                            sh "docker push ${imageName}"
                        }
                    }
                }
            }
        }

        stage('Deploy to GKE Cluster') {
            steps {
                // Bind the GCP Service Account Key file directly to your variable: GKE_KEY
                withCredentials([file(credentialsId: env.GCP_KEY_CREDS_ID, variable: 'GKE_KEY')]) {
                    // Break out of internal Jenkins cluster proxy traps so kubectl looks out to GCP
                    withEnv([
                        'KUBERNETES_SERVICE_HOST=', 
                        'KUBERNETES_SERVICE_PORT='
                    ]) {
                        script {
                            echo "=========================================="
                            echo "STEP 4: Authenticating Jenkins with GKE"
                            echo "=========================================="
                            
                            // Escape $GKE_KEY so the shell evaluates the path on the host node
                            sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                            sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                            
                            echo "=========================================="
                            echo "STEP 5: Deploying App to Kubernetes (GKE)"
                            echo "=========================================="
                            
                            // Apply base structure configs
                            sh "kubectl apply -f k8s-deploy.yaml"
                            
                            // Patch pods dynamically to ensure the new tags spark a rolling update
                            sh "kubectl set image deployment/store-api-1 api-1=\${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-api-2 api-2=\${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-api-3 api-3=\${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-ui ui=\${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                            
                            echo "=========================================="
                            echo "STEP 6: Verifying Deployment Status"
                            echo "=========================================="
                            sh "kubectl rollout status deployment/store-ui"
                            sh "kubectl get service"
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Drop system authentication cookies from the runner host node
            sh 'docker logout || true'
        }
    }
}
