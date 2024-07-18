pipeline {
    agent any

    environment {
        KOYEB_API_KEY = '472oxtmihyhrcm79n3h9r5fwyc7fkhib37hvkg8dfsvmucxf7kylmuel9wb5wsqx'  // Directly use your Koyeb API key
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
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    source venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Deploy to Koyeb') {
            steps {
                sh '''
                    source venv/bin/activate
                    koyeb service update your-service-name --branch main --api-key $KOYEB_API_KEY
                '''
            }
        }
    }

    post {
        always {
            sh 'deactivate || true'
            cleanWs()
        }
    }
}
