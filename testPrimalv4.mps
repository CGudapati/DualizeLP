NAME          TESTPROB
ROWS
 N  COST
 G  LIM1
 G  LIM2
 G  LIM3
 G  LIM4
 G  LIM5
 L  LIM6
 E  LIM7
COLUMNS
    X1        COST                 1   LIM1                 1
    X1        LIM5                 2   LIM6                 1
    X1        LIM7                 1
    X2        LIM2                 2   COST                 1    
    X3        COST                 3   LIM1                 2
    X3        LIM3                 3   LIM5                 3
    X4        LIM1                 3   COST                 1
    X5        COST                 3   LIM4                 1
    X6        LIM2                 4   LIM3                 4
    X6        COST                 1   LIM6                 1
    X6        LIM7                 2
    X7        COST                 3   LIM1                 2
    X8        LIM1                 3   LIM2                 3
    X8        LIM4                 3   COST                 1
    X9        LIM1                 9   LIM2                 4
    X9        LIM3                 1   LIM5                 1
    X9        COST                 1   LIM6                 1
    X9        LIM7                 2
    X10       LIM2                 9   LIM4                 4
    X10       COST                 1   LIM7                 3
RHS
    RHS1      LIM1                20   LIM2                30
    RHS1      LIM3                10   LIM4                15
    RHS1      LIM5                 5   LIM6                20
    RHS1      LIM7                10
BOUNDS
 FR BOUND     X1                  
 FR BOUND     X3                  
 FR BOUND     X6                  
ENDATA
