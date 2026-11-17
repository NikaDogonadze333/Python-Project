from storage import load_tasks, save_tasks
from models import Task

def add_task(tasks):
    title = input("შეიყვანეთ დავალების სათაური: ").strip()
    if not title:
        raise ValueError("სათაური არ შეიძლება იყოს ცარიელი")

    description = input("შეიყვანეთ აღწერა: ").strip()
    deadline = input("შეიყვანეთ დედლაინი (მაგ: 2026-12-01): ").strip()
    priority = input("შეიყვანეთ პრიორიტეტი (Low, Medium, High): ").strip()
    project = input("შეიყვანეთ პროექტის სახელი (ან დატოვეთ ცარიელი): ").strip()
    
    if not project:
        project = "General"

    new_task = Task(title, description, deadline, priority, project)
    tasks.append(new_task)
    save_tasks(tasks)
    print("დავალება წარმატებით დაემატა!")

def list_tasks(tasks):
    if not tasks:
        print("დავალებები არ მოიძებნა.")
        return

    for i, task in enumerate(tasks):
        print(f"\n--- დავალება #{i} ---")
        print(f"სათაური: {task.title}")
        print(f"აღწერა: {task.description}")
        print(f"დედლაინი: {task.deadline}")
        print(f"პრიორიტეტი: {task.priority}")
        print(f"პროექტი: {task.project}")
        print(f"სტატუსი: {task.status}")

def change_status(tasks):
    list_tasks(tasks)
    if not tasks:
        return

    index = int(input("აირჩიეთ დავალების ნომერი სტატუსის შესაცვლელად: "))
    if 0 <= index < len(tasks):
        print("აირჩიეთ ახალი სტატუსი: 1. pending, 2. in-progress, 3. completed")
        choice = input("არჩევანი: ").strip()
        status_map = {"1": "pending", "2": "in-progress", "3": "completed"}
        
        if choice in status_map:
            tasks[index].update_status(status_map[choice])
            save_tasks(tasks)
            print("სტატუსი წარმატებით შეიცვალა!")
        else:
            print("არასწორი არჩევანი!")
    else:
        print("არასწორი ინდექსი!")

def delete_task(tasks):
    list_tasks(tasks)
    if not tasks:
        return

    index = int(input("აირჩიეთ წასაშლელი დავალების ნომერი: "))
    if 0 <= index < len(tasks):
        removed = tasks.pop(index)
        save_tasks(tasks)
        print(f"დავალება '{removed.title}' წაიშალა!")
    else:
        print("არასწორი ინდექსი!")

def main():
    tasks = load_tasks()
    while True:
        print("\n--- Task Manager მენიუ ---")
        print("1. დავალების დამატება")
        print("2. ყველა დავალების ნახვა")
        print("3. დავალების სტატუსის შეცვლა")
        print("4. დავალების წაშლა")
        print("5. გასვლა")

        choice = input("აირჩიეთ მოქმედება: ").strip()

        try:
            if choice == "1":
                add_task(tasks)
            elif choice == "2":
                list_tasks(tasks)
            elif choice == "3":
                change_status(tasks)
            elif choice == "4":
                delete_task(tasks)
            elif choice == "5":
                break
            else:
                print("არასწორი არჩევანი!")
        except ValueError as e:
            print(f"შეცდომა: {e}")

if __name__ == "__main__":
    main()