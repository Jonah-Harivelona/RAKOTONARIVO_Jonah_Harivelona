# Projet : GESTION HÔPITAL ET PHARMACIE

Ce projet Odoo regroupe quatre modules principaux permettant de gérer un hôpital et ses pharmacies affiliées.

## 📂 Structure des modules

- `hospital/`  
  Gestion des patients, médecins, symptômes, maladies, consultations, rondes infirmières, etc.

- `pharmacy/`  
  Gestion des médicaments, de leur stock, des commandes, des équivalences, etc.

- `hospital_pharmacy/`  
  Lien entre l’hôpital et les différentes pharmacies (transfert de prescriptions, historique, etc.).

- `hospital_staff/`  
  Gestion du personnel hospitalier (infirmiers, médecins, affectation, droits d’accès, etc.).

## ✅ Fonctionnalités principales

- **Hospital**  
  - Création et suivi des patients  
  - Enregistrement et suivi des symptômes et diagnostics  
  - Gestion des consultations (avec prescriptions associées)  
  - Rondes infirmières quotidiennes/hebdomadaires  
  - Export PDF des rondes de la semaine  

- **Pharmacy**  
  - Catalogue des médicaments  
  - Gestion du stock (entrées/sorties)  
  - Alertes de réapprovisionnement  
  - Traitement des commandes  
  - Gestion des équivalences pharmaceutiques  

- **Hospital_Pharmacy**  
  - Liaison entre une consultation et la pharmacie délivrant les médicaments  
  - Transfert automatique des prescriptions vers la pharmacie  
  - Historique des remises de médicaments aux patients  

- **Hospital_Staff**  
  - Gestion des employés (médecins, infirmiers, administrateurs)  
  - Attribution des rôles et droits d’accès  
  - Horaires de travail et planning de ronde pour le personnel soignant  

## 🚀 Installation et déploiement

1. **Cloner le dépôt**  
   ```bash
   git clone https://github.com/Jonah-Harivelona/RAKOTONARIVO_Jonah_Harivelona.git

2. Copier les modules dans l’arborescence Odoo
Par exemple, si ton Odoo local utilise le dossier odoo/addons/, fais :

bash
cp -r RAKOTONARIVO_Jonah_Harivelona/* /chemin/vers/ton/odoo/addons/

Vérifier que le fichier __manifest__.py de chaque module contient bien depends sur les modules requis (ex. base, web, mail, report, etc.).

Démarrer le serveur Odoo

bash
cd /chemin/vers/ton/odoo
./odoo-bin -d nom_de_ta_base --addons-path=/chemin/vers/ton/odoo/addons
Installer les modules dans l’interface

Connecte-toi à Odoo en tant qu’admin.

Va dans Applications, clique sur Mettre à jour la liste des modules, puis recherche :

hospital

pharmacy

hospital_pharmacy

hospital_staff

Pour chacun, clique sur Installer.

👤 Auteur
Nom : RAKOTONARIVO Jonah Harivelona
Formation : Electronique Système Informatique et Intelligence Artificielle

📜 Licence
Ce projet est sous licence LGPL-3.
