class LFSR:
    def __init__(self, initial_state: list, tap_positions: list):
        self.register = initial_state
        self.tap_positions = tap_positions

    def step(self):
        first_bit = 0
        for idx in self.tap_positions:
            first_bit = first_bit ^ self.register[idx - 1]

        last_bit = self.register[-1]

        self.register = self.register[:-1]
        self.register.insert(0, first_bit)

        return last_bit

