from time import sleep

class Time_Table_Builder:
    def __init__(self):
        def s(txt, delay=0.04):
            for char in txt:
                print(char, end='', flush=True)
                sleep(delay)
            print()

        def welcome():
            s("Welcome To Time Table Builder 💪🏻")
            s("Here you can enter your activities and specify how much time you will spend on them.")
            s("Let's Get Started! ✨")

        def add_activities_and_time():
            try:
                s("\nSo Now\nEnter The Activities And Their Time\n")
                activities_and_time = []
                s("First enter how many activities you will do: ")
                no_of_activities = int(input(">> "))
                for i in range(no_of_activities):
                    s(f'Enter activity #{i+1} and time with a comma (e.g. study,4):')
                    activity_and_time = input(">> ")
                    try:
                        activity, time = [x.strip() for x in activity_and_time.split(",")]
                        float(time)  # Validate time is a number
                        activities_and_time.append((activity, time))
                        s(f"Activity {i+1} saved ✅\n")
                    except Exception:
                        s("Invalid format! Please enter as: activity,time (e.g. study,4)")
                        return

            except (ValueError, KeyboardInterrupt):
                s("\nInvalid Number! Try Again ❌")
                return

            # After collecting activities_and_time, print the time table
            if activities_and_time:
                s("\nYour TIME TABLE:")
                s("{:<20} | {:<10}".format("Activity", "Time (hrs)"))
                s("-" * 33)
                for activity, time in activities_and_time:
                    s("{:<20} | {:<10}".format(activity, time))
            else:
                s("No activities entered.")

        welcome()
        add_activities_and_time()

a = Time_Table_Builder()
