from drawing import Drawer
from game_object import IBlock, OBlock, TBlock, LBlock, JBlock, SBlock, ZBlock
import random
import time
import keyboard

#테트리스 클래스
class Tetris:
    def __init__(self):
        #그리기 모듈 생성
        self.drawer = Drawer(30, 30)
        self.drawer.clear()
        self.drawer.set_cursor_visible(False)

        #사용가능한 블록들의 종류
        self.BLOCK_LIST = [IBlock, OBlock, TBlock,
                           LBlock, JBlock, SBlock, ZBlock]
        #블록을 담는 상자 12 x 24
        self.box_w = 12     #상자의 가로길이
        self.box_h = 24     #상자의 세로길이
        self.box = []

        for w in range(self.box_w):
            self.box.append([None] * self.box_h)

        # 태두리 배경 12 x 24
        self.bg_w = 12
        self.bg_h = 24
        self.background = []    #'■' 로 테두리를 감싼다.

        for x in range(self.bg_w):
            self.background.append([''] * self.bg_h)
            for y in range(self.bg_h):
                # 벽
                if not (1 <= x <= self.bg_w - 2 and 0 <= y <= self.bg_h - 2):
                    self.background[x][y] = '■'
                #경계선
                elif (1 <= x <= self.bg_w - 2) and y == 2:
                    self.background[x][y] = '--'  #ㅂ 누르고 한자한다음 첫번째 문자 2개
                # 빈 공간
                else:
                    self.background[x][y] = '  ' # <- 띄어쓰기 2번

        # 미리보기 칸
        self.pv_w = 7
        self.pv_h = 7
        self.preview = []
        for x in range(self.pv_w):
            self.preview.append([''] * self.pv_h)
            for y in range(self.pv_h):
                if not (1 <= x <= self.pv_w - 2 and 1 <= y <= self.pv_h - 2):
                    self.preview[x][y] = '■'
                else:
                    self.preview[x][y] = '  '  #띄어쓰기 2번

        # 내가 현재 컨트롤중인 블록
        self.focus = self.create_random_block([self.box_w // 2, 0])
        #생성된 컨트롤 블록이 I, J, L 중 하나면 y좌표를 1로 설정한다.
        if type(self.focus) in (IBlock, JBlock, LBlock):
            self.focus.set_pivot([self.box_w // 2, 1])

        #다음에 내려올 블록
        self.next = self.create_random_block([self.box_w + self.pv_w // 2, self.pv_h // 2])

    #게임 내에 존재하는 모든 오브젝트를 그리자
    def draw_all(self):
        #게임 배경을 그린다.
        for x in range(self.bg_w):
            for y in range(self.bg_h):
                self.drawer.print_at(x, y, self.background[x][y])

        #박스에 담긴 블럭들을 그린다.
        for x in range(self.box_w):
            for y in range(self.box_h):
                if self.box[x][y] is not None:
                    self.box[x][y].draw(self.drawer)

        #미리보기 칸을 그린다.
        for x in range(self.pv_w):
            for y in range(self.pv_h):
                self.drawer.print_at(x + self.bg_w, y, self.preview[x][y])

        #미리보기 블록을 그린다
        self.next.draw(self.drawer)
        #현재 컨트롤 중인 블록을 그린다.
        self.focus.draw(self.drawer)

        self.drawer.flush()
    # BLOCK_LIST에서 랜덤한 블록 클래스를 하나 골라 저장된 위치에 블록을 생성한다.
    def create_random_block(self, coordinate):
        block_class = random.choice(self.BLOCK_LIST)
        return block_class(coordinate)

    def is_ground(self):
        for block in self.focus.blocks:
            x = block.coord[0]
            down_y = block.coord[1] + 1
            if down_y == self.box_h -1 or self.box[x][down_y] is not None:
                return True
        return False


    #fcous블럭이 움직이는 방향에 벽이 있는지 판별하는 매서드.
    def is_wall(self, x_offset):
        for block in self.focus.blocks:
            move_x = block.coord[0] + x_offset
            y = block.coord[1]
            if move_x == 0 or move_x == self.box_w - 1 or self.box[move_x][y] is not None:
                return True
        return False



    def fix_block(self):
        for block in self.focus.blocks:
            x = block.coord[0]
            y = block.coord[1]
            self.box[x][y] = block
        self.focus = self.next
        self.focus.set_pivot([self.box_w // 2, 0])
        if type(self.focus) in (IBlock, JBlock, LBlock):
            self.focus.set_pivot([self.box_w // 2, 1])
        self.next = self.create_random_block([self.box_w + self.pv_w // 2, self.pv_h // 2])

    def go_down(self):
        self.focus.move_offset([0, 1])
        pass

    def go_left(self):
        self.focus.move_offset([-1, 0])
        pass

    def go_right(self):
        self.focus.move_offset([1, 0])
        pass

    def turn_cw(self):
        self.focus.turn_cw()
        for block in self.focus.blocks:
            x = block.coord[0]
            y = block.coord[1]
            if x <= 0 or x >= self.box_w - 1 or y >= self.box_h - 1 or self.box[x][y] is not None:
               self.focus.turn_ccw()
               break


    def turn_ccw(self):
        self.focus.turn_ccw()
        self.focus.turn_cw()
        for block in self.focus.blocks:
            x = block.coord[0]
            y = block.coord[1]
            if x <= 0 or x >= self.box_w - 1 or y >= self.box_h - 1 or self.box[x][y] is not None:
               self.focus.turn_cw()
               break


    #게임을 진행한다.
    def run(self):
        is_run = True

        fps = 0
        dps = 0
        mps = 0

        prev_time = time.time()       #이전 시간(루프가 한바퀴 돌기 전)
        while is_run:
            curr_time = time.time()     #현재 시간(루프가 돌고 난후)
            loop_time = curr_time - prev_time      #루프가 한바퀴 도는데 걸리는 시간

            #루프를 도는데 걸리는 시간 계속 누적합산
            dps += loop_time
            mps += loop_time
            fps += loop_time

            # 1/30초 마다 화면을 그려준다(30fps)
            if fps >= 1/30:
                self.draw_all()

            # 0.5초 마다 블럭이 한칸씩 내린다.
            if dps >= 0.5:
                if self.is_ground():
                    self.fix_block()
                self.go_down()
                dps = 0
            #최소0.1초마다 움직일 수 있다.
            if mps >= 0.1:
                #왼쪽 방향키를 누른 경우
                if keyboard.is_pressed("left"):
                    if not self.is_wall(-1):
                        self.go_left()
                        mps = 0
                #오른쪽 방향키를 누른 경우
                if keyboard.is_pressed("right"):
                    if not self.is_wall(1):
                        self.go_right()
                        mps = 0
                if keyboard.is_pressed("down"):
                    if not self.is_ground():
                        self.go_down()
                        mps = 0
                        dps = 0
                    else:
                        self.fix_block()
                        mps = 0
                        dps = 0

                if keyboard.is_pressed("z"):
                    self.turn_ccw()
                    mps = 0

                if keyboard.is_pressed("x"):
                    self.turn_cw()
                    mps = 0


            prev_time = curr_time
        pass


tetris = Tetris()
tetris.run()
