from nmigen import *
from .types import *

class ImmGen(Elaboratable):
    # TODO: Allow for arbitrary width
    def __init__(self):
        self.instruction        = Signal(32)
        self.imm                = Signal(32)

    def elaborate(self, platform):
        m = Module()

        opcode =    self.instruction[0:7]
        immI   =    Cat(self.instruction[20:31], Repl(self.instruction[31], 21))
        immS   =    Cat(self.instruction[7:12], self.instruction[25:31], Repl(self.instruction[31], 21))
        immB   =    Cat(C(0), self.instruction[8:12], self.instruction[25:31], self.instruction[7],
                        Repl(self.instruction[31], 21))
        immU   =    Cat(Repl(C(0), 12), self.instruction[12:32])
        immJ   =    Cat(C(0), self.instruction[21:25], self.instruction[25:31], self.instruction[20],
                        self.instruction[12:20], Repl(self.instruction[31], 12))

        with m.Switch(opcode):
            with m.Case(Rv32iTypes.I_Jump.value, Rv32iTypes.I_Load.value, Rv32iTypes.I_Arith):
                m.d.comb += self.imm.eq(immI)
            with m.Case(Rv32iTypes.S.value):
                m.d.comb += self.imm.eq(immS)
            with m.Case(Rv32iTypes.B.value):
                m.d.comb += self.imm.eq(immB)
            with m.Case(Rv32iTypes.U_Add.value, Rv32iTypes.U_Load.value):
                m.d.comb += self.imm.eq(immU)
            with m.Case(Rv32iTypes.J.value):
                m.d.comb += self.imm.eq(immJ)

        return m
