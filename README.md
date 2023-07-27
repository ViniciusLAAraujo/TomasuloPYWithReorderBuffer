# Tomasulo With Reorder Buffer

## Description

The "Tomasulo With Reorder Buffer" is a simulator based on the Tomasulo algorithm with a reorder buffer. It follows the principles outlined in "Computer Architecture: A Quantitative Approach" by John L. Hennessy and David A. Patterson (Chapter 3.6 5th edition). The simulator allows you to load RISC-V instructions and displays the reorder buffer, reservation stations, and register bank at different states of execution.

**Screenshot of Console Output:**

![Example](https://github.com/ViniciusLAAraujo/TomasuloPYWithReorderBuffer/assets/90988825/0f068f41-95fd-4e77-b0e3-c16cd84b2184)

## Table of Contents

1. [Description](#description)
2. [About](#about)
3. [How to Use the Code](#how-to-use-the-code)
4. [How to Run](#how-to-run)
4. [How to Run](#how-to-run)
5. [Possible Improvements](#possible-improvements)

## About

The "Tomasulo With Reorder Buffer" simulator is a college project designed to understand the Tomasulo algorithm with a reorder buffer. Unlike traditional simulators, it was not required the calculation of actual values in instructions. Instead, the focus is on displaying the reorder buffer's execution states during the simulation. This approach provides a clearer understanding of instruction flow, data dependency management, and the benefits of speculative execution. The simulator serves as an educational tool to explore the concepts of modern computer architecture effectively.

### How to Use the Code

1. **Clone the Repository:**

2. **Prepare the Instruction File:**

Create a file named `instructions.txt` (`instructions02.txt` could also be found in the project, it servers as another example of instructions) in the root directory of the cloned repository. Place the RISC-V instructions in the file in the correct format. Supported instructions are: 'ADD', 'SUB', 'SLLI', 'SRLI', 'OR', 'BEQ', 'BNE', 'AND', 'LW', and 'LB'.

For more information on RISC-V instructions and their formats, refer to the official RISC-V guide [here](https://mark.theis.site/riscv/).

3. **Functional Units:**

The simulator supports the following functional units:

- 'MEM': Used for 'LW' and 'LB' instructions.
- 'ATM': Used for 'ADD'and 'SUB'
- 'LOG': Used for 'SLLI', 'SRLI', 'OR', 'BEQ', 'BNE' and 'AND'.


In the code, the reservation stations for each functional unit are instantiated using the UF variable. The UF vector of strings defines the names of the reservation stations for the corresponding functional units. Each reservation station can hold information related to the instructions being executed, such as opcode, source registers, destination register, and immediate values.

To ensure proper execution and prevent potential infinite loops during simulation, the code requires the creation of at least one reservation station for each functional unit. 3 examples of how to set this variable up can be found when it is istanciated in the code.

4. **Reorder Buffer Size:**

The size of the reorder buffer will be equal to the number of instructions in the `instructions.txt` file. All instructions are issued at the beginning, and then the reorder buffer's instructions are committed or wiped accordingly.

5. **Running the Simulation:**

- When you run the program, it will show you the current state of the reorder buffer, reservation stations, and register bank.
- After each state execution, the program will wait for any key pressed (except 0). Pressing any key will move the simulation one step.
- If you press 0, the program will execute all the states until all instructions are committed or wiped.

6. **Jump Execution:**

At the start of the program, the variable `JUMP` decides if 'BEQ' and 'BNE' instructions will execute the jump or not. When `JUMP` is set to 'JUMP', these instructions execute the jump, cleaning the instructions below them in the reorder buffer and reservation station. On the other hand, when JUMP is set to 'NJUMP', the flow continues as normal, and the instructions are processed without jumping. This is done because there is no requirement of producing values in this simulator.

## How to Run

1. Ensure you have Python 3 installed on your system.

- [Python Official Website](https://www.python.org/downloads/)

2. Clone this repository to your local machine.

3. Prepare the `instructions.txt` file with RISC-V instructions in the root directory of the cloned repository.

4. Open a terminal or command prompt and navigate to the repository's root directory.

5. Run the simulator using the following command:

 ```bash
 python tomasulo_with_reorderbuffer_compact.py
 ```

6. Follow the instructions displayed in the console to proceed with the simulation.

## Possible Improvements

1. Code Refactoring with Design Patterns.
2. Implement Reorder Buffer with a Queue of instructions.
3. Actual Value Calculation.