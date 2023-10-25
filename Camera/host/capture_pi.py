from ipaddress import ip_address
import paramiko

# Function to trigger image capture on the Raspberry Pi
def capture_image_on_pi(colony_id):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect('192.168.0.199', username='pi', password='raspberry')
        print("SSH connection established successfully")
    except Exception as e:
        print(f"SSH connection failed: {e}")
    script_path = '/home/pi/Documents/gitreps/DWARVES/Camera/RPi/capture_image.py'
    command = f'python3 {script_path} {colony_id}'
    print(f"Executing command: {command}")
    stdin, stdout, stderr = ssh.exec_command(command)
    print("Command executed")
    ssh.close()

# Example usage
colony_id = 'colonyID_2'  # Replace with the desired colony ID
capture_image_on_pi(colony_id)