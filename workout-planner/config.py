class Schedule:
    def __init__(self, init_schedule: dict[str:list]):
        if not init_schedule:
            self.schedule = {
            # key-value pair in the dictionary
            # with the key being an hour and value being a list of tasks that happen at that time
            '0': [None] * 60,
            '1': [None] * 60,
            '2': [None] * 60,
            '3': [None] * 60,
            '4': [None] * 60,
            '5': [None] * 60,
            '6': [None] * 60,
            '7': [None] * 60,
            '8': [None] * 60,
            '9': [None] * 60,
            '10': [None] * 60,
            '11': [None] * 60,
            '12': [None] * 60,
            '13': [None] * 60,
            '14': [None] * 60,
            '15': [None] * 60,
            '16': [None] * 60,
            '17': [None] * 60,
            '18': [None] * 60,
            '19': [None] * 60,
            '20': [None] * 60,
            '21': [None] * 60,
            '22': [None] * 60,
            '23': [None] * 60
            }
        else:
            self.schedule = init_schedule

    def add_task(self, task: str, start_time: str, end_time: str):
        """ Adds task to the schedule. Returns the schedule with the task added to the given time """

        start_hour = int(start_time[0:2]) # convert the start hour to int
        start_min = int(start_time[3:]) # convert the start min to int
        end_hour = int(end_time[0:2]) # convert the end hour to int
        end_min = int(end_time[3:]) # convert the end min to int
        duration_hour = end_hour - start_hour # calculate the diff in hours
        duration_min = end_min - start_min # calculate the diff in minutes
        total_duration = (duration_hour * 60) + duration_min # calculate and convert total duration in minutes

        if start_hour == end_hour and start_min > end_min:
            return "Error: Invalid time range for the task"

        stop = False
        hour = 0
        minute = start_min
        total_added = 0

        while not stop:
            if minute == 59:
                self.schedule[str(start_hour + hour)][minute] = task
                minute = 0
                hour += 1
            else:
                self.schedule[str(start_hour + hour)][minute] = task
                minute += 1


            total_added = total_added + 1

            if total_added == total_duration:
                stop = True

    def get_all_tasks(self):
        """ Returns a list of tuples with a task title and time period of the task """

        start_hour = 0
        start_minute = 0
        end_hour = 0
        end_minute = 0
        task = ""
        all_tasks = []

        for i in self.schedule:
            for j in range(len(self.schedule[i])):
                # checks for tasks in the given hour
                if self.schedule[i][j] is not None and task == "":
                    task = self.schedule[i][j]
                    start_hour = i # hour when the task starts
                    start_minute = j # specific minute when the task starts
                elif (task != "" and self.schedule[i][j] is None) or (self.schedule[i][j] is not None and self.schedule[i][j] != task and task != ""):
                    end_hour = i # assign the end hour
                    end_minute = j # assign the end minute

                    # if the digits are less than 10, put 0 before the digit
                    if int(start_hour) < 10:
                        start_hour = f"0{start_hour}"
                    if start_minute < 10:
                        start_minute = f"0{start_minute}"
                    if int(end_hour) < 10:
                        end_hour = f"0{end_hour}"
                    if end_minute < 10:
                        end_minute = f"0{end_minute}"

                    all_tasks.append((task, f"{start_hour} : {start_minute} - {end_hour} : {end_minute}"))

                    task = ""

        return all_tasks # return statement to get all the tasks



    def print_schedule(self):
        """ Used for debugging while working on the class Schedule """

        for i in self.schedule:
            print(i, self.schedule[i], "\n")



# debugging code
'''timesheet = Schedule(None)
timesheet.add_task("Lunch", "00:00", "02:23")
print("Created new object of the class Schedule")
new_obj = Schedule(timesheet.schedule)
new_obj.print_schedule()
print("Adding new task to the new object of the Schedule class")
new_obj.add_task("Class", "10:50", "12:05")
new_obj.print_schedule()

print("===========================")
print(new_obj.get_all_tasks())
new_obj.add_task('Physics', "13:00", "13:50")
print(new_obj.get_all_tasks())
new_obj.add_task('Something Else', "13:51", "14:00")
print(new_obj.get_all_tasks())'''

