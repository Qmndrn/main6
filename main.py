import argparse
import json


def add_expense(budget, expenses, description, amount):
    if amount > budget:
        print(
            "Не можем добавить трату, кол-ва ваших денег не хватает, "
            "сначала укажите ваш точный бюджет"
        )
        return budget

    expenses.append({"description": description, "amount": amount})

    print(f"Добавлена трата: {description}, потрачено: {float(amount)}")
    return budget - amount


def get_total_expenses(expenses):
    return sum(expense["amount"] for expense in expenses)


def show_budget_details(first_budget, budget, expenses):
    print(f"Изнчально было денег: {first_budget}")
    print("Траты:")
    for expense in expenses:
        print(f"{expense['description']}: {expense['amount']};")
    print(f"Всего потрачено: {get_total_expenses(expenses)}")
    print(
        f"Добавлено в баланс: "
        f"{budget - first_budget + get_total_expenses(expenses)}"
    )
    print(f"Текущий баланс: {budget}")
    print()


def save_budget_details(filepath, first_budget, expenses, budget):
    data = {
        "изначальный баланс": first_budget,
        "траты": expenses,
        "текущий баланс": budget,
    }

    with open(f"{filepath}/data.json", "w") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)


def load_budget_data(filepath):
    try:
        with open(f"{filepath}/data.json", "r") as file:
            data = json.load(file)

        first_budget = data["изначальный баланс"]
        expenses = data["траты"]
        budget = data["текущий баланс"]

        return first_budget, expenses, budget

    except (FileNotFoundError, json.JSONDecodeError):
        return None, None, None


def update_budget(budget):
    new_budget = float(input("Введите новый бюджет: "))
    added_money = new_budget - budget
    budget = new_budget

    if new_budget >= 0:
        print(f"Добавлено денег: {added_money}")
    else:
        print(f"Убавлено денег: {added_money}")
    print(f"Обновленный бюджет: {budget}")
    print()
    return budget


def init_question(budget, first_budget, expenses, filepath):
    while True:
        print(
            """Что вы хотите сделать?:
1. Добавить траты
2. Показать оставшийся баланс
3. Обновить бюджет
4. История баланса
5. Очистить историю баланса
6. Выйти"""
        )

        answ = int(input("Ваш выбор: "))
        print()
        if answ == 1:
            reason = input("Введите описание траты (на что вы потратили деньги): ")
            spended = float(input("Введите количество потраченных денег: "))
            budget = add_expense(budget, expenses, reason, spended)
            print()
        elif answ == 2:
            print(f"Оставшийся баланс: {budget}")
            print()
        elif answ == 3:
            budget = update_budget(budget)
        elif answ == 4:
            show_budget_details(first_budget, budget, expenses)
        elif answ == 5:
            data = {
                "изначальный баланс": first_budget,
                "траты": [],
                "текущий баланс": first_budget,
            }
            with open(f"{filepath}/data.json", "w") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            budget = first_budget
            expenses = []
            print("История очищена")
            print()
        elif answ == 6:
            save_budget_details(filepath, first_budget, expenses, budget)
            print("Выход")
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--filepath", default="/home/mndrn/Рабочий стол/vscode/main6")
    args = parser.parse_args()
    filepath = args.filepath
    loaded = load_budget_data(args.filepath)
    first_budget, expenses, budget = loaded

    if first_budget is not None:
        init_question(budget, first_budget, expenses, filepath)
    else:
        budget = float(input("Введите ваш баланс: "))
        first_budget = budget
        expenses = []
        init_question(budget, first_budget, expenses, filepath)


if __name__ == "__main__":
    main()
