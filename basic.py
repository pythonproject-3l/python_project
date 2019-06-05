import pygame as pg

pg.init()

class Button():

    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline = None): # win:哪一張畫布 / outline:按鈕邊框顏色
        if outline:
            pg.draw.rect(win, outline, (self.x+2, self.y-2, self.width+4, self.height+4), 0) #畫布, 顏色, [x座標, y座標, 寬度, 高度, 線寬]

        pg.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pg.font.SysFont('arial', 32)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
        return False

StartButton = Button((0,225,0), 400, 350, 200, 50, 'Start')
RestartButton = Button((0,225,0), 200, 350, 150, 50, 'Restart')
ExitButton = Button((0,0,225), 600, 350, 150, 50, 'Exit')

class Game :

    def __init__(self) :
        self.board = [
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1]
                                       ]
        self.x_point = [100, 200, 400, 600, 800, 900, 1000]
        self.y_point = [160, 320, 480]
        self.start = False
        self.which_choice = False
        self.win = None
        self.choice_player = ''
        self.turn = 1
        width, height = 1000, 480
        self.screen = pg.display.set_mode((width, height), 0, 32)
        self.red = [(0,40), (100,40), (0,200), (100,200), (0,360), (100,360)]
        self.blue = [(800,40), (900,40), (800,200), (900,200), (800,360), (900,360)]
        self.start_game = pg.image.load('start_game.png').convert()
        self.red1_1 = pg.image.load('red1.png').convert_alpha()
        self.red1_2 = pg.image.load('red1.png').convert_alpha()
        self.red2_1 = pg.image.load('red2.png').convert_alpha()
        self.red2_2 = pg.image.load('red2.png').convert_alpha()
        self.red3_1 = pg.image.load('red3.png').convert_alpha()
        self.red3_2 = pg.image.load('red3.png').convert_alpha()
        self.blue1_1 = pg.image.load('blue1.png').convert_alpha()
        self.blue1_2 = pg.image.load('blue1.png').convert_alpha()
        self.blue2_1 = pg.image.load('blue2.png').convert_alpha()
        self.blue2_2 = pg.image.load('blue2.png').convert_alpha()
        self.blue3_1 = pg.image.load('blue3.png').convert_alpha()
        self.blue3_2 = pg.image.load('blue3.png').convert_alpha()

        self.now = ''
        self.selected = None
        self.selected_offset_x = 0
        self.selected_offset_y = 0
        self.starting_point_x = None
        self.starting_point_y = None

    def interface_gui(self) :
        pg.display.set_caption('Our Project')
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        font = pg.font.SysFont("arial", 80)
        text = font.render("CUPS", 1, (0, 0, 255))
        bg.blit(text, (390, 100))
        StartButton.draw(bg, (0,0,0))
        self.screen.blit(bg, (0, 0))
        pg.display.update()
        self.event()

    def restart_gui(self) :
        bg = pg.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        font = pg.font.SysFont("arial", 80)
        if self.win == 0:
            text = font.render("RED WIN!!", 1, (225, 0, 0))
        else:
            text = font.render("BLUE WIN!!", 1, (225, 0, 0))

        bg.blit(text, (300, 100))
        RestartButton.draw(bg, (0,0,0))
        ExitButton.draw(bg, (0,0,0))
        self.screen.blit(bg, (0, 0))
        pg.display.update()

        self.win = None
        self.start = False
        self.event()

    def game_start(self) :
        choice = pg.image.load('intro2.png').convert()
        self.screen.blit(choice, (200, 0))
        pg.display.update()

    def who_start(self, choice) :
        self.screen.fill((0,0,0))
        self.which_choice = True
        if choice == 'o' :
            self.choice_player = 'o'
        else :
            self.choice_player = 'x'
        self.screen.blit(self.start_game, (200, 0))
        self.screen.blit(self.red1_1, self.red[0])
        self.screen.blit(self.red1_2, self.red[1])
        self.screen.blit(self.red2_1, self.red[2])
        self.screen.blit(self.red2_2, self.red[3])
        self.screen.blit(self.red3_1, self.red[4])
        self.screen.blit(self.red3_2, self.red[5])

        self.screen.blit(self.blue1_1, self.blue[0])
        self.screen.blit(self.blue1_2, self.blue[1])
        self.screen.blit(self.blue2_1, self.blue[2])
        self.screen.blit(self.blue2_2, self.blue[3])
        self.screen.blit(self.blue3_1, self.blue[4])
        self.screen.blit(self.blue3_2, self.blue[5])
        pg.display.update()

    def getpos(self) :
        org_x, org_y = pg.mouse.get_pos()
        x, y = org_x, org_y
        xp = False
        yp = False
        i = 0
        j = 0
        #print('org_x:', x, "org_y:", y)
        #print('red_0:',self.red[0])
        for x_pt in self.x_point:
            if x < x_pt  and not xp:
                if x_pt < 2 or x_pt > 4:
                    x = x_pt - 100
                else:
                    x = x_pt - 200
                xp = True
                break
            i += 1
        for y_pt in self.y_point:
            if y < y_pt and not yp:
                y = y_pt - 160
                yp = True
                break
            j += 1

        #print('new_x:', x, 'new_y:', y)
        if self.selected is None:
            return org_x, org_y, x, y
        else:
            return i, j, x, y

    def print_cups(self) :
        self.screen.fill((0,0,0))
        self.screen.blit(self.start_game, (200, 0))

        self.screen.blit(self.red3_1, self.red[4])
        self.screen.blit(self.red3_2, self.red[5])
        self.screen.blit(self.blue3_1, self.blue[4])
        self.screen.blit(self.blue3_2, self.blue[5])

        self.screen.blit(self.red2_1, self.red[2])
        self.screen.blit(self.red2_2, self.red[3])
        self.screen.blit(self.blue2_1, self.blue[2])
        self.screen.blit(self.blue2_2, self.blue[3])

        self.screen.blit(self.red1_1, self.red[0])
        self.screen.blit(self.red1_2, self.red[1])
        self.screen.blit(self.blue1_1, self.blue[0])
        self.screen.blit(self.blue1_2, self.blue[1])

        pg.display.update()


    def choice(self) :
        self.selected = None
        org_x, org_y, x, y = self.getpos()
        self.starting_point_x = x
        self.starting_point_y = y
        ## 點選的那個位置是可以被點的
        if self.choice_player == 'o': #紅色先發
            if self.turn % 2 == 1: #輪到紅色
                for i, c in enumerate(self.red):
                    if c[0] == x and c[1]-40 == y:
                        print('red:')
                        print(i)
                        self.now = 'o'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return
            else: #輪到藍色
                for i, c in enumerate(self.blue):
                    if c[0] == x and c[1]-40 == y:
                        print("blue:")
                        print(i)
                        self.now = 'x'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return
        else: # 藍色先發
            if self.turn % 2 == 1: #輪到藍色
                for i, c in enumerate(self.blue):
                    if c[0] == x and c[1]-40 == y:
                        self.now = 'x'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return

            else: #輪到紅色
                for i, c in enumerate(self.red):
                    if c[0] == x and c[1]-40 == y:
                        self.now = 'o'
                        self.selected = i
                        self.selected_offset_x = x - org_x
                        self.selected_offset_y = y - org_y
                        return

        ## 點錯顏色
        print("oops:")
        self.selected = None

    def move(self):
        x, y = pg.mouse.get_pos()
        if self.choice_player == 'o': #紅色先發
            if self.turn % 2 == 1: #輪到紅色
                self.red[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.red[self.selected])
            else:
                self.blue[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.blue[self.selected])
        else: #輪到藍色
            if self.turn % 2 == 1: #輪到藍色
                self.blue[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.blue[self.selected])
            else:
                self.red[self.selected] = (x + self.selected_offset_x, y + self.selected_offset_y)
                #print(self.red[self.selected])

    def who_win(self, winner) :
        if winner == 0 :
            print('red win!')
        else :
            print('blue win!')


    def is_win(self):
        wins = [
            [self.board[0][2], self.board[0][3], self.board[0][4]], # 橫(1)
            [self.board[1][2], self.board[1][3], self.board[1][4]], # 橫(2)
            [self.board[2][2], self.board[2][3], self.board[2][4]], # 橫(3)
            [self.board[0][2], self.board[1][2], self.board[2][2]], # 直(1)
            [self.board[0][3], self.board[1][3], self.board[2][3]], # 直(2)
            [self.board[0][4], self.board[1][4], self.board[2][4]], # 直(3)
            [self.board[0][2], self.board[1][3], self.board[2][4]], # 斜(1)
            [self.board[0][4], self.board[1][3], self.board[2][2]]  # 斜(2)
        ]

        for win in wins :
            if not min(win) == -1 and win[0]%2 == win[1]%2 and win[1]%2 == win[2]%2 :
                self.who_win(win[0]%2)
                self.win = win[0] % 2
                print('win')

    def set_board(self):
        print("set board")
        print('now:',self.now)
        print('selected:',self.selected)
        ## 用來判斷是否符合大杯子蓋小杯子的規則

        i, j, x, y = self.getpos() # [j,i] 為目的地在self.board的位置
        #print('x:', j)
        #print('y:', i)
        print('org:', self.board[j][i])
        if self.board[j][i] == -1 and self.now == 'o':
            if self.board[j][i] == 0 or self.selected == 1: # 大的
                self.board[j][i] = 0
            elif self.selected == 2 or self.selected == 3: # 中的
                self.board[j][i] = 2
            else: # 小的
                self.board[j][i] = 4

        elif self.board[j][i] == -1 and self.now == 'x':
            if self.selected == 0 or self.selected == 1: # 大的
                self.board[j][i] = 1
            elif self.selected == 2 or self.selected == 3: # 中的
                self.board[j][i] = 3
            else: # 小的
                self.board[j][i] = 5
        elif (self.board[j][i] == 2 or self.board[j][i] == 4) and self.now == 'x' and (self.selected == 0 or self.selected == 1): # 如果原先放的是紅中或是紅小，然後準備放的是藍大
                self.board[j][i] = 1                                                                # 那就是藍大
        elif self.board[j][i] == 4 and self.now == 'x' and (self.selected == 2 or self.selected == 3):                            # 如果原先放的是紅小，然後準備放的是藍中，
                self.board[j][i] = 3                                                                # 那就是藍中
        elif (self.board[j][i] == 3 or self.board[j][i] == 5) and self.now == 'o' and (self.selected == 0 or self.selected == 1): # 如果原先放的是藍中或是藍小，然後準備放的是紅大
                self.board[j][i] = 0                                                                # 那就是紅大
        elif self.board[j][i] == 5 and self.now == 'o' and (self.selected == 2 or self.selected == 3):                            # 如果原先放的是藍小，然後準備放的是紅中
                self.board[j][i] = 2                                                                # 那就是紅中
        else: # 不符合移動規則要把圖片放回原位
            print('oops')
            if self.now == 'o':
                self.red[self.selected] = (self.starting_point_x, self.starting_point_y + 40)
                self.turn -= 1
            else:
                self.blue[self.selected] = (self.starting_point_x, self.starting_point_y + 40)
                self.turn -= 1

        self.is_win()

        self.turn += 1

    def event(self):
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT :
                    pg.quit()

                elif event.type == pg.MOUSEBUTTONDOWN and not self.start:
                    pos = pg.mouse.get_pos()
                    ## 起始頁面動作
                    if StartButton.isOver(pos):
                        self.start = True
                        self.game_start()
                        print('clicked the start button')

                    ## 贏家頁面
                    elif RestartButton.isOver(pos):
                        self.__init__()
                        self.start = True
                        self.game_start()
                        print('clicked the restart button')

                    elif ExitButton.isOver(pos):
                        pg.quit()
                        print('clicked the ExitButton button')

                ## 選擇Ｏ開始或是X開始的頁面
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_1 and self.start and not self.which_choice :
                        self.who_start('o') # Red

                    elif event.key == pg.K_2 and self.start and not self.which_choice :
                        self.who_start('x') # Blue

                ## 遊戲頁面
                ## 1. click
                elif event.type == pg.MOUSEBUTTONDOWN and self.start and self.which_choice and self.win is None:
                    print('turn = ', self.turn)
                    self.choice()

                ## 2. drag
                elif event.type == pg.MOUSEMOTION and self.start and self.which_choice and self.win is None:
                    if self.selected is not None:
                        self.move()

                ## 3. drop
                elif event.type == pg.MOUSEBUTTONUP and self.start and self.which_choice and self.win is None:
                    if self.selected is not None:
                        self.set_board()
                        self.print_cups()
                        print(self.board)
                    self.selected = None


            if self.selected != None  and self.win is None :
                self.print_cups()

            if self.win is not None:
                self.restart_gui()


game = Game()
game.interface_gui()
pg.quit()
