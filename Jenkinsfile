stage('Build & Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-hub-pass', 
                                                 passwordVariable: 'DOCKER_PASSWORD', 
                                                 usernameVariable: 'DOCKER_USER_VAR')]) {
                    script {
                        // =========================================================
                        // 🔍 DIAGNOSTIC LOGS: Let's see the filesystem layout
                        // =========================================================
                        echo "--- [DEBUG] Checking root workspace contents ---"
                        sh "ls -la"

                        echo "--- [DEBUG] Checking inside the Docker folder ---"
                        sh "ls -la Docker || echo 'Docker folder does not exist at this exact name/case!'"
                        
                        echo "--- [DEBUG] Searching the workspace for api_1 ---"
                        sh "find . -type d -name 'api_1' || echo 'Could not find api_1 anywhere'"
                        // =========================================================

                        sh 'echo "${DOCKER_PASSWORD}" | docker login -u "${DOCKER_USER_VAR}" --password-stdin'
                        
                        dir('Docker') {
                            def services = ['api_1', 'api_2', 'api_3']
                            services.each { name ->
                                sh "docker build -t ${DOCKER_USER}/${name}:${env.BUILD_NUMBER} ./${name}"
                                sh "docker push ${DOCKER_USER}/${name}:${env.BUILD_NUMBER}"
                            }
             
                            sh "docker build -t ${DOCKER_USER}/products:latest ./products"
                            sh "docker push ${DOCKER_USER}/products:latest"
                            
                            sh "docker build -t ${DOCKER_USER}/frontend:${env.BUILD_NUMBER} ./frontend"
                            sh "docker push ${DOCKER_USER}/frontend:${env.BUILD_NUMBER}"
                        }
                    }
                }
            }
        }
