Writeup forensic # by Notfound

>>> mmls  76b0c868ab7397cc6a0c0a1e107e3079.raw 
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000000127   0000000128   Unallocated
002:  000:000   0000000128   0000198783   0000198656   NTFS / exFAT (0x07)
003:  -------   0000198784   0000204799   0000006016   Unallocated

On voit une partition NTFS qui commence à l'offset 128 et termine à l'offset 198783. Du coup j'utilise dd (cc @saxx)

>>> dd if=76b0c868ab7397cc6a0c0a1e107e3079.raw of=ntfs_part.raw bs=512 skip=128 count=198783
198783+0 enregistrements lus
198783+0 enregistrements écrits
101776896 octets (102 MB, 97 MiB) copiés, 1,89805 s, 53,6 MB/s

>>> file ntfs_part.raw 
ntfs_part.raw: DOS/MBR boot sector, code offset 0x58+2, OEM-ID "-FVE-FS-", sectors/cluster 8, reserved sectors 0, Media descriptor 0xf8, sectors/track 63, heads 16, hidden sectors 128, FAT (32 bit), sectors/FAT 8160, serial number 0x0, unlabeled; NTFS, sectors/track 63, physical drive 0x1fe0, $MFT start cluster 393217, serial number 02020454d414e204f, checksum 0x41462020

Je remarque rapidement le flag -FVE-FS- qui me fait souvenir d'un bitlocker. Du coup, bah go bitlocker2john :

>>> bitlocker2john -i ntfs_part.raw >> hash_bitlocker
>>> cat hash_bitlocker
...
User Password hash:
$bitlocker$0$16$6946a04b89585fea10b4817c9a3917c9$1048576$12$c0297b4057a9d50103000000$60$724b0b483ed7b6c3cef283d34830adb006f1ae732a39b2eccf84959b53a1735fb9cb2f67e88282ccf5b1a04cc0a74d84778097b2db1cb689a70bfd79
Hash type: User Password with MAC verification (slower solution, no false positives)
$bitlocker$1$16$6946a04b89585fea10b4817c9a3917c9$1048576$12$c0297b4057a9d50103000000$60$724b0b483ed7b6c3cef283d34830adb006f1ae732a39b2eccf84959b53a1735fb9cb2f67e88282ccf5b1a04cc0a74d84778097b2db1cb689a70bfd79
Hash type: Recovery Password fast attack
$bitlocker$2$16$b95e642d93ec40c16a7a77b87bc3cadf$1048576$12$c0297b4057a9d50106000000$60$60f1218fafabac6be20ecf31565d4e15f3e0ef3b5650e6d30535f7bd08eed2c6dc0992252927140339b470b794a6f2338b07369d1ec9e969d677b262
Hash type: Recovery Password with MAC verification (slower solution, no false positives)
$bitlocker$3$16$b95e642d93ec40c16a7a77b87bc3cadf$1048576$12$c0297b4057a9d50106000000$60$60f1218fafabac6be20ecf31565d4e15f3e0ef3b5650e6d30535f7bd08eed2c6dc0992252927140339b470b794a6f2338b07369d1ec9e969d677b262

J'ai laissé tourner à peine 1 minute, puis j'ai mount le volume avec dislocker :

>>> john --show hash_bitlocker 
?:password
?:password
>>> mkdir mountpoint_bitlocker
>>> dislocker -V ntfs_part.raw  -v -u  mountpoint_bitlocker/
Enter the user password: 
>>> mount |grep bitlock
dislocker on /home/notfound/CHALLENGES/FIC2020/FIC/mountpoint_bitlocker type fuse.dislocker (rw,nosuid,nodev,relatime,user_id=1000,group_id=100)

On a maintenant une image disk "non chiffrée". Donc forensic classique :

>>> fls dislocker-file 
r/r 4-128-4:    $AttrDef
r/r 8-128-2:    $BadClus
r/r 8-128-1:    $BadClus:$Bad
r/r 6-128-4:    $Bitmap
r/r 7-128-1:    $Boot
d/d 11-144-4:    $Extend
r/r 2-128-1:    $LogFile
r/r 0-128-1:    $MFT
r/r 1-128-1:    $MFTMirr
r/r 9-128-8:    $Secure:$SDS
r/r 9-144-11:    $Secure:$SDH
r/r 9-144-5:    $Secure:$SII
r/r 10-128-1:    $UpCase
r/r 3-128-3:    $Volume
r/r 39-128-1:    flag.txt
d/d 35-144-6:    System Volume Information
-/r * 64-128-2:    ls
-/r * 65-128-2:    fic.zip
-/r * 66-128-2:    f1.zip
-/r * 67-128-2:    f2.zip
-/r * 68-128-2:    f3.zip
-/r * 69-128-2:    f4.zip
V/V 256:    $OrphanFiles

Le fichier fic.zip a l'air intéressant, affichons le :

>>> icat dislocker-file 66-128-2 | icat dislocker-file 66-128-2  | gzip -dc 
https://gist.github.com/bosal43833/3e815abc3f92e45963a8aafc8acfe411

Pwned. Merci au revoir.
