pipeline {
environment { 
DOCKER_ID = "henryfoster" 
DOCKER_IMAGE_MOVIE = "movie-service"
DOCKER_IMAGE_CAST = "cast-service"
DOCKER_TAG = "v.${BUILD_ID}.0" 
}
agent any 
stages {
        stage('Docker Build'){ 
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
        stage(' Docker run'){ 
            environment
            {
                DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE")  
                DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
            }
                steps {
                    script {
                    sh '''
                    docker rm -f $DOCKER_IMAGE_MOVIE
                    docker run -d -p 8001:8000 -e DATABASE_URI=$DATABASE_URL_MOVIE --name $DOCKER_IMAGE_MOVIE $DOCKER_ID/$DOCKER_IMAGE_MOVIE:$DOCKER_TAG uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop asyncio
                    sleep 10
                    '''
                    }
                    script {
                    sh '''
                    docker rm -f $DOCKER_IMAGE_CAST
                    docker run -d -p 8002:8000 -e DATABASE_URI=$DATABASE_URL_CAST --name $DOCKER_IMAGE_CAST $DOCKER_ID/$DOCKER_IMAGE_CAST:$DOCKER_TAG uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop asyncio
                    sleep 10
                    '''
                    }
                }
            }

        stage('Test Acceptance'){ 
            steps {
                sh 'curl localhost:8002/api/v1/casts/docs'
                sh 'curl localhost:8001/api/v1/movies/docs'
            }
        }
        stage('Docker Push'){ 
            environment
            {
                DOCKER_PASS = credentials("DOCKER_HUB_PASS")  
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
        KUBECONFIG = credentials("config")  
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE")  
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
stage('Deployment in QA'){
        environment
        {
        KUBECONFIG = credentials("config") 
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE")  
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
                  --namespace qa
                helm upgrade --install cast ./charts --values=values.yml \
                  --set image.repository=$DOCKER_ID/$DOCKER_IMAGE_CAST \
                  --set image.tag=$DOCKER_TAG \
                  --set env[0].name=DATABASE_URI --set env[0].value="$DATABASE_URL_CAST" \
                  --set fullnameOverride=cast-service \
                  --set ingress.hosts[0].paths[0].path=/api/v1/casts \
                  --set ingress.hosts[0].paths[0].pathType=Prefix \
                  --namespace qa
                '''
                }
            }

        }
stage('Deploiement en staging'){
        environment
        {
        KUBECONFIG = credentials("config")  
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE")  
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
        when {
            expression { env.BRANCH_NAME == 'master' }
        }

        environment
        {
        KUBECONFIG = credentials("config")  
        DATABASE_URL_MOVIE = credentials("DATABASE_URL_MOVIE")  
        DATABASE_URL_CAST = credentials("DATABASE_URL_CAST")
        CAST_SERVICE_HOST_URL = "http://cast-service/api/v1/casts/"
        }
            steps {
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
post { 

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
}
}
