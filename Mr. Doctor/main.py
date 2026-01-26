from time import sleep

def s(txt, delay=0.02):
    for c in txt:
        print(c, end='', flush=True)
        sleep(delay)
    print()

def main():
    s("Welcome To Mr. Doctor!")
    s("Here you can save like in which disease which Medicine should be taken!")
    s("Let's Get Started!")
    name = input("\nName of Medicine>> ")
    t_tu_s = input("\nTube(Tu), Tablet(Ta) or Syrup(S)>> ")
    disease = input(f"\nIn which Disease {t_tu_s} {name} Should be Used>> ")
    s("\n\n\tSaved ✅ Successfuly")
    s(f"\nName -> {name}")
    s(f"Tube, Talblet or Syrup -> {t_tu_s}")
    s(f"Disease -> {disease}")
    s("\n\n\tThanks for Using This Programme... GoodByee...")
    with open("Medicines.txt", "a") as f:
        f.write(f"Name -> {name}\nTube, Tablet or Syrup -> {t_tu_s}\nDisease -> {disease}\n\n")
    exit()

main()
