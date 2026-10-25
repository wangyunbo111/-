import pygame
import random
import sys, os

# ===================== 适配打包路径 =====================
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# ===================== 配置 =====================
MAX_SIZE = 9
CELL_BASE = 70
# 图片现在在 Picktrue 文件夹里
BG_FILE = get_resource_path("Picktrue/26.4 Snapshot 5.png")

pygame.init()
pygame.font.init()
font_num = pygame.font.SysFont("simhei", 32, bold=True)
font_info = pygame.font.SysFont("simhei", 24)
font_win = pygame.font.SysFont("simhei", 28, bold=True)

unlock = {3}
current_size = 3
board = []
empty_idx = 0
step_count = 0
win_text = ""

screen = pygame.display.set_mode((800, 700))
pygame.display.set_caption("数字华容道 Python版｜解锁至9×9")

bg_img = None
try:
    bg_img = pygame.image.load(BG_FILE).convert()
    bg_img = pygame.transform.scale(bg_img, (800, 700))
except Exception as e:
    print("背景图加载失败：", e)
    bg_img = None


def get_neighbors(idx, n):
    x = idx % n
    y = idx // n
    res = []
    if y > 0:
        res.append(idx - n)
    if y < n - 1:
        res.append(idx + n)
    if x > 0:
        res.append(idx - 1)
    if x < n - 1:
        res.append(idx + 1)
    return res


def shuffle_board(n):
    global empty_idx
    total = n * n
    board = list(range(1, total)) + [0]
    empty_idx = total - 1
    for _ in range(n * 100):
        neib = get_neighbors(empty_idx, n)
        pick = random.choice(neib)
        board[empty_idx], board[pick] = board[pick], board[empty_idx]
        empty_idx = pick
    return board


def init_board(n):
    global board, empty_idx, step_count, win_text
    step_count = 0
    win_text = ""
    board = shuffle_board(n)


def check_win(n):
    total = n * n
    for i in range(total - 1):
        if board[i] != i + 1:
            return False
    return True


def draw():
    screen.fill((30, 30, 30))
    if bg_img:
        screen.blit(bg_img, (0, 0))
        s = pygame.Surface((800, 700))
        s.set_alpha(100)
        s.fill((0, 0, 0))
        screen.blit(s, (0, 0))

    txt1 = font_info.render(f"当前：{current_size}×{current_size}  |  步数：{step_count}", True, (255,255,255))
    screen.blit(txt1, (20, 10))

    unlock_str = "、".join([f"{x}×{x}" for x in sorted(unlock)])
    txt2 = font_info.render(f"已解锁：{unlock_str}", True, (220,220,220))
    screen.blit(txt2, (20, 40))

    btn_y = 75
    btn_w, btn_h = 70, 32
    for s in range(3, MAX_SIZE + 1):
        rect = pygame.Rect(20 + (s-3)*(btn_w+6), btn_y, btn_w, btn_h)
        if s in unlock:
            color = (60, 90, 130)
        else:
            color = (40, 40, 40)
        pygame.draw.rect(screen, color, rect, border_radius=5)
        t = font_info.render(f"{s}×{s}", True, (255,255,255))
        screen.blit(t, (rect.x+12, rect.y+2))

    reset_rect = pygame.Rect(500, btn_y, 110, 32)
    pygame.draw.rect(screen, (60,90,130), reset_rect, border_radius=5)
    tr = font_info.render("重新打乱", True, (255,255,255))
    screen.blit(tr, (reset_rect.x+10, reset_rect.y+2))

    n = current_size
    cell_size = CELL_BASE - (n-3)*4
    gap = 4
    board_w = n * cell_size + (n-1)*gap
    ox = (800 - board_w)//2
    oy = 130

    for i, val in enumerate(board):
        cx = i % n
        cy = i // n
        x = ox + cx*(cell_size+gap)
        y = oy + cy*(cell_size+gap)
        r = pygame.Rect(x, y, cell_size, cell_size)
        if val == 0:
            pygame.draw.rect(screen, (15,15,15), r, border_radius=6)
        else:
            pygame.draw.rect(screen, (15, 50, 90), r, border_radius=6)
            num_surf = font_num.render(str(val), True, (255,255,255))
            screen.blit(num_surf, (x + cell_size//2 - num_surf.get_width()//2,
                                   y + cell_size//2 - num_surf.get_height()//2))

    if win_text:
        wt = font_win.render(win_text, True, (100, 255, 130))
        screen.blit(wt, (20, 620))

    pygame.display.flip()


def handle_click(mx, my):
    global current_size, board, empty_idx, step_count, win_text
    n = current_size

    btn_y = 75
    btn_w, btn_h = 70, 32
    for s in range(3, MAX_SIZE + 1):
        rect = pygame.Rect(20 + (s-3)*(btn_w+6), btn_y, btn_w, btn_h)
        if rect.collidepoint(mx, my):
            if s in unlock:
                current_size = s
                init_board(current_size)
            return

    reset_rect = pygame.Rect(500, btn_y, 110, 32)
    if reset_rect.collidepoint(mx, my):
        init_board(current_size)
        return

    cell_size = CELL_BASE - (n-3)*4
    gap = 4
    board_w = n * cell_size + (n-1)*gap
    ox = (800 - board_w)//2
    oy = 130
    for i, val in enumerate(board):
        cx = i % n
        cy = i // n
        x = ox + cx*(cell_size+gap)
        y = oy + cy*(cell_size+gap)
        r = pygame.Rect(x, y, cell_size, cell_size)
        if r.collidepoint(mx, my):
            neib = get_neighbors(empty_idx, n)
            if i in neib:
                board[empty_idx], board[i] = board[i], board[empty_idx]
                empty_idx = i
                step_count += 1
                if check_win(n):
                    if current_size >= MAX_SIZE:
                        win_text = f"🎉 通关 {current_size}×{current_size}！已是最高难度！"
                    else:
                        next_s = current_size + 1
                        win_text = f"🎉 通关 {current_size}×{current_size}！解锁 {next_s}×{next_s}"
                        unlock.add(next_s)
            return


init_board(current_size)
running = True
while running:
    draw()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = pygame.mouse.get_pos()
            handle_click(mx, my)

pygame.quit()
