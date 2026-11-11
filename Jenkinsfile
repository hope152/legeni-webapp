pipeline {
    agent any

    parameters {
        string(name: 'DOCKERHUB_ID', defaultValue: 'touffa', description: 'Votre identifiant Docker Hub')
        booleanParam(name: 'PUSH', defaultValue: true, description: "Pousser l'image sur Docker Hub")
    }

    environment {
        IMAGE          = "${params.DOCKERHUB_ID}/legeni-webapp"
        VERSION        = "1.0.${env.BUILD_NUMBER}"
        TEST_CONTAINER = "webapp-ci-${env.BUILD_NUMBER}"
        CI_NETWORK     = "ci-net-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build image') {
            steps {
                sh 'docker build --build-arg APP_VERSION=$VERSION -t $IMAGE:$VERSION -t $IMAGE:latest .'
            }
        }

        stage("Test d'acceptance") {
            steps {
                sh '''
                    docker network create $CI_NETWORK
                    docker run -d --name $TEST_CONTAINER --network $CI_NETWORK -p 5000:5000 $IMAGE:$VERSION
                    sleep 5
                    docker run --rm --network $CI_NETWORK curlimages/curl:8.11.1 \
                        -sf --retry 10 --retry-connrefused --retry-delay 1 http://$TEST_CONTAINER:5000/health
                '''
            }
        }

        stage('Push Docker Hub') {
            when { expression { params.PUSH } }
            steps {
                sh '''
                    echo "dckr_pat_lSZ6mWjj5lIuN5kjwrrvFxDIC50I" | docker login -u "$DOCKERHUB_ID" --password-stdin
                    docker push $IMAGE:$VERSION
                    docker push $IMAGE:latest
                '''
            }
        }
    }

    post {
        always {
            sh 'docker rm -f $TEST_CONTAINER || true; docker network rm $CI_NETWORK || true'
        }
    }
}
