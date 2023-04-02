from turtle import Turtle, Screen
import random
from DummyCoreManager import DummyManager


dummy_manager = DummyManager()
screen = Screen()
newTur = Turtle(shape="turtle")
floor = Turtle(shape="square")
floor.color("gray")
floor.shapesize(stretch_wid=1, stretch_len=20)
screen.bgpic("picturs/desktop.png")
floor.penup()
floor.goto(0, -300)


score_turtle = Turtle()
score_turtle.penup()
score_turtle.hideturtle()
score_turtle.goto(-380, 260)
screen.setup(width=800, height=600)

def getScore():
    random_number = random.random()
    print(random_number)
    return random_number

def updateTurtleLocation(newTur, score):
    if score <= 0.5 and score <= 1:
        new_y = score * 0.00100
        num_steps_up = int(score * 10)
        speed = int(score * 0.03)-5
        floor.goto(floor.xcor(), floor.ycor()+2)
        floor.speed=-2
        for i in range(num_steps_up):
            newTur.goto(newTur.xcor(), newTur.ycor() + 1)
            newTur.speed(speed)
            if newTur.ycor() > screen.window_height() / 2:
                newTur.sety(screen.window_height() / 2)
                break
 


    # Update score display
    score_turtle.clear()
    score_turtle.write(f"Score: {score:.2f}", align="left", font=("Arial", 16, "normal"))


while True:
    score = dummy_manager.get_corr()
    updateTurtleLocation(newTur, score)
    screen.update()

screen.done()
