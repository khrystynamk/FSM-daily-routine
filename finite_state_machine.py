"""
Finite state machine (FSM) for daily routine simulation.
"""

import random
from enum import Enum
from arrayqueue import ArrayQueue


class StateEnum(Enum):
    """
    Enum for defining student's states.
    """
    SLEEP = "Sleep"
    EAT = "Eat"
    BREAKDOWN = "Breakdown"
    CAT_HUGGING = "Cat Hugging"
    REST = "Rest"
    STUDY = "Study"
    STRETCH = "Stretch"
    TRAVEL = "Travel"


class Student:
    """
    Class for the UCU student (me).
    """

    def __init__(
        self,
        state: StateEnum,
        energy=100,
        happiness=50,
        deadlines=4,
        current_location="Home",
    ) -> None:
        self.state = state
        self.energy = energy
        self.happiness = happiness
        self.current_location = current_location
        self.deadlines = deadlines

    @staticmethod
    def change_location(self, energy_impact, happiness_impact, hour, *args):
        """
        Change location of the student.
        """
        self.current_location = args[0][0]
        hour += 2
        print(f"{hour}:00: I arrived at {self.current_location}")
        return (self, None, hour)

    @staticmethod
    def start_the_day(self, *args):
        """
        Starting the day.
        """
        weekday = random.randint(1, 5)
        if weekday in (1, 4, 5):
            print(
                "6:00: Yay, I’m going to make it in time to the university!\
 Even though I’m still exhausted…"
            )
            new_hour = 6
        elif weekday in (2, 3):
            print(
                "7:00: Hell no, I overslept!\
 Is there going to be at least one day, when I come in time?"
            )
            new_hour = 7

        return (
            self,
            State(
                student.change_location,
                self,
                -10,
                0,
                False,
                "Ukrainian Catholic University",
            ),
            new_hour,
        )

    @staticmethod
    def eat(self, energy_impact, happiness_impact, hour, *args):
        """
        Making a person eat something.
        """
        self.state = StateEnum.EAT
        self.energy += energy_impact
        self.happiness += happiness_impact
        if hour == 6:
            hour += 1
            print(
                f"{hour}:00: Granola for breakfast was perfect,\
 but it's so hard to start working..."
            )
        elif hour in range(14, 18):
            hour += 1
            print(
                f"{hour}:00: Quick lunch boosts mood and energy.\
 Now it's time to meet all the deadlines."
            )
        elif hour in range(18, 22):
            hour += 1
            print(f"{hour}:00: Finally, the last meal of the day!")

        return (self, None, hour)

    @staticmethod
    def hug_the_cat(self, energy_impact, happiness_impact, hour, *args):
        """
        A random event of hugging a cat.
        """
        probability = random.uniform(0, 1)
        hour += 1
        if probability > 0.3 and (self.energy <= 40 and self.happiness <= 40):
            self.state = StateEnum.CAT_HUGGING
            self.energy += energy_impact
            self.happiness += happiness_impact
            print(
                f"{hour}:00: There is nothing better to boost my mood than a fluffy 6 kilogram cat."
            )
        else:
            print(f"{hour}:00: I guess the cat is not really happy to see me today :(")
        return (self, None, hour)

    @staticmethod
    def stretching(self, energy_impact, happiness_impact, hour, *args):
        """
        A random event of stretching.
        """
        probability = random.uniform(0, 1)
        if probability > 0.5 and (self.energy >= 20 and self.deadlines == 0):
            self.state = StateEnum.STRETCH
            self.energy += energy_impact
            self.happiness += happiness_impact
            hour += 1
            print(
                f"{hour}:00: What a great time I had during the workout! \
Worn out, but definitely pleased."
            )
        else:
            print(
                f"{hour}:00: I don't think I have enough energy and\
 time to do some stretching today..."
            )
        return (self, None, hour)

    @staticmethod
    def study(self, energy_impact, happiness_impact, hour, *args):
        """
        The studying event.
        """
        study_to_do = self.deadlines
        for _ in range(study_to_do):
            self.deadlines -= 1
            self.energy += energy_impact
            hour += 2
        self.happiness += happiness_impact
        print(f"{hour}:00: All the studying is done!")

        return (self, None, hour)

    @staticmethod
    def breakdown(self, energy_impact, happiness_impact, hour, *args):
        """
        The breakdown event.
        """
        self.state = StateEnum.BREAKDOWN
        hour += 1
        self.energy += energy_impact
        self.happiness += happiness_impact
        print(
            f"{hour}:00: I don't think I can keep up with all the deadlines and studying,\
 I'm desperate!"
        )
        return (self, None, hour)

    @staticmethod
    def rest(self, energy_impact, happiness_impact, hour):
        """
        
        """
        if hour in range(18, 22) and self.deadlines == 0:
            self.state = StateEnum.REST
            self.energy += energy_impact
            self.happiness += happiness_impact
            hour += 2
        return (self, None, hour)

    @staticmethod
    def end_the_day(self, energy_impact, happiness_impact, hour, *args):
        """
        Ending the day.
        """
        self.state = StateEnum.SLEEP
        hour += 1
        print(
            f"{hour}:00: This exhausting day has come to an end\
 and I'm absolutely delighted to be in my warm and comfy bed."
        )
        hour = 0
        return (self, None, hour)


class State:
    """
    Class for the state.
    """

    def __init__(
        self,
        handler,
        person: Student,
        energy_impact,
        happiness_impact=0,
        terminal=False,
        *args,
    ) -> None:
        self.energy_impact = energy_impact
        self.happiness_impact = happiness_impact
        self.terminal = terminal
        self.handler = handler
        self.person = person
        self.arguments = args

    def execute_handler(self, hour):
        if self.handler:
            return self.handler(
                self.person,
                self.energy_impact,
                self.happiness_impact,
                hour,
                self.arguments,
            )
        return (self.person, None, hour)


class FSM:
    """
    Finite state machine (FSM) for daily routine simulation.
    """

    HOUR = 0
    EVENT_QUEUE = ArrayQueue()
    VISITED_UNI = False
    ADDED_HOME_ACTIVITIES = False

    def add_event(self, event: State):
        """
        Adding event to the queue of events.
        """
        self.EVENT_QUEUE.add(event)

    def run_routine(self, person: Student):
        """
        Method to run the daily routine.
        """
        while not self.EVENT_QUEUE.isEmpty():
            event: State = self.EVENT_QUEUE.pop()
            if event is not None:
                (person, next_event, hour) = event.execute_handler(self.HOUR)

                if event.terminal:
                    break

                self.HOUR = hour

            if next_event is not None:
                self.add_event(next_event)

            if person.current_location == "Ukrainian Catholic University":
                if not self.VISITED_UNI:
                    if person.deadlines >= 3:
                        self.add_event(State(Student.breakdown, person, -10, -40))
                    self.add_event(State(Student.study, person, -30, -20))
                    self.add_event(State(Student.eat, person, 20, 10))
                    self.add_event(
                        State(Student.change_location, person, -10, 0, False, "Home")
                    )
                self.VISITED_UNI = True

            if (
                person.current_location == "Home"
                and self.VISITED_UNI
                and not self.ADDED_HOME_ACTIVITIES
            ):
                self.add_event(State(Student.hug_the_cat, person, 0, 20))
                self.add_event(State(Student.stretching, person, -30, 30))
                self.add_event(State(Student.eat, person, 30, 10))
                self.ADDED_HOME_ACTIVITIES = True

            if self.HOUR in range(21, 25) and person.deadlines == 0:
                self.add_event(State(person.end_the_day, person, 100, 50, True))
        print("-----------------------------")
        print(
            f"Finally, this long day has ended and by the end of the day my energy\
 level had dropped to {person.energy} and level of happiness is {person.happiness}."
        )


routine = FSM()
student = Student(StateEnum.SLEEP)
routine.add_event(State(Student.start_the_day, student, 0))
routine.add_event(State(Student.eat, student, 30, 10))
routine.run_routine(student)
