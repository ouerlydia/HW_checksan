Avant toute chose, il faut vérifier l'insatallation du python minimum version  2.7.5 sur la machine avec  la commande : python --version , sinon il est nécessaire de l'installer.
Comamnde d'exécution : 
 
./hw_checksan.sh netapp nexus1 nexus2 ucs...

le script prend en arguments des fichiers d' entrée  qui doivent être dans le même répertoire courant : 

 fichier : Netapp
 fichier : nexsus1
 fichier : nexsus2
 fichiers : ucs

Rq : Faut pas changer le nom du dossier, les noms des scripts ni les noms des classes.
 
Exemple de construction du fichier netapp depuis les sorties de commandes suivantes séparées nécésserement par un saut de ligne :

site1-nfv01-clust01::> network interface show -data-protocol fcp -fields wwpn
vserver                   lif              wwpn
------------------------- ---------------- -----------------------
site1-nfv01-svm99-socleOSP svm99-FCoE_lif01 20:00:00:a0:98:ab:ea:4a
site1-nfv01-svm99-socleOSP svm99-FCoE_lif02 20:01:00:a0:98:ab:ea:4a
site1-nfv01-svm99-socleOSP svm99-FCoE_lif03 20:02:00:a0:98:ab:ea:4a
site1-nfv01-svm99-socleOSP svm99-FCoE_lif04 20:03:00:a0:98:ab:ea:4a
site1-nfv05-svm99-socleOSP svm99-FCoE_lif01 20:04:00:a0:98:ab:ea:4a
site1-nfv05-svm99-socleOSP svm99-FCoE_lif02 20:05:00:a0:98:ab:ea:4a
site1-nfv05-svm99-socleOSP svm99-FCoE_lif03 20:06:00:a0:98:ab:ea:4a
site1-nfv05-svm99-socleOSP svm99-FCoE_lif04 20:07:00:a0:98:ab:ea:4a

site1-nfv01-clust01::> lun igroup show -fields initiator
vserver                   igroup          initiator
------------------------- --------------- -----------------------------------------------
site1-nfv01-svm99-socleOSP ig_nfv01_bl0101 20:00:00:25:b5:00:00:2f,20:00:00:25:b5:00:00:5f
site1-nfv01-svm99-socleOSP ig_nfv01_bl0102 20:00:00:25:b5:00:00:0f,20:00:00:25:b5:00:00:3f
site1-nfv01-svm99-socleOSP ig_nfv01_bl0103 20:00:00:25:b5:00:00:1f,20:00:00:25:b5:00:01:ff
site1-nfv01-svm99-socleOSP ig_nfv01_bl0104 20:00:00:25:b5:00:01:df,20:00:00:25:b5:00:01:ef
site1-nfv01-svm99-socleOSP ig_nfv01_bl0105 20:00:00:25:b5:00:01:bf,20:00:00:25:b5:00:01:cf
site1-nfv01-svm99-socleOSP ig_nfv01_bl0106 20:00:00:25:b5:00:02:4e,20:00:00:25:b5:00:02:7e
site1-nfv01-svm99-socleOSP ig_nfv01_bl0107 20:00:00:25:b5:00:02:2e,20:00:00:25:b5:00:02:5e
site1-nfv01-svm99-socleOSP ig_nfv01_bl0108 20:00:00:25:b5:00:02:0e,20:00:00:25:b5:00:02:3e
site1-nfv01-svm99-socleOSP ig_nfv01_bl0201 20:00:00:25:b5:00:01:4f,20:00:00:25:b5:00:01:5f
site1-nfv01-svm99-socleOSP ig_nfv01_bl0202 20:00:00:25:b5:00:01:2f,20:00:00:25:b5:00:01:3f
20:00:00:25:b5:05:02:6e,20:00:00:25:b5:05:02:9e
site1-nfv05-svm99-socleOSP ig_nfv05_bl0504 20:00:00:25:b5:05:00:ae,20:00:00:25:b5:05:01:4e
site1-nfv05-svm99-socleOSP ig_nfv05_bl0505 20:00:00:25:b5:05:02:2e,20:00:00:25:b5:05:02:3e
site1-nfv05-svm99-socleOSP ig_nfv05_bl0506 20:00:00:25:b5:05:02:0e,20:00:00:25:b5:05:02:1e
site1-nfv05-svm99-socleOSP ig_nfv05_bl0507 20:00:00:25:b5:05:03:be,20:00:00:25:b5:05:03:de

site1-nfv01-clust01::> lun mapping show -fields igroup
vserver                   path                                       igroup
------------------------- ------------------------------------------ ---------------
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0101/lun_nfv01_bl0101 ig_nfv01_bl0101
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0102/lun_nfv01_bl0102 ig_nfv01_bl0102
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0103/lun_nfv01_bl0103 ig_nfv01_bl0103
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0104/lun_nfv01_bl0104 ig_nfv01_bl0104
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0105/lun_nfv01_bl0105 ig_nfv01_bl0105
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0106/lun_nfv01_bl0106 ig_nfv01_bl0106
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0107/lun_nfv01_bl0107 ig_nfv01_bl0107
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0108/lun_nfv01_bl0108 ig_nfv01_bl0108
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0201/lun_nfv01_bl0201 ig_nfv01_bl0201
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0202/lun_nfv01_bl0202 ig_nfv01_bl0202
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0203/lun_nfv01_bl0203 ig_nfv01_bl0203
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0204/lun_nfv01_bl0204 ig_nfv01_bl0204
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0205/lun_nfv01_bl0205 ig_nfv01_bl0205
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0206/lun_nfv01_bl0206 ig_nfv01_bl0206
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0207/lun_nfv01_bl0207 ig_nfv01_bl0207
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0208/lun_nfv01_bl0208 ig_nfv01_bl0208
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0301/lun_nfv01_bl0301 ig_nfv01_bl0301
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0302/lun_nfv01_bl0302 ig_nfv01_bl0302
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0303/lun_nfv01_bl0303 ig_nfv01_bl0303
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0304/lun_nfv01_bl0304 ig_nfv01_bl0304
site1-nfv01-svm99-socleOSP /vol/vol_lun_nfv01_bl0305/lun_nfv01_bl0305 ig_nfv01_bl0305
