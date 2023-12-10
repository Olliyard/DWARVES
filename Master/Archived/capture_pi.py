import paramiko
import os
import sys

# Method to trigger image capture on the Raspberry Pi and receive data
def capture_and_receive_data(colonyID):
    # Create a connection to the Raspberry Pi
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('192.168.0.123', username='pi', password='raspberry')

    # Trigger image capture and processing on the Raspberry Pi
    stdin, stdout, stderr = ssh.exec_command(f'python3 /home/pi/Documents/gitreps/DWARVES/RobotController/Camera/captureImage.py {colonyID}')

    # Wait for the command to complete
    exit_status = stdout.channel.recv_exit_status()

    if exit_status == 0:
        # Receive data from the Raspberry Pi
        sftp = ssh.open_sftp()
        print(f'Locating colony{colonyID} images files...')
        
        # List files in the folder
        image_files = [file for file in sftp.listdir(f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}/') if file.endswith(('.jpg', '.txt', '.png'))]
        print(f'Files found: {image_files}')

        # Loop through the files and receive them
        for file in image_files:
            remote_path = f'/home/pi/Documents/gitreps/DWARVES/RobotController/Camera/colony{colonyID}'
            local_path = f'/home/stud/Documents/gitreps/DWARVES/Master/colony{colonyID}'

            # Make local dir if none
            os.makedirs(local_path, exist_ok=True)
            try:
                sftp.get(f'{remote_path}/{file}', f'{local_path}/{file}')
                print("Extracting images...")
            
            except Exception as e:
                print(f"Error extracting images: {str(e)}")

        print(f'Image data for colony{colonyID} successfully extracted to {local_path}.')
        
        # Remove folders on the Raspberry Pi
        stdin, stdout, stderr = ssh.exec_command(f'rm -rf {remote_path}')

        # Wait for the command to complete
        exit_status = stdout.channel.recv_exit_status()

        # Close the connection
        sftp.close()
        ssh.close()

    else:
        # If the command was not successful, handle the error as needed
        print(f"Error: {stderr.read().decode('utf-8')}")
        ssh.close()
        return None

# Get commandline colony ID
if len(sys.argv) > 1:
    colonyID = sys.argv[1]
    capture_and_receive_data(colonyID)
else:
    print("Please provide a colonyID as a command-line argument.")
