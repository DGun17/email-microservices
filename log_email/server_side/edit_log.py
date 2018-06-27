def get_action():
    opt = -1
    while opt < 1 or opt > 2:
        print("Menu.")
        print("1. Put log.")
        print("2. Exit.")
        opt = int(input("Seleccione opcion: "))

    return opt


def get_info():
    print("="*30)
    t = -1
    while t < 1 or t > 4:
        print("Log type")
        print("1. Debug.")
        print("2. Info.")
        print("3. Warning.")
        print("4. Error.")

        t = int(input("Select log type: "))

    ty_pe = ""
    if t == 1:
        ty_pe = "[Debug]"
    elif t == 2:
        ty_pe = "[Info]"
    elif t == 3:
        ty_pe = "[Warning]"
    elif t == 4:
        ty_pe = "[Error]"

    print("=" * 30)
    print("Datetime Log")

    anio = int(input("Year: "))
    day = int(input("Day: "))
    month = int(input("Month: "))

    date_time = str(anio)+"-"+str(day)+"-"+str(month)

    print("=" * 30)
    m = input("Log message: ")

    return ty_pe, date_time, m


if __name__ == '__main__':
    exited = False
    while not exited:
        option = get_action()
        if option == 1:
            tip, date, msg = get_info()
            log = f"{tip}_{date}_{msg}\n"

            with open('logs.log', 'a') as f:
                f.write(log)
        elif option == 2:
            exited = True

