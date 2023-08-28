actions = [".exit", "select", "insert"]
es_ejecutable = True
while es_ejecutable:
    user_input = input("sql>")  # Espera la entrada del usuario
    user_input = user_input.lower()
    if any(user_input == action for action in actions):
        if user_input == ".exit":
            print("Terminado")
            es_ejecutable = False
        if user_input == "select":
            print("SELECT no implementado")
        if user_input == "insert":
            print("INSERT no implementado")
    else:
        print("Accion no reconocida")
