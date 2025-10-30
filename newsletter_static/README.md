# Module Newsletter Static Files

Module Odoo simple pour servir les images et fichiers statiques des newsletters.

## Structure

```
newsletter_static/
├── __manifest__.py           # Configuration du module
├── __init__.py              # Fichier Python requis
├── static/
│   └── newsletter/          # Placez vos images ici
│       ├── image1.jpg
│       ├── image2.png
│       └── ...
└── README.md
```

## Installation

### 1. Activer le mode développeur

Dans Odoo, allez dans **Paramètres** → En bas de page, cliquez sur **Activer le mode développeur**

### 2. Mettre à jour la liste des applications

- Allez dans **Applications** (menu principal)
- Cliquez sur les trois points (⋮) en haut à droite
- Cliquez sur **Mettre à jour la liste des Apps**
- Confirmez l'action

### 3. Installer le module

- Toujours dans **Applications**
- Utilisez la barre de recherche et tapez : `Newsletter Static Files`
- Cliquez sur le bouton **Installer**

**Alternative via ligne de commande :**

```bash
# Redémarrer Odoo pour détecter le nouveau module
sudo systemctl restart odoo

# Installer le module via odoo-bin (en tant qu'utilisateur odoo)
/opt/odoo/odoo-bin -c /opt/odoo/odoo.conf -d VOTRE_BASE_DE_DONNEES -i newsletter_static --stop-after-init
```

## Utilisation

### Ajouter des images

1. Copiez vos images dans le dossier :
   ```bash
   cp mon-image.jpg /opt/odoo/user/newsletter_static/static/newsletter/
   ```

2. Vérifiez les permissions :
   ```bash
   chown -R odoo:odoo /opt/odoo/user/newsletter_static/
   ```

### Accéder aux images

Les images seront accessibles via l'URL :

```
https://destock.info/newsletter_static/static/newsletter/VOTRE_FICHIER.jpg
```

**Exemples :**
- Image JPG : `https://destock.info/newsletter_static/static/newsletter/banniere.jpg`
- Image PNG : `https://destock.info/newsletter_static/static/newsletter/logo.png`
- PDF : `https://destock.info/newsletter_static/static/newsletter/catalogue.pdf`

### Utilisation dans les emails HTML

```html
<img src="https://destock.info/newsletter_static/static/newsletter/banniere.jpg" alt="Banniere" />
```

## Notes

- Pas besoin de redémarrer Odoo après avoir ajouté de nouvelles images
- Les fichiers statiques sont mis en cache par nginx pendant 24h
- Tous les types de fichiers sont supportés (images, PDF, CSS, JS, etc.)
- La taille maximale des fichiers est limitée par nginx (actuellement 5GB)

## Dépannage

### Le module n'apparaît pas dans la liste

```bash
# Redémarrer Odoo
sudo systemctl restart odoo

# Vérifier les logs
tail -f /var/log/odoo/odoo.log
```

### Les images ne s'affichent pas

1. Vérifier les permissions :
   ```bash
   ls -la /opt/odoo/user/newsletter_static/static/newsletter/
   ```

2. Vérifier que le fichier existe :
   ```bash
   ls /opt/odoo/user/newsletter_static/static/newsletter/
   ```

3. Tester l'accès direct via curl :
   ```bash
   curl -I https://destock.info/newsletter_static/static/newsletter/votre-image.jpg
   ```

### Vérifier que le module est installé

Dans Odoo :
- **Applications** → Retirer le filtre "Apps" → Chercher "Newsletter"
- Le module devrait apparaître avec un badge vert "Installé"
