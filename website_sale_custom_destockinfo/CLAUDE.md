# CLAUDE.md - Module website_sale_custom_destockinfo

Ce fichier fournit le contexte et les informations essentielles pour travailler sur ce module Odoo.

## Vue d'ensemble

Module de customisation e-commerce pour Destock Info, spécialisé dans la vente de matériel informatique reconditionné.

## Architecture des feature_block

### Concept
Les `feature_block` sont des éléments visuels qui affichent les caractéristiques techniques des produits (CPU, RAM, écran, etc.) sur les cartes produits.

### Structure actuelle

#### HTML (product_card_views.xml)
```xml
<div class="feature_block screen_block pe-0" t-if="product.screen_size_id">
    <dt class="dt_card">Size</dt>
    <dd class="dd_card" t-out="product.screen_size_id.name"/>
</div>
```

#### CSS (sale_card_style.scss)
- `.feature_block` : Container principal (text-align: center, min-width: 80px)
- `dt` : Label gris (#e5e7eb), uppercase, font-size: 10px
- `dd` : Valeur avec fond coloré, texte blanc, bold, font-size: 13px

### Types de feature_block et leurs couleurs
- `screen_block` : Orange (#ff951f) - Taille d'écran
- `cpu_block` : Violet (#bf5da7) - Processeur
- `ram_block` : Vert (#AAD94A) - Mémoire
- `hard_drive_type_block` : Bleu (#4a88d9) - Type de disque
- `os_block` : Bleu clair (#77B3E1) - Système d'exploitation
- `qual_block` : Rouge (#c13750) - Qualité d'écran
- `graphic_block` : Vert foncé (#49951e) - Carte graphique

## Modification en cours : Design avec icônes

### Objectif
Remplacer les encarts colorés (dt/dd) par un affichage en ligne avec icône + texte, inspiré du style newsletter.

### Nouvelle structure implémentée
```xml
<div class="feature_block screen_block" t-if="product.screen_size_id">
    <img src="/website_sale_custom_destockinfo/static/src/img/characteristic-icons/size.png" class="feature_icon me-1"/>
    <span class="feature_value" t-out="product.screen_size_id.name"/>
</div>
```

### Icônes disponibles
- **Icônes custom dans `static/src/img/characteristic-icons/`** :
  - `cpu.png` : Processeur
  - `ram.png` : Mémoire RAM
  - `storage.png` : Stockage/Disque dur
  - `os.png` : Système d'exploitation
  - `size.png` : Taille d'écran
  - `resolution.png` : Résolution/Qualité d'écran
  - `hdmi.png`, `dp.png`, `input-dvi.png`, `vga.png`, `usb-c.png` : Connectiques vidéo
- Font Awesome : Toujours disponible comme fallback
- Phosphor Icons : Via module `pyper_fonts_phosphor`

### Mapping des icônes
- `screen_block` → `size.png`
- `cpu_block` → `cpu.png`
- `ram_block` → `ram.png`
- `hard_drive_type_block` → `storage.png`
- `os_block` → `os.png`
- `qual_block` → `resolution.png`
- `video_input_block` → Détection intelligente du type (HDMI, DP, DVI, VGA, USB-C)

## Structure des fichiers

### Templates XML (`views/`)
- `product_card_views.xml` : Structure des cartes produits
- `shop_views.xml` : Layout de la page shop
- `product_page_views.xml` : Page détail produit
- `filters_views.xml` : Filtres de recherche
- `categories_home_shop.xml` : Affichage des catégories

### Styles SCSS (`static/src/scss/`)
- `sale_card_style.scss` : Styles des cartes produits et feature_block
- `shop_style.scss` : Styles généraux du shop

### Classes CSS importantes
- `.o_wsale_product_grid_wrapper` : Container principal des cartes
- `.card_product` : Carte produit individuelle
- `.feature_block` : Blocs de caractéristiques
- `.price_block_card` : Affichage des prix

## Conventions du module

### Classes CSS
- Utilisation de Bootstrap 5 (m-1, px-3, etc.)
- Classes BEM pour les composants custom
- Classes préfixées pour les types (screen_block, cpu_block, etc.)

### Templates Odoo
- Héritage via `inherit_id`
- Modifications via `xpath`
- Conditions avec `t-if`
- Affichage avec `t-out` ou `t-field`

### Modèles de données
Les caractéristiques proviennent du module `pyper_product_extend_features_it` :
- `product.screen_size_id`
- `product.processor_id`
- `product.ram_capacity_id`
- `product.hard_drive_type_id`
- `product.operating_system_id`
- etc.

## Workflow de développement

### Modification des styles
1. Éditer les fichiers SCSS
2. Redémarrer Odoo : `docker-compose restart odoo`
3. Vider le cache : Mode développeur → Vider les caches
4. Hard refresh : Ctrl+Shift+R

### Test des modifications
- Vérifier sur différentes tailles d'écran
- Tester avec différents types de produits
- Valider l'affichage mobile

## Notes importantes

- Le module dépend de `destockinfo_website` et `website_sale_only_available_attributes`
- Les assets SCSS sont chargés en `prepend` pour override les styles Odoo
- Le module est en `auto_install`

---
*Dernière mise à jour : 2025-07-17*