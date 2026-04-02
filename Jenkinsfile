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

        // stage('Find DVC Repo Path') {
        //     steps {
        //         script {
        //             env.DVC_DIR = sh(
        //                 script: "find . -name dvc.yaml -exec dirname {} \\; | head -n 1",
        //                 returnStdout: true
        //             ).trim()
        //         }
        //         echo "DVC Directory found at: ${env.DVC_DIR}"
        //     }
        // }

        stage('Run DVC Pipeline') {
            steps {
                sh '''
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt
                cd Learning_Path_Recommender
                dvc repro
                '''
            }
        }

        stage('Run MLflow UI (Optional)') {
            steps {
                sh '''
                . $VENV/bin/activate
                nohup mlflow ui --host 0.0.0.0 --port $MLFLOW_PORT > mlflow.log 2>&1 &
                '''
            }
        }

        stage('Run API (Optional)') {
            steps {
                sh '''
                cd $DVC_DIR
                . ../$VENV/bin/activate
                nohup python3 -m src.api.app > api.log 2>&1 &
                '''
            }
        }
    }
}