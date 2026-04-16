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
                if [ ! -d "$VENV" ]; then
                    python3 -m venv $VENV
                fi

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
                dvc pull || true
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

                echo "Starting MLflow..."

                nohup mlflow ui \
                --host 0.0.0.0 \
                --port $MLFLOW_PORT \
                --backend-store-uri file:./mlruns \
                > mlflow.log 2>&1 &

                sleep 5
                echo "===== MLFLOW LOG ====="
                cat mlflow.log || true
                '''
            }
        }

        stage('Run API DEBUG') {
            steps {
                sh '''
                set -x   # show every command

                . $VENV/bin/activate
                export PYTHONPATH=$PWD

                echo "Current directory:"
                pwd
                ls -R

                echo "Starting API..."

                python3 src/api/app.py
                '''
            }
        }

        stage('Verify API') {
            steps {
                sh '''
                echo "Testing API..."

                curl http://localhost:5000 || true
                '''
            }
        }
    }
}