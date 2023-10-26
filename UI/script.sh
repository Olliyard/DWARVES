#!/bin/bash

# ANSI color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m' # No color, to reset

# Function to clear the screen and display the ASCII art
clear_screen() {
    clear
    echo -e "${GREEN}"
    cat << "EOF"
$$$$$$$\  $$\      $$\  $$$$$$\  $$$$$$$\  $$\    $$\ $$$$$$$$\  $$$$$$\        $$\   $$\ $$$$$$\ 
$$  __$$\ $$ | $\  $$ |$$  __$$\ $$  __$$\ $$ |   $$ |$$  _____|$$  __$$\       $$ |  $$ |\_$$  _|
$$ |  $$ |$$ |$$$\ $$ |$$ /  $$ |$$ |  $$ |$$ |   $$ |$$ |      $$ /  \__|      $$ |  $$ |  $$ |  
$$ |  $$ |$$ $$ $$\$$ |$$$$$$$$ |$$$$$$$  |\$$\  $$  |$$$$$\    \$$$$$$\        $$ |  $$ |  $$ |  
$$ |  $$ |$$$$  _$$$$ |$$  __$$ |$$  __$$<  \$$\$$  / $$  __|    \____$$\       $$ |  $$ |  $$ |  
$$ |  $$ |$$$  / \$$$ |$$ |  $$ |$$ |  $$ |  \$$$  /  $$ |      $$\   $$ |      $$ |  $$ |  $$ |  
$$$$$$$  |$$  /   \$$ |$$ |  $$ |$$ |  $$ |   \$  /   $$$$$$$$\ \$$$$$$  |      \$$$$$$  |$$$$$$\ 
\_______/ \__/     \__|\__|  \__|\__|  \__|    \_/    \________| \______/        \______/ \______|

EOF
echo -e "${NC}" # Reset color
}

# Function to check colonies
check_colonies() {
    clear_screen
    echo "Checking colonies..."
    jq -r '. as $in | keys[] | "Colony \(.): Occupied: \($in[.].occupied)"' settings.json
    echo "0. Back to main menu"
}

# Function to display JSON data for a specific colony
display_colony_data() {
    colony_name="$1"
    colony_data=$(jq ".$colony_name" settings.json)
    clear_screen
    echo "Colony Data for $colony_name:"
    echo "$colony_data"
    echo "0. Back to main menu"
}

# Function to change specific settings for a colony
change_colony_settings() {
    colony_name="$1"

    while true; do
        clear_screen
        colony_data=$(jq ".$colony_name" settings.json)
        echo "Changing settings for Colony $colony_name:"
        
        # Temperature limits
        min_temperature=15
        max_temperature=30
        
        # Light intensity limits
        min_light_intensity=0
        max_light_intensity=1
        
        # Observation interval limits
        min_observation_interval=1
        max_observation_interval=24
        
        # Daytime hours limits
        min_daytime_hours=1
        max_daytime_hours=24

        # Display daytime settings
        echo "Daytime Settings:"
        echo "1. Daytime temperature: $(jq -r ".$colony_name.daytime_temperature" settings.json) (Limit: $min_temperature-$max_temperature°C)"
        echo "2. Daytime light intensity: $(jq -r ".$colony_name.daytime_light_intensity" settings.json) (Limit: $min_light_intensity-$max_light_intensity)"
        echo "3. Daytime hours: $(jq -r ".$colony_name.daytime_hours" settings.json) (Limit: $min_daytime_hours-$max_daytime_hours hours)"
        
        # Display nighttime settings
        echo "Nighttime Settings:"
        echo "4. Nighttime temperature: $(jq -r ".$colony_name.nighttime_temperature" settings.json) (Limit: $min_temperature-$max_temperature°C)"
        echo "5. Nighttime light intensity: $(jq -r ".$colony_name.nighttime_light_intensity" settings.json) (Limit: $min_light_intensity-$max_light_intensity)"
        
        # Display Observation interval setting
        echo "Observation Settings:"
        echo "6. Observation interval: $(jq -r ".$colony_name.observation_interval" settings.json) (Limit: $min_observation_interval-$max_observation_interval hours)"
        
        echo "0. Back to main menu"
        read -p "Enter the setting to change (or 0 to go back): " setting_choice

        case $setting_choice in
            0)
                break
                ;;
            1)
                while true; do
                    read -p "Enter the new Daytime temperature: " new_value
                    if ((new_value >= min_temperature && new_value <= max_temperature)); then
                        jq ".$colony_name.daytime_temperature = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Temperature must be between $min_temperature and $max_temperature°C."
                    fi
                done
                ;;
            2)
                while true; do
                    read -p "Enter the new Daytime light intensity: " new_value
                    if ((new_value >= min_light_intensity && new_value <= max_light_intensity)); then
                        jq ".$colony_name.daytime_light_intensity = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Light intensity must be between $min_light_intensity and $max_light_intensity."
                    fi
                done
                ;;
            3)
                while true; do
                    read -p "Enter the new Daytime hours: " new_value
                    if ((new_value >= min_daytime_hours && new_value <= max_daytime_hours)); then
                        jq ".$colony_name.daytime_hours = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Daytime hours must be between $min_daytime_hours and $max_daytime_hours."
                    fi
                done
                ;;
            4)
                while true; do
                    read -p "Enter the new Nighttime temperature: " new_value
                    if ((new_value >= min_temperature && new_value <= max_temperature)); then
                        jq ".$colony_name.nighttime_temperature = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Temperature must be between $min_temperature and $max_temperature°C."
                    fi
                done
                ;;
            5)
                while true; do
                    read -p "Enter the new Nighttime light intensity: " new_value
                    if ((new_value >= min_light_intensity && new_value <= max_light_intensity)); then
                        jq ".$colony_name.nighttime_light_intensity = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Light intensity must be between $min_light_intensity and $max_light_intensity."
                    fi
                done
                ;;
            6)
                while true; do
                    read -p "Enter the new Observation interval: " new_value
                    if ((new_value >= min_observation_interval && new_value <= max_observation_interval)); then
                        jq ".$colony_name.observation_interval = $new_value" settings.json > tmpfile && mv tmpfile settings.json
                        break
                    else
                        echo "Invalid input. Observation interval must be between $min_observation_interval and $max_observation_interval hours."
                    fi
                done
                ;;
            *)
                echo "Invalid choice. Please select a valid option."
                ;;
        esac
    done
}





# Function to pause until the user presses a key
pause() {
    read -n 1 -s -r -p "Press any key to continue..."
}

# Function to insert a new colony
insert_new_colony() {
    # Check if the loading zone is empty
    loading_zone_occupied=$(jq -r '.loadingZone.occupied' settings.json)
    
    if [ "$loading_zone_occupied" == "true" ]; then
        clear_screen
        echo "The loading zone is empty. Enter a colony first."
        pause
    else
        clear_screen
        echo "Available non-occupied colonies:"
        jq -r 'to_entries[] | select(.value.occupied == false) | "\(.key): \(.value.id)"' settings.json
        echo "0. Back to main menu"
        
        read -p "Enter the number of the colony to insert (or 0 to go back): " colony_choice
        if [ "$colony_choice" != "0" ]; then
            colonies=$(jq -r 'to_entries[] | select(.value.occupied == false) | "\(.key)"' settings.json)
            colony_name=$(echo "$colonies" | sed -n "${colony_choice}p")
            jq ".$colony_name.occupied = true" settings.json > tmpfile && mv tmpfile settings.json
            jq '.loadingZone.occupied = true' settings.json > tmpfile && mv tmpfile settings.json
            clear_screen
            echo "Colony $colony_name has been marked as occupied."
            
            # Use the pause function to wait before returning to the main menu
            pause
        fi
    fi
}


# Function to withdraw an old colony
withdraw_old_colony() {
    # Check if the loading zone is empty
    loading_zone_occupied=$(jq -r '.loadingZone.occupied' settings.json)
    
    if [ "$loading_zone_occupied" == "false" ]; then
        clear_screen
        echo "Loading zone is not empty. Remove the colony first."
        pause
    else
        clear_screen
        echo "Occupied colonies:"
        jq -r 'to_entries[] | select(.value.occupied == true) | "\(.key): \(.value.id)"' settings.json
        echo "0. Back to main menu"
        
        read -p "Enter the number of the colony to withdraw (or 0 to go back): " colony_choice
        if [ "$colony_choice" != "0" ]; then
            colonies=$(jq -r 'to_entries[] | select(.value.occupied == true) | "\(.key)"' settings.json)
            colony_name=$(echo "$colonies" | sed -n "${colony_choice}p")
            jq ".$colony_name.occupied = false" settings.json > tmpfile && mv tmpfile settings.json
            jq '.loadingZone.occupied = false' settings.json > tmpfile && mv tmpfile settings.json
            clear_screen
            echo "Colony $colony_name has been withdrawn and the loading zone is now free."
            
            # Use the pause function to wait before returning to the main menu
            pause
        fi
    fi
}


# Main menu
while true; do
    clear_screen
    echo "Options:"
    echo "1. Check colonies"
    echo "2. Insert New colony"
    echo "3. Withdraw old Colony"
    echo "4. Quit"

    read -p "Enter your choice: " choice

    case $choice in
        1)
            check_colonies
            read -p "Enter the number of the colony to view details or change settings (0 to go back to the main menu): " colony_choice
            if [ "$colony_choice" != "0" ]; then
                colonies=$(jq -r 'keys[]' settings.json)
                colony_name=$(echo "$colonies" | sed -n "${colony_choice}p")
                display_colony_data "$colony_name"
                read -p "1. Change settings 0. Back to the main menu: " action
                if [ "$action" == "1" ]; then
                    change_colony_settings "$colony_name"
                fi
            fi
            ;;
        2)
            insert_new_colony
            ;;
        3)
            withdraw_old_colony
            ;;
        4)
            clear_screen
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Please select a valid option."
            pause
            ;;
    esac
done
