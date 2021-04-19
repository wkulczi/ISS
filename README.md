# ISS
Kolejny projekt na PUT. 

Wszystkie opisy i tłumaczenia dostępne na YouTracku

#### Backend - uruchamianie

Będąc w folderze głównym (ISS):
Linux/Mac:
```
$ export FLASK_APP=issProject
$ export FLASK_ENV=development
$ flask run
```
Windows (cmd):
```
> set FLASK_APP=issProject
> set FLASK_ENV=development
> flask run
```
Windows (powershell):
```
> $env:FLASK_APP = "issProject"
> $env:FLASK_ENV = "development"
> flask run
```

Albo użyj konfiguracji PyCharm:
![Konfiguracja](https://i.ibb.co/C8MQFTP/conf.png)

#### Frontend - uruchamianie
Please zainstaluj [WSL](https://www.windowscentral.com/install-windows-subsystem-linux-windows-10) :(, za każdym razem gdy uruchamiasz Node.js na Windowsie ginie jedna foka.
![Foka](https://i.pinimg.com/originals/df/eb/5a/dfeb5a442a78652da010c25a29630494.jpg)

Node: v15.11.0 ([Instalacja Node tutorial](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-18-04) lub [Node Version Manager](https://github.com/nvm-sh/nvm)))

Yarn v1.22.10 ([Instalacja Yarn](https://classic.yarnpkg.com/en/docs/install/#debian-stable))

Po zainstalowaniu wszystkiego przejdź do folderu `/frontend` i wywołaj 
```
yarn dev
```