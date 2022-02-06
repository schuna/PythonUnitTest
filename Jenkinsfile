pipeline {
    agent {label 'gce'}
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'pytest --cov=src tests/'
            }
            post {
                always {
                    junit 'test-reports/reports.xml'
                }
            }
        }
        stage('Archive') {
            steps {
                sh 'python -m build'
            }
            post {
                success {
                    archiveArtifacts 'dist/**'
                }
            }
        }
    }
}