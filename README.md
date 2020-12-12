# Readme

## Build the Docker Image
1. Build the container image by running ```build_docker_image.ps1``` in a PowerShell session.
2. Run ```docker images``` and verify that the image named ```teqniqly/wineratingscollector``` is in the list.

## Run the Container Locally
Run the container:
```bash
docker run -it --rm teqniqly/wineratingscollector 
```

### Environment Variables (optional)

#### DB_START_PAGE
Specifies at which page to start the database inserts. This is used when the app needs to be restarted. If not specified
defaults to 1.

#### SLEEP_TIME
Specifies the time to pause in seconds after inserting data. If not specified, defaults to 2 seconds. When
DB_START_PAGE >= the current page, the sleep time is increased by a factor of 2.5.

## Push the Image to Azure Container Registry

1. Login to Azure Container Registry:
    ```shell script
    az acr login teqniqlyacr
    ```
2. Tag the local image:
    ```shell script
    docker tag teqniqly/wineratingscollector teqniqlyacr.azurecr.io/teqniqly/wineratingscollector:latest
    ```
3. Push the image:
    ```shell script
    docker push teqniqlyacr.azurecr.io/teqniqly/wineratingscollector:latest
    ```
4. Verify the image with the expected tag has been pushed:
    ```shell script
    az acr repository show-tags --name teqniqlyacr --repository teqniqly/wineratingscollector
    ```

## Create the Azure Container Instance

Run the following command to create and run the container:
```shell script
az container create --resource-group teqniqly-app-rg --name wineratingscollector --image teqniqlyacr.azurecr.io/teqniqly/wineratingscollector:latest --registry-username teqniqlyacr --registry-password password
```