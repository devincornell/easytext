#from subprocess import run
import os

if __name__ == '__main__':
    with open('test_commands.sh', 'r') as f:
        commands = [l for l in f.read().split('\n') if len(l) > 0]
    
    for comm in commands:
        print('trying command:', comm)
        #run(comm.split())
        os.system(comm)
        
