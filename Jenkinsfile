pipeline {
    agent any

    parameters {
        string(name: 'ENV_NAME', defaultValue: 'All', description: 'Enter environment (Merge, Prod, or All)')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/ishanpathak98/yaml-sum-to-s3-pipeline.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pip3 install boto3 pyyaml'
            }
        }

        stage('Run Python Script') {
            steps {
                sh "python3 sum_env_values.py ${params.ENV_NAME}"
            }
        }
    }

    post {
        success {
            echo '✅ Pipeline finished successfully.'
        }
        failure {
            echo '❌ Pipeline failed.'
        }
    }
}
