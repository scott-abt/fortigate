#!/usr/bin/env python3

from getpass import getpass,getuser
import paramiko

def main():
    username = input("Username: ")
    oldpass = getpass("Password: ")
    commands = open("./commands.txt")
    host_list = open("fgt_list.csv")
    build_command = str()
    for compart in commands:
        build_command += compart.strip() + "\n"
    print(build_command)
    for hostname in host_list:
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
            client.connect(hostname.strip(), port=22, username=username, password=oldpass)

            stdin, stdout, stderr = client.exec_command("exec backup config flash \"before automated change\"")
            print(type(stdout))
            print(stdout.read())
            
            stdin, stdout, stderr = client.exec_command(build_command)
            print(stdout.read())

            stdin, stdout, stderr = client.exec_command("exec backup config flash \"after automated change\"")
            print(stdout.read())
            
        except Exception as e:
            print("*************************\nTHERE WAS A PROBLEM")
            print(e)
            pass

        finally:
            client.close()

if __name__ == "__main__":
    main()
