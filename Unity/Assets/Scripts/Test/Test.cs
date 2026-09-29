using UnityEngine;
using UnityEngine.XR;
using System.Collections.Generic;

public class XRDeviceSanityCheck : MonoBehaviour
{
    private float timer = 0f;

    void Update()
    {
        timer += Time.deltaTime;

        List<InputDevice> allDevices = new List<InputDevice>();
        InputDevices.GetDevices(allDevices);

        Debug.Log($"[{timer:F1}s] Found {allDevices.Count} XR devices total.");

        foreach (var device in allDevices)
        {
            Debug.Log($"  Device: {device.name}, Characteristics: {device.characteristics}, Valid: {device.isValid}");
        }
    }
}