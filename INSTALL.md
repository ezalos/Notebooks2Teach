# Setup installation

## Logiciels :
  - python3.8 (ou version supérieure): https://www.python.org/downloads/
    - il est important que python soit dans le PATH
    - il est important que l'installation puisse permettre la création de venv (sous Linux, c'est un second package à installer): https://docs.python.org/3/library/venv.html
  - vs-code: https://code.visualstudio.com/download 
  - git: notamment dans le but de pouvoir cloner des repository github

## Librairies pythons
Pour les librairies pythons bien installer librairies du fichier en pièce jointe

[all_requriements.txt](./all_requriements.txt)

## Pour les GPU:

Bien installer CUDA pour pouvoir utiliser les GPU NVDIA pour les exercices de Deep Learning du dernier jour.

Pour le verifier:
- Installer PyTorch : https://pytorch.org/get-started/locally/#start-locally
  - Pour mon ordinateur sous Linux c'est : `pip install torch`

- Puis, exécuter ce code avec python :

```py
import torch;

if torch.cuda.is_available() and torch.cuda.device_count() > 0:
    print("CUDA is available and has devices!")
else:
    print("CUDA is not available or has no devices!")
```

Si après exécution du script le programme output "`CUDA is available and has devices!`" alors c'est tout bon !
