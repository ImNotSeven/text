import pygame
import time
import random

from pygame.sprite import Sprite

screen_width = 900
screen_heigh = 700

class BaseItem(Sprite):#定义一个基类
    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

class MainGame():
    window = None
    my_plane = None
    enemyPlaneList=[]#存储敌方飞机的列表
    enemyPlaneCount=5#存储敌方飞机的数量
    myBulletList=[]#储存我方飞机子弹的列表
    enemyBulletList=[]#存储敌方子弹的列表
    explodeList=[]#存储爆炸效果列表
    cloudList=[]#存储云的列表
    def __init__(self):
        pass
    def StartGame(self):#开始游戏
        pygame.display.init()#加载主窗口
        MainGame.window = pygame.display.set_mode([screen_width,screen_heigh])#设置主窗口大小
        self.createMyplane()#初始化我方飞机
        self.createEnemyPlane()#初始化敌方飞机，将敌方飞机添加到列表
        self.createCloud()#初始化云
        pygame.display.set_caption('飞机大战1.0')#设置窗口的标题
        while True:
            #使循环速度变慢使飞机速度变慢
            time.sleep(0.03)
            MainGame.window.fill('white')#窗口设置填充颜色
            self.GetEvent()#获取事件
            MainGame.window.blit(self.GetTextSurface('敌方飞机剩余数量%d'%len(MainGame.enemyPlaneList)),(10,10))
            if MainGame.my_plane and MainGame.my_plane.live:#调用飞机显示方法,判断我方飞机是否存活
                MainGame.my_plane.displayPlane()
            else:#删除我方飞机
                del MainGame.my_plane
                MainGame.my_plane=None
            self.blitEnemyPlane()#循环遍历敌方飞机列表，展示敌方飞机
            self.blitMyBullet()#循环遍历显示我方飞机的子弹
            self.blitEnemyBullet()#循环遍历敌方子弹列表名战士敌方子弹
            self.blitExplode()#循环遍历爆炸列表,展示爆炸效果
            self.blitCloud()# 循环遍历云列表,展示云
            if MainGame.my_plane and MainGame.my_plane.live:
                if not MainGame.my_plane.stop:#如果飞机的开关是开启，才可以移动
                    MainGame.my_plane.move()#调用移动方法
                    MainGame.my_plane.hitCloud()
                    MainGame.my_plane.myPlane_hit_enemyPlane()#检测我方飞机是否与敌方飞机是否发生破撞
            pygame.display.update()

    def blitCloud(self):#循环遍历云列表,展示云
        for cloud in MainGame.cloudList:
            if cloud.live:#判断云是否存活
                cloud.displayCloud()#调用云的显示方法
            else:#从云列表移除
                MainGame.cloudList.remove(cloud)


    def createCloud(self):
        for i in range(3):
            cloud=Cloud(i*300,220)#初始化云
            MainGame.cloudList.append(cloud)#将云添加到列表中




    def createMyplane(self):#创建我方飞机的方法
        MainGame.my_plane = MyPlane(350,350)
        music=Music('image/start.wav')#创建music对象
        music.play()#播放音乐
    def createEnemyPlane(self):#初始化敌方飞机，将地方飞机添加到列表
        top=100
        for i in range(MainGame.enemyPlaneCount):#循环生成敌方飞机
            left=random.randint(0,600)
            speed=random.randint(1,4)
            enemy=EnemyPlane(left,top,speed)
            MainGame.enemyPlaneList.append(enemy)

    def blitExplode(self):#循环遍历爆炸列表,展示爆炸效果
        for explode in MainGame.explodeList:#判断是否活着
            if explode.live:#展示
                explode.displayExplode()
            else:#在爆炸列表中删除
                MainGame.explodeList.remove(explode)


    def blitEnemyPlane(self):#循环遍历敌方飞机列表，展示敌方飞机
        for enemyPlane in MainGame.enemyPlaneList:
            if enemyPlane.live:#判断当前敌方飞机是否活着
                enemyPlane.displayPlane()
                enemyPlane.randMove()
                enemyPlane.hitCloud()#调用检测是否与云碰撞
                if MainGame.my_plane and MainGame.my_plane.live:
                    enemyPlane.enemyPlane_hit_myPlane()#检测敌方飞机是否与我方飞机发生碰撞
                enemyBullet = enemyPlane.shot()  # 发射子弹
                if enemyBullet:  # 判断敌方子弹是否为none，如果不是则添加到敌方子弹列表
                    MainGame.enemyBulletList.append(enemyBullet)  # 将敌方子弹存储到敌方子弹列表中
            else:#不活着则从敌方飞机列表移除
                MainGame.enemyPlaneList.remove(enemyPlane)


    def blitMyBullet(self):#循环遍历我方飞机子弹存储列表
        for myBullet in MainGame.myBulletList:
            if myBullet.live:#判断当前子弹状态是否为活着状态，如果是则显示并移动
                myBullet.displayBullet()
                myBullet.move()#调用子弹的移动方法
                myBullet.myBullet_hint_enemyPlane()#调用检测我方子弹是否与敌方飞机发生碰撞
                myBullet.hitCloud()#检测我方子弹是否与云发生碰撞
            else:#否则在列表中删除
                MainGame.myBulletList.remove(myBullet)

    def blitEnemyBullet(self):#循环遍历敌方子弹列表名战士敌方子弹
        for enemyBullet in MainGame.enemyBulletList:
            if enemyBullet.live:#判断敌方子弹是否存活
                enemyBullet.displayBullet()
                enemyBullet.move()
                enemyBullet.enemyBullet_hit_myPlane()
                enemyBullet.hitCloud()#检测敌方子弹是否与云发生碰撞
            else:
                MainGame.enemyBulletList.remove(enemyBullet)






    def EndGame(self):
        print('谢谢游玩')
        exit()
    def GetTextSurface(self,text):#左上角文字绘制
        pygame.font.init()#初始化字体模块
        font = pygame.font.SysFont('kaiti',18)#获取字体font对象
        textSurface = font.render(text,True,'red')#绘制文字信息
        return textSurface
    def GetEvent(self):
        EventList = pygame.event.get()#获取所有事件
        for Event in EventList:
            if Event.type == pygame.QUIT:#判断按下的是否为退出，如果是则退出
                self.EndGame()
            if Event.type == pygame.KEYDOWN:#判断的是否是键盘的按下(上下左右)
                if not MainGame.my_plane:#当飞机不存在或死亡
                    if Event.key == pygame.K_ESCAPE:
                        self.createMyplane()#让飞机重生
                if MainGame.my_plane and MainGame.my_plane.live:
                    if Event.key == pygame.K_LEFT:
                        MainGame.my_plane.direction = 'L'  # 切换方向
                        MainGame.my_plane.stop = False
                        # MainGame.my_plane.move()
                        print('按下左键飞机向左移动')
                    elif Event.key == pygame.K_RIGHT:
                        MainGame.my_plane.direction = 'R'  # 切换方向
                        MainGame.my_plane.stop = False
                        # MainGame.my_plane.move()
                        print('按下右键飞机向右移动')
                    elif Event.key == pygame.K_UP:
                        MainGame.my_plane.direction = 'U'  # 切换方向
                        MainGame.my_plane.stop = False
                        # MainGame.my_plane.move()
                        print('按下上键飞机向上移动')
                    elif Event.key == pygame.K_DOWN:
                        MainGame.my_plane.direction = 'D'  # 切换方向
                        MainGame.my_plane.stop = False
                        # MainGame.my_plane.move()
                        print('按下下键飞机向下移动')
                    elif Event.key == pygame.K_SPACE:
                        print('发射子弹')
                        if len(MainGame.myBulletList) < 3:  # 限制发射3颗子弹
                            my_Bullet = Bullet(MainGame.my_plane)  # 创建我方飞机发射子弹
                            MainGame.myBulletList.append(my_Bullet)
                            music=Music('image/Gunfire.wav')#发射子弹音效
                            music.play()
            if Event.type == pygame.KEYUP:#松开方向键飞机停止移动，修改开关状态
                if Event.key == pygame.K_UP or Event.key == pygame.K_DOWN or Event.key == pygame.K_LEFT or Event.key == pygame.K_RIGHT:#判断松开的键位是上下左右时菜停止移动
                    if MainGame.my_plane and MainGame.my_plane.live:
                        MainGame.my_plane.stop=True
class Plane(BaseItem):
    def __init__(self,left,top):#添加左距离left和上距离top
        # 保存加载的图片
        self.images = {'U':pygame.image.load('image/planeU.png'),
                       'D':pygame.image.load('image/planeD.png'),
                       'L':pygame.image.load('image/planeL.png'),
                       'R':pygame.image.load('image/planeR.png')}
        self.direction='U'#方向
        self.image=self.images[self.direction]#根据图片方向获取图片
        self.rect=self.image.get_rect()#根据图片获取区域
        self.rect.left=left#设置区域的left和top
        self.rect.top=top
        #速度决定移动的快慢
        self.speed=6
        self.stop=True#飞机移动开关
        self.live=True#是否活着
        self.oldLeft=self.rect.left
        self.oldTop=self.rect.top



    def move(self):#移动
        self.oldLeft=self.rect.left#移动后记录原始坐标
        self.oldTop=self.rect.top

        if self.direction == 'L':#判断飞机方向进行移动
            if self.rect.left>0:#判断飞机距离左边界是否大于0，是则能飞行
                self.rect.left -= self.speed
        elif self.direction == 'R':
            if self.rect.left+self.rect.height<screen_width:
                self.rect.left += self.speed
        elif self.direction == 'U':
            if self.rect.top>0:
                self.rect.top -= self.speed
        elif self.direction == 'D':
            if self.rect.top+self.rect.width<screen_heigh:
                self.rect.top += self.speed

    def shot(self):#射击
        return  Bullet(self)

    def stay(self):
        self.rect.left=self.oldLeft
        self.rect.top=self.oldTop

    def hitCloud(self):#检测飞机是否与云发生碰撞
        for cloud in MainGame.cloudList:
            if pygame.sprite.collide_rect(self,cloud):
                self.stay()#将坐标设置为移动之前的坐标

    def displayPlane(self):#展示飞机方法
        self.image=self.images[self.direction]
        MainGame.window.blit(self.image,self.rect)

class Music():
    def __init__(self,filename):
        self.filename=filename
        pygame.mixer.init()#初始化音乐混合器
        pygame.mixer.music.load(self.filename)#加载音乐
    def play(self):
        pygame.mixer.music.play()

class MyPlane(Plane):
    def __init__(self,left,top):
        super(MyPlane,self).__init__(left,top)

    def myPlane_hit_enemyPlane(self):
        for enemyPlane in MainGame.enemyPlaneList:
            if pygame.sprite.collide_rect(self,enemyPlane):
                self.stay()

class EnemyPlane(Plane):
    def __init__(self,left,top,speed):
        super(EnemyPlane,self).__init__(left,top)#调用父类的初始化方法
        self.images = {'U': pygame.image.load('image/enemyU.png'),
                       'D': pygame.image.load('image/enemyD.png'),
                       'L': pygame.image.load('image/enemyL.png'),
                       'R': pygame.image.load('image/enemyR.png')}
        self.direction=self.randDirection()#调用方法随机生成敌方飞机方向
        self.image=self.images[self.direction]#根据方向获取图片
        self.rect=self.image.get_rect()#获取区域
        self.rect.left=left#对left和top赋值
        self.rect.top=top
        self.speed=speed#速度
        self.flag=True#移动开关
        self.step = 50#新增一个步数变量

    def enemyPlane_hit_myPlane(self):
        if pygame.sprite.collide_rect(self,MainGame.my_plane):
            self.stay()
    def randDirection(self):#随机生成敌方飞机方向
        num=random.randint(1,4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num ==4:
            return 'R'

    def randMove(self):#敌方飞机随机移动方法
        if self.step<=0:
            self.direction=self.randDirection()
            self.step=50#步数复位
        else:
            self.move()
            self.step-=1#步数递减

    def shot(self):
        num=random.randint(1,500)#随机生成100以内的数
        if num<10:
            return Bullet1(self)

class Bullet(BaseItem):
    def __init__(self,plane):
        self.image=pygame.image.load('image/bullet.png')#加载图片
        self.direction=plane.direction#飞机方向决定子弹方向
        self.rect=self.image.get_rect()
        if self.direction == 'U':#子弹的left和top与方向有关
            self.rect.left=plane.rect.left+plane.rect.width/2-self.rect.width/2
            self.rect.top=plane.rect.top-self.rect.height
        elif self.direction == 'D':
            self.rect.left=plane.rect.left+plane.rect.width/2-self.rect.width/2
            self.rect.top=plane.rect.top+plane.rect.height
        elif self.direction == 'L':
            self.rect.left = plane.rect.left - plane.rect.width / 2 - self.rect.width / 2
            self.rect.top = plane.rect.top + plane.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left=plane.rect.left+plane.rect.width
            self.rect.top=plane.rect.top+plane.rect.width/2 - self.rect.width/2

        self.speed = 6#子弹的速度
        self.live=True#子弹的转台,是否碰到墙壁，修改此状态

    def move(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                self.live=False#修改子弹状态
        elif self.direction == 'D':
            if self.rect.top+self.rect.height<screen_heigh:
                self.rect.top+=self.speed
            else:
                self.live = False  # 修改子弹状态
        elif self.direction == 'R':
            if self.rect.left+self.rect.width<screen_width:
                self.rect.left+=self.speed
            else:
                self.live = False  # 修改子弹状态
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                self.live = False  # 修改子弹状态

    def hitCloud(self):#子弹是否碰撞云
        for cloud in MainGame.cloudList:
            if pygame.sprite.collide_rect(self,cloud):
                self.live=False
                cloud.hp-=1
                if cloud.hp<=0:#修改云的生存状态
                    cloud.live=False
    def displayBullet(self):#显示子弹
        MainGame.window.blit(self.image,self.rect)

    def myBullet_hint_enemyPlane(self):#我方子弹与敌方飞机的碰撞
        for enemyPlane in MainGame.enemyPlaneList:#循环遍历敌方飞机列表，判断是否发生碰撞
            if pygame.sprite.collide_rect(enemyPlane,self):
                enemyPlane.live=False#修改敌方飞机和我方子弹的状态
                self.live=False
                explode=Explode(enemyPlane)#创建爆炸对象
                MainGame.explodeList.append(explode)
                music = Music('image/bang.wav')
                music.play()

    def enemyBullet_hit_myPlane(self):#敌方飞机与我方飞机碰撞
        if MainGame.my_plane and MainGame.my_plane.live:
            if pygame.sprite.collide_rect(MainGame.my_plane, self):
                explode=Explode(MainGame.my_plane)#产生爆炸对象
                MainGame.explodeList.append(explode)#将爆炸对象添加到爆炸列表中
                self.live=False#修改敌方子弹与我方飞机状态
                MainGame.my_plane.live=False
                music = Music('image/fire.wav')
                music.play()

class Bullet1(BaseItem):
    def __init__(self,plane):
        self.image=pygame.image.load('image/bullet1.png')#加载图片
        self.direction=plane.direction#飞机方向决定子弹方向
        self.rect=self.image.get_rect()
        if self.direction == 'U':#子弹的left和top与方向有关
            self.rect.left=plane.rect.left+plane.rect.width/2-self.rect.width/2
            self.rect.top=plane.rect.top-self.rect.height
        elif self.direction == 'D':
            self.rect.left=plane.rect.left+plane.rect.width/2-self.rect.width/2
            self.rect.top=plane.rect.top+plane.rect.height
        elif self.direction == 'L':
            self.rect.left = plane.rect.left - plane.rect.width / 2 - self.rect.width / 2
            self.rect.top = plane.rect.top + plane.rect.width/2 - self.rect.width/2
        elif self.direction == 'R':
            self.rect.left=plane.rect.left+plane.rect.width
            self.rect.top=plane.rect.top+plane.rect.width/2 - self.rect.width/2

        self.speed = 6#子弹的速度
        self.live=True#子弹的转台,是否碰到墙壁，修改此状态

    def move(self):
        if self.direction == 'U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                self.live=False#修改子弹状态
        elif self.direction == 'D':
            if self.rect.top+self.rect.height<screen_heigh:
                self.rect.top+=self.speed
            else:
                self.live = False  # 修改子弹状态
        elif self.direction == 'R':
            if self.rect.left+self.rect.width<screen_width:
                self.rect.left+=self.speed
            else:
                self.live = False  # 修改子弹状态
        elif self.direction == 'L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                self.live = False  # 修改子弹状态

    def hitCloud(self):#子弹是否碰撞云
        for cloud in MainGame.cloudList:
            if pygame.sprite.collide_rect(self,cloud):
                self.live=False
                cloud.hp-=1
                if cloud.hp<=0:#修改云的生存状态
                    cloud.live=False
    def displayBullet(self):#显示子弹
        MainGame.window.blit(self.image,self.rect)

    def myBullet_hint_enemyPlane(self):#我方子弹与敌方飞机的碰撞
        for enemyPlane in MainGame.enemyPlaneList:#循环遍历敌方飞机列表，判断是否发生碰撞
            if pygame.sprite.collide_rect(enemyPlane,self):
                enemyPlane.live=False#修改敌方飞机和我方子弹的状态
                self.live=False
                explode=Explode(enemyPlane)#创建爆炸对象
                MainGame.explodeList.append(explode)
                music = Music('image/bang.wav')
                music.play()

    def enemyBullet_hit_myPlane(self):#敌方飞机与我方飞机碰撞
        if MainGame.my_plane and MainGame.my_plane.live:
            if pygame.sprite.collide_rect(MainGame.my_plane, self):
                explode=Explode(MainGame.my_plane)#产生爆炸对象
                MainGame.explodeList.append(explode)#将爆炸对象添加到爆炸列表中
                self.live=False#修改敌方子弹与我方飞机状态
                MainGame.my_plane.live=False
                music = Music('image/fire.wav')
                music.play()

class Cloud():
    def __init__(self,left,top):
        self.image=pygame.image.load('image/cloud.png')#加载云图片
        self.rect=self.image.get_rect()#获取云的区域
        self.rect.left=left#设置位置的left和top
        self.rect.top=top
        self.live=True#是否活着
        self.hp=5
    def displayCloud(self):
        MainGame.window.blit(self.image,self.rect)




class Explode():
    def __init__(self,plane):
        self.rect=plane.rect#爆炸位置由当前子弹打中的坦克位置决定
        self.images=[pygame.image.load('image/blast4.png'),
                     pygame.image.load('image/blast3.png'),
                     pygame.image.load('image/blast2.png'),
                     pygame.image.load('image/blast1.png'),
                     pygame.image.load('image/blast0.png'),
                     ]
        self.step=0
        self.image=self.images[self.step]
        self.live=True#是否活着

    def displayExplode(self):
        if self.step<len(self.images):
            self.image=self.images[self.step]#根据索引获取爆炸对象
            self.step+=1
            MainGame.window.blit(self.image,self.rect)#添加到主窗口
        else:#修改活着的状态
            self.live=False
            self.step=0


if __name__ =='__main__':
    MainGame().StartGame()