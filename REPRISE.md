# Reprise : où on en est (23/10/2026)

> À lire après `CLAUDE.md`, avant `CARTE.md`. Réécrit à chaque fin de séance, pour qu'une nouvelle session reprenne sans rien redemander. Les décisions du cadrage du 18/10 sont dans le tableau « Ce qui est déjà tranché » de la carte.

## Pourquoi ce projet existe (les mots d'Amir)
- Être payé 800 €/j et plus : maîtriser le métier d'ingénieur logiciel au-delà de ses expériences passées, et tenir une discussion technique serrée (montée en charge, déploiement, observabilité, coût, latence).
- Apprendre en faisant, puis le raconter : Amir doit être **propriétaire** du projet, capable de l'expliquer face caméra et de distinguer le signal du bruit.
- Une vidéo divertissante pour CTO et tech leads, inspirée de « How Many Users Can a $12 Server Handle? » et de sa suite communautaire (optimisations successives, chaque compromis expliqué).
- Réaliste pour un grand groupe européen : d'où la banque, l'hébergement souverain, et des modèles non chinois.

## État au 23/10/2026 (à réécrire à chaque fin de séance)
- **Fait** : P1 (prototype complet) ; D1 (image Docker publique) ; G4, G5, G6 tranchés ; P0 partie 1 jouée la nuit du 22/10 ([rapport](mesures/P0-nuit-22-10.md)) ; G11 revérifié depuis les fichiers le 23/10.
- **Ticket en cours : [G11](tickets/G11-qualite-au-repos.md)**, décision présentée, **en attente de la reformulation d'Amir**. Preuves : aucun modèle d'une carte publié sur banking_knowledge, Mistral Large y fait 6,4 % ; 5 de nos 7 réussites sont des transferts à un humain (le diagnostic « goulot = recherche » est retiré) ; le critère « −5 points » a 36 à 63 % de puissance à 10-25 % de repos. Recommandation : changer de banc en gardant la banque (TauIndianBankBench, NPCI, MIT), repli τ² retail ou telecom ; banking_knowledge en séquence descriptive.
- **Rien ne tourne.** Aucune machine louée. Dépense totale du GPU à ce jour : environ 10 dollars. Séance du 23/10 : 0 dollar.

## Prochaine action précise
Obtenir la reformulation d'Amir sur G11. Si l'option 1 est actée : vérification gratuite de TauIndianBankBench (code, version du harnais τ², compatibilité avec notre serveur MCP, lecture de tâches). Rien ne se loue avant.

## Infrastructure (au 23/10)
- **Location** : SkyPilot 0.14.1 multi-fournisseurs (Nebius, Lambda, RunPod, Shadeform, Vast) ; recettes dans `pod/*-skypilot.yaml`. Nebius demande une reconnexion d'Amir par navigateur quand son jeton expire.
- **Image** : `ghcr.io/amirk-s/agent-sous-charge-gpu:vllm0.32.0-tau96a3ef92` (CUDA 13.0 : hôte compatible requis).
- **Clés** (hors dépôt) : `~/.config/openrouter/env`, `~/.lambda_cloud/`, `~/.runpod/config.toml`, `~/.shadeform/`, `~/.nebius/`. Le serveur MCP RunPod de Claude Code est hors service (clé révoquée) : passer par SkyPilot ou l'API REST.
- **τ³ en local** : `~/.cache/agent-sous-charge/tau2-bench` (commit 96a3ef92), hors du Bureau.
- **Client simulé** : `openrouter/openai/gpt-6-luna` (G5).

## Comment travailler avec Amir sur ce projet
- En français, court, une question à la fois avec une recommandation ; pas de tiret long.
- Toute commande qui attend une saisie (clé, mot de passe) ne marche pas depuis la zone de message de l'app : utiliser une fenêtre de saisie masquée (comme `pod/configurer-cle-runpod.sh`) ou le panneau Terminal.
- Toute dépense : la montrer avant, avec son prix, et attendre son accord.
- Avant chaque nouvelle tâche, il apprécie la version « plus profonde, pas plus grosse » (ce qu'un pro ferait, la matière brute, les méthodes, la preuve externe) puis le prompt réécrit.
- Il veut un journal signal / bruit : chaque décision, et ce qu'on a écarté en route.
