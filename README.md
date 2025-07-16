Summary: Deploying a Streamlit App on Amazon Linux EC2
This guide outlines the complete process to deploy your Python Streamlit application (USENT_0714.py) on an Amazon Linux EC2 instance, using a virtual environment and nohup for background execution.
Prerequisites (On your Local Machine & AWS Console)
1.	AWS EC2 Instance:
o	Launch an Amazon Linux EC2 instance (e.g., Amazon Linux 2023 AMI).
o	Ensure your usent-kp.pem (or your key pair) is accessible on your local machine.
2.	Security Group Configuration (AWS Console):
o	SSH (Port 22): Add an inbound rule to allow TCP traffic on port 22 from your IP address (or 0.0.0.0/0 for broader, less secure access).
o	Streamlit (Port 8501): Add an inbound rule to allow TCP traffic on port 8501 from your IP address (or 0.0.0.0/0). This is crucial for accessing your app.
Step 1: Connect to EC2 and Prepare the Environment
1.	Connect via SSH from your local machine:
Bash
ssh -i /path/to/your-key-pair.pem ec2-user@YOUR_EC2_PUBLIC_IP_OR_DNS
(Replace /path/to/your-key-pair.pem and YOUR_EC2_PUBLIC_IP_OR_DNS).
2.	Update system packages (on EC2):
```bash
sudo yum update -y       # For Amazon Linux 2 (older)
```


OR for Amazon Linux 2023:
#####  sudo dnf update -y
(We used dnf in our session, which indicates you're on AL2023 or a very recent AL2).
3.	Install Python development tools and pip (on EC2):
```Bash
sudo dnf install -y git python3-devel python3-pip
```
##### OR for older AL2:
##### sudo yum install -y git python3-devel python3-pip
Step 2: Transfer Your Project Files
You have two primary options to get your usent_st_simple project directory onto the EC2 instance.
Option A: Using scp (from your Local Machine)
•	From your local machine's terminal, navigate to the directory containing usent_st_simple.
•	Run:
Bash
scp -i /path/to/your-key-pair.pem -r usent_st_simple ec2-user@YOUR_EC2_PUBLIC_IP_OR_DNS:~
Option B: Using git clone (from EC2)
•	If your project is in a Git repository (like the one you provided), you can clone it directly on the EC2 instance.
•	On EC2, ensure you are in your home directory:
```Bash
cd ~
```
•	Then clone your repository:

```Bash
git clone https://github.com/CDQ-Analyst/usent_st_simple.git
```
Step 3: Set Up Python Virtual Environment and Install Dependencies (On EC2)
1.	Go to your home directory:
```Bash
cd ~
```
2.	Create the virtual environment:

```Bash
python3 -m venv my_project_venv
```
4.	Activate the virtual environment:
```
Bash
source my_project_venv/bin/activate
```

Your prompt will change to (my_project_venv) [ec2-user@ip-...:~$].
6.	Navigate into your project directory:
```
Bash
cd usent_st_simple
```
Your prompt will change to (my_project_venv) [ec2-user@ip-...:~/usent_st_simple]$.
7.	Edit requirements.txt to remove built-in modules:
This step is crucial to prevent "No matching distribution found" errors for modules like io, os, zipfile, time, etc., which are part of Python's standard library.
```
Bash
nano requirements.txt
```
o	Delete any lines that only contain built-in module names (e.g., io, os, zipfile, time). Keep only external packages like streamlit, pandas, matplotlib, openpyxl.
o	Save: Ctrl+O, then Enter.
o	Exit: Ctrl+X.
8.	Install project dependencies:
```
Bash
pip install -r requirements.txt
```
Step 4: Fix Image Paths in Your Streamlit App (On EC2)
1.	Edit your Streamlit application script (USENT_0714.py):
The error Error opening 'C:\Users\...' indicated a Windows-style path.
```
Bash
nano USENT_0714.py
```
2.	Locate the image path (e.g., logo_link_cxpt = "C:\Users\sulay\Documents\...\USENT_Logo-removebg.png") and change it to a relative Linux path.
Since USENT_Logo-removebg.png is in the same directory as your script, you can simply use:
Python
logo_link_cxpt = "USENT_Logo-removebg.png"
#### Or directly in st.image if hardcoded:
#### st.image("USENT_Logo-removebg.png", width=100, caption=None)
3.	Save changes (Ctrl+O, Enter) and exit nano (Ctrl+X).
Step 5: Run Your Streamlit Application (On EC2)
Use nohup and & to run your Streamlit app in the background, allowing it to continue even after you close your SSH connection.
```
Bash
nohup python3 -m streamlit run USENT_0714.py --server.port 8501 --server.enableCORS false --server.enableXsrfProtection false &
```
Step 6: Access Your Streamlit App
1.	Get the Network URL:
The Streamlit app prints its access URLs to nohup.out.
```
Bash
cat nohup.out
```
Look for the Network URL: http://<Private_IP_Address>:8501.
2.	Open in your browser (from your local machine):
Use your EC2 instance's Public IPv4 Address (found in the AWS EC2 console) with port 8501:
http://YOUR_EC2_PUBLIC_IP_ADDRESS:8501
Step 7: Managing Your Application (On EC2)
•	To check if it's running:
```
Bash
ps aux | grep streamlit
```
•	To stop the app:
Find the Process ID (PID) from the ps aux output (the second column) and use:
```
Bash
kill <PID>
```
#### If it doesn't stop, try:
#### kill -9 <PID>
