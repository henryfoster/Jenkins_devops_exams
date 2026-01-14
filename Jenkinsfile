pipeline {
environment { // Declaration of environment variables
DOCKER_ID = "henryfoster" // replace this with your docker-id
DOCKER_IMAGE_MOVIE = "movie-service"
DOCKER_IMAGE_CAST = "cast-service"
DOCKER_TAG = "v.${BUILD_ID}.0" // we will tag our images with the current build in order to increment the value by 1 with each new build
}
agent any // Jenkins will be able to select all available agents
stages {
        stage('Docker Build'){ // docker build image stage
            steps {
                script {
                sh '''
                 docker rmi $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG || true
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG movie-service/
                sleep 6
                '''
                }
                script {
                sh '''
                 docker rmi $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG || true
                 docker build -t $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG cast-service/
                sleep 6
                '''
                }
            }
        
        }
        stage(' Docker run'){ // run container from our built image
            environment
            {
                DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE") // retrieve database URL from Jenkins secret
                DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
            }
                steps {
                    script {
                    sh '''
                    docker rm -f $DOCKER_IMAGE_MOVIE
                    docker run -d -p 80:8000 -e DATABASE_URL=$DATABASE_URL_MOVIE --name $DOCKER_IMAGE_MOVIE $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop asyncio
                    sleep 10
                    '''
                    }
                    script {
                    sh '''
                    docker rm -f $DOCKER_IMAGE_CAST
                    docker run -d -p 81:8000 -e DATABASE_URL=$DATABASE_URL_CAST --name $DOCKER_IMAGE_CAST $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop asyncio
                    sleep 10
                    '''
                    }
                }
            }

        stage('Test Acceptance'){ // we launch the curl command to validate that the container responds to the request
            steps {
                sh 'curl localhost:81'
                sh 'curl localhost:80'
            }
        }
        stage('Docker Push'){ //we pass the built image to our docker hub account
            environment
            {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS") // we retrieve docker password from secret text called docker_hub_pass saved on jenkins
            }

            steps {

                script {
                sh '''
                docker login -u $DOCKER_ID -p $DOCKER_PASS
                docker push $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG
                docker push $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG
                '''
                }
            }

        }

stage('Deployment in dev'){
        environment
        {
        KUBECONFIG = credentials("config") // we retrieve kubeconfig from secret file called config saved on jenkins
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE") // retrieve database URL from Jenkins secret
        DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
        CAST_SERVICE_HOST_URL = "http://cast-service/api/v1/casts/"
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                ls
                cat $KUBECONFIG > .kube/config
                cp charts/values.yaml values.yml
                cat values.yml
                sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                helm upgrade --install movie ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_MOVIE" \
                  --set env[1].name=CAST_SERVICE_HOST_URL --set env[1].value="$CAST_SERVICE_HOST_URL" \
                  --set ingress.hosts[0].paths[0].path=/api/v1/movies \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace dev
                helm upgrade --install cast ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_CAST" \
                  --set fullnameOverride=cast-service \
                  --set ingress.hosts[0].paths[0].path=/api/v1/casts \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace dev
                '''
                }
            }

        }
stage('Deploiement en staging'){
        environment
        {
        KUBECONFIG = credentials("config") // we retrieve kubeconfig from secret file called config saved on jenkins
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE") // retrieve database URL from Jenkins secret
        DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
        CAST_SERVICE_HOST_URL = "http://cast-service/api/v1/casts/"
        }
            steps {
                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                ls
                cat $KUBECONFIG > .kube/config
                cp charts/values.yaml values.yml
                cat values.yml
                sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                helm upgrade --install movie ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_MOVIE" \
                  --set env[1].name=CAST_SERVICE_HOST_URL --set env[1].value="$CAST_SERVICE_HOST_URL" \
                  --set ingress.hosts[0].paths[0].path=/api/v1/movies \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace staging
                helm upgrade --install cast ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_CAST" \
                  --set fullnameOverride=cast-service \
                  --set ingress.hosts[0].paths[0].path=/api/v1/casts \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace staging
                '''
                }
            }

        }
  stage('Deploiement en prod'){
        environment
        {
        KUBECONFIG = credentials("config") // we retrieve kubeconfig from secret file called config saved on jenkins
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE") // retrieve database URL from Jenkins secret
        DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
        CAST_SERVICE_HOST_URL = "http://cast-service/api/v1/casts/"
        }
            steps {
            // Create an Approval Button with a timeout of 15minutes.
            // this require a manuel validation in order to deploy on production environment
                    timeout(time: 15, unit: "MINUTES") {
                        input message: 'Do you want to deploy in production ?', ok: 'Yes'
                    }

                script {
                sh '''
                rm -Rf .kube
                mkdir .kube
                ls
                cat $KUBECONFIG > .kube/config
                cp charts/values.yaml values.yml
                cat values.yml
                sed -i "s+tag.*+tag: ${DOCKER_TAG}+g" values.yml
                helm upgrade --install movie ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_MOVIE \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_MOVIE" \
                  --set env[1].name=CAST_SERVICE_HOST_URL --set env[1].value="$CAST_SERVICE_HOST_URL" \
                  --set ingress.hosts[0].paths[0].path=/api/v1/movies \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace prod
                helm upgrade --install cast ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_CAST" \
                  --set fullnameOverride=cast-service \
                  --set ingress.hosts[0].paths[0].path=/api/v1/casts \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace prod
                '''
                }
            }

        }

}
post { // send email when the job has failed
    // ..
    failure {
        echo "This will run if the job failed"
        mail to: "pikatchugengar@gmail.com",
             subject: "${env.JOB_NAME} - Build # ${env.BUILD_ID} has failed",
             body: "For more info on the pipeline failure, check out the console output at ${env.BUILD_URL}"
    }
    success {
        echo "This will run if the job succeeded"
        mail to: "pikatchugengar@gmail.com",
             subject: "${env.JOB_NAME} - Build # ${env.BUILD_ID} has succeeded",
             body: "For more info on the pipeline success, check out the console output at ${env.BUILD_URL}"
    }
    // ..
}
}
