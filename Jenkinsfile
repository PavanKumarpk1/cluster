pipeline {
    agent any
    stages {
        stage('Checkout Code') {
            steps {
                cleanWs()
                git url: 'https://github.com/PavanKumarpk1/prj1.git', branch: 'main'
            }
        }
        stage('Debug Paths') {
            steps {
                script {
                    echo "--- 1. Jenkins absolute workspace path ---"
                    sh "pwd"
                    
                    echo "--- 2. Direct folder contents ---"
                    sh "ls -R"
                }
            }
        }
    }
}
