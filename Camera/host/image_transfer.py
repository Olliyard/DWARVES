import subprocess

# Define your Raspberry Pi SSH information
pi_username = "pi"
pi_ip = "192.168.0.199"
pi_pass = "raspberry"

# Define your colony names (directory names)
colonies = ["colonyID_1", "colonyID_2", "colonyID_3",
            "colonyID_4", "colonyID_5", "colonyID_6",
            "colonyID_7", "colonyID_8", "colonyID_9"]

# Define the local path on the main MCU
main_mcu_path = "/home/stud/Documents/gitreps/DWARVES/Camera/host"

# Iterate through colonies and transfer images
for colony in colonies:
    # Set the source path on the Raspberry Pi
    source_path = f"{pi_username}@{pi_ip}:/home/pi/Documents/gitreps/DWARVES/Camera/RPi/{colony}/"

    # Set the destination path on the main MCU
    destination_path = f"{main_mcu_path}/{colony}"

    # Construct and execute the scp command
    scp_command = f"scp -r {source_path} {destination_path}"
    try:
        subprocess.run(scp_command, shell=True, check=True)
        print(f"Images from {colony} transferred successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error transferring images from {colony}: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
