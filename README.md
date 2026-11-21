# AIML501 – Chest X-Ray Pneumonia Classification (Streamlit)

Streamlit app that compares two transfer-learned CNNs, **ResNet18** and **DenseNet121**, on chest X-ray images (NORMAL vs PNEUMONIA). Built for AIML-501 Residency Day 2.

## Files
| File | Purpose |
|---|---|
| `app.py` | Streamlit application |
| `requirements.txt` | Dependencies (CPU-only PyTorch) |
| `resnet18_pneumonia.pth` | Trained ResNet18 weights (Day 1) |
| `densenet121_pneumonia.pth` | Trained DenseNet121 weights (Day 1) |
| `model_comparison_results.csv` | Day 1 test-set metrics |

## Models
Both models start from ImageNet weights with frozen backbones and a new 2-class linear head, trained for 2 epochs on the Kaggle *Chest X-Ray Images (Pneumonia)* dataset with class-weighted cross-entropy. Preprocessing: resize to 224×224, grayscale to 3 channels, ImageNet normalization.

Day 1 test-set results:

| Model | Accuracy | Precision | Recall | Specificity | F1 | ROC-AUC |
|---|---|---|---|---|---|---|
| ResNet18 | 0.833 | 0.797 | 0.985 | 0.581 | 0.881 | 0.958 |
| DenseNet121 | 0.809 | 0.770 | 0.990 | 0.509 | 0.866 | 0.959 |

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Educational use only.** Not a medical device. Not for diagnosis, triage, or treatment. Do not upload identifiable patient images.
