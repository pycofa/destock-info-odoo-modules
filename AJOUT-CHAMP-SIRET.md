# Affichage du numéro SIRET sur la page "Mon Compte"

## Question
Comment afficher le numéro de SIRET sur la page `/my/account` ?

## Réponse

### Fichier à modifier

**`/opt/odoo/user/website_sale_custom_destockinfo/views/portal_my_details_fields.xml`**

Ce fichier est le bon choix car :
- Il customise déjà la page `/my/account` (hérite de `portal.portal_my_details_fields`)
- Il contient déjà des modifications sur les champs du formulaire
- C'est le module dédié aux customisations e-commerce de Destock Info

### Modification à apporter

Ajouter un nouveau bloc XPath après le champ VAT Number existant :

```xml
<xpath expr="//input[@name='vat']/.." position="after">
    <div class="mb-3 col-xl-6">
        <label class="col-form-label label-optional" for="company_registry">SIRET</label>
        <input type="text" name="company_registry" class="form-control border-1"
               t-att-value="partner.company_registry" />
    </div>
</xpath>
```

### Fichier complet après modification

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <template id="portal_my_details_fields_inherit" inherit_id="portal.portal_my_details_fields">
        <xpath expr="//label[@for='vat']" position="after">
            <span class="fst-italic">(optional)</span>
        </xpath>

        <!-- NOUVEAU : Ajout du champ SIRET -->
        <xpath expr="//input[@name='vat']/.." position="after">
            <div class="mb-3 col-xl-6">
                <label class="col-form-label label-optional" for="company_registry">SIRET</label>
                <input type="text" name="company_registry" class="form-control border-1"
                       t-att-value="partner.company_registry" />
            </div>
        </xpath>

        <xpath expr="//div" position="before">
            <t t-if="infos_missing">
                <div class="alert alert-warning">Please enter your details to access the store.</div>
            </t>
        </xpath>
    </template>

</odoo>
```

### Explications techniques

#### Champ utilisé : `company_registry`
- **Modèle** : `res.partner`
- **Champ** : `company_registry`
- **Description** : Champ standard Odoo pour stocker le numéro d'enregistrement de l'entreprise (SIRET en France)
- **Type** : Char (texte)

#### Structure HTML
- **`<div class="mb-3 col-xl-6">`** : Container Bootstrap (margin-bottom + colonne de 6/12 sur XL screens)
- **`<label class="col-form-label label-optional">`** : Label avec classe Odoo pour champs optionnels
- **`<input class="form-control border-1">`** : Input avec classes Bootstrap + border-1 (cohérent avec les autres champs du module)
- **`t-att-value="partner.company_registry"`** : Attribut Qweb pour afficher la valeur depuis le modèle partner

#### Positionnement
- **`expr="//input[@name='vat']/.."`** : Sélectionne le div parent du champ VAT
- **`position="after"`** : Insère le nouveau champ SIRET juste après le champ VAT Number

### Autres modules concernés

Il existe un autre module qui customise cette page :

**`/opt/odoo/user/destockinfo_website/views/portal_views.xml`**
- Modifie uniquement les classes CSS des champs existants
- Ajoute `border-1` aux inputs pour le style
- N'ajoute pas de nouveaux champs

### Workflow de déploiement

Après la modification du fichier XML :

1. **Mettre à jour le module** :
   ```bash
   cd /opt/odoo
   ./odoo-bin -u website_sale_custom_destockinfo -d nom_base
   ```

2. **Ou mettre à jour tous les modules** :
   ```bash
   ./db update-all nom_base
   ```

3. **Vider le cache** (si nécessaire) :
   - Aller en mode développeur
   - Menu → Vider les caches

4. **Tester** :
   - Aller sur `mysite.com/my/account`
   - Vérifier que le champ SIRET apparaît après le champ VAT Number
   - Tester la sauvegarde d'un numéro SIRET

### Notes importantes

- Le champ `company_registry` est **optionnel** (classe `label-optional`)
- Aucune validation n'est ajoutée par défaut (le format SIRET n'est pas validé)
- Le champ est éditable même si des documents ont été émis (contrairement au VAT qui peut être verrouillé)
- Pour ajouter une validation du format SIRET, il faudrait modifier le contrôleur Python du module `portal`

### Alternative : Champ SIRET en read-only

Si vous souhaitez afficher le SIRET en lecture seule :

```xml
<xpath expr="//input[@name='vat']/.." position="after">
    <div class="mb-3 col-xl-6" t-if="partner.company_registry">
        <label class="col-form-label">SIRET</label>
        <div class="form-control-plaintext" t-out="partner.company_registry"/>
    </div>
</xpath>
```

---

*Documentation créée le 2025-10-20*
*Projet : Destock Info - Odoo 17.0*
