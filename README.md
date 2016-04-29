# PIR_Telegram
Alarme maison utilisant un Raspberry PI, un capteur pyroélectrique et le module de caméra, toutes les notifications sont envoyées sur Telegram.

##Prérequis :
Le script utilise la librairie [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) pour se connecter sur [Telegram](https://telegram.org/), veuillez y suivre les instructions pour l'installer.

Sur votre [Raspberry Pi](https://www.raspberrypi.org/), il faut installer gpac afin que les vidéos soient converties en mp4 pour être compatible avec Telegram.

    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo apt-get intall gpac
Le script est presque près à être utiliser. Vérifier que votre capteur pyroélectrique ainsi que la caméra soient bien connectés à votre Raspberry Pi, vérifier dans le script les commentaires, afin de le modifier à vos besoins.

##Utilisation :
Pour lancer le script :

    sudo python pir_telegram.py &
Si vous êtes sur la dernière version de Raspbian le sudo n'est pas obligatoire, vous pouvez enlever le & à la fin de la commande pour que le script ne soit pas lancer en arrière plan.

Vous n'avez plus qu'à parler à votre bot sur Telegram pour utiliser votre alarme maison.

-----
*J'utilise Python 2.7 sur une Raspbian Wheezy, pas certain que le script fonctionne sur Python 3.*
