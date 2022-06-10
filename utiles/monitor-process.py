import psutil
import time
from subprocess import check_output

processName = 'mc'                             # Definimos el nombre del proceso que buscamos

def get_pid(name):

    try:
        pid = check_output(["pidof","-s",name])
        return int(pid)

    except Exception:
        print("Proceso no encontrado")
        exit()

orig_pid = get_pid(processName)

while (True):

    for proc in psutil.process_iter():        # Buscamos por todos los procesos del sistema
        
        if processName.lower() in proc.name().lower():
            pinfo = proc.as_dict(attrs=['pid', 'name', 'create_time'])
            pid   = pinfo['pid']
            time.sleep(2)

            if pid != orig_pid:
                print("EL PID HA CAMBIADO, NUEVO PID: ", pid)
                print("SE ENVIA EMAIL DE ALERTA")
                exit()
            else:
                print("PID", orig_pid)