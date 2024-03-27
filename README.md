# The Simplified AIML Platform

The Platform simplified the deployment of Python applications by providing a centralized server point with a standardized environment for running all applications.

## Features

⚡️**Centralized Deployment:** Deploy Flask applications on a centralized server, streamlining the deployment process and ensuring consistency across applications.

🛠**CLI Tool:** The platform offers a command-line interface (CLI) tool that creates application skeleton structures ready for deployment on the platform. Once registered, applications can be easily deployed using this tool.

👮‍**Security with JWT:** The platform enhances security by enabling or disabling JWT (JSON Web Token) authentication. Clients ID and Secret registered via the CLI tool can generate JWT tokens with customizable expiration times to securely access applications within the platform.

🔗**Database Connector:**

![Database Connector](https://skillicons.dev/icons?i=elasticsearch,mongodb,sqlite,redis,windows)

## 💻Tech Stack

**Python:** Version 3.11.1

![TechStack](https://skillicons.dev/icons?i=python,flask)

# 📂 Platform Structure

    .
    ├── 📂 app
        ├── 📂 security
            ├── 📂 security
            ├── __init__.py
            ├── routes.py                           # security handler for JWT token
        ├── __init__.py                             # Application registration Handler
    ├── 📂 libraries                                # Application dependent python packages
    ├── 📂 Log                                      # Platform Log
        ├── 📂 ErrorData                            # Error Information temp directory
        ├── Log.txt                                 # Application processing log
    ├── 📂 sentence-transformers_all-mpnet-base-v2  # Pre-trained S-BERT Model
    ├── __init__.py
    ├── apppool.py                                  # Platform recycle apppool Handler
    ├── config.ini                                  # Platform configuration
    ├── featureaiml.py                              # AIML Model Handler
    ├── featuredbconnect.py                         # Database Connector
    ├── featureversion.py                           # Platform Version Info
    ├── featurelog.py                               # Platform Log Handler
    ├── featureRequirements.py                      # Python Packages version
    ├── featurestoreprocedure.py                    # Stored Procedure Execution Handler
    ├── GeneratePassword.py                         # DB Password Handler
    ├── README.md
    ├── register.py                                 # CLI tool
    ├── server.py                                   # centralized server hosting
    ├── web.config                                  # IIS web application configuration

# Getting Started

**Pre-requisites**

- Python [v3.11.1](https://www.python.org/ftp/python/3.11.1/python-3.11.1-amd64.exe)
- HttpPlaftform Handler [v1.2](https://go.microsoft.com/fwlink/?LinkId=690721)
- Microsoft SQL Server ODBC [v17](https://go.microsoft.com/fwlink/?linkid=2249004)

# Installation

Clone the project or copy the provided Source Code

```bash
    git clone https://github.com/pankaj-chongtham/rest-api-python.git
```

Go to project directory

```bash
    cd featureapi
```

Open Command-Prompt from project directory

```bash
    cmd
```

Create Environment

```bash
    python -m venv env
```

or

```
    py -m venv env
```

Activate Environment

```
    env\Scripts\activate
```

Installation the python packages

```bash
    pip install -r featureapiRequirements.txt --no-index --find-links libraries
```

# Hosting platform in Internet Information Service (IIS)

### Create application app pool

```bash
appPoolName = FEATUREAPI
.NET CLR version = No Managed Code
Managed pipeline mode: Integrated
Select Start application pool immediately
```

### Open Advanced Settings of FEATUREAPI appPool\*\*\*\*

```bash
Under (General) Section:
    Start Mode = AlwaysRunning
Under Process Model Section:
    Idle Time-out (minutes) = 0

[Apply the Changes]
```

### Create Application under DefaultWebSite

**Click** on Application

Alias:**_featureapi_**

Application pool:**_FEATUREAPI_**

Physical path:**_{drive}/Program Files (x86)/Utilities/featureapi_**

Select: **_Enable Preload_**

[Apply the changes]

### Application Configuration

**Click** on Configuration Editor

Drop down & Select: **_➡️system.webServer ➡️ httPlatform_**

arguments:**_-m waitress --port %HTTP_PLATFORM_PORT% server:app_**

processesPerApplication:**_10_**

processPath:**_{drive}\Program Files(x86)\Utilities\featureapi\env\Scripts\python.exe_**

**Click** again on 'featureapi' application

**Double-Click** on Handler Mappings

**Double-Click** on 'featureapiHttpPlatformHandler'

Modify the Settings as:
Executable (optional):**_{drive}\Program Files (x86)\Utilities\featureapi\env\Scripts\python.exe_**

**Click** on 'Request Restrictions'

**Unselect** Invoke handler only if required is mapped to:

[Apply the changes]

**Refresh** Default Web Site\featureapi

**Recycle** FEATUREAPI AppPool

# Testing the Application

### Using postman

![Postman](https://skillicons.dev/icons?i=postman)

**GET** http://localhost/featureapi/v1/version

or

**GET** http://**hostname**/featureapi/v1/version

or

**GET** http://**ip-address**/featureapi/v1/version

**_Expected Response_**

```json
{ "productVersion": "v1.0" }
```

### Using Command-Prompt

![Postman](https://skillicons.dev/icons?i=windows)

```bash
curl -X GET "http://localhost/featureapi/v1/version
```

**_Expected Response_**

```json
{ "productVersion": "v1.0" }
```

### Using Python

![Postman](https://skillicons.dev/icons?i=python)

```python
import requests
requests.get("http://localhost/featureapi/v1/version")
```

**_Expected Response_**

```response
b'{"productVersion": "v1.0"}'
```

# Troubleshooting

#### Open Command-Prompt from featureapi directory

```
env\Scripts\activate
py server.py
```

_Expected Response_

```
* Serving Flask app 'app'
* Debug Mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
* Running on http://127.0.0.1:5000
```

#### 1. Error: ModuleNotFoundError

```bash
Example: ModuleNotFoundError: No module named 'sklearn'
```

_Resolution:_

```bash
env\Scripts\activate
pip install sklearn

Note: sklearn is missing in this example.
```

#### 2. Error: Python not Installed properly.

```bash
Example: 'py' or 'python' is not recognized as an internal or external command, operable program or batch file.
```

_Resolution:_

Open Command-Prompt

```bash
where python
```

Expected Output:

```
C:\{installation path}\python.exe
```

If same error is still shown, re-install python exe.

## Model - Process Flow

![model](/data/architecture/model.png)

## Architecture

![architecture](/data/architecture/architecture.png)
