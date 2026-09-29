using UnityEngine;

public class OrderVisuals : MonoBehaviour
{
    // TAKE AWAY
    [Header("Take Away")]
    public GameObject takeAwayLarge;
    public GameObject takeAwayMedium;
    public GameObject takeAwaySmall;


    // COFFEE / LATTE / CAPPUCCINO
    [Header("Coffee")]
    public GameObject coffeeSmall;
    public GameObject coffeeMedium;
    public GameObject coffeeLarge;



    // TEA / HOT CHOCOLATE
    [Header("Empty Cups")]
    public GameObject emptyCupSmall;
    public GameObject emptyCupMedium;
    public GameObject emptyCupLarge;



    // OTHER OBJECTS
    [Header("Ingredients")]
    public GameObject jugMilk;
    public GameObject teapot;
    public GameObject plateSugar;
    public GameObject plateChocolate;
    public GameObject sugarCube;
    public GameObject chocolate;

    [Header("Espresso")]
    public GameObject espresso;

    [Header("Payment")]
    public GameObject payMachine;



    // ICE CUBES
    [Header("Coffee Small Ice")]
    public GameObject[] coffeeSmallIce;

    [Header("Coffee Medium Ice")]
    public GameObject[] coffeeMediumIce;

    [Header("Coffee Large Ice")]
    public GameObject[] coffeeLargeIce;

    [Header("Empty Cup Small Ice")]
    public GameObject[] emptyCupSmallIce;

    [Header("Empty Cup Medium Ice")]
    public GameObject[] emptyCupMediumIce;

    [Header("Empty Cup Large Ice")]
    public GameObject[] emptyCupLargeIce;



    // DISPLAY ORDER
    public void DisplayOrder(CoffeeShopManager.Beverage beverage, CoffeeShopManager.DrinkSize size, 
        bool hasSugar, bool hasMilk, bool hasIce, int iceAmount, CoffeeShopManager.ConsumptionLocation location)
    {
        // First remove everything from the previous order.
        // HideAll();

        
        // TAKE AWAY
        // If the customer wants takeaway, ONLY the appropriate takeaway object is displayed.
        if (location == CoffeeShopManager.ConsumptionLocation.TakeAway)
        {
            ShowTakeAway(size);
            return;
        }


        // BEVERAGE
        switch (beverage)
        {
            case CoffeeShopManager.Beverage.BrewedCoffee:
                ShowCoffee(size, false, hasIce, iceAmount);
                break;

            case CoffeeShopManager.Beverage.Cappuccino:
                ShowCoffee(size, true, hasIce, iceAmount);
                break;

            case CoffeeShopManager.Beverage.Latte:
                ShowCoffee(size, true, hasIce, iceAmount);
                break;

            case CoffeeShopManager.Beverage.Espresso:
                ShowObject(espresso);
                break;

            case CoffeeShopManager.Beverage.Tea:
                ShowEmptyCup(size, hasIce, iceAmount);
                ShowObject(teapot);
                break;

            case CoffeeShopManager.Beverage.HotChocolate:
                ShowEmptyCup(size, hasIce, iceAmount);
                ShowObject(plateChocolate);
                ShowObject(chocolate);
                break;
        }


        // ADDITIONS
        if (hasMilk)
        {
            ShowObject(jugMilk);
        }

        if (hasSugar)
        {
            ShowObject(plateSugar);
            ShowObject(sugarCube);
        }
    }


    // TAKE AWAY
    private void ShowTakeAway(CoffeeShopManager.DrinkSize size)
    {
        switch (size)
        {
            case CoffeeShopManager.DrinkSize.Small:
                ShowObject(takeAwaySmall);
                break;

            case CoffeeShopManager.DrinkSize.Medium:
                ShowObject(takeAwayMedium);
                break;

            case CoffeeShopManager.DrinkSize.Large:
                ShowObject(takeAwayLarge);
                break;
        }
    }



    // COFFEE
    private void ShowCoffee(CoffeeShopManager.DrinkSize size, bool cappuccinoOrLatte,
        bool hasIce, int iceAmount)
    {
        GameObject coffee = null;
        GameObject[] ice = null;

        switch (size)
        {
            case CoffeeShopManager.DrinkSize.Small:
                coffee = coffeeSmall;
                ice = coffeeSmallIce;
                break;

            case CoffeeShopManager.DrinkSize.Medium:
                coffee = coffeeMedium;
                ice = coffeeMediumIce;
                break;

            case CoffeeShopManager.DrinkSize.Large:
                coffee = coffeeLarge;
                ice = coffeeLargeIce;
                break;
        }

        if (coffee == null)
            return;

        ShowObject(coffee);

        // Coffee1 = brewed coffee
        // Coffee4 = cappuccino / latte
        Transform coffee1 = coffee.transform.Find("Coffee1");
        Transform coffee4 = coffee.transform.Find("Coffee4");

        if (coffee1 != null)
            coffee1.gameObject.SetActive(!cappuccinoOrLatte);

        if (coffee4 != null)
            coffee4.gameObject.SetActive(cappuccinoOrLatte);

        if (hasIce)
        {
            ShowIceCubes(ice, iceAmount);
        }
    }


    // TEA / HOT CHOCOLATE
    private void ShowEmptyCup(CoffeeShopManager.DrinkSize size, bool hasIce, int iceAmount)
    {
        GameObject cup = null;
        GameObject[] ice = null;

        switch (size)
        {
            case CoffeeShopManager.DrinkSize.Small:
                cup = emptyCupSmall;
                ice = emptyCupSmallIce;
                break;

            case CoffeeShopManager.DrinkSize.Medium:
                cup = emptyCupMedium;
                ice = emptyCupMediumIce;
                break;

            case CoffeeShopManager.DrinkSize.Large:
                cup = emptyCupLarge;
                ice = emptyCupLargeIce;
                break;
        }

        if (cup == null)
            return;

        ShowObject(cup);

        if (hasIce)
        {
            ShowIceCubes(ice, iceAmount);
        }
    }


    // ICE
    private void ShowIceCubes(GameObject[] iceCubes, int amount)
    {
        if (iceCubes == null)
            return;

        for (int i = 0; i < iceCubes.Length; i++)
        {
            if (iceCubes[i] != null)
            {
                iceCubes[i].SetActive(i < amount);
            }
        }
    }


    // HIDE EVERYTHING
    public void HideAll()
    {
        SetActive(takeAwayLarge, false);
        SetActive(takeAwayMedium, false);
        SetActive(takeAwaySmall, false);

        SetActive(coffeeSmall, false);
        SetActive(coffeeMedium, false);
        SetActive(coffeeLarge, false);

        SetActive(emptyCupSmall, false);
        SetActive(emptyCupMedium, false);
        SetActive(emptyCupLarge, false);

        SetActive(jugMilk, false);
        SetActive(teapot, false);

        SetActive(plateSugar, false);
        SetActive(plateChocolate, false);

        SetActive(sugarCube, false);
        SetActive(chocolate, false);

        SetActive(espresso, false);

        SetActive(payMachine, false);


        HideIceCubes(coffeeSmallIce);
        HideIceCubes(coffeeMediumIce);
        HideIceCubes(coffeeLargeIce);

        HideIceCubes(emptyCupSmallIce);
        HideIceCubes(emptyCupMediumIce);
        HideIceCubes(emptyCupLargeIce);
    }


    // PAYMENT
    public void ShowPayMachine()
    {
        // HideAll();
        ShowObject(payMachine);
    }


    // HELPERS
    private void ShowObject(GameObject obj)
    {
        if (obj != null)
        {
            obj.SetActive(true);
        }
    }

    private void SetActive(GameObject obj, bool value)
    {
        if (obj != null)
        {
            obj.SetActive(value);
        }
    }

    private void HideIceCubes(GameObject[] iceCubes)
    {
        if (iceCubes == null)
            return;

        foreach (GameObject ice in iceCubes)
        {
            if (ice != null)
            {
                ice.SetActive(false);
            }
        }
    }
}