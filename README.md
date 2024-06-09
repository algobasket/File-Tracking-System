# GMS - File Tracking System

![Logo](https://github.com/algobasket/File-Tracking-System/blob/main/staticfiles/images/logo.png)

## Description
**GMS - File Tracking System** is a system where various users with different roles can share, forward, approve, and access files. The roles include Admin, Dakghar (file uploader), GMS, GM (General Manager), CO, DO, HOS, etc. Files are forwarded in a hierarchical manner among these roles. This system is built using Django, a Python framework.

## Setup Instructions

### 1. Put IP in .env file
### 2. Replace local domain in `nginx.config` and `.env` file
### 3. Change `ENV_TYPE` in `.env` file:
   - `local` if you want to run locally
   - `docker` or `production` for other environments

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

## Conclusion
The GMS - File Tracking System provides a robust solution for managing file sharing, forwarding, approval, and access among users with different roles in an organization. By following the setup and installation instructions, you can easily deploy this system on both Windows and Linux environments. Ensure to configure your `.env` file correctly to suit your deployment environment, and enjoy streamlined file management with GMS.

You can fork our repo or press that star. Email us if you need any help. Support or sponsor if you find our projects to be cool.

