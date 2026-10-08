def get_bmi_category(bmi: float) -> str:
    """Returns the BMI category label based on the BMI value."""
    if bmi <= 16:
        return "Severely Underweight"
    elif bmi <= 18.5:
        return "Underweight"
    elif bmi <= 25:
        return "Healthy"
    elif bmi <= 30:
        return "Overweight"
    else:
        return "Severely Overweight"


def main():
    try:
        height_cm = float(input("Enter your height in centimeters: "))
        weight_kg = float(input("Enter your weight in kg: "))

        if height_cm <= 0 or weight_kg <= 0:
            print("Error: Height and weight must be positive values.")
            return

        height_m = height_cm / 100
        bmi = weight_kg / (height_m ** 2)

        print(f"\nYour Body Mass Index (BMI) is: {bmi:.2f}")
        print(f"Category: {get_bmi_category(bmi)}")

    except ValueError:
        print("Error: Please enter valid numeric values.")


if __name__ == "__main__":
    main()