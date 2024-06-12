This application use for control translation stage (DDS100/M) developed based on Python language.

Main file for user : MAIN Application for USER.py 
    main program with UI for users.

Main file for developer : MAIN Application for DEVELOPER.py
    main program fordeveloper.

How to use application
1.Open VScode
2.Open MAIN&UI V3.py
3.Click play button on the right top of VScode program.
4.Wait untill apllication pop up UI window
5.Enter values in each parameter.
6.Click Enter.
7.Click Start.
8.After finished run application , Open result.csv file for see result in table form.
  
How to tuning PID parameters ?
    1. Tuning 'PROPORTIONAL' or 'Kp' First . Tuning it until translation stage move nearly closet to the reference image.
    2. Then tuning 'INTEGRAL' or 'Ki' for reduce error from 'PROPORTIONAL' or 'Kp'.
    3. Then tuning 'DERIVATIVE' or 'Kd' for reduce overshoot.

How it effect ?
'PROPORTIONAL' or 'Kp' effect to the current error ( setpoint - measured output of the system ).
'INTEGRAL' or 'Ki' effect to the contribution of the accumulated error over time to the control signal .
'DERIVATIVE' or 'Kd' effect to the stability and responsiveness of the control loop .

