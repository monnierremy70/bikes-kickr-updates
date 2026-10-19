# BIKES KICKR — mises a jour

Depot public de diffusion des mises a jour signees preparees par Remy.

## Installer

Depuis la page locale du boitier : **Mise a jour > Verifier les mises a jour**, avec le Wi-Fi maison connecte. Installer a la fin de la seance, sans couper l alimentation.

Depuis une ancienne V3 : telecharger le fichier `.kcal` de son modele dans Releases, puis l envoyer depuis Mise a jour. Les reglages enregistres sont conserves.

- Heltec WiFi LoRa 32 V4 / ESP32-S3 : `BIKES_KICKR_heltec-v4.kcal`.
- ESP32-WROOM-32 / 32D / 32E classique, 4 Mo : `BIKES_KICKR_wroom32.kcal`.

Le boitier verifie le modele, la signature RSA-2048/SHA-256 et l empreinte du contenu. La V3.2 ne cherche que des versions stables plus recentes. Aucune cle ni connexion GitHub n est necessaire dans le boitier.

## Utiliser

Dans Zwift, choisir le boitier BIKES pour la puissance et la cadence, et le KICKR directement pour la resistance. Pour comparer avec deux Assioma DUO, utiliser le double canal L/R et selectionner chaque cote une fois : les selections sont memorisees. Pour un capteur total/unifie U, utiliser une seule source.

L historique conserve les cinq derniers essais dans le boitier. Les fichiers CSV sont telechargeables depuis Historique. Les trois paliers permettent de comparer l ecart a plusieurs puissances ; toute modification du pourcentage reste protegee par le mot de passe individuel fourni par Remy.

## Publication par Remy

Les seuls fichiers de firmware presents ici sont les paquets signes publics. Ne jamais ajouter une archive PROPRIETAIRE, PRIVE_REMY, SecurityConfig.h ou une cle privee.

Le workflow verifie les deux signatures avec `cle_publique.pem`, puis prepare une release en brouillon lorsque `release-request.json` est ajoute ou modifie. Apres les essais sur le materiel, publier ce brouillon depuis Releases. Une release encore en brouillon n est pas proposee aux membres.

Pour une future version : remplacer les deux paquets dans `release-files`, mettre a jour le numero dans `release-request.json` et les notes, puis creer le nouveau brouillon. Une release deja publiee ne sera pas ecrasee par le script.
