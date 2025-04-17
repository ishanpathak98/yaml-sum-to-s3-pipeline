pipeline {
    agent any

    parameters {
        choice(name: 'ENVIRONMENT', choices: ['dev', 'test', 'prod'], description: 'Select the environment')
        string(name: 'BUCKET_NAME', defaultValue: 'my-yaml-sum-bucket', description: 'Enter the target S3 bucket name')
    }

    environment {
        AWS_DEFAULT_REGION = 'us-east-2' // Change to 'us-east-2' for Ohio region
    }

    stages {
        stage('Checkout SCM') {
            steps {
                git credentialsId: 'github-pat', url: 'https://github.com/ishanpathak98/yaml-sum-to-s3-pipeline.git', branch: 'main'
            }
        }

        stage('Prepare Environment') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Verify Files') {
            steps {
                echo "📁 Verifying YAML and Python files"
                sh 'ls -la'
            }
        }

        stage('Run Python Script') {
            steps {
                withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']]) {
                    sh '''
                        . venv/bin/activate
                        python3 sum_env_values.py ${ENVIRONMENT} ${BUCKET_NAME}
                    '''
                }
            }
        }

        stage('Verify S3 Upload') {
            steps {
                echo "✅ Upload complete. Check your S3 bucket: ${params.BUCKET_NAME}"
            }
        }
    }

    post {
        success {
            echo "✅ Build completed successfully for '${params.ENVIRONMENT}'"
        }
        failure {
            echo "❌ Build failed for '${params.ENVIRONMENT}'. Please check logs."
        }
    }
}
