vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("VLAN corresponde a Rango Normal")
elif 1006 <= vlan <= 4094:
    print("VLAN corresponde a Rango Extendido")
else:
    print("Número de VLAN no válido")
