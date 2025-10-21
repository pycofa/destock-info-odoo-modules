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

## 📊 Analyse : Impact Submodule sur CHANGELOG.md

### Contexte

Ce fichier `AJOUT-CHAMP-SIRET.md` est situé dans le répertoire `addons/` qui est configuré comme **submodule Git** du projet principal.

### Repositories Concernés

1. **Repo principal** : [`devpycofa/destockinfo-docker`](https://github.com/devpycofa/destockinfo-docker)
   - Branch : `master`
   - Contient : Infrastructure Docker + configuration Odoo
   - CHANGELOG.md : ✅ Présent

2. **Repo submodule** : [`devpycofa/destock-info-odoo-modules`](https://github.com/devpycofa/destock-info-odoo-modules)
   - Branch : `main`
   - Contient : Modules Odoo custom (dont ce fichier)
   - CHANGELOG.md : ❌ Absent

### Vérification Effectuée (2025-10-21)

```bash
# État du CHANGELOG.md principal
✅ Local  : 49 lignes, 1 section [Unreleased] (propre)
⚠️  GitHub : 80+ lignes, 2 sections [Unreleased] (duplications)

# Raison du décalage
Commits locaux 54901b6..bc7d9a4 non encore synchronisés avec GitHub
```

### Comportement Confirmé : Submodule + CHANGELOG.md

#### ❌ Ce qui N'APPARAÎT PAS dans le CHANGELOG.md

Les commits **internes** au submodule `addons/` ne sont PAS trackés par git-cliff du repo principal :

```bash
# Exemple : Si vous commitez dans addons/
cd addons/
git add AJOUT-CHAMP-SIRET.md
git commit -m "docs: ajouter guide champ SIRET"
git push origin main
```

**Résultat** : Ce commit reste invisible pour le CHANGELOG.md du repo principal ❌

#### ✅ Ce qui APPARAÎT dans le CHANGELOG.md

Seul le commit de **mise à jour du pointeur de submodule** est visible :

```bash
# Dans le repo principal
git add addons
git commit -m "feat(modules): mettre à jour modules Odoo avec guide SIRET"
git push origin master
```

**Résultat dans CHANGELOG.md** :
```markdown
### Fonctionnalités
- Mettre à jour modules Odoo avec guide SIRET
```

### Solutions Recommandées

#### Option 1 : Messages de Commit Descriptifs (✅ Recommandé)

Quand vous mettez à jour le submodule, détaillez les changements :

```bash
git commit -m "feat(modules): ajouter champ SIRET sur page Mon Compte

Détails du submodule addons/ :
- Ajout de AJOUT-CHAMP-SIRET.md (guide technique)
- Modification de portal_my_details_fields.xml
- Nouveau champ company_registry affiché après VAT"
```

#### Option 2 : CHANGELOG.md Séparé dans Submodule

Créer un `addons/CHANGELOG.md` indépendant pour tracker les modifications du submodule.

#### Option 3 : Script Custom de Fusion

Script qui fusionne les changelogs des 2 repos (complexe, non recommandé).

### État Actuel du Projet

```
Repo principal (destockinfo-docker)
├── CHANGELOG.md          ← Trackage automatique via git-cliff ✅
├── .github/workflows/
│   └── changelog.yml     ← Workflow automatique ✅
├── scripts/
│   └── generate-changelog.sh ← Script de génération ✅
└── addons/               ← Submodule (modifications invisibles) ⚠️
    └── AJOUT-CHAMP-SIRET.md (ce fichier)
```

### ✅ Solution Implémentée (2025-10-21)

**État** : Le tracking automatique des commits du submodule est maintenant **ACTIVÉ** ✅

**Technologie** : git-cliff avec `recurse_submodules = true`

**Ce qui a été fait** :
1. ✅ Activation de `recurse_submodules` dans [cliff.toml](../cliff.toml#L39)
2. ✅ Modification du template pour afficher la variable `submodule_commits`
3. ✅ Ajout de `submodules: recursive` dans le workflow GitHub Actions
4. ✅ Test validé : les commits du submodule apparaissent automatiquement

**Résultat dans CHANGELOG.md** :
```markdown
## [Unreleased]

### Fonctionnalités
- Mettre à jour modules Odoo

### Modifications dans les modules (addons/)

#### Documentation
- [addons] Ajouter analyse impact submodule sur CHANGELOG.md
- [addons] Tidy AJOUT-CHAMP-SIRET.md formatting

#### Maintenance
- [addons] Exclude venv from git
```

**Fonctionnement** :
- Quand le pointeur du submodule est mis à jour dans le repo parent
- git-cliff **détecte automatiquement** tous les commits entre l'ancienne et la nouvelle révision
- Ces commits apparaissent dans une section dédiée **"Modifications dans les modules (addons/)"**
- Chaque commit est préfixé `[addons]` pour identification claire

**Documentation complète** :
- [CLAUDE.md](../CLAUDE.md#L200-L247) - Section "Tracking des Commits du Submodule"
- [CHANGELOG-AUTOMATION.md](../CHANGELOG-AUTOMATION.md#L153-L227) - Guide complet
- [cliff.toml](../cliff.toml) - Configuration technique

---

_Documentation créée le 2025-10-20_
_Analyse submodule ajoutée le 2025-10-21_
_Solution implémentée le 2025-10-21_
_Projet : Destock Info - Odoo 17.0_
