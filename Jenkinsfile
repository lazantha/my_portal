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
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    python manage.py test
                '''
            }
        }

        stage('Install Koyeb CLI') {
            steps {
                sh '''
                    curl -sL https://get.koyeb.com | bash
                    echo "PATH before update: $PATH"
                    export PATH=$PATH:$HOME/.koyeb/bin
                    echo "PATH after update: $PATH"
                    which koyeb || echo "koyeb binary not found"
                    ls -al $HOME/.koyeb/bin || echo "Directory $HOME/.koyeb/bin not found"
                '''
            }
        }

        stage('Verify Koyeb CLI Installation') {
            steps {
                sh '''
                    export PATH=$PATH:$HOME/.koyeb/bin
                    koyeb --version || echo "koyeb command not found"
                '''
            }
        }

        stage('Deploy to Koyeb') {
            steps {
                sh '''
                    . venv/bin/activate
                    export PATH=$PATH:$HOME/.koyeb/bin
                    koyeb service update your-service-name --branch main --api-key $KOYEB_API_KEY
                '''
            }
        }
    }

    post {
        always {
            sh '''
                . venv/bin/activate || true
                deactivate || true
                cleanWs()
            '''
        }
    }
}
