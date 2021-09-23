#!/bin/bash

cmd=$(basename $0)

function disco() {
    df -h
    exit 0
}

function procesos() {
    ps aux
    exit 0
}

function usage() {

cat << EOF
Usage: ${cmd} [OPTION]...
Imprime el estado de los procesos o uso de disco dependiendo del parametro de entrada

Argumentos.
    -h, --help      Muestra esta ayuda
    -d, disco       Muestra el estado del disco
    -p, procesos    Muestra el estado de los procesos

EOF
}

while [[ $# -gt 0 ]]        # Cogemos las variables que vengan por linea de comando
#while [[ ! -z "$1" ]]      # Otra manera de hacer los mismo
do
    case $1 in
        -h|--help)
            showHelp=true
            shift
            ;;

        -d|--disco)
            shift
#           disco                       # Podemos ejecutar la funcion disco
            echo "Valor de -d: $1"      # O bien coger el valor del parametro introducido en la linea de comando
            ;;

        -p|--procesos)
            shift
#           procesos                    # Podemos ejecutar la funcion procesos
            echo "Valor de -p: $1"      # O bien coger el valor del parametro introducido en la linea de comando
            ;;      

         *)
            echo "${cmd}: Unrecognized option '$1'"
            echo "Try '${cmd} --help' for more info"
            exit 1
            ;;            
    esac
shift
done

if [[ "${showHelp}" = "true" ]]; then
    usage
    exit 0
fi

if [[ $# -eq 0 ]]; then
    echo "Introduzca un parametro al menos. Use -h para mostrar ayuda en pantalla"
    exit 0
fi