import sys
sys.path.append("..")

from host_side.publisher import run as public


filename = 'logs.log'

if __name__ == '__main__':
    try:
        open(filename, 'r')
    except FileNotFoundError:
        with open(filename, 'w') as f:
            pass
    finally:
        file = open(filename, 'r')
        tam = len(file.readlines())
        file.close()

    while True:
        with open(filename, 'r') as f:
            info = f.readlines()
            if len(info) > tam:
                print(f"[*] File {filename} update ... run publisher")
                done = public()
                if done:
                    print("[*] Publisher run correctly")
                tam = len(info)



