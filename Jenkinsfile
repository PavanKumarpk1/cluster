pipeline {
    agent any
    
    environment {
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
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

        stage('Build & Push Images') {
            steps {
                withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDS_ID, 
                                                 passwordVariable: 'DOCKER_PASS', 
                                                 usernameVariable: 'DOCKER_USER')]) {
                    script {
                        sh 'echo "${DOCKER_PASS}" | docker login -u "${DOCKER_USER}" --password-stdin'
                        
                        def services = ['api_1', 'api_2', 'api_3', 'frontend']
                        
                        services.each { name ->
                            def imageName = "${DOCKER_USER}/${name}:${env.BUILD_NUMBER}"
                            echo "=========================================="
                            echo "Building and Pushing Image: ${imageName}"
                            echo "=========================================="
                            
                            // FIX: Using absolute path targeting the capitalized 'Docker' directory
                            sh "docker build -t ${imageName} \${WORKSPACE}/Docker/${name}"
                            sh "docker push ${imageName}"
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
                            sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                            sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                            
                            // FIX: Absolute path targeting k8s-deploy.yaml
                            sh "kubectl apply -f \${WORKSPACE}/Docker/k8s-deploy.yaml"
                            
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
    
    post {
        always {
            sh 'docker logout || true'
        }
    }
}
