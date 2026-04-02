pipeline {
    agent any

    environment {
        VENV = "venv"
        MLFLOW_PORT = "5001"
    }

    stages {

        stage('Clone Repo') {
            steps {
                git 'https://github.com/Vinay-Manjunath/Learning_Path_Recommender.git'
            }
        }

        stage('Setup Python') {
            steps {
                sh '''
                python3 -m venv $VENV
                . $VENV/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                '''
            }
        }

        stage('Pull DVC Data') {
            steps {
                sh '''
                . $VENV/bin/activate
                dvc pull
                '''
            }
        }

        stage('Run Pipeline (DVC + MLflow)') {
            steps {
                sh '''
                . $VENV/bin/activate

                # Run MLflow tracking server in background
                nohup mlflow ui --host 0.0.0.0 --port $MLFLOW_PORT > mlflow.log 2>&1 &

                # Run pipeline
                dvc repro
                '''
            }
        }

        stage('Run API (Optional)') {
            steps {
                sh '''
                . $VENV/bin/activate
                nohup python3 -m src.api.app > api.log 2>&1 &
                '''
            }
        }
    }
}