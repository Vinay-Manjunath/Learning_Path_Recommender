pipeline {
    agent any

    stages {

        stage('Clone') {
            steps {
                git 'https://github.com/Vinay-Manjunath/Learning_Path_Recommender.git'
            }
        }

        stage('Install') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('DVC Pipeline') {
            steps {
                sh 'dvc repro'
            }
        }

        stage('Train + MLflow') {
            steps {
                sh 'python src/features/build_embeddings.py'
            }
        }

        stage('Deploy API') {
            steps {
                sh 'nohup python src/api/app.py &'
            }
        }
    }
}