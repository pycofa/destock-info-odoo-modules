# Destock Info Custom Website Sale Module

Module Odoo 17 pour les customisations e-commerce de Destock Info.

## Description

Ce module étend les fonctionnalités de vente en ligne d'Odoo pour Destock Info avec :
- Customisation des cartes produits
- Styles SCSS personnalisés pour le shop
- Modification de l'affichage des catégories
- Gestion des filtres et de l'affichage des prix
- Interface adaptée pour la vente de matériel informatique reconditionné

## Installation

1. Copier le module dans le dossier `addons/` de votre installation Odoo
2. Redémarrer Odoo : `docker-compose restart odoo`
3. Activer le mode développeur
4. Mettre à jour la liste des modules
5. Installer le module "Destock custom website sale"

## Dépendances

- website_sale
- website_sale_only_available_attributes
- destockinfo_website

## Structure

```
website_sale_custom_destockinfo/
├── controller/          # Contrôleurs pour shop et portail
├── l18n/               # Traductions françaises
├── models/             # Modèles (product, categories)
├── security/           # Règles d'accès
├── static/
│   └── src/
│       ├── img/        # Images (wifi, bluetooth, ssd)
│       └── scss/       # Styles personnalisés
└── views/              # Templates XML
```

## Licence

Krafter Proprietary License - Copyright Krafter SAS <hey@krafter.io>

## Auteur

Krafter SAS - https://krafter.io