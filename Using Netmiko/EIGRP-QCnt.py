#Importing necessary modules
from netmiko import ConnectHandler
import threading
import os.path
import subprocess
import time
import sys
import re
import ipaddress
import io


#Get and Validate the IP(s)
def ip_is_valid():
    check = False
    global ip_list

    while True:
        print ("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")
        ip_file = input("*** Please Enter the IP file name [example: ip.txt] *** : ")
        print ("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")
        #You can specifiy your IP file name like below and remove the above question ;)
	#ip_file = "ip.txt"
        try:
			#Opening the IP file
            selected_ip_file = open(ip_file, 'r')
            #Starting from the begining of the file
            selected_ip_file.seek(0)
            #Reading each line and craeting a list of IP addresses
            ip_list = selected_ip_file.readlines()
			#Close the IP file
            selected_ip_file.close()

        except IOError:
            print("\n*** the given IP fime name is wrong!! Please correct it and try againg!! ***" % ip_file)

        #IP Validity
        for ip in ip_list:
           try:
                ip = ip.rstrip()
                ipaddress.ip_address(ip)
                check_flag = True
                break

           except ValueError:
                print('\n*** At least one IP address was invalind !! ***\n')
                check_flag = False
                continue


        if check_flag == False:
            continue

        elif check_flag == True:
            break

    #Reachability
    print("\n*** Reachability are checking . . . ***\n")

    check_flag = False

    while True:
        for ip in ip_list:
            ping_reply = subprocess.call(['ping', '-c', '2', '-w', '2', '-q', '-n', ip], stdout = subprocess.PIPE)

            if ping_reply == 0:
                check_flag = True
                continue

            elif ping_reply == 2:
                print("\n***Device is unreachable *** : ", ip)
                check_flag = False
                break

            else:
                print("\n*** Faied ping to device *** : ", ip)
                check_flag = False
                break

        #Flag Checking
        if check_flag == False:
            print("*** Please re-check IP address list or device. ***\n")
            ip_is_valid()

        elif check_flag == True:
            print('\n*** Great !!! All devicese are reachable !!! ***\n\n')
            break

#Checking user file validity
def user_is_valid():
    global user_file

    while True:
        print ("\n# # # # # # # # # # # # # # # # # # # # # # # # # # # #\n")
        print ("*** Note : Usename and Password should be separated by comma , ***\n")
        user_file = input("*** Please Enter the Username & Password file name [example: id.txt ] *** : ")
        #You can specifiy your user/pass file name like below and remove the above question ;)
	#user_file = "username.txt"
        #OS.path will check the existence of given file!
	if os.path.isfile(user_file) == True:
            break
        else:
            print("\n ***There is no %s !! Please check it againg !! ***\n" % user_file)
            continue

try:
    ip_is_valid()

except KeyboardInterrupt:
    print("\n\n** Programm aborted by user!!!!!!! ***\n")
    sys.exit()

try:
    user_is_valid()

except KeyboardInterrupt:
    print("\n\n** Programm aborted by user!!!!!!! ***\n")
    sys.exit()


#SSHv2 connection
def open_ssh_conn(ip):
    global router_output
    try:
        #Reading the Username and Password file
        selected_user_file = open(user_file, 'r')
        selected_user_file.seek(0)

        #selecting the Usenrame
        username = selected_user_file.readlines()[0].split(',')[0]

        #Starting from the beginning of the file
        selected_user_file.seek(0)

        #selecting the Password
        password = selected_user_file.readlines()[0].split(',')[1].rstrip("\n")
        Router = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': Username,
            'password': passsword
            }

        net_connect = ConnectHandler(**Router)
        output = net_connect.send_command('show ip eigrp neighbors\n')

        selected_user_file.close()

        hostname1 = re.findall(r"(.+)#show ip eigrp neighbors", output)
        print ("\n\n")
        print ("**********************************************************")
        print ("Starint for hostname %s . . . . . \n" %hostname1[0])

	#Changing the type of output to makes it readable by readlines module!
        all_outputs = output.readlines()
        for line in all_outputs:
            line = line.strip()
            out = re.findall(r"^\d+\s{1,}(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).{55,65}\s{1,}(\d+)\s{1,}\d+", line)
            if out :
                print(" The Queue Count for neighbor %s is : %s  \n" %(out[0][0],out[0][1]) )
        print("\n *** Device %s Done !!! ***\n" %hostname1[0])
        print("**********************************************************")

        time.sleep(1)

    except NetMikoTimeoutException:
        print("*** Authentication invalid For %s" %ip)
        print("*** Please check the Usernmae and Password !!***\n\n")


#Threading
def create_threads():
    threads = []
    for ip in ip_list:
        th = threading.Thread(target = open_ssh_conn, args = (ip,))
        th.start()
        threads.append(th)

    for th in threads:
        th.join()

create_threads()
