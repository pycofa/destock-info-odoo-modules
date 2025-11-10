# Destockinfo reCAPTCHA Login & Signup

## Description

Ce module étend le module natif `google_recaptcha` d'Odoo pour ajouter le support de Google reCAPTCHA v3 sur les pages de connexion et d'inscription.

**Par défaut, le module `google_recaptcha` d'Odoo supporte uniquement :**
- Page de réinitialisation de mot de passe (`/web/reset_password`)

**Ce module ajoute le support pour :**
- Page de connexion (`/web/login`) ✅
- Page d'inscription (`/web/signup`) ✅

## Prérequis

1. **Module `google_recaptcha` installé et activé** (module natif Odoo 17)
2. **Clés Google reCAPTCHA v3 configurées** dans Paramètres > Général > Intégrations > Google reCAPTCHA
   - Site Key (clé publique)
   - Secret Key (clé secrète)

## Installation

1. Copier ce module dans `addons/`
2. Redémarrer Odoo
3. Mettre à jour la liste des applications (mode développeur)
4. Rechercher "destockinfo_recaptcha_login"
5. Cliquer sur "Installer"

## Configuration Google reCAPTCHA

Si ce n'est pas déjà fait :

1. Aller sur https://www.google.com/recaptcha/admin
2. Créer un nouveau site :
   - Type : **reCAPTCHA v3** (recommandé, invisible)
   - Domaines : `localhost`, `destock.info`, `*.destock.info`
3. Copier la **Site Key** et la **Secret Key**
4. Dans Odoo : Paramètres > Général > Intégrations > Google reCAPTCHA
   - Coller les clés
   - Sauvegarder

## Fonctionnement Technique

### Architecture

Le module ajoute deux widgets JavaScript :

**1. LoginCaptcha** pour la page `/web/login` :
- S'attache au formulaire `.oe_login_form`
- Intercepte l'événement `submit`
- Appelle l'API Google reCAPTCHA pour obtenir un token (action: "login")
- Injecte le token comme champ caché dans le formulaire
- Soumet le formulaire avec le token

**2. SignupCaptcha** pour la page `/web/signup` :
- S'attache au formulaire `.oe_signup_form`
- Même logique que LoginCaptcha
- Utilise l'action "signup" pour Google reCAPTCHA
- Validation backend via controller personnalisé

### Workflow Login

```
User submits login form
         ↓
LoginCaptcha intercept submit event
         ↓
Call Google reCAPTCHA API (action: "login")
         ↓
Get token (score 0.0-1.0)
         ↓
Inject <input name="recaptcha_token_response" value="token"/>
         ↓
Submit form to Odoo backend
         ↓
Odoo validates token with Google API
         ↓
If score >= threshold (default 0.5) → allow login
If score < threshold → deny login (bot detected)
```

### Workflow Signup

```
User submits signup form
         ↓
SignupCaptcha intercept submit event
         ↓
Call Google reCAPTCHA API (action: "signup")
         ↓
Get token (score 0.0-1.0)
         ↓
Inject <input name="recaptcha_token_response" value="token"/>
         ↓
Submit form to /web/signup (POST)
         ↓
DestockinfoAuthSignupHome controller validates token
         ↓
If valid → proceed with normal signup
If invalid → show error message and reject signup
```

### Fichiers

```
destockinfo_recaptcha_login/
├── __init__.py                              # Import controllers
├── __manifest__.py                          # Manifest Odoo (version 1.0.8)
├── README.md                                # Cette documentation
├── controllers/
│   ├── __init__.py                          # Import main
│   └── main.py                              # Controller signup avec validation reCAPTCHA
└── static/src/js/
    ├── login_recaptcha.js                   # Widget LoginCaptcha
    ├── login_recaptcha_start.js             # Démarrage widget login
    ├── signup_recaptcha.js                  # Widget SignupCaptcha
    └── signup_recaptcha_start.js            # Démarrage widget signup
```

## Validation

### Test Fonctionnel Login

1. Ouvrir `/web/login` dans le navigateur
2. Ouvrir DevTools (F12) > Console
3. Vérifier les logs `[Destock reCAPTCHA]` :
   ```
   🚀 Module login_recaptcha_start.js loaded on login page
   🔄 Attempting to start LoginCaptcha widget...
   ✅ Login form found, attaching LoginCaptcha widget...
   ✅ Widget successfully attached to login form
   ```
4. Essayer de se connecter avec identifiants valides
5. La connexion doit fonctionner normalement

### Test Fonctionnel Signup

1. Ouvrir `/web/signup` dans le navigateur
2. Ouvrir DevTools (F12) > Console
3. Vérifier les logs `[Destock reCAPTCHA]` :
   ```
   🚀 Module signup_recaptcha_start.js loaded on signup page
   🔄 Attempting to start SignupCaptcha widget...
   ✅ Signup form found, attaching SignupCaptcha widget...
   ✅ Widget successfully attached to signup form
   ```
4. Essayer de créer un compte
5. La création de compte doit fonctionner normalement

### Test Anti-Bot

Le reCAPTCHA v3 fonctionne de manière invisible. Google analyse le comportement de l'utilisateur et retourne un score (0.0 = bot, 1.0 = humain).

Pour tester la protection anti-bot :
1. Utiliser un script automatisé (curl, selenium, etc.)
2. Essayer de se connecter sans interaction humaine
3. Odoo devrait bloquer la tentative (score trop bas)

### Vérifier les Logs

```bash
# Vérifier que le module est bien chargé
docker-compose logs web | grep destockinfo_recaptcha_login

# Vérifier les requêtes reCAPTCHA
docker-compose logs web | grep -i recaptcha
```

## Troubleshooting

### reCAPTCHA ne s'affiche pas

**Symptôme :** Aucun changement visible sur `/web/login`

**Solutions :**
1. Vérifier que le module est bien installé :
   ```bash
   docker-compose exec -T db psql -U odoo -d destock.info -c \
     "SELECT name, state FROM ir_module_module WHERE name = 'destockinfo_recaptcha_login';"
   ```
   → Doit retourner `installed`

2. Vérifier que les assets sont bien chargés (DevTools > Network > login_recaptcha.js)

3. Régénérer les assets :
   ```bash
   ./scripts/regenerate-assets.sh
   docker-compose restart web
   ```

### Erreur "reCAPTCHA validation failed"

**Symptôme :** Impossible de se connecter, erreur reCAPTCHA

**Solutions :**
1. Vérifier que les clés reCAPTCHA sont correctes dans Paramètres
2. Vérifier que le domaine est bien ajouté dans Google reCAPTCHA Admin
3. Tester les clés manuellement :
   ```bash
   curl -X POST https://www.google.com/recaptcha/api/siteverify \
     -d "secret=VOTRE_SECRET_KEY" \
     -d "response=TEST_TOKEN"
   ```

### Erreur JavaScript dans la console

**Symptôme :** Erreur `ReCaptcha is not defined` ou similaire

**Solutions :**
1. Vérifier que `google_recaptcha` est bien installé
2. Vider le cache du navigateur (Ctrl+Shift+R)
3. Redémarrer Odoo

## Configuration Avancée

### Ajuster le seuil de validation

Par défaut, Odoo accepte les scores >= 0.5. Pour modifier :

1. Aller dans Paramètres > Technique > Paramètres système
2. Chercher la clé `recaptcha_min_score`
3. Modifier la valeur (0.0 - 1.0)
   - 0.0 = accepte tout (pas de protection)
   - 1.0 = accepte uniquement humains certains (très strict)
   - **0.5 = recommandé** (équilibre sécurité/UX)

### Désactiver reCAPTCHA temporairement

Pour tester sans reCAPTCHA :
1. Désinstaller le module `destockinfo_recaptcha_login`
2. Ou supprimer les clés dans Paramètres > Google reCAPTCHA

## Dépendances

- `google_recaptcha` (module natif Odoo 17)
- `web` (module natif Odoo)

## Licence

Copyright Krafter SAS <hey@krafter.io>
Krafter Proprietary License

## Auteur

Krafter SAS
https://krafter.io
