pipeline {
    agent any
    
    environment {
        // GCP Configurations
        GCP_PROJECT_ID     = 'project-0a90b5af-55e0-4752-866'
        GKE_CLUSTER_NAME   = 'production-gke-cluster'
        GKE_ZONE           = 'us-east1-b'
        
        // Credentials IDs
        DOCKER_CREDS_ID    = 'docker-hub-pass' 
        GCP_KEY_CREDS_ID   = 'gke-deploy-key'
        
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
                        
                        def fullImage = "${env.DOCKER_USER}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}"
                        
                        echo "=========================================="
                        echo "BUILDING & PUSHING: ${fullImage}"
                        echo "=========================================="
                        
                        sh "docker build -t ${fullImage} ."
                        sh "docker push ${fullImage}"
                    }
                }
            }
        }

        stage('Deploy to GKE Cluster') {
            steps {
                // Re-bind the docker credentials here so DOCKER_USER is safely available for the deployment command
                withCredentials([
                    usernamePassword(credentialsId: env.DOCKER_CREDS_ID, passwordVariable: 'DOCKER_PASS', usernameVariable: 'DOCKER_USER'),
                    file(credentialsId: env.GCP_KEY_CREDS_ID, variable: 'GKE_KEY')
                ]) {
                    withEnv([
                        'KUBERNETES_SERVICE_HOST=', 
                        'KUBERNETES_SERVICE_PORT='
                    ]) {
                        script {
                            sh "gcloud auth activate-service-account --key-file=\$GKE_KEY --project=${env.GCP_PROJECT_ID}"
                            sh "gcloud container clusters get-credentials ${env.GKE_CLUSTER_NAME} --zone ${env.GKE_ZONE} --project=${env.GCP_PROJECT_ID}"
                            
                            sh "kubectl apply -f deployment.yaml"
                            
                            echo "=========================================="
                            echo "UPDATING KUBERNETES DEPLOYMENT IMAGE..."
                            echo "=========================================="
                            
                            // Using standard shell variables instead of Groovy string interpolation to avoid scope cracks
                            sh """
                                container_name=\$(kubectl get deployment my-web-app -o jsonpath='{.spec.template.spec.containers[0].name}')
                                kubectl set image deployment/my-web-app \${container_name}=\${DOCKER_USER}/${env.IMAGE_NAME}:${env.BUILD_NUMBER}
                            """
                            
                            echo "Verifying rollout status..."
                            sh "kubectl rollout status deployment/my-web-app"
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
