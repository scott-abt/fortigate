#!/usr/bin/env python3

from getpass import getpass,getuser
import paramiko

def get_new_pass():
    newpass = getpass("New password: ")
    newpass_confirm = getpass("Confirm new password: ")
    if newpass != newpass_confirm:
        print("Password does not match")
        get_new_pass()
    else:
        return(newpass)

def main():
    username = input("Username: ")
    oldpass = getpass("Old password: ")
    newpass = get_new_pass()
    bkup_cmd = "exec backup config flash \"before password change\""
    command = "config system admin\nedit admin\nset password \"{}\"\nend\nexec backup config flash \"Password changed\"".format(newpass)
    host_list = open("fgt_list.csv")

    for hostname in host_list:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            client.connect(hostname, port=22, username=username, password=oldpass)

            stdin, stdout, stderr = client.exec_command(bkup_cmd)
            print(type(stdout))
            print(stdout.read())
            
            stdin, stdout, stderr = client.exec_command(command)
            print(stdout.read())
            
        except Exception as e:
            print("*************************\nTHERE WAS A PROBLEM")
            print(e)
            pass

        finally:
            client.close()

if __name__ == "__main__":
    main()
