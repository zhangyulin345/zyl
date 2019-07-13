
import pygame  # 将pygame库导入到python程序中
from pygame.locals import *  # 导入pygame中的常量
import sys                   # 导入系统模块
SCREENWIDTH = 822  # 窗口宽度
SCREENHEIGHT = 199  # 窗口高度
FPS = 30  # 更新画面的时间


# 定义一个移动地图类
class MyMap():

    def __init__(self, x, y):
        # 加载背景图片
        self.bg = pygame.image.load("image/bg.png").convert_alpha()
        self.x = x
        self.y = y

    def map_rolling(self):
        if self.x < -790:  # 小于-790说明地图已经完全移动完毕
            self.x = 800  # 给地图一个新的坐标点
        else:
            self.x -= 5  # 5个像素向左移动

    # 更新地图
    def map_update(self):
        SCREEN.blit(self.bg, (self.x, self.y))

# 背景音乐按钮
class Music_Button():
    is_open = True   # 背景乐音的标记
    def __init__(self):
        self.open_img = pygame.image.load('image/btn_open.png').convert_alpha()
        self.close_img = pygame.image.load('image/btn_close.png').convert_alpha()
        self.bg_music = pygame.mixer.Sound('audio/bg_music.wav')  # 加载背景音乐
    # 判断鼠标是否在，按钮的范围内
    def is_select(self):
        # 获取鼠标，的坐标
        point_x, point_y = pygame.mouse.get_pos()
        w, h = self.open_img.get_size()             # 获取按钮图片的大小
        # 判断鼠标是否在按钮范围内
        in_x = point_x > 20 and point_x < 20 + w
        in_y = point_y > 20 and point_y < 20 + h
        return in_x and in_y





from itertools import cycle  # 导入迭代工具


# 玛丽类
class Marie():
    def __init__(self):
        # 初始化小玛丽矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.jumpState = False  # 跳跃的状态
        self.jumpHeight = 130  # 跳跃的高度
        self.lowest_y = 140  # 最低坐标
        self.jumpValue = 0  # 跳跃增变量
        # 小玛丽动图索引
        self.marieIndex = 0
        self.marieIndexGen = cycle([0, 1, 2])
        # 加载小玛丽图片
        self.adventure_img = (
            pygame.image.load("image/adventure1.png").convert_alpha(),
            pygame.image.load("image/adventure2.png").convert_alpha(),
            pygame.image.load("image/adventure3.png").convert_alpha(),
        )
        self.jump_audio = pygame.mixer.Sound('audio/jump.wav')  # 跳音效
        self.rect.size = self.adventure_img[0].get_size()
        self.x = 50;  # 绘制小玛丽的X坐标
        self.y = self.lowest_y;  # 绘制小玛丽的Y坐标
        self.rect.topleft = (self.x, self.y)

    # 跳状态
    def jump(self):
        self.jumpState = True

    # 小玛丽移动
    def move(self):
        if self.jumpState:  # 当起跳的时候
            if self.rect.y >= self.lowest_y:  # 如果站在地上
                self.jumpValue = -5  # 以5个像素值向上移动
            if self.rect.y <= self.lowest_y - self.jumpHeight:  # 小玛丽到达顶部回落
                self.jumpValue = 5  # 以5个像素值向下移动
            self.rect.y += self.jumpValue  # 通过循环改变玛丽的Y坐标
            if self.rect.y >= self.lowest_y:  # 如果小玛丽回到地面
                self.jumpState = False  # 关闭跳跃状态

    # 绘制小玛丽
    def draw_marie(self):
        # 匹配小玛丽动图
        marieIndex = next(self.marieIndexGen)
        # 绘制小玛丽
        SCREEN.blit(self.adventure_img[marieIndex],
                    (self.x, self.rect.y))

import random  # 随机数
# 障碍物类
class Obstacle():
    score = 1  # 分数
    move = 5   # 移动距离
    obstacle_y = 150  # 障碍物y坐标
    def __init__(self):
        # 初始化障碍物矩形
        self.rect = pygame.Rect(0, 0, 0, 0)
        # 加载障碍物图片
        self.missile = pygame.image.load("image/missile.png").convert_alpha()
        self.pipe = pygame.image.load("image/pipe.png").convert_alpha()
        # 加载分数图片
        self.numbers = (pygame.image.load('image/0.png').convert_alpha(),
                        pygame.image.load('image/1.png').convert_alpha(),
                        pygame.image.load('image/2.png').convert_alpha(),
                        pygame.image.load('image/3.png').convert_alpha(),
                        pygame.image.load('image/4.png').convert_alpha(),
                        pygame.image.load('image/5.png').convert_alpha(),
                        pygame.image.load('image/6.png').convert_alpha(),
                        pygame.image.load('image/7.png').convert_alpha(),
                        pygame.image.load('image/8.png').convert_alpha(),
                        pygame.image.load('image/9.png').convert_alpha())
        # 加载加分音效
        self.score_audio = pygame.mixer.Sound('audio/score.wav')  # 加分
        # 0和1随机数
        r = random.randint(0, 1)
        if r == 0:  # 如果随机数为0显示导弹障碍物相反显示管道
            self.image = self.missile   # 显示导弹障碍
            self.move = 15              # 移动速度加快
            self.obstacle_y = 100       # 导弹坐标在天上
        else:
            self.image = self.pipe      # 显示管道障碍
        # 根据障碍物位图的宽高来设置矩形
        self.rect.size = self.image.get_size()
        # 获取位图宽高
        self.width, self.height = self.rect.size
        # 障碍物绘制坐标
        self.x = 800
        self.y = self.obstacle_y
        self.rect.center = (self.x, self.y)

    # 障碍物移动
    def obstacle_move(self):
        self.rect.x -= self.move

    # 绘制障碍物
    def draw_obstacle(self):
        SCREEN.blit(self.image, (self.rect.x, self.rect.y))

    # 获取分数
    def getScore(self):
        self.score
        tmp = self.score;
        if tmp == 1:
            self.score_audio.play()  # 播放加分音乐
        self.score = 0;
        return tmp;

    # 显示分数
    def showScore(self, score):
        # 获取得分数字
        self.scoreDigits = [int(x) for x in list(str(score))]
        totalWidth = 0  # 要显示的所有数字的总宽度
        for digit in self.scoreDigits:
            # 获取积分图片的宽度
            totalWidth += self.numbers[digit].get_width()
        # 分数横向位置
        Xoffset = (SCREENWIDTH - (totalWidth+30))
        for digit in self.scoreDigits:
            # 绘制分数
            SCREEN.blit(self.numbers[digit], (Xoffset, SCREENHEIGHT * 0.1))
            # 随着数字增加改变位置
            Xoffset += self.numbers[digit].get_width()

# 游戏结束的方法
def game_over():
    bump_audio = pygame.mixer.Sound('audio/bump.wav')  # 撞击
    bump_audio.play()  # 播放撞击音效
    # 获取窗体宽、高
    screen_w = pygame.display.Info().current_w
    screen_h = pygame.display.Info().current_h
    # 加载游戏结束的图片
    over_img = pygame.image.load('image/gameover.png').convert_alpha()
    # 将游戏结束的图片绘制在窗体的中间位置
    SCREEN.blit(over_img, ((screen_w - over_img.get_width()) / 2,
                                       (screen_h - over_img.get_height()) / 2))


def mainGame():
    score = 0  # 得分
    over = False  # 游戏结束标记
    global SCREEN, FPSCLOCK
    pygame.init()  # 经过初始化以后我们就可以尽情地使用pygame了。

    # 使用Pygame时钟之前，必须先创建Clock对象的一个实例，
    # 控制每个循环多长时间运行一次。
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))  # 通常来说我们需要先创建一个窗口，方便我们与程序的交互。
    pygame.display.set_caption('玛丽冒险')  # 设置窗口标题

    # 创建地图对象
    bg1 = MyMap(0, 0)
    bg2 = MyMap(800, 0)

    # 创建小玛丽对象
    marie = Marie()

    addObstacleTimer = 0  # 添加障碍物的时间
    list = []  # 障碍物对象列表

    music_button = Music_Button()     # 创建背景音乐按钮对象
    btn_img  = music_button.open_img  # 设置背景音乐按钮的默认图片
    music_button.bg_music.play(-1)    # 循环播放背景音乐

    while True:
        # 获取单击事件
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONUP:  # 判断鼠标事件
                if music_button.is_select():        # 判断鼠标是否在静音按钮范围
                    if music_button.is_open:        # 判断背景音乐状态
                        btn_img = music_button.close_img # 单击后显示关闭状态的图片
                        music_button.is_open = False    # 关闭背景音乐状态
                        music_button.bg_music.stop()    # 停止背景音乐的播放
                    else:
                        btn_img = music_button.open_img
                        music_button.is_open = True
                        music_button.bg_music.play(-1)
            # 如果单击了关闭窗口就将窗口关闭
            if event.type == QUIT:
                pygame.quit()  # 退出窗口
                sys.exit()  # 关闭窗口

            # 单击键盘空格键，开启跳的状态
            if event.type == KEYDOWN and event.key == K_SPACE:
                if marie.rect.y >= marie.lowest_y:  # 如果小玛丽在地面上
                    marie.jump_audio.play()  # 播放小玛丽跳跃音效
                    marie.jump()  # 开启小玛丽跳的状态

                if over == True:  # 判断游戏结束的开关是否开启
                    mainGame()  # 如果开启将调用mainGame方法重新启动游戏




        if over == False:
            # 绘制地图起到更新地图的作用
            bg1.map_update()
            # 地图移动
            bg1.map_rolling()
            bg2.map_update()
            bg2.map_rolling()

            # 小玛丽移动
            marie.move()
            # 绘制小玛丽
            marie.draw_marie()

            # 计算障碍物间隔时间
            if addObstacleTimer >= 1300:
                r = random.randint(0, 100)
                if r > 40:
                    # 创建障碍物对象
                    obstacle = Obstacle()
                    # 将障碍物对象添加到列表中
                    list.append(obstacle)
                # 重置添加障碍物时间
                addObstacleTimer = 0

            # 循环遍历障碍物
            for i in range(len(list)):
                # 障碍物移动
                list[i].obstacle_move()
                # 绘制障碍物
                list[i].draw_obstacle()

                # 判断小玛丽与障碍物是否碰撞
                if pygame.sprite.collide_rect(marie, list[i]):
                    over = True  # 碰撞后开启结束开关
                    game_over()  # 调用游戏结束的方法
                    music_button.bg_music.stop()
                else:
                    # 判断小玛丽是否跃过了障碍物
                    if (list[i].rect.x + list[i].rect.width) < marie.rect.x:
                        # 加分
                        score += list[i].getScore()
                # 显示分数
                list[i].showScore(score)

        addObstacleTimer += 20  # 增加障碍物时间
        SCREEN.blit(btn_img, (20, 20)) # 绘制背景音乐按钮
        pygame.display.update()  # 更新整个窗口
        FPSCLOCK.tick(FPS)  # 循环应该多长时间运行一次


if __name__ == '__main__':
    mainGame()
