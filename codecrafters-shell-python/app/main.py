import sys
import subprocess
import os
def list_all_directories(searcg):
    root_dir='/'
    try:
        # Use os.walk to traverse the directory tree
        for dirpath, dirnames, filenames in os.walk(root_dir):
            for dirname in dirnames:
                full_path = os.path.join(dirpath, dirname)
                # print(full_path+"\n")
                if(full_path==searcg):
                    return 1
    except PermissionError:
        print("Permission denied. You might need elevated permissions to access some directories.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return 0


def find_command_in_path(command):
    # Get the PATH environment variable
    path_env = os.environ.get('PATH', '')
    # print(path_env)
    # print(os.pathsep)
    # Split the PATH into individual directories
    directories = path_env.split(os.pathsep)
    # print(directories)
    # print(directories)
    # Search for the command in each directory
    for directory in directories:
        command_path = os.path.join(directory, command)
        if os.path.isfile(command_path) and os.access(command_path, os.X_OK):
            return command_path
    
    # Return None if the command is not found
    return None

types=["echo","exit","type",'pwd','cd']
def main():
    # Uncomment this block to pass the first stage
    while(True):
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        s=input()
        if(s.startswith("type")):
            s=s.replace('type ',"")
            if(s in types):
                print(s+' is a shell builtin')
            elif(find_command_in_path(s)):
                print(find_command_in_path(s))
            else:
                print(s+': not found')
        elif(s.startswith("echo")):
            s=s.replace("echo ","")
            print(s)
        elif(s=="exit 0"):

            break
        elif(s=='pwd'):
            print(os.getcwd())
        elif(s.split(' ')[0]=='cd'):
            if(s[3]=='/'):
                di=s.split(' ')[1]
                # print(os.environ.get('PATH', '').split(os.pathsep))
                if list_all_directories(di):
                    os.chdir(di)
                
                else:
                    print('cd: '+di+': No such file or directory')
            elif s[3]=='~':
                curPath= os.path.expanduser("~")

                s=s[5:len(s)]
                s=s.split('/')
                for i in s:
                    curPath=curPath+'/'
                    curPath=curPath+i
                    while(curPath[-1]=='/'):
                        curPath=curPath[0:len(curPath)-1]
                if(list_all_directories(curPath)):
                    os.chdir(curPath)
                else:
                    print('cd: '+curPath+': No such file or directory')
                    
            else:
                s=s[3:len(s)]
                li=s.split('/')
                ar=[]
                curdi=os.getcwd().split('/')
                n=0
                for i in li:
                    if i=='..':
                        n=n+1
                    elif(i!='.'):
                        ar.append(i)
                dii='/'
                for i in range(0,len(curdi)-n):
                    dii=dii+curdi[i]
                    dii=dii+'/'
                for i in range(0,len(ar)):
                    dii=dii+ar[i]
                    dii=dii+'/'
                if dii[1]=='/':
                    dii=dii[1:len(dii)]
                while(dii[-1]=='/'):
                    dii=dii[0:len(dii)-1]
                # print(dii)
                if(list_all_directories(dii)):
                    os.chdir(dii)
                else:
                    print('cd: '+dii+': No such file or directory')

                
            
                
            
        elif (find_command_in_path(s.split(' ')[0])):
            r=find_command_in_path(s.split(' ')[0])
            # print(r)
            command_args=s.split(' ')[1:len(s.split(' '))]
            # print(r)
            # print(command_args)
            subprocess.run([r]+command_args, check=True)

        elif(s):
            print(s+": command not found")


if __name__ == "__main__":
    main()
