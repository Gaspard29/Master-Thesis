using System;
using System.IO;
using TMPro;
using UnityEngine;

public class PredictionUI : MonoBehaviour
{
    public TextMeshProUGUI predictionText;
    public event Action<string> OnPredictionReceived;
    private string predictionFile;
    void Start()
    {
        Debug.Log("PredictionDisplay started!");
        predictionFile = Path.Combine( Application.dataPath, "../Recordings/prediction.txt");
        predictionText.text = "Waiting...";
    }

    void Update()
    {
        if (!File.Exists(predictionFile))
            return;

        string prediction = File.ReadAllText(predictionFile).Trim();
        predictionText.text = prediction;
        OnPredictionReceived?.Invoke(prediction);
        File.Delete(predictionFile);
    }
}