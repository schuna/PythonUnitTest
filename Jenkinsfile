pipeline {
    agent {label 'gce'}
    stages {
        stage('Test') {
            steps {
                sh 'pip install -r requirements.txt'
                sh 'python -m pytest --cov=src tests/'
            }
            post {
                always {
                    junit 'test-reports/report.xml'
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
