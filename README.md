# File Tracking System

![Logo](https://github.com/algobasket/File-Tracking-System/blob/main/staticfiles/images/logo.png)

## Description
**FIND YOUR LAN IP ADDRESS**

## Setup Instructions

### 1. Put IP in .env file
### 2. Replace local domain in `nginx.config` and `.env` file

## Installation

### Windows Installation
1. Open PowerShell with administrative privileges.
2. Navigate to the project root.
    ```shell
    cd path/to/project/root
    ```
3. Run the deployment script:
    ```shell
    ./deploy-docker-windows.ps1
    ```

### Linux Installation
1. On a Linux Ubuntu system, navigate to the project root.
    ```shell
    cd path/to/project/root
    ```
2. Make the scripts executable:
    ```shell
    chmod +x add-host-entry.sh
    chmod +x deploy-docker-linux.sh
    ```
3. Run the deployment script:
    ```shell
    ./deploy-docker-linux.sh
    ```

## Accessing the Application

- The application will be running at: [http://efhz.lan/](http://efhz.lan/)
- PhpMyAdmin will be running at: [http://efhz.lan:8080/](http://efhz.lan:8080/)

### LAN Access
- App: `http://LAN-IP.lan/`
- PhpMyAdmin: `http://LAN-IP.lan:8080/`

