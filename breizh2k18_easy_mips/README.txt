================================================================
########## chall description
================================================================
Titre: arm_now them all
Points: 250

Host: METTRE HOST ICI, Port: 4242
Download: ./vuln

================================================================
########## note pour kaluche et saxx
================================================================
Demarrer le challenge comme suit:
$ ./docker.sh
-------------------------

Mettre a disposition des joueurs le port 4242 et le binaire ./vuln.
Le flag est dans le chall et peut être reset avec le script ./regenerate_flag.sh
-------------------------

Pour tester si le challenge est bien setup faire:
$ nc host 4242
BabyHttp brought to you by @chaign_c
-------------------------

Pour tester si la vm est pwnable avec ma solution:
$ docker exec -it ctf bash
$ ./exploit.py
$ cat flag
...
-------------------------

Ceci est un challenge mipsel, exploit d'un stack overflow avec zero protection.
Pas d'aslr, pas de ssp, pas de nx...
Une erreur dans une pauvre boucle de urlencode,
    mais c'est un peu plus marrant a exploit qu'un strcpy.

La vm mipsel va démarer est bind le port 4242 du host,
  ce port doit être accéssible aux joueurs.
  Ca sera leur seul vecteur d'attaque, ils auront également
     accès au binaire et au code source.

Le docker doit être redémarré automatiquement toutes les 5 minutes,
   de cette manière elle reste clean.
