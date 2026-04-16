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

        stage('Setup Python (reuse venv)') {
            steps {
                sh '''
                if [ ! -d "$VENV" ]; then
                    python3 -m venv $VENV
                    . $VENV/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                else
                    echo "Using existing venv"
                fi
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

        stage('Run DVC Pipeline') {
            steps {
                sh '''
                . $VENV/bin/activate
                dvc repro
                '''
            }
        }

        stage('Run MLflow UI') {
            steps {
                sh '''
                . $VENV/bin/activate
                nohup mlflow ui --host 0.0.0.0 --port $MLFLOW_PORT > mlflow.log 2>&1 &
                '''
            }
        }

        stage('Run API') {
            steps {
                sh '''
                . $VENV/bin/activate
                nohup python3 -m src.api.app > api.log 2>&1 &
                '''
            }
        }
    }
}