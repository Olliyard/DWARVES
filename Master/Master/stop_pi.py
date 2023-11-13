import paramiko

# Function to remotely stop the script on the Raspberry Pi
def stop_script_on_pi(pi_ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(pi_ip, username='pi', password='raspberry')  # Replace with your Raspberry Pi's credentials
    script_path = '/home/pi/Documents/gitreps/DWARVES/Camera/RPi/capture_image.py'
    command = f'pkill -f "python3 {script_path}"'
    ssh.exec_command(command)
    ssh.close()
    print(f'Script at path "{script_path}" on the Raspberry Pi has been stopped.')

# Example usage
pi_ip = '192.168.0.199'  # Replace with your Raspberry Pi's IP address
stop_script_on_pi(pi_ip)
