def get_action():

def get_info():
    t = input("Ingrese tipo de log: ")
    d = input("Ingrese fecha de creacion del log: ")
    m = input("Ingrese mensaje del log: ")

    return t, d, m


if __name__ == '__main__':
    salir = False
    while not salir:
        opt = get_action()
        if opt == 1:
            tip, date, msg = get_info()
            log = f"[{tip}] {date} {msg}"

            with open('logs.log', 'a') as f:
                f.write(log)
        elif opt == 2:
            salir = True