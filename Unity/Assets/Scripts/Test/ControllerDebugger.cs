using UnityEngine;
using UnityEngine.XR;

public class ControllerDebugger : MonoBehaviour
{
    private InputDevice leftHand;
    private InputDevice rightHand;

    private bool leftFound = false;
    private bool rightFound = false;

    void Update()
    {
        // Try to find the left controller
        if (!leftHand.isValid)
        {
            leftHand = InputDevices.GetDeviceAtXRNode(XRNode.LeftHand);

            if (leftHand.isValid && !leftFound)
            {
                Debug.Log("Left controller found!");
                leftFound = true;
            }
        }

        // Try to find the right controller
        if (!rightHand.isValid)
        {
            rightHand = InputDevices.GetDeviceAtXRNode(XRNode.RightHand);

            if (rightHand.isValid && !rightFound)
            {
                Debug.Log("Right controller found!");
                rightFound = true;
            }
        }

        PrintController(leftHand, "LEFT");
        PrintController(rightHand, "RIGHT");
    }

    void PrintController(InputDevice device, string name)
    {
        if (!device.isValid)
            return;

        if (device.TryGetFeatureValue(CommonUsages.devicePosition, out Vector3 position))
        {
            Debug.Log($"{name} Position: {position}");
        }

        if (device.TryGetFeatureValue(CommonUsages.deviceRotation, out Quaternion rotation))
        {
            Debug.Log($"{name} Rotation: {rotation.eulerAngles}");
        }
    }
}