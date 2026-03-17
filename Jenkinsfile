pipeline {
    agent any

    stages {
        stage('🕵️ Pre-checks') {
            steps {
                echo 'Validando que el código esté completo...'
                sh 'ls -R'
            }
        }

        stage('📦 Build Image') {
            steps {
                echo 'Construyendo la imagen de Docker...'
                // Esto crea la imagen con el nombre del equipo
                sh 'docker build -t drive-equipo-4 .'
            }
        }

        stage('🚀 Deploy') {
            steps {
                echo 'Desplegando contenedor...'
                // Detiene el contenedor anterior si existe para evitar errores
                sh 'docker stop drive-app || true'
                sh 'docker rm drive-app || true'
                // Corre el nuevo con los cambios más recientes
                sh 'docker run -d --name drive-app -p 3000:3000 drive-equipo-4'
            }
        }
    }
}