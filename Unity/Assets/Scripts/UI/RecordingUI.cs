using TMPro;
using UnityEngine;

public class RecordingUI : MonoBehaviour
{
    public static RecordingUI Instance;

    public TMP_Text text;

    void Awake()
    {
        Instance = this;
    }

    public void UpdateDisplay(bool recording, int frames, float time)
    {
        if (recording)
        {
            text.text =
                $"Recording\n" +
                $"Frames : {frames}\n" +
                $"Time : {time:F2}s";
        }
        else
        {
            text.text =
                $"Idle\nFrames : {frames}";
        }
    }
}