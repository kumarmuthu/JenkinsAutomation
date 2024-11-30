import subprocess

# Command to start Jenkins with PowerShell in an elevated mode
jenkins_path = r"C:\Program Files\Jenkins\jenkins.exe"
powershell_command = f'Start-Process -FilePath "{jenkins_path}" -ArgumentList "start" -Verb RunAs'

result = subprocess.run(
    ["powershell", "-Command", powershell_command],
    capture_output=True,
    text=True
)

print("Standard Output:", result.stdout)
print("Standard Error:", result.stderr)

"""
import subprocess
import os

# Path to Jenkins WAR file and Java executable
jenkins_jar_path = r"C:\Program Files\Jenkins\jenkins.war"  # Update with actual path to jenkins.war
java_path = r"C:\Program Files\Java\jdk-21\bin\java.exe"  # Update with actual Java path

# Set the JENKINS_HOME environment variable to point to the existing Jenkins home directory
os.environ['JENKINS_HOME'] = "C:\\Users\\ADMIN\\.jenkins"  # Update with the actual path to your Jenkins home

# Verify the JENKINS_HOME value
print("JENKINS_HOME is set to:", os.getenv('JENKINS_HOME'))

# Command to run Jenkins using java -jar
jenkins_start_cmd = [
    java_path,
    "-DJENKINS_HOME=" + os.environ['JENKINS_HOME'],
    "-jar",
    jenkins_jar_path,
    "--httpPort=8080"
]

# Run the command
result = subprocess.run(
    jenkins_start_cmd,
    capture_output=True,
    text=True,
    shell=True  # Use shell=True if the command requires shell processing
)

print("Standard Output:", result.stdout)
print("Standard Error:", result.stderr)
"""