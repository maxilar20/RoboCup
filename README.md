# RoboCup

The goal of this project was to develop a simulated football game between two teams of NAO robots. The project utilized a behavioural programming approach to develop a rudimentary artificial intelligence that controls the different player categories such as Attacker, Defender, and Goalkeeper. The coding language used for this was Python. In addition to the player control code, a supervisor code was implemented to control and time the overall game. The supervisor is a decision-based code that handles faults, exceptions, and foul play by players while keeping track of the score and time.

The project utilized the Webots simulation software to create a 3D simulation environment for the game. The 3D models of the NAO robots were created using SolidWorks and Fusion 360 and were implemented in the simulation. A GUI was developed using PyGame to keep track of the match in 2D, which showed the player movement as well as the timer and score.

The game involved two teams, each comprising four NAO robots assigned the roles of attackers, a defender, and a goalkeeper. Each team consists of two attackers, one defender, and one goalkeeper. The referee acted as the simulation controller code on top of the hierarchy to manage game flow, control faults, exceptions, and foul play while recording game time and scores.

The players were controlled by their respective team coach class that implemented control functions for the players. The 3D simulation environment, such as the field, ball, penalty markers, and goal posts, were defined according to the official RoboCup simulation rule book.

The outcome of the project was a 20-minute simulation where the two teams of NAO robots tried to score goals while avoiding opponents and penalties using various decision-making techniques, which are further detailed in the software modelling section of the report. Overall, the project was successful in achieving the goal based on the regulations set by the project specification document.
