stage('Deploy to GKE Cluster') {
    steps {
        // Binds the GCP Service Account Key JSON file path directly to GKE_KEY
        withCredentials([file(credentialsId: env.GCP_KEY_CREDS_ID, variable: 'GKE_KEY')]) {
            withEnv([
                'KUBERNETES_SERVICE_HOST=', 
                'KUBERNETES_SERVICE_PORT='
            ]) {
                script {
                    echo "Authenticating with GKE Cluster using GKE_KEY..."
                    
                    // Use the exact GKE_KEY variable here
                    sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                    sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                    
                    echo "Applying manifests..."
                    sh "kubectl apply -f k8s-deploy.yaml"
                    
                    echo "Patching deployments..."
                    sh "kubectl set image deployment/store-api-1 api-1=\${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-api-2 api-2=\${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-api-3 api-3=\${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                    sh "kubectl set image deployment/store-ui ui=\${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                }
            }
        }
    }
}
