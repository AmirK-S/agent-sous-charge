# D1 · déploiement · Image Docker de l'expérience

**Statut :** fait le 21/10 (image publique, vérifiée sur une L40S Nebius).

## Ce qui est fait (21/10)
- `docker/Dockerfile` : base `nvidia/cuda:13.0.3-devel-ubuntu24.04` (nvcc pour la compilation des noyaux de vLLM), uv 0.11.25 et Python 3.12 géré par uv (en-têtes inclus), `/opt/venv` (vLLM 0.32.0, OpenTelemetry), `/opt/venv-tau` (τ³ au commit `96a3ef92`, depuis son verrou, extra knowledge, websockets 15.0.1, MCP 2.3.0, OpenTelemetry, OpenInference). Ni notre code, ni clé, ni poids du modèle.
- `.github/workflows/image.yml` : construction par GitHub Actions (place libérée sur le disque de la machine de GitHub), publication sur `ghcr.io/amirk-s/agent-sous-charge-gpu:vllm0.32.0-tau96a3ef92`. Deux constructions réussies le 21/10.
- `pod/installer-pod.sh` se branche sur `/opt` quand l'image est là (liens symboliques) ; **vLLM désormais épinglé à 0.32.0** (il ne l'était pas : 0.32.0 obtenue par chance à chaque installation).
- `pod/image-skypilot.yaml` : la recette qui lance une machine sur l'image.

## Trouvailles
- **vLLM 0.32.0 embarque PyTorch 2.13 compilé pour CUDA 13.0** (manifeste de la première construction). Nos recettes demandaient CUDA 12.8 au minimum : ça a marché par chance (pilotes 580, compatibles CUDA 13). Image passée sur CUDA 13.0, recettes annotées : hôte compatible CUDA 13.0 requis.
- L'API de GitHub ne permet pas de changer la visibilité d'un paquet ; l'accès de `gh` n'a pas non plus le droit `read:packages`.

## Vérification sur une carte (21/10, Nebius eu-north1, spot)
- Image rendue publique par Amir (accès anonyme vérifié : manifeste HTTP 200).
- **Location → vLLM qui répond : 24 min 48 s** : environ 10 min de téléchargement et d'ouverture de l'image, 10 min 47 s pour le script (essentiellement les 45 Go de poids), 2 min 13 s de chargement du modèle (contre 16 s le 19/10 : disque du conteneur plus lent). Versions affichées sur la machine : vLLM 0.32.0, τ³ `96a3ef92` ; cache KV 97 712 tokens, identique.
- **Conclusion honnête** : l'image donne un environnement identique partout (son but pour le pilote), pas un gain de temps : ce sont les téléchargements qui dominent. Shadeform ne lance pas d'image Docker via SkyPilot.
- **Suite proposée** : garder les poids sur un volume réseau du centre de données (Nebius) pour ne plus les retélécharger ; à chiffrer (stockage mensuel) avant de le créer.

## Ce qui était à faire (fait)
1. **Amir** : rendre le paquet public (un clic) : https://github.com/users/AmirK-S/packages/container/agent-sous-charge-gpu/settings → « Change visibility » → Public.
2. Vérifier sur une L40S : `sky launch -c d1 pod/image-skypilot.yaml -i 10 --down -y`, mesurer le temps entre la location et le premier `curl` qui répond (contre environ 20 min avec l'installation complète). Environ 0,30 $, dans le budget de 3 $ accordé le 21/10 (environ 1,90 $ restants).
