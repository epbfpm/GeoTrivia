import turtle
import pandas
from random import choice


class Point:

    def __init__(self, c, x, y):
        self.create(c, x, y)
        self.list = []

    def create(self, c, x, y):
        new_point = turtle.Turtle()
        new_point.shape('circle')
        new_point.shapesize(0.3)
        new_point.pencolor('black')
        new_point.fillcolor('red')
        new_point.penup()
        new_point.setpos(x, y)
        new_point.write(arg=c, move=False, align='left', font=('Arial', 10, 'bold'))



class Text(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.setpos(0, -20)

    def end(self):
        self.clear()
        self.write(arg=f'Parabéns! Você acertou todas as capitais!', move=False, align='center',
                   font=('Arial', 20, 'normal'))

    def death(self):
        self.clear()
        self.write(arg=f'Você precisa voltar pra escola...', move=False, align='center', font=('Arial', 20, 'normal'))


class Lives(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.hideturtle()
        self.penup()
        self.setpos(200, 250)

    def refresh(self, vd):
        self.clear()
        self.write(arg=f'Vidas: {vd}', move=False, align='left', font=('Arial', 20, 'normal'))

def restart(x, y, r):
    save_dic = {
        'retain': r,
        'lives': [x],
        'score': [y],
    }
    save = pandas.DataFrame(save_dic)
    save.to_csv('./br/save.csv')
    parameter_dic = {
        'Capital': capitais,
        'Estado': estados
    }
    save = pandas.DataFrame(parameter_dic)
    save.to_csv('./br/prm.csv')
# screen parameters
screen = turtle.Screen()
screen.title('Capitais do Brasil')
screen.tracer(0)

# background
image = './br/map.gif'
screen.addshape(image)
turtle.shape(image)

# positions
file = './br/list.csv'
data = pandas.read_csv(file)
if pandas.read_csv('./br/save.csv').retain.item() == 0:
    capitais = data.Capital.to_list()
    estados = data.Estado.to_list()
else:
    capitais = pandas.read_csv('./br/prm.csv').Capital.to_list()
    estados = pandas.read_csv('./br/prm.csv').Estado.to_list()

# score
vd = int(pandas.read_csv('./br/save.csv').lives.item())
scr = int(pandas.read_csv('./br/save.csv').score.item())
vidas = Lives()
vidas.refresh(vd)
end = Text()

# game
while vd > 0 and scr < 27:
    screen.update()
    estado = choice(estados)
    guess = screen.textinput(f'{scr}/27 capitais', f'Qual a capital de {estado}?').title()
    if guess in capitais and capitais.index(guess) == estados.index(estado):
        capitais.remove(guess)
        estados.remove(estado)
        row = data[data.Capital == guess]
        x = int(row.x)
        y = int(row.y)
        c = row.Capital.item()
        print(c)
        print(row.Estado)
        point = Point(c, x, y)
        scr += 1

    else:
        vd -= 1
        vidas.refresh(vd)

    restart(vd, scr, 0)
    continue


    print(row)
    print(c)
if scr == 27:
    restart(3, 0, 1)
    end.end()
if vd == 0:
    restart(3, 0, 1)
    end.death()

# def get_cor(x, y):
#     print(x, y)
# turtle.onscreenclick(get_cor)

turtle.mainloop()
screen.exitonclick()
