using UnityEngine;
using TMPro;

public class CoffeeShopManager : MonoBehaviour
{
    // Possible states
    public enum OrderState
    {
        Idle, ChoosingBeverage, ChoosingSize, AddOrRemove,
        ChoosingAddition, ChoosingIceAmount, ChoosingLocation
    }

    // Possible beverages

    public enum Beverage
    {
        None, BrewedCoffee, Tea,  Latte,
        Cappuccino, HotChocolate, Espresso
    }

    // Possible sizes
    public enum DrinkSize
    {
        None, Small, Medium, Large
    }

    // Possible locations
    public enum ConsumptionLocation
    {
        None, TakeAway, Bar, Table
    }

    // Current state / order

    public OrderState currentState = OrderState.Idle;
    public Beverage currentBeverage = Beverage.None;
    public DrinkSize currentSize = DrinkSize.None;

    public bool hasSugar = false;
    public bool hasMilk = false;
    public bool hasIce = false;
    public int iceAmount = 0;

    public ConsumptionLocation currentLocation = ConsumptionLocation.None;

    // UI
    [Header("Dialogue")]
    public TextMeshProUGUI dialogueText;

    [Header("Visuals")]
    public OrderVisuals orderVisuals;

    private PredictionUI predictionUI;


    
    // Start
    private void Start()
    {
        predictionUI = FindFirstObjectByType<PredictionUI>();

        if (predictionUI != null)
        {
            predictionUI.OnPredictionReceived += OnPredictionReceived;
        }

        ChangeState(OrderState.Idle);
    }


    private void OnDestroy()
    {
        if (predictionUI != null)
        {
            predictionUI.OnPredictionReceived -= OnPredictionReceived;
        }
    }



    // Receive a gesture prediction
    public void OnPredictionReceived(string prediction)
    {
        
        prediction = prediction.Trim().ToLower();

        Debug.Log("Gesture received: " + prediction + " | Current state: " + currentState);

        switch (currentState)
        {
            case OrderState.Idle:
                HandleIdle(prediction);
                break;

            case OrderState.ChoosingBeverage:
                HandleBeverage(prediction);
                break;

            case OrderState.ChoosingSize:
                HandleSize(prediction);
                break;

            case OrderState.AddOrRemove:
                HandleAddOrRemove(prediction);
                break;

            case OrderState.ChoosingAddition:
                HandleAddition(prediction);
                break;

            case OrderState.ChoosingIceAmount:
                HandleIceAmount(prediction);
                break;

            case OrderState.ChoosingLocation:
                HandleLocation(prediction);
                break;
        }
    }

 
    // STATE 0 : Idle
    private void HandleIdle(string prediction)
    {
        if (prediction == "order")
        {
            ResetOrder();
            ChangeState(OrderState.ChoosingBeverage);
        }
        else if (prediction == "pay")
        {
            ShowDialogue("You can pay at the bar");

            if (orderVisuals != null)
            {
                orderVisuals.ShowPayMachine();
            }
        }
    }



    // STATE 1 : Choosing beverage
    private void HandleBeverage(string prediction)
    {
        switch (prediction)
        {
            case "brewed coffee":
                currentBeverage = Beverage.BrewedCoffee;
                ChangeState(OrderState.ChoosingSize);
                break;

            case "tea":
                currentBeverage = Beverage.Tea;
                ChangeState(OrderState.ChoosingSize);
                break;

            case "latte":
                currentBeverage = Beverage.Latte;
                ChangeState(OrderState.ChoosingSize);
                break;

            case "cappuccino":
                currentBeverage = Beverage.Cappuccino;
                ChangeState(OrderState.ChoosingSize);
                break;

            case "hot chocolate":
                currentBeverage = Beverage.HotChocolate;
                ChangeState(OrderState.ChoosingSize);
                break;

            case "espresso":
                currentBeverage = Beverage.Espresso;

                // Espresso skips the size question
                ChangeState(OrderState.AddOrRemove);
                break;

            default:
                Debug.Log("Invalid beverage gesture: " + prediction);
                break;
        }
    }



    // STATE 2 : Choosing size
    private void HandleSize(string prediction)
    {
        switch (prediction)
        {
            case "small":
                currentSize = DrinkSize.Small;
                ChangeState(OrderState.AddOrRemove);
                break;

            case "medium":
                currentSize = DrinkSize.Medium;
                ChangeState(OrderState.AddOrRemove);
                break;

            case "large":
                currentSize = DrinkSize.Large;
                ChangeState(OrderState.AddOrRemove);
                break;

            default:
                Debug.Log("Invalid size gesture: " + prediction);
                break;
        }
    }


    // STATE 2.5 : Add or remove
    private void HandleAddOrRemove(string prediction)
    {
        if (prediction == "add")
        {
            ChangeState(OrderState.ChoosingAddition);
        }
        else if (prediction == "remove")
        {
            ChangeState(OrderState.ChoosingLocation);
        }
        else
        {
            Debug.Log("Invalid add/remove gesture: " + prediction);
        }
    }



    // STATE 3 : Choosing addition
    private void HandleAddition(string prediction)
    {
        if (prediction == "sugar")
        {
            hasSugar = true;
            ChangeState(OrderState.AddOrRemove);
        }
        else if (prediction == "milk")
        {
            hasMilk = true;
            ChangeState(OrderState.AddOrRemove);
        }
        else if (prediction == "iced")
        {
            hasIce = true;
            ChangeState(OrderState.ChoosingIceAmount);
        }
        else
        {
            Debug.Log("Invalid addition gesture: " + prediction);
        }
    }



    // STATE 4 : Choosing ice amount
    private void HandleIceAmount(string prediction)
    {
        switch (prediction)
        {
            case "quantity (1)":
                iceAmount = 1;
                ChangeState(OrderState.AddOrRemove);
                break;

            case "quantity (2)":
                iceAmount = 2;
                ChangeState(OrderState.AddOrRemove);
                break;

            case "quantity (3)":
                iceAmount = 3;
                ChangeState(OrderState.AddOrRemove);
                break;

            default:
                Debug.Log("Invalid ice amount gesture: " + prediction);
                break;
        }
    }



    // STATE 5 : Choosing location
    private void HandleLocation(string prediction)
    {
        switch (prediction)
        {
            case "take-away":
                currentLocation = ConsumptionLocation.TakeAway;
                ShowDialogue("Your order is ready to be taken on the bar.");
                FinishOrder();
                break;

            case "bar":
                currentLocation = ConsumptionLocation.Bar;
                ShowDialogue("Your order is ready on the bar");
                FinishOrder();
                break;

            case "table":
                currentLocation = ConsumptionLocation.Table;
                ShowDialogue("Your order is ready on the bar, feel free to take it at any table you want.");
                FinishOrder();
                break;

            default:
                Debug.Log("Invalid location gesture: " + prediction);
                break;
        }
    }

    // Change state
    private void ChangeState(OrderState newState)
    {
        currentState = newState;
        Debug.Log("STATE → " + currentState);
        switch (currentState)
        {
            case OrderState.Idle:
                ShowDialogue("Waiting for your order...");
                break;

            case OrderState.ChoosingBeverage:
                ShowDialogue("What would you like to order?");
                break;

            case OrderState.ChoosingSize:
                ShowDialogue("Which size would you like for your " + GetBeverageName() + "?");
                break;

            case OrderState.AddOrRemove:
                ShowDialogue("Would you like to add something?");
                break;

            case OrderState.ChoosingAddition:
                ShowDialogue("Would you like ice, sugar or milk with your " + GetBeverageName() + "?");
                break;

            case OrderState.ChoosingIceAmount:
                ShowDialogue("How many ice cubes would you like?");
                break;

            case OrderState.ChoosingLocation:
                ShowDialogue("Where would you like to drink your " + GetBeverageName() + "?");
                break;
        }
    }


    // Finish order
    private void FinishOrder()
    {
        Debug.Log("ORDER COMPLETE");

        Debug.Log(
            "Beverage: " + currentBeverage
            + " | Size: " + currentSize
            + " | Sugar: " + hasSugar
            + " | Milk: " + hasMilk
            + " | Ice: " + iceAmount
            + " | Location: " + currentLocation
        );

        if (orderVisuals != null)
        {
            orderVisuals.DisplayOrder(currentBeverage, currentSize, hasSugar,
                hasMilk, hasIce, iceAmount, currentLocation);
        }

        currentState = OrderState.Idle;
    }



    // Reset order
    private void ResetOrder()
    {
        currentBeverage = Beverage.None;
        currentSize = DrinkSize.None;

        hasSugar = false;
        hasMilk = false;
        hasIce = false;

        iceAmount = 0;

        currentLocation = ConsumptionLocation.None;
    }


    // --------------------------------------------------
    // Helpers
    // --------------------------------------------------

    private string GetBeverageName()
    {
        switch (currentBeverage)
        {
            case Beverage.BrewedCoffee:
                return "brewed coffee";

            case Beverage.Tea:
                return "tea";

            case Beverage.Latte:
                return "latte";

            case Beverage.Cappuccino:
                return "cappuccino";

            case Beverage.HotChocolate:
                return "hot chocolate";

            case Beverage.Espresso:
                return "espresso";

            default:
                return "drink";
        }
    }


    private void ShowDialogue(string message)
    {
        Debug.Log(message);

        if (dialogueText != null)
        {
            dialogueText.text = message;
        }
    }
}