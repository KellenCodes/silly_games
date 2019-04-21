from Tkinter import *
import random
import time
import sys

class Ball:
    def __init__(self, balls):
        self.balls = balls
        self.canvas = balls.canvas
        self.paddle = balls.paddle
        self.score = balls.score
        self.id = self.canvas.create_oval(10, 10, 25, 25, fill=balls.colors[0])
        self.canvas.move(self.id, balls.xPos[0], balls.yPos[0])
        starts = [-1,1]
        random.shuffle(starts)
        self.x = starts[0]
        self.y = -1
        self.canvas_height = self.canvas.winfo_height()
        self.canvas_width = self.canvas.winfo_width()
        self.bigRando = [0.25,0.35,0.45,0.55,0.65,0.75]
        self.littleRando = [0.05, 0.1, 0.15, 0.2]
        self.tinyRando = [0.01, 0.02, 0.03, 0.04]
        self.currentXRando = self.bigRando
        self.currentYRando = self.bigRando
        self.hit_bottom = False
        self.trigger_new_ball = False

    def hit_paddle(self,pos):
            paddle_pos = self.canvas.coords(self.paddle.id)
            if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
                if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                    self.score.score += round((abs(self.x) + abs(self.y)) / 2, 1)
                    return True
            return False
        
    def draw(self):
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id)
            random.shuffle(self.currentYRando)
            random.shuffle(self.currentXRando)
            if self.hit_paddle(pos) == True: #somewhere in the paddle's perimeter
                self.y = -1*(abs(self.y) + self.currentYRando[0])
            if pos[1] <= 0:                         #very high on screen
                self.y = abs(self.y) + self.currentYRando[0]
            if pos[3] >= self.canvas_height:        #very low on screen
                self.hit_bottom = True
                self.balls.delete(self)
            if pos[0] <= 0:                         # very left
                self.x = abs(self.x) + self.currentXRando[0]
            if pos[2] >= self.canvas_width:         # very right
                self.x = -1*(abs(self.x) + self.currentXRando[0])

            if abs(self.x) + abs(self.y) > 11 and self.trigger_new_ball == False:
                self.trigger_new_ball = True
                self.balls.new()
                
            if abs(self.x) >= 4:
                self.currentXRando = self.littleRando
            elif abs(self.x) >= 10:
                self.currentXRando = self.tinyRando
            elif abs(self.x) >= 20:
                self.currentXRando = [0]    
                
            if abs(self.y) >= 4:
                self.currentYRando = self.littleRando
            elif abs(self.y) >= 10:
                self.currentYRando = self.tinyRando
            elif abs(self.y) >= 20:
                self.currentYRando = [0]

class Paddle:
    def __init__(self, canvas):
        self.canvas = canvas
        self.colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
        random.shuffle(self.colors)
        self.id = canvas.create_rectangle(0, 0, 100, 21, fill=self.colors[0])
        self.canvas.move(self.id, 0, 300)

        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        self.canvas.bind_all('<KeyRelease-Left>', self.x_stop)
        self.canvas.bind_all('<KeyRelease-Right>', self.x_stop)

    def draw(self):
        pos = self.canvas.coords(self.id)
        if pos[0] >= 0 and pos[2] <= self.canvas_width:
            self.canvas.move(self.id, self.x, 0)
        elif pos[0] <= 0:
            correct = abs(pos[0])
            self.canvas.move(self.id, correct, 0)
        elif pos[2] >= self.canvas_width:
            correct = -1*(pos[2] - self.canvas_width)
            self.canvas.move(self.id, correct, 0)

    def turn_left(self, evt):
        self.x = -8
    def turn_right(self, evt):
        self.x = 8
    def x_stop(self, evt):
        self.x = 0

class Score:
    def __init__(self, canvas):
        self.score = 0
        self.canvas = canvas
        self.id = canvas.create_text(250,100, text=self.score, font=("Comic Sans", 50))

    def draw(self):
        self.score = round(self.score, 1)
        self.canvas.itemconfig(self.id, text=self.score)


class Balls:
    def __init__(self, canvas, paddle, score):
        self.canvas = canvas
        self.paddle = paddle
        self.score = score
        self.colors = ["white", "black", "red", "green", "blue", "cyan", "yellow", "magenta"]
        random.shuffle(self.colors)
        self.ball_count = 0
        self.xPos = range(10, 490)
        self.yPos = range(10, 100)
        self.balls = []

    def new(self):
        random.shuffle(self.colors)
        random.shuffle(self.xPos)
        random.shuffle(self.yPos)
        self.balls.append(Ball(self))
        self.ball_count += 1

    def delete(self, ball):
        self.balls.remove(ball)
        self.ball_count -= 1
        self.canvas.delete(ball.id)
    
    def draw(self):
        for ball in self.balls:
            ball.draw()

def setup():
    tk = Tk()
    tk.title("Game")
    tk.resizable(0,0)
    tk.wm_attributes("-topmost", 1)
    canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0)
    canvas.pack()
    def close(event):
        tk.withdraw()
        sys.exit()
    canvas.bind_all('<Escape>', close)
    tk.update()
    return canvas, tk
    
def gameplay():
    canvas, tk = setup()

    score = Score(canvas)
    paddle = Paddle(canvas)
    balls = Balls(canvas, paddle, score)
    
    balls.new()
    gametick = 0
    gamedifficulty = 1800
    while 1:
        if balls.ball_count > 0:
            score.draw()
            balls.draw()
            paddle.draw()
        else:
            canvas.create_text(250,200, text="Game Over", font=("Comic Sans", 50))
            
            
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
        gametick += 1

        if gamedifficulty / gametick == 0 and balls.ball_count > 0:
            balls.new()
            gamedifficulty += 100
            gametick = 0
        
if __name__ == "__main__":
    gameplay()

