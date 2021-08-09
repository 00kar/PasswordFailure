import os
from getpass import getuser

# Getting username
username = str(getuser())

# Checking if package exists
# If it does not exist istalls that
if not os.path.exists("/usr/bin/ffmpeg"):
    os.system("sudo apt install ffmpeg")

# Checking if directory exists
# If it does not exist creating that new directory
if not os.path.exists("/media/thief"):
    os.system("sudo mkdir /media/thief")

# Checking if file exists
# If it does not exist creating that file
file_path = "/home/" + username + "/grabpicture"
if not os.path.exists(file_path):
    os.system("sudo touch " + file_path)
    os.system("sudo chmod 775 " + file_path)   # Making it executable file
    os.system("sudo chown " + username + ":" + username + " " + file_path)   # Changing user from root to single user to make possible following commands
    my_script = [
        "#!/bin/bash \n",
        "ts=`date +%s` \n",
        "ffmpeg -f video4linux2 -s vga -i /dev/video0 -vframes 1 /media/thief/vid-$ts.%01d.jpg \n",
        "exit 0"
        ]
    grabpicture = open(file_path, "w+")   # Openning 'grabpicture' to write in it  
    grabpicture.writelines(my_script)    # Adding all members of 'my_script' as a text to 'grabpicture'  
    grabpicture.close()    # Closing and saving the text
    os.system("sudo mv " + file_path + " /usr/local/bin/") 
    os.system("sudo sed -i 's/success=1/success=2/' /etc/pam.d/common-auth")    # Configuring PAM to call this on every failed attempt
    os.system("sudo sed -i '17 a auth    [default=ignore]                pam_exec.so seteuid /usr/local/bin/grabpicture' /etc/pam.d/common-auth")
