# Gesture Interaction in Virtual Reality

This repository contains the code and resources developed for my Master's thesis, **"Gesture Interaction in Virtual Reality"**.

---

# Python

The `Python` folder contains the scripts used for recording gestures, preparing the recorded data, training machine learning models, and performing gesture prediction.

## Recording New Gestures

To record new gesture samples from a participant, use:

```text
experiment_manager.py
```

Run it with:

```bash
python experiment_manager.py
```

This script manages the recording experiment and allows new gesture performances from a participant to be recorded.

The recorded data is then stored in its raw form and can subsequently be processed using `prepare_data.py`.

---

## Preparing the Data

The file:

```text
prepare_data.py
```

is used to transform the recorded data from its **raw format** into the format required by the machine learning models.

The general workflow is:

```text
Raw gesture recordings
        ↓
prepare_data.py
        ↓
Prepared dataset
        ↓
Machine learning training
```

This step should be performed before training a model on newly recorded data.

---

## Training an SVM

The file:

```text
train_model.py
```

is used to train a Support Vector Machine (SVM) on the prepared gesture data.

The general workflow is:

```text
Prepared data
      ↓
train_model.py
      ↓
Trained SVM
      ↓
Saved model
```

The trained models are stored in the `saved_models` folder.

---

## CNN Training

The repository also contains a notebook used for training the Convolutional Neural Network (CNN). It was used with kaggle.

The notebook contains the code required to:

* Load the prepared gesture dataset.
* Train the CNN model.
* Evaluate the model.
* Save the trained CNN model.

The resulting model can then be used for gesture prediction in the VR environment.

---

## Saved Models

The `Python/saved_models` folder contains the trained machine learning models used by the project.

Different models can be stored separately so that they can be selected and tested in the prediction system.

---

## Gesture Prediction

The file:

```text
predictor.py
```

is used to predict the gesture being performed by the user in the VR environment.

The general workflow is:

```text
VR Controller
      ↓
Gesture performed
      ↓
Unity records movement
      ↓
Predictor
      ↓
Machine Learning Model
      ↓
Predicted gesture
      ↓
Unity interaction
```

The predictor loads a previously trained model from `saved_models` and uses the recorded controller data to classify the gesture.

---

## Unity Scripts

The main scripts used by Unity are located in:

```text
Unity/Assets/Scripts/
```

These scripts are responsible for the main functionality of the VR application, including:

* Gesture recording
* User interface (UI)
* Application management
* Communication between different components of the VR environment
* Management of the gesture recognition process

---

## Unity

The `Unity` folder is a complete Unity project and should be opened directly using Unity Hub.

---

# Author

**Gaspard Jaumotte**

**Master's Thesis:**
*Gesture Interaction in Virtual Reality*