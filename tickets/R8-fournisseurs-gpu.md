# R8 · recherche · Fournisseurs de GPU

**Statut :** résolu le 18/10 (sous-agent ; plusieurs prix viennent d'agrégateurs, disponibilité à reconfirmer avant location)

## Résolution
| Fournisseur | L40S | H100 PCIe | H100 SXM |
|---|---|---|---|
| RunPod Community | 0,79 $ (rupture le 18/10) | 1,99 $ | 2,69 $ |
| RunPod Secure | 1,09 $ | 2,89 $ | 3,99 $ |
| Vast.ai | ~0,80 $ | ? | dès 1,79 $ |
| Verda (Finlande) | 0,87 $ spot ; 1,74 $ | ? | 2,13 $ spot ; 4,25 $ |
| Scaleway (Paris) | 1,40 €/h officiel | ~4,20 € (tiers) | 3,23 $ |
| OVHcloud | 1,80 $ (tiers) | ~2,99 $ (tiers) | ? |
| Nebius | 1,55 $ ; préemptible 0,74 $ | ? | 4,50 $ ; préemptible dès 0,79 $ |
| Lambda | ? | 3,29 $ | 3,99 à 4,29 $ (rupture) |

Sources : runpod.io/pricing, lambda.ai/pricing, nebius.com/prices, scaleway.com/fr/tarifs/gpu (18/10/2026) ; computeprices.com et spheron.network pour le reste.

- Pièges : pas de spot pendant un test de charge (interruptions) ; hôtes non vérifiés de qualité variable ; ruptures fréquentes aux prix bas ; aucune donnée sur la variabilité entre machines identiques, à mesurer nous-mêmes avant chaque campagne.
- Recommandation : RunPod Secure ou Vast.ai (hôtes vérifiés) pour la reproductibilité ; Scaleway Paris (L40S 1,40 €/h) comme option européenne, surcoût d'environ 30 à 60 % sur la L40S, soit 80 à 160 $ de plus par GPU sur 250 h.
- Révision de l'estimation de budget : au prix fiable (1,09 $/h et non 0,79), 100 à 250 h par GPU sur deux GPU font environ 220 à 550 $ sur L40S.
