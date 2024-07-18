pipeline {
    agent any

    environment {
        KOYEB_API_KEY = credentials('koyeb-api-key')
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/lazantha/my_portal.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                    #!/bin/bash
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    #!/bin/bash
                    source venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Deploy to Koyeb') {
            steps {
                sh '''
                    #!/bin/bash
                    source venv/bin/activate
                    koyeb service update your-service-name --branch main --api-key $KOYEB_API_KEY
                    nohup python3 manage.py runserver 0.0.0.0:8000 &
                '''
            }
        }
    }

    post {
        always {
            sh '''
                #!/bin/bash
                deactivate || true
                cleanWs()
            '''
        }
    }
}
