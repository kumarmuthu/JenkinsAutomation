# JenkinsAutomation
Jenkins server starts from cmd.exe with help of python subprocess
* **StartJenkinsServer** (from cmd.exe and REST API verification)
* **SubprocessUtility** (common user)
* **
* **

# Jenkins Installation Guide with Java Setup
This guide explains how to download and install Jenkins, configure Java (JDK 21), and set up the environment variables for Java.
* **

## 1. Download and Install Java (JDK 21)
### Step-1: Download Java 21
- Visit the official Oracle JDK 21 download page:
  - [Java 21 x64 `.exe` Installer](https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.exe)
  - [Java 21 x64 `.msi` Installer](https://download.oracle.com/java/21/latest/jdk-21_windows-x64_bin.msi)
- Choose either `.exe` or `.msi` depending on your preference (for most users, `.exe` is recommended).

### Step-2: Install Java
- Run the downloaded installer and follow the instructions to install Java.
- By default, it will be installed in `C:\Program Files\Java\jdk-21`.

* **

## 2. Set Up Java Environment Variables
### Step-1: Set `JAVA_HOME`
- Right-click on **This PC** or **My Computer** and select **Properties**.
- Click **Advanced system settings** → **Environment Variables**.
- Under **System Variables**, click **New**.
  - **Variable name**: `JAVA_HOME`
  - **Variable value**: `C:\Program Files\Java\jdk-21`
- Click **OK**.

### Step-2: Add Java to `Path`
- In the same **Environment Variables** window, under **System Variables**, scroll down and find `Path`.
- Select `Path` and click **Edit**.
- Click **New** and add the following:

  - `%JAVA_HOME%\bin`

- Click **OK** to save changes.

### Step-3: Verify Java Installation
- Open a new **Command Prompt** window and run the following commands:
```bash
java -version
```

```bash
java version "21.0.4" 2024-07-16 LTS
Java(TM) SE Runtime Environment (build 21.0.4+8-LTS-274)
Java HotSpot(TM) 64-Bit Server VM (build 21.0.4+8-LTS-274, mixed mode)
```

- Also verify the `JAVA_HOME` value:
  - `echo %JAVA_HOME%`
This should return:
  - `C:\Program Files\Java\jdk-21`
* **

## 3. Download and Install Jenkins
### Step-1: Download Jenkins
- Go to the official Jenkins website and download the latest LTS version:
  - [Jenkins LTS Download](https://www.jenkins.io/download/)
- Choose the Windows installer (`.msi`).

### Step-2: Install Jenkins
- Run the downloaded `.msi` file and follow the installation steps.
- During installation, Jenkins will check for a compatible Java version. If you've set up `JAVA_HOME` correctly, it should detect Java 21.

### Step-3: Complete Jenkins Setup
- After installation, open Jenkins in your browser using:
  ```
  http://localhost:8080
  ```
- Use the **initialAdminPassword** located at:
  ```
  C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword
  ```

### Step-4: Troubleshooting: Missing Secrets Directory and File
If you cannot see the secrets directory or the `initialAdminPassword` file, follow these steps:

  1. **Restart Jenkins**:
     - Open the **Run** dialog (Windows + R), type `services.msc`, and press Enter.
     - Find **Jenkins** in the list, right-click on it, and select **Restart**.

  2. **Check the Secrets Directory**:
     - Open Command Prompt and run:
       ```bash
       dir "C:\ProgramData\Jenkins\.jenkins\secrets"
       ```

  3. **Check Jenkins Log Files**:
      - If the secrets directory is still missing, you can check the log files for any errors:
        ```bash
        type "C:\Program Files\Jenkins\jenkins.err.log"
        type "C:\Program Files\Jenkins\jenkins.out.log"
        ```
   
      - Follow the on-screen instructions to complete the Jenkins setup and create the admin user.
         ```
         Jenkins initial setup is required. An admin user has been created and a password generated.
         Please use the following password to proceed to installation:
      
         754240566b9e4748b1698f4f87ae9615
      
         This may also be found at: C:\ProgramData\Jenkins\.jenkins\secrets\initialAdminPassword
         ```

## Step-5: Verify Jenkins Installation
- Ensure that Jenkins is running correctly by visiting:
  ```
  http://localhost:8080
  ```
- You can start/stop Jenkins via the **Services** management console in Windows.

## Step-6: Jenkins Workspace

```C:\ProgramData\Jenkins\.jenkins\workspace```

* **