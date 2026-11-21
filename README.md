# AIML501 – Chest X-Ray Pneumonia Classification (Streamlit)

Streamlit app that compares two transfer-learned CNNs, **ResNet18** and **DenseNet121**, on chest X-ray images (NORMAL vs PNEUMONIA). Built for AIML-501 Residency Day 2.

**Live app:** https://aiml501-pneumonia-detection.streamlit.app

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

## Robustness test (Step 14, run on the live app)
| Test image | Actual | ResNet18 | Prob. | DenseNet121 | Prob. |
|---|---|---|---|---|---|
| `test_images/NORMAL_test.jpeg` (original test set) | NORMAL | NORMAL | 80.6% | NORMAL | 62.9% |
| `test_images/PNEUMONIA_test.jpeg` (original test set) | PNEUMONIA | PNEUMONIA | 97.6% | PNEUMONIA | 96.8% |
| `test_images/ext_normal.jpg` (external, adult) | NORMAL | **PNEUMONIA** | 73.2% | NORMAL | 63.3% |
| `test_images/ext_pneumonia.jpg` (external, adult) | PNEUMONIA | PNEUMONIA | 97.4% | PNEUMONIA | 99.9% |
| `test_images/unrelated_dog.jpg` | Not an X-ray | **PNEUMONIA** | 99.7% | **PNEUMONIA** | 100.0% |

Screenshots are in `screenshots/`. Both models give a confident NORMAL/PNEUMONIA label to a dog photo: a 2-class softmax has no "not an X-ray" option.

Image credits: Kaggle *Chest X-Ray Images (Pneumonia)* test set; Wikimedia Commons: Mikael Häggström, *Normal posteroanterior (PA) chest radiograph* and *X-ray of lobar pneumonia* (CC0); Aciarium, *Search and Rescue Dog, Austrian Red Cross Perchtoldsdorf* (CC BY 4.0).

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

> **Educational use only.** Not a medical device. Not for diagnosis, triage, or treatment. Do not upload identifiable patient images.
