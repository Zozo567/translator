# Translator service

This application provides translation services from English to multiple specified target languages. The application supports translations into Spanish, French, German, Japanese, Arabic, Hindi, and Portuguese.

## Requirements
- Docker
- docker-compose

## Installation
- Rename .env.sample to .env
- Run command:
```sh
make start
```

## Usage
Visit:
http://localhost:8080/api/v1/docs 

Testing Request body:
```
{
  "text": "[param name] fees are calculated as follows: [param description]",
  "target_language": "HU"
}
```

## Monitoring: 
- Open your web browser and navigate to http://localhost:3000.
- Log in with the default credentials (admin/admin) and change the password when prompted.
- Click on the gear icon (⚙️) on the left sidebar and select Data Sources.
- Click Add data source, select Prometheus, and set the URL to http://prometheus:9090.
- Click Save & Test to verify the connection.

