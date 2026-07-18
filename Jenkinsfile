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
                withCredentials([usernamePassword(credentialsId: 'docker-hub-pass', 
                                                 passwordVariable: 'DOCKER_PASSWORD', 
                                                 usernameVariable: 'DOCKER_USER_VAR')]) {
                    script {
                        sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USER_VAR}" --password-stdin'
                        
                        def services = ['api_1', 'api_2', 'api_3']
                        services.each { name ->
                            sh "docker build -t ${DOCKER_USER}/${name}:${env.BUILD_NUMBER} ./${name}"
                            sh "docker push ${DOCKER_USER}/${name}:${env.BUILD_NUMBER}"
                        }
         
                        // MODIFIED: Changed :latest to use build numbers so Kubernetes always knows a new version exists
                        sh "docker build -t ${DOCKER_USER}/products:${env.BUILD_NUMBER} ./products"
                        sh "docker push ${DOCKER_USER}/products:${env.BUILD_NUMBER}"
                        
                        sh "docker build -t ${DOCKER_USER}/frontend:${env.BUILD_NUMBER} ./frontend"
                        sh "docker push ${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                    }
                }
            }
        }
 
        stage('Deploy to GKE') {
            steps {
                withCredentials([file(credentialsId: 'gke-deploy-key', variable: 'GKE_KEY')]) {
                    withEnv([
                        'KUBERNETES_SERVICE_HOST=', 
                        'KUBERNETES_SERVICE_PORT='
                    ]) {
                        script {
                            echo "Authenticating with Google Cloud Platform..."
                            sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=project-0a90b5af-55e0-4752-866"
                            
                            echo "Fetching GKE cluster credentials..."
                            sh "gcloud container clusters get-credentials production-gke-cluster --zone us-east1-b --project=project-0a90b5af-55e0-4752-866"
                            
                            echo "Applying Kubernetes Manifests..."
                            sh "kubectl apply -f k8s-deploy.yaml"
                            
                            echo "Applying Ingress Routing Manifest..."
                            sh "kubectl apply -f ingress.yaml"
                 
                            echo "Updating deployment container images..."
                            sh "kubectl set image deployment/store-api-1 api-1=${DOCKER_USER}/api_1:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-api-2 api-2=${DOCKER_USER}/api_2:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-api-3 api-3=${DOCKER_USER}/api_3:${env.BUILD_NUMBER}"
                            sh "kubectl set image deployment/store-ui ui=${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                            
                            echo "Deployment successful! Check 'kubectl get ingress app-ingress' for your single LoadBalancer IP."
                        }
                    }
                }
            }
        }
    }
}
