pipeline {
    agent any
    stages {
        stage("clone code") {
            steps {
                echo "cloning the code"
                git url:"https://github.com/RamTati29/flask-system-monitor.git", branch: "main"
            }
        }
        stage("build") {
            steps {
                echo "building code"
                sh "docker build -t flask-system-monitor ."
            }
        }
        stage("push to dockerhub") {
            steps {
                echo "pushing the image to dockerhub"
                withCredentials([usernamePassword(credentialsId:"dockerhub", passwordVariable:"dockerhubPass",usernameVariable:"dockerhubUser")]){
                sh "docker tag flask-system-monitor ${env.dockerhubUser}/flask-system-monitor:latest"
                sh "docker login -u ${env.dockerhubUser} -p ${env.dockerhubPass}"
                sh "docker push ${env.dockerhubUser}/flask-system-monitor:latest"
                }
            }
        }
        stage("deploy") {
            steps {
                echo "deploying to container"
                sh "docker-compose down && docker-compose up -d"
            }
        }
    }
}
