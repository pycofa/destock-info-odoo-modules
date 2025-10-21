# Test du Tracking Automatique de Submodule

Ce fichier est un test pour vérifier que git-cliff track correctement les commits du submodule addons/.

## Fonctionnement testé

- Commit créé dans le submodule addons/
- Pointeur mis à jour dans le repo parent
- Changelog généré automatiquement
- Commit du submodule visible dans section "Modifications dans les modules (addons/)"

## Résultat attendu

Ce commit devrait apparaître dans CHANGELOG.md avec le préfixe [addons].

---
*Test créé le 2025-10-21*
