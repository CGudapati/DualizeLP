NAME          TESTDUAL
OBJSENSE
    MAX
ROWS
 N  RHS1
 E  X1
 L  X2
 E  X3
 L  X4
 L  X5
 E  X6
 L  X7
 L  X8
 L  X9
 L  X10
COLUMNS
    LIM1      RHS1      20.0
    LIM1      X1        1.0
    LIM1      X3        2.0
    LIM1      X4        3.0
    LIM1      X7        2.0
    LIM1      X8        3.0
    LIM1      X9        9.0
    LIM2      RHS1      30.0
    LIM2      X2        2.0
    LIM2      X6        4.0
    LIM2      X8        3.0
    LIM2      X9        4.0
    LIM2      X10       9.0
    LIM3      RHS1      10.0
    LIM3      X3        3.0
    LIM3      X6        4.0
    LIM3      X9        1.0
    LIM4      RHS1      15.0
    LIM4      X5        1.0
    LIM4      X8        3.0
    LIM4      X10       4.0
    LIM5      RHS1      5.0
    LIM5      X1        2.0
    LIM5      X3        3.0
    LIM5      X9        1.0
    LIM6      RHS1      20.0
    LIM6      X1        1.0
    LIM6      X6        1.0
    LIM6      X9        1.0
    LIM7      RHS1      10.0
    LIM7      X1        1.0
    LIM7      X6        2.0
    LIM7      X9        2.0
    LIM7      X10       3.0
RHS
    COST      X1        1.0
    COST      X2        1.0
    COST      X3        3.0
    COST      X4        1.0
    COST      X5        3.0
    COST      X6        1.0
    COST      X7        3.0
    COST      X8        1.0
    COST      X9        1.0
    COST      X10       1.0
BOUNDS
 MI B1        LIM6
 UP B1        LIM6      0
 FR B1        LIM7
ENDATA
