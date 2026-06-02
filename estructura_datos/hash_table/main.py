from tablas import Tabla

def main():
    tam = 5
    mi_hash = Tabla(tam)
    mi_hash.agregar('Marcos', tam)
    mi_hash.agregar('Juan', tam) 
    mi_hash.agregar('Paulo', tam)
    mi_hash.agregar('Diana', tam)

    print("'Diana' esta en la tabla Hash:", mi_hash.buscar('Diana', tam))
    print("'index de Diana' en la tabla Hash:", mi_hash.indexado('Diana', tam))

if __name__ == '__main__':
    main()


