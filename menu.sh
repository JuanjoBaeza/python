#!/bin/bash

nombres='Kyle Cartman Kenny Stop'

PS3='Selecciona personaje: '

select nombre in $nombres
do
  if [ $nombre == 'Stop' ]
  then
    break
  fi
  echo Hola $nombre
done

echo Adios
