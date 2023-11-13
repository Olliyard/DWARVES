import paramiko

# Function to trigger image capture on the Raspberry Pi
def capture_image_on_pi(colonyID, obsInterval):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('192.168.0.199', username='pi', password='raspberry')
        print("SSH connection established successfully")
    except Exception as e:
        print(f"SSH connection failed: {e}")
    script_path = '/home/pi/Documents/gitreps/DWARVES/Camera/RPi/capture_image.py'
    command = f'python3 {script_path} {colonyID} {obsInterval}'
    print(f"Executing command: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    print("Command executed")
    ssh.close()

# Example usage
colonyID = 'colonyID_2' # Replace with the desired colony ID
obsInterval = 30        # Replace with the desired observation interval
capture_image_on_pi(colonyID, obsInterval)