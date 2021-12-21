from turing.machine import TuringMachine


class WindowedWall:

    def __init__(self, len):
        self.initial_state = "init"
        self.accepting_states = ["final"],
        self.transition_function = {("init", "0"): ("stepA", "W", "R"),
                                    ("init", "1"): ("stepA", "W", "R"),
                                    ("init", " "): ("ends", " ", "L"),

                                    ("stepA", "0"): ("stepB", "G", "R"),
                                    ("stepA", "1"): ("stepBN", "G", "R"),
                                    ("stepA", " "): ("ends", " ", "L"),

                                    ("stepB", "0"): ("stepC", "G", "R"),
                                    ("stepB", "1"): ("stepAN", "W", "R"),
                                    ("stepB", " "): ("ends", " ", "L"),

                                    ("stepC", "0"): ("stepA", "W", "R"),
                                    ("stepC", "1"): ("stepCN", "W", "R"),
                                    ("stepC", " "): ("ends", " ", "L"),

                                    ("stepAN", "0"): ("stepC", "G", "R"),
                                    ("stepAN", "1"): ("stepB", "W", "R"),
                                    ("stepAN", " "): ("ends", " ", "L"),

                                    ("stepBN", "0"): ("stepA", "W", "R"),
                                    ("stepBN", "1"): ("stepC", "G", "R"),
                                    ("stepBN", " "): ("ends", " ", "L"),

                                    ("stepCN", "0"): ("stepB", "G", "R"),
                                    ("stepCN", "1"): ("stepA", "W", "R"),
                                    ("stepCN", " "): ("ends", " ", "L"),

                                    ("ends", "G"): ("final", "W", "N"),
                                    ("ends", "W"): ("final", "W", "N"),
                                    }
        self.final_states = {"final"}
        self.tape = self.build_tape(len)

    def build_tape(self, length):
        tape = "1" if length % 2 else "11"
        while len(tape) < length:
            tape = "0{}0".format(tape)
        return "{} ".format(tape)

    def build(self):
        t = TuringMachine(self.tape,
                          initial_state=self.initial_state,
                          final_states=self.final_states,
                          transition_function=self.transition_function)

        while not t.final():
            t.step()

        return t.get_tape()
