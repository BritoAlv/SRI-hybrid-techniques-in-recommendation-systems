# README

## Autores

- Álvaro Luis González Brito C-312 [@BritoAlv](https://github.com/BritoAlv)
- David Lezcano Becerra C-312 [@david-dlb](https://github.com/david-dlb)
- Javier Lima García C-312 [@limaJavier](https://github.com/limaJavier)

## Requerimientos

### Hardware

Para un correcto y fluido funcionamiento de la aplicación se requiere una RAM de mínimo 8GB. Puede que con 4GB, el sistema sea capaz de funcionar, pero no se han realizado pruebas bajo esas circunstancias, por lo cual no hay garantías.

### PYTHONPATH

Para permitir el uso de referencias entre distintos directorios que contienen scripts de Python, por favor, cambie su **PYTHONPATH** a `src`:

Como ejemplo, en un entorno *Linux* con bash, diríjase al archivo .bashrc y coloque la siguiente línea al final:

```bash
export PYTHONPATH="${PYTHONPATH}:/path to src directory/"
```

Para más detalles, por favor, diríjase al siguiente [enlace](https://www.geeksforgeeks.org/python-import-module-from-different-directory/).


### Xterm

Para un correcto funcionamiento del script `startup.sh` es necesario el programa **Xterm**.

Como ejemplo, puede instalarlo en un entorno *Debian* (*Linux distro*) de la siguiente manera:

```bash
sudo apt-get install xterm
```

Para Windows o IOS diríjase a los siguientes enlaces: 
- [xterm en Windows](https://stackoverflow.com/questions/4199594/xterm-on-windows) 
- [xterm en IOS](https://apps.apple.com/us/app/xterminal-ssh-terminal-shell/id1544728400)

### Paquetes

En el proyecto fueron utilizados una serie de paquetes de Python, por favor, ejecute el script de bash **packages.sh** para garantizar que los posee todos correctamente instalados.

```bash
bash packages.sh
```