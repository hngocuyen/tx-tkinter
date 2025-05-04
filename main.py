import tkinter as tk
from tkinter import messagebox, font as tkFont, scrolledtext
import random
import math
from collections import deque
import os
wd = 900
wh = 750
xx = 60
drr = 0.1
pra = 0.2
nen = '#282c34'
nencv = '#3c4048'
xxa = '#454a54'
gab = '#1e2127'
textcl = '#abb2bf'
bright = '#ffffff'
cvclor = '#8B4513'
grclor = '#484e5a'
tclor = '#ff4757'
erx = '#3742fa'
bb = '#ffa502'
btg = '#525965'
btf = bright
bttt = '#98c379'
btcl = '#e06c75'
wineffect = '#39FF14'
wineffect1 = '#ffd700'
htrml = 30
dbto = [50, 100, 500, 1000, 5000]
cctao = 15
oknhe = 5000
vaichuong = 2500
tilesaubamot = 0.2
canvastrum = 320
graphec = 250
CONTROL_uyencoder_HEIGHT = 130
cvtth = canvastrum + graphec + 20
mwit = 600
cwit = wd - mwit - 60
BOT_CHAT_MIN_DELAY = 1
BOT_CHAT_MAX_DELAY = 5
STATE_btTING = 'btTING'
STATE_WAITING_ROLL = 'WAITING_ROLL'
STATE_ROLLING = 'ROLLING'
STATE_REVEALING = 'REVEALING'
STATE_SHOWING_RESULT = 'SHOWING'
STATE_IDLE = 'IDLE'

class TaiXiuFinalCorrectedGame(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Tài Xỉu VIP - Chuẩn')
        self.geometry(f'{wd}x{wh}')
        self.resizable(False, False)
        self.configure(bg=nen)
        self.cfont()
        self.game_state = STATE_IDLE
        self.balance = 100000
        self.cumulative_bt_amount = 0
        self.final_bt_amount = 0
        self.selected_bt_choice = None
        self.current_selection_choice = None
        self.bt_confirmed_this_round = False
        self.dice_values = [1, 1, 1]
        self.result = ''
        self.total_score = 0
        self.history = deque(maxlen=htrml)
        self.can_reveal = False
        self.dice_item_ids = [[], [], []]
        self.cover_item_id = None
        self.canvas_countdown_text_id = None
        self.virtual_tai_bt = 0
        self.virtual2008iu_bt = 0
        self.is_dragging_cover = False
        self.drag_offset2008 = 0
        self.drag_offset1907 = 0
        self.btting_countdown_value = cctao
        self.btting_timer_id = None
        self.auto_reveal_timer_id = None
        self.bot_chat_timer_id = None
        self.win_effect_timer_id = None
        self.win_amount_effect_timer_id = None
        self.bot_chat_lines = self.load_chat_messages()
        self.tinh()
        self.taowd()
        self.taocanvas()
        self.updatesodu()
        self.update_cumulative_bt_display()
        self.cau()
        self.set_controls_state(STATE_IDLE)
        self.after(500, self.start_new_round)
        self.start_bot_chat_loop()
        self.protocol('WM_DELETE_WINDOW', self.on_close)

    def cfont(self):
        default_size = 10
        self.default_font = tkFont.Font(family='Segoe UI', size=default_size)
        self.bold_font = tkFont.Font(family='Segoe UI', size=default_size, weight='bold')
        self.large_bold_font = tkFont.Font(family='Segoe UI', size=default_size + 4, weight='bold')
        self.countdown_font = tkFont.Font(family='Segoe UI Semibold', size=default_size + 18, weight='bold')
        self.graph_point_font = tkFont.Font(family='Segoe UI', size=default_size - 2, weight='bold')
        self.graph_axis_font = tkFont.Font(family='Segoe UI', size=default_size - 2)
        self.result_font = tkFont.Font(family='Segoe UI', size=default_size + 2, weight='bold')
        self.chat_font = tkFont.Font(family='Segoe UI', size=default_size - 1)
        self.win_effect_font = tkFont.Font(family='Impact', size=default_size + 6)
        self.virtual_bt_font = tkFont.Font(family='Segoe UI', size=default_size - 1)
        self.win_amount_font = tkFont.Font(family='Segoe UI', size=default_size + 4, weight='bold')

    def tinh(self):
        self.pd = 10
        self.dg = 15
        total_dice_width = xx * 3 + self.dg * 2
        main_canvas_width_eff = mwit - 40
        self.dice_start2008 = (main_canvas_width_eff - total_dice_width) // 2 + 20
        self.dice1907 = canvastrum // 2 - xx // 2 - 20
        self.dice_uyencoder20081 = self.dice_start2008 - self.pd
        self.dice_uyencoder19071 = self.dice1907 - self.pd
        self.dice_uyencoder20082 = self.dice_start2008 + total_dice_width + self.pd
        self.dice_uyencoder19072 = self.dice1907 + xx + self.pd
        self.dice_uyencoder_center2008 = (self.dice_uyencoder20081 + self.dice_uyencoder20082) / 2
        self.dice_uyencoder_center1907 = (self.dice_uyencoder19071 + self.dice_uyencoder19072) / 2
        dice_uyencoder_width = self.dice_uyencoder20082 - self.dice_uyencoder20081
        dice_uyencoder_height = self.dice_uyencoder19072 - self.dice_uyencoder19071
        diameter = max(dice_uyencoder_width, dice_uyencoder_height) + 40
        radius = diameter / 2
        self.initial_cover20081 = self.dice_uyencoder_center2008 - radius
        self.initial_cover19071 = self.dice_uyencoder_center1907 - radius
        self.initial_cover20082 = self.dice_uyencoder_center2008 + radius
        self.initial_cover19072 = self.dice_uyencoder_center1907 + radius
        self.cover_width_actual = diameter
        self.cover_height_actual = diameter
        self.graph_uyencoder1907_start = canvastrum + 10
        self.graph_uyencoder2008_start = 40
        self.graph_uyencoder2008_end = mwit - 40 - 20
        self.graph_uyencoder1907_end = self.graph_uyencoder1907_start + graphec
        self.graph_width = self.graph_uyencoder2008_end - self.graph_uyencoder2008_start
        self.graphec_eff = graphec - 30
        self.graph1907_bottom = self.graph_uyencoder1907_end - 15
        self.graph1907_top = self.graph_uyencoder1907_start + 15

    def taowd(self):
        self.main_frame = tk.Frame(self, bg=nen)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=(10, 0))
        self.game_uyencoder_frame = tk.Frame(self.main_frame, bg=nen)
        self.game_uyencoder_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        self.info_frame = tk.Frame(self.game_uyencoder_frame, bg=nen, pady=5)
        self.info_frame.pack(fill=tk.X)
        self.balance_label = tk.Label(self.info_frame, text=f'Số dư: ${self.balance:,}', font=self.bold_font, bg=nen, fg=bright)
        self.balance_label.pack(side=tk.LEFT, padx=10)
        self.cumulative_bt_label = tk.Label(self.info_frame, text='Cược: $0', font=self.default_font, bg=nen, fg=textcl)
        self.cumulative_bt_label.pack(side=tk.RIGHT, padx=10)
        self.canvas = tk.Canvas(self.game_uyencoder_frame, width=mwit - 40, height=cvtth, bg=nencv, relief=tk.FLAT, bd=0, highlightthickness=0)
        self.canvas.pack(pady=5, fill=tk.X)
        self.virtual_bt_frame = tk.Frame(self.game_uyencoder_frame, bg=nencv)
        self.virtual_bt_frame.pack(fill=tk.X, pady=(0, 5))
        self.virtual_tai_label = tk.Label(self.virtual_bt_frame, text='TÀI: $0', font=self.virtual_bt_font, bg=nencv, fg=tclor)
        self.virtual_tai_label.pack(side=tk.LEFT, padx=30)
        self.virtual2008iu_label = tk.Label(self.virtual_bt_frame, text='XỈU: $0', font=self.virtual_bt_font, bg=nencv, fg=erx)
        self.virtual2008iu_label.pack(side=tk.RIGHT, padx=30)
        self.control_frame = tk.Frame(self.game_uyencoder_frame, bg=nen, pady=5)
        self.control_frame.pack(fill=tk.X, padx=10)
        self.control_frame.grid_rowconfigure((0, 1), weight=1)
        self.control_frame.grid_columnconfigure((0, 1, 2, 3, 4, 5), weight=1)
        style_args_tai = {'font': self.large_bold_font, 'width': 8, 'bg': tclor, 'fg': 'white', 'relief': tk.FLAT, 'pady': 5, 'state': tk.DISABLED}
        style_args2008iu = {'font': self.large_bold_font, 'width': 8, 'bg': erx, 'fg': 'white', 'relief': tk.FLAT, 'pady': 5, 'state': tk.DISABLED}
        self.bt_tai_button = tk.Button(self.control_frame, text='TÀI', command=lambda: self.select_choice('Tài'), **style_args_tai)
        self.bt_tai_button.grid(row=0, column=0, columnspan=3, padx=(0, 2), pady=5, sticky='ew')
        self.bt2008iu_button = tk.Button(self.control_frame, text='XỈU', command=lambda: self.select_choice('Xỉu'), **style_args2008iu)
        self.bt2008iu_button.grid(row=0, column=3, columnspan=3, padx=(2, 0), pady=5, sticky='ew')
        self.bottom_control_frame = tk.Frame(self.control_frame, bg=nen)
        self.bottom_control_frame.grid(row=1, column=0, columnspan=6, pady=(5, 0), sticky='ew')
        self.bt_options_frame = tk.Frame(self.bottom_control_frame, bg=nen)
        self.bt_options_frame.pack(side=tk.LEFT, padx=(0, 10))
        bt_btn_style = {'font': self.default_font, 'width': 5, 'bg': btg, 'fg': btf, 'relief': tk.FLAT, 'borderwidth': 1, 'state': tk.DISABLED}
        for amount in dbto:
            display_amount = f'{amount // 1000000}M' if amount >= 1000000 else f'{amount // 1000}K' if amount >= 1000 else str(amount)
            btn = tk.Button(self.bt_options_frame, text=display_amount, command=lambda a=amount: self.add_bt_amount(a), **bt_btn_style)
            btn.pack(side=tk.LEFT, padx=2)
        self.action_buttons_frame = tk.Frame(self.bottom_control_frame, bg=nen)
        self.action_buttons_frame.pack(side=tk.RIGHT)
        action_btn_base_style = {'width': 6, 'relief': tk.FLAT, 'borderwidth': 1, 'state': tk.DISABLED}
        self.all_in_button = tk.Button(self.action_buttons_frame, text='All In', command=self.all_in, bg='orange', fg='black', font=self.default_font, **action_btn_base_style)
        self.all_in_button.pack(side=tk.LEFT, padx=2)
        self.clear_bt_button = tk.Button(self.action_buttons_frame, text='Xóa', command=self.clear_bt, bg=btcl, fg='white', font=self.default_font, **action_btn_base_style)
        self.clear_bt_button.pack(side=tk.LEFT, padx=2)
        self.confirm_bt_button = tk.Button(self.action_buttons_frame, text='Cược', command=self.confirm_bt, bg=bttt, fg='black', font=self.bold_font, width=6, relief=tk.FLAT, borderwidth=1, state=tk.DISABLED)
        self.confirm_bt_button.pack(side=tk.LEFT, padx=2)
        self.chat_frame = tk.Frame(self.main_frame, bg=nen, width=cwit)
        self.chat_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        tk.Label(self.chat_frame, text=' Kênh Chat ', font=self.bold_font, bg='#454a54', fg=bright).pack(pady=(0, 5), fill=tk.X)
        self.chat_box = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, font=self.chat_font, state=tk.DISABLED, bd=0, relief=tk.FLAT, highlightthickness=0, bg='#2E3440', fg='#D8DEE9', width=int(cwit / 8), height=int(wh * 0.85 / 15))
        self.chat_box.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.result_frame = tk.Frame(self, bg=nen, pady=5)
        self.result_frame.pack(fill=tk.X, padx=10, side=tk.BOTTOM)
        self.win_amount_effect_label = tk.Label(self.result_frame, text='', font=self.win_amount_font, bg=nen, fg=wineffect1)
        self.win_amount_effect_label.pack()
        self.win_effect_label = tk.Label(self.result_frame, text='', font=self.win_effect_font, bg=nen, fg=wineffect)
        self.win_effect_label.pack()
        self.dice_result_label = tk.Label(self.result_frame, text='', font=self.bold_font, bg=nen, fg=bright, height=1)
        self.dice_result_label.pack()
        self.win_lose_label = tk.Label(self.result_frame, text='', font=self.result_font, bg=nen, height=1)
        self.win_lose_label.pack()

    def taocanvas(self):
        self.canvas.create_rectangle(self.dice_uyencoder20081, self.dice_uyencoder19071, self.dice_uyencoder20082, self.dice_uyencoder19072, fill=xxa, outline='', tags='xxa', state=tk.HIDDEN)
        self.cover_item_id = self.canvas.create_oval(self.initial_cover20081, self.initial_cover19071, self.initial_cover20082, self.initial_cover19072, fill=cvclor, outline='black', width=2, tags='cover', state=tk.HIDDEN)
        self.canvas.tag_bind('cover', '<ButtonPress-1>', self.on_cover_press)
        self.canvas.tag_bind('cover', '<B1-Motion>', self.on_cover_drag)
        self.canvas.tag_bind('cover', '<ButtonRelease-1>', self.on_cover_release)
        countdown_center1907 = self.dice_uyencoder_center1907
        self.canvas_countdown_text_id = self.canvas.create_text(self.dice_uyencoder_center2008, countdown_center1907, text='', font=self.countdown_font, fill='orange', anchor=tk.CENTER, state=tk.HIDDEN)
        self.canvas.create_rectangle(self.graph_uyencoder2008_start - 30, self.graph_uyencoder1907_start - 10, self.graph_uyencoder2008_end + 10, self.graph_uyencoder1907_end + 10, fill=gab, outline=grclor, tags='graph_bg', width=1)
        score_range = 18 - 3
        for score in range(3, 19):
            y = self.map_score_to1907(score)
            line_color = grclor
            self.canvas.create_line(self.graph_uyencoder2008_start, y, self.graph_uyencoder2008_end, y, fill=line_color, tags='graph_grid_h', width=1)
            if score % 3 == 0 or score == 18:
                self.canvas.create_text(self.graph_uyencoder2008_start - 10, y, text=str(score), anchor='e', fill=textcl, font=self.graph_axis_font, tags='graph_axis1907')
        num_v_lines = int(self.graph_width / 40)
        for i in range(1, num_v_lines + 1):
            x = self.graph_uyencoder2008_start + i * (self.graph_width / (num_v_lines + 1))
            self.canvas.create_line(x, self.graph1907_top, x, self.graph1907_bottom, fill=grclor, tags='graph_grid_v', width=1)

    def map_score_to1907(self, score):
        return self.graph1907_bottom - (score - 3) / (18 - 3) * self.graphec_eff

    def draw_die(self, x, y, size, value):
        item_ids = []
        bg_id = self.canvas.create_rectangle(x, y, x + size, y + size, fill='white', outline='black', width=1)
        item_ids.append(bg_id)
        padding = size * pra
        dot_radius = size * drr
        center2008 = x + size / 2
        center1907 = y + size / 2
        left2008 = x + padding
        right2008 = x + size - padding
        top1907 = y + padding
        mid1907 = center1907
        bottom1907 = y + size - padding
        dot_positions = {'top_left': (left2008, top1907), 'top_right': (right2008, top1907), 'mid_left': (left2008, mid1907), 'center': (center2008, center1907), 'mid_right': (right2008, mid1907), 'bottom_left': (left2008, bottom1907), 'bottom_right': (right2008, bottom1907)}
        dots_to_draw = []
        if value == 1:
            dots_to_draw = ['center']
        elif value == 2:
            dots_to_draw = ['top_left', 'bottom_right']
        elif value == 3:
            dots_to_draw = ['top_left', 'center', 'bottom_right']
        elif value == 4:
            dots_to_draw = ['top_left', 'top_right', 'bottom_left', 'bottom_right']
        elif value == 5:
            dots_to_draw = ['top_left', 'top_right', 'center', 'bottom_left', 'bottom_right']
        elif value == 6:
            dots_to_draw = ['top_left', 'top_right', 'mid_left', 'mid_right', 'bottom_left', 'bottom_right']
        elif value == '?':
            dots_to_draw = ['center']
        for pos_key in dots_to_draw:
            cx, cy = dot_positions[pos_key]
            dot_id = self.canvas.create_oval(cx - dot_radius, cy - dot_radius, cx + dot_radius, cy + dot_radius, fill='black', outline='')
            item_ids.append(dot_id)
        return item_ids

    def clear_all_dice_drawings(self):
        for i in range(3):
            self.clear_die_drawing(i)

    def clear_die_drawing(self, index):
        if 0 <= index < 3:
            for item_id in self.dice_item_ids[index]:
                try:
                    self.canvas.delete(item_id)
                except tk.TclError:
                    pass
            self.dice_item_ids[index] = []

    def update_dice_drawing(self, init=False):
        values_to_draw = [1, 1, 1] if init else self.dice_values
        self.clear_all_dice_drawings()
        for i in range(3):
            x = self.dice_start2008 + i * (xx + self.dg)
            self.dice_item_ids[i] = self.draw_die(x, self.dice1907, xx, values_to_draw[i])

    def updatesodu(self):
        self.balance_label.config(text=f'Số dư: ${self.balance:,}')

    def update_cumulative_bt_display(self):
        self.cumulative_bt_label.config(text=f'Đang cược: ${self.cumulative_bt_amount:,}')

    def update_virtual_bts_display(self):
        self.virtual_tai_label.config(text=f'TÀI: ${self.virtual_tai_bt:,}')
        self.virtual2008iu_label.config(text=f'XỈU: ${self.virtual2008iu_bt:,}')

    def set_controls_state(self, state):
        is_btting = state == STATE_btTING
        can_interact_bt = is_btting and (not self.bt_confirmed_this_round)
        bt_choice_state = tk.NORMAL if can_interact_bt else tk.DISABLED
        self.bt_tai_button.config(state=bt_choice_state)
        self.bt2008iu_button.config(state=bt_choice_state)
        if is_btting:
            self.bt_tai_button.config(bg=tclor, relief=tk.FLAT if self.current_selection_choice != 'Tài' else tk.SUNKEN)
            self.bt2008iu_button.config(bg=erx, relief=tk.FLAT if self.current_selection_choice != 'Xỉu' else tk.SUNKEN)
            if self.current_selection_choice == 'Tài':
                self.bt_tai_button.config(bg='#cc3a3a')
            if self.current_selection_choice == 'Xỉu':
                self.bt2008iu_button.config(bg='#2c34c7')
        else:
            self.bt_tai_button.config(state=tk.DISABLED, bg='#555555', relief=tk.FLAT)
            self.bt2008iu_button.config(state=tk.DISABLED, bg='#555555', relief=tk.FLAT)
        bt_option_state = tk.NORMAL if can_interact_bt else tk.DISABLED
        for widget in self.bt_options_frame.winfo_children():
            widget.config(state=bt_option_state)
        self.all_in_button.config(state=bt_option_state)
        self.clear_bt_button.config(state=bt_option_state)
        self.update_confirm_button_state()
        if self.balance <= 0 and (not is_btting):
            self.bt_tai_button.config(state=tk.DISABLED, bg='#555555')
            self.bt2008iu_button.config(state=tk.DISABLED, bg='#555555')
            for widget in self.bt_options_frame.winfo_children():
                widget.config(state=tk.DISABLED)
            self.all_in_button.config(state=tk.DISABLED)
            self.clear_bt_button.config(state=tk.DISABLED)
            self.confirm_bt_button.config(state=tk.DISABLED)

    def update_confirm_button_state(self):
        if self.game_state == STATE_btTING and (not self.bt_confirmed_this_round):
            can_confirm = self.current_selection_choice is not None and self.cumulative_bt_amount > 0 and (self.cumulative_bt_amount <= self.balance)
            self.confirm_bt_button.config(state=tk.NORMAL if can_confirm else tk.DISABLED)
        else:
            self.confirm_bt_button.config(state=tk.DISABLED)

    def start_new_round(self):
        print('\n--- Bắt đầu vòng mới (Giai đoạn cược 15s) ---')
        self.game_state = STATE_btTING
        self.cancel_timers()
        self.cumulative_bt_amount = 0
        self.final_bt_amount = 0
        self.selected_bt_choice = None
        self.current_selection_choice = None
        self.bt_confirmed_this_round = False
        self.can_reveal = False
        self.update_cumulative_bt_display()
        self.set_controls_state(STATE_btTING)
        self.virtual_tai_bt = random.randint(5000, 200000)
        self.virtual2008iu_bt = random.randint(5000, 200000)
        self.update_virtual_bts_display()
        self.clear_all_dice_drawings()
        try:
            if self.cover_item_id:
                self.canvas.itemconfig(self.cover_item_id, state=tk.HIDDEN)
            if self.canvas_countdown_text_id:
                self.canvas.itemconfig(self.canvas_countdown_text_id, state=tk.NORMAL)
            self.canvas.itemconfig('xxa', state=tk.HIDDEN)
        except tk.TclError:
            pass
        self.win_lose_label.config(text='')
        self.dice_result_label.config(text='')
        self.clear_win_effect()
        self.clear_win_amount_effect()
        self.btting_countdown_value = cctao
        self.update_btting_countdown()

    def update_btting_countdown(self):
        if self.game_state != STATE_btTING and self.game_state != STATE_WAITING_ROLL:
            if self.canvas_countdown_text_id:
                try:
                    self.canvas.itemconfig(self.canvas_countdown_text_id, text='')
                except tk.TclError:
                    pass
            self.btting_timer_id = None
            return
        if self.btting_countdown_value >= 0:
            if self.canvas_countdown_text_id:
                try:
                    self.canvas.itemconfig(self.canvas_countdown_text_id, text=f'{self.btting_countdown_value}')
                    self.canvas.tag_raise(self.canvas_countdown_text_id)
                except tk.TclError:
                    pass
            self.btting_countdown_value -= 1
            self.btting_timer_id = self.after(1000, self.update_btting_countdown)
        else:
            print(' -> Hết giờ cược.')
            if self.canvas_countdown_text_id:
                try:
                    self.canvas.itemconfig(self.canvas_countdown_text_id, state=tk.HIDDEN)
                except tk.TclError:
                    pass
            self.btting_timer_id = None
            self.end_btting_phase(timeout=True)

    def add_bt_amount(self, amount):
        if self.game_state != STATE_btTING or self.bt_confirmed_this_round:
            return
        new_bt = self.cumulative_bt_amount + amount
        self.cumulative_bt_amount = min(new_bt, self.balance)
        self.update_cumulative_bt_display()
        self.update_confirm_button_state()

    def all_in(self):
        if self.game_state != STATE_btTING or self.bt_confirmed_this_round:
            return
        self.cumulative_bt_amount = self.balance
        self.update_cumulative_bt_display()
        self.update_confirm_button_state()

    def clear_bt(self):
        if self.game_state != STATE_btTING or self.bt_confirmed_this_round:
            return
        self.cumulative_bt_amount = 0
        self.update_cumulative_bt_display()
        self.update_confirm_button_state()

    def select_choice(self, choice):
        if self.game_state != STATE_btTING or self.bt_confirmed_this_round:
            return
        self.current_selection_choice = choice
        print(f' -> Đã chọn (chưa xác nhận): {choice}')
        if choice == 'Tài':
            self.bt_tai_button.config(relief=tk.SUNKEN, bg='#cc3a3a')
            self.bt2008iu_button.config(relief=tk.FLAT, bg=erx)
        else:
            self.bt2008iu_button.config(relief=tk.SUNKEN, bg='#2c34c7')
            self.bt_tai_button.config(relief=tk.FLAT, bg=tclor)
        self.update_confirm_button_state()

    def confirm_bt(self):
        if self.game_state != STATE_btTING:
            return
        if self.current_selection_choice is None:
            messagebox.showwarning('Chưa chọn cửa', 'Vui lòng chọn TÀI hoặc XỈU.')
            return
        if self.cumulative_bt_amount <= 0:
            messagebox.showwarning('Chưa đặt tiền', 'Vui lòng chọn mức cược.')
            return
        if self.cumulative_bt_amount > self.balance:
            messagebox.showwarning('Không đủ số dư', 'Số tiền cược vượt quá số dư.')
            return
        self.final_bt_amount = self.cumulative_bt_amount
        self.selected_bt_choice = self.current_selection_choice
        self.bt_confirmed_this_round = True
        print(f' -> Xác nhận cược: {self.selected_bt_choice} - ${self.final_bt_amount:,} (Chờ hết giờ)')
        if self.selected_bt_choice == 'Tài':
            self.virtual_tai_bt += int(self.final_bt_amount * random.uniform(1.5, 5.0))
        else:
            self.virtual2008iu_bt += int(self.final_bt_amount * random.uniform(1.5, 5.0))
        self.update_virtual_bts_display()
        self.game_state = STATE_WAITING_ROLL
        self.set_controls_state(STATE_WAITING_ROLL)

    def end_btting_phase(self, timeout=False):
        if self.game_state not in [STATE_btTING, STATE_WAITING_ROLL]:
            return
        self.cancel_btting_timer()
        if self.canvas_countdown_text_id:
            try:
                self.canvas.itemconfig(self.canvas_countdown_text_id, state=tk.HIDDEN)
            except tk.TclError:
                pass
        if timeout and (not self.bt_confirmed_this_round):
            if self.current_selection_choice is not None and self.cumulative_bt_amount > 0 and (self.cumulative_bt_amount <= self.balance):
                self.final_bt_amount = self.cumulative_bt_amount
                self.selected_bt_choice = self.current_selection_choice
                print(f' -> Hết giờ, tự động xác nhận cược: {self.selected_bt_choice} - ${self.final_bt_amount:,}')
                if self.selected_bt_choice == 'Tài':
                    self.virtual_tai_bt += int(self.final_bt_amount * random.uniform(0.5, 2.0))
                else:
                    self.virtual2008iu_bt += int(self.final_bt_amount * random.uniform(0.5, 2.0))
                self.update_virtual_bts_display()
            else:
                print(' -> Hết giờ, không có cược hợp lệ. Chỉ lắc.')
                self.final_bt_amount = 0
                self.selected_bt_choice = None
        self.game_state = STATE_ROLLING
        self.set_controls_state(STATE_ROLLING)
        self.execute_roll()

    def execute_roll(self):
        print(' -> Đang lắc...')
        if random.random() < tilesaubamot:
            combo = [1, 3, 6]
            random.shuffle(combo)
            self.dice_values = combo
            print('  -> Ra bộ đặc biệt (1-3-6)!')
        else:
            self.dice_values = [random.randint(1, 6) for _ in range(3)]
        self.total_score = sum(self.dice_values)
        is_triple = len(set(self.dice_values)) == 1 and set(self.dice_values) != {1, 3, 6}
        is_special_combo = set(self.dice_values) == {1, 3, 6}
        result_code = '?'
        if is_triple:
            self.result = 'Bộ Ba'
            result_code = 'B'
        elif is_special_combo:
            self.result = 'Xỉu'
            result_code = 'X'
        elif 4 <= self.total_score <= 10:
            self.result = 'Xỉu'
            result_code = 'X'
        elif 11 <= self.total_score <= 17:
            self.result = 'Tài'
            result_code = 'T'
        else:
            self.result = '??'
        self.history.append({'code': result_code, 'score': self.total_score})
        try:
            self.canvas.itemconfig('xxa', state=tk.NORMAL)
        except tk.TclError:
            pass
        self.update_dice_drawing()
        if self.cover_item_id:
            self.reset_cover_position()
            try:
                self.canvas.itemconfig(self.cover_item_id, state=tk.NORMAL)
                self.canvas.tag_raise(self.cover_item_id)
            except tk.TclError:
                pass
        self.game_state = STATE_REVEALING
        self.can_reveal = True
        print(' -> Lắc xong, bắt đầu chờ mở 5 giây.')
        self.cancel_auto_reveal_timer()
        self.auto_reveal_timer_id = self.after(oknhe, self.auto_reveal)

    def auto_reveal(self):
        print(' -> Hết 5 giây chờ mở.')
        if self.game_state == STATE_REVEALING:
            print('   -> Tự động hiển thị kết quả.')
            self.show_final_result()
        self.auto_reveal_timer_id = None

    def show_final_result(self):
        if self.game_state not in [STATE_REVEALING, STATE_ROLLING]:
            return
        if self.win_lose_label.cget('text') != '':
            return
        self.game_state = STATE_SHOWING_RESULT
        self.cancel_auto_reveal_timer()
        self.can_reveal = False
        print(f' -> Hiển thị kết quả: {self.result} - {self.total_score}')
        win = False
        msg = ''
        win_amount = 0
        if self.final_bt_amount > 0 and self.selected_bt_choice:
            if self.result == 'Bộ Ba':
                win = False
                msg = f'Bộ ba! Thua -${self.final_bt_amount:,}'
            elif self.selected_bt_choice == self.result:
                win = True
                win_amount = int(self.final_bt_amount * 0.95)
                msg = f'Thắng!'
            else:
                win = False
                msg = f'Thua -${self.final_bt_amount:,}'
            original_balance = self.balance
            if win:
                self.balance += win_amount
            else:
                self.balance -= self.final_bt_amount
            if self.balance < 0:
                self.balance = 0
            self.updatesodu()
            if win:
                self.win_amount_effect_label.config(text=f'+{win_amount:,}')
                self.clear_win_amount_effect_timer()
                self.win_amount_effect_timer_id = self.after(vaichuong + 500, self.clear_win_amount_effect)
            if original_balance > 0 and self.balance <= 0:
                messagebox.showinfo('Hết tiền', 'Bạn đã hết tiền!')
        else:
            msg = 'Không cược'
            self.win_lose_label.config(fg=textcl)
        dice_str = ' - '.join(map(str, self.dice_values))
        self.dice_result_label.config(text=f'{dice_str} ({self.total_score}đ) -> {self.result}')
        if self.final_bt_amount > 0 and self.selected_bt_choice:
            self.win_lose_label.config(text=msg, fg=wineffect if win else '#FF6347')
            if win:
                self.win_effect_label.config(text='THẮNG LỚN!')
                self.clear_win_effect_timer()
                self.win_effect_timer_id = self.after(vaichuong, self.clear_win_effect)
        else:
            self.win_lose_label.config(text=msg)
        self.cau()
        self.cumulative_bt_amount = 0
        self.update_cumulative_bt_display()
        delay_before_new_round = 3000
        self.after(delay_before_new_round, self.start_new_round)
        self.set_controls_state(STATE_SHOWING_RESULT)

    def clear_win_effect(self):
        self.win_effect_label.config(text='')
        self.win_effect_timer_id = None

    def clear_win_effect_timer(self):
        if self.win_effect_timer_id:
            self.after_cancel(self.win_effect_timer_id)
            self.win_effect_timer_id = None

    def clear_win_amount_effect(self):
        self.win_amount_effect_label.config(text='')
        self.win_amount_effect_timer_id = None

    def clear_win_amount_effect_timer(self):
        if self.win_amount_effect_timer_id:
            self.after_cancel(self.win_amount_effect_timer_id)
            self.win_amount_effect_timer_id = None

    def cau(self):
        self.canvas.delete('graph_points')
        history_len = len(self.history)
        if history_len == 0:
            return
        point_radius = 9
        line_width = 2
        coords_list = []
        x_spacing = self.graph_width / (htrml - 1) if htrml > 1 else self.graph_width
        start_index = max(0, history_len - htrml)
        drawable_history = list(self.history)[start_index:]
        for i, data in enumerate(drawable_history):
            res_code = data['code']
            score = data['score']
            x = self.graph_uyencoder2008_start + i * x_spacing
            y = self.map_score_to1907(score)
            color = '#cccccc'
            if res_code == 'T':
                color = tclor
            elif res_code == 'X':
                color = erx
            elif res_code == 'B':
                color = bb
            else:
                color = 'grey'
            self.canvas.create_oval(x - point_radius, y - point_radius, x + point_radius, y + point_radius, fill=color, outline='white', width=1.5, tags='graph_points')
            self.canvas.create_text(x, y, text=str(score), fill='white', font=self.graph_point_font, tags='graph_points')
            coords_list.extend([x, y])
        if len(coords_list) >= 4:
            self.canvas.create_line(coords_list, fill='#aaaaaa', width=line_width, tags='graph_points', smooth=False)

    def reset_cover_position(self):
        try:
            if not self.cover_item_id:
                return
            coords = self.canvas.coords(self.cover_item_id)
            if not coords:
                return
            current20081, current19071 = (coords[0], coords[1])
            delta2008 = self.initial_cover20081 - current20081
            delta1907 = self.initial_cover19071 - current19071
            if delta2008 != 0 or delta1907 != 0:
                self.canvas.move(self.cover_item_id, delta2008, delta1907)
            self.canvas.tag_raise(self.cover_item_id)
        except tk.TclError:
            pass

    def on_cover_press(self, event):
        if self.game_state != STATE_REVEALING:
            return
        items = self.canvas.find_withtag(tk.CURRENT)
        if self.cover_item_id in items:
            self.is_dragging_cover = True
            try:
                cover_coords = self.canvas.coords(self.cover_item_id)
                self.drag_offset2008 = event.x - cover_coords[0]
                self.drag_offset1907 = event.y - cover_coords[1]
                self.canvas.tag_raise(self.cover_item_id)
            except tk.TclError:
                pass

    def on_cover_drag(self, event):
        if not self.is_dragging_cover or self.game_state != STATE_REVEALING:
            return
        new20081 = event.x - self.drag_offset2008
        new19071 = event.y - self.drag_offset1907
        new20082 = new20081 + self.cover_width_actual
        new19072 = new19071 + self.cover_height_actual
        try:
            self.canvas.coords(self.cover_item_id, new20081, new19071, new20082, new19072)
        except tk.TclError:
            pass

    def on_cover_release(self, event):
        if not self.is_dragging_cover:
            return
        self.is_dragging_cover = False
        if self.game_state == STATE_REVEALING and (not self.is_cover_sufficiently_over_dice()):
            print(' -> Người dùng tự mở bát!')
            self.show_final_result()

    def is_cover_sufficiently_over_dice(self):
        try:
            if not self.cover_item_id:
                return False
            cover_coords = self.canvas.coords(self.cover_item_id)
        except tk.TclError:
            return False
        if not cover_coords:
            return False
        cx1, cy1, cx2, cy2 = cover_coords
        cover_center2008 = (cx1 + cx2) / 2
        cover_center1907 = (cy1 + cy2) / 2
        dice_uyencoder_center2008 = (self.dice_uyencoder20081 + self.dice_uyencoder20082) / 2
        dice_uyencoder_center1907 = (self.dice_uyencoder19071 + self.dice_uyencoder19072) / 2
        distance = math.sqrt((cover_center2008 - dice_uyencoder_center2008) ** 2 + (cover_center1907 - dice_uyencoder_center1907) ** 2)
        allowed_distance = (self.dice_uyencoder20082 - self.dice_uyencoder20081) / 2.5
        return distance < allowed_distance

    def load_chat_messages(self, filename='chat_messages.txt'):
        if not os.path.exists(filename):
            print(f"Warning:'{filename}' not found. Creating sample file.")
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write('Bắt đầu nào!\n')
                    f.write('Chúc anh em may mắn.\n')
                return ['Bắt đầu nào!', 'Chúc anh em may mắn.']
            except Exception as e:
                print(f'Error creating sample chat file: {e}')
                return ['Chat error.']
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = [line.strip() for line in f if line.strip()]
            return lines if lines else ['Chat file is empty.']
        except Exception as e:
            print(f"Error reading chat file '{filename}': {e}")
            return ['Chat error.']

    def start_bot_chat_loop(self):
        self.cancel_bot_chat_timer()
        self.post_bot_message()

    def post_bot_message(self):
        if not self.bot_chat_lines:
            return
        message = random.choice(self.bot_chat_lines)
        prefix = random.choice(["BotVip", "CaoThuẩn", "LínhMới", "MaCao", "Admin","HungPro", "NoHope", "SoaiCa123", "MeoDen", "GaChien","XiuXiu", "TaiTai", "NhanhNhuChop", "ChayBo", "KinhKong","NoobKing", "ThuaNuaRoi", "SieuNhan", "VIPBoy", "ZzChanLezZ","ThienDiaHoi", "TamQuoc", "TuongThan", "NinjaAoDen", "GaiXinh2002","MocDai", "GiauThatSu", "BanTai123", "VoDich", "KeCauMay","KeCuopBanh", "FanXiu", "TaiChay", "AdminBot", "CaoThuFake","No1TaiXiu", "KeThuaCuoc", "MienNam1", "ThuaRoiBo", "XacSong","ThanTai", "DenHetSuc", "CayTheGioi", "SoKeo", "GaoNepGaoTe","GaFullNoc", "KyLanDen", "Pro7sao", "VipKhongKhoe", "GameThuLaGi","TaiCay", "NguLam", "ThichAnThua", "HotGirlBaoXau", "MeoXauTinh","TrumCuoi", "ThanhNienCoDon", "TamLyBatOn", "DanChoXom", "TraiLangBen","LaoHacTaiXiu", "ZzXiuZz", "PhucBac", "BoyCauCa", "NguoiTuongLai","BotBanTai", "HeoCon", "ChayTien", "ChuyenNghiep", "DaiGiaAo","ThichGiaiTri", "DanBien", "DanhThue", "CuocDoiBot", "NhaCaiGiau","BoLaChienThang", "ProTai", "ThuaDenVang", "SoDoDep", "SiCo","VoDoiXiu", "LayVoBot", "GhetAdmin", "NguoiBiAn", "KeSanTai","FanChuot", "MauThua", "SuyNghiLai", "CoLenNao", "DoiChutThoi","NguoiLa", "DaiCaXom", "TrumXom", "AoDenVaoGame", "GaChoKhoc","BotCungKhoc", "TaiXiuOnline", "HoiBotXiu", "VoNghich", "KhocTrongGame","NangTieuThu", "MeTai", "VoXiu", "TamLyThatThu", "KhoChoiVcl","TeamAllIn", "NghiThat", "TaiLaChanLy", "XiuViTinhYeu", "BotMayMan"])

        try:
            self.chat_box.config(state=tk.NORMAL)
            self.chat_box.insert(tk.END, f'{prefix}: {message}\n', ('bot_message',))
            self.chat_box.see(tk.END)
            self.chat_box.config(state=tk.DISABLED)
            self.chat_box.tag_config('bot_message', foreground='#98c379')
        except tk.TclError:
            print('Lỗi khi cập nhật chat box (có thể đã đóng)')
            self.cancel_bot_chat_timer()
            return
        delay = random.randint(BOT_CHAT_MIN_DELAY, BOT_CHAT_MAX_DELAY)
        self.bot_chat_timer_id = self.after(delay, self.post_bot_message)

    def cancel_bot_chat_timer(self):
        if self.bot_chat_timer_id:
            self.after_cancel(self.bot_chat_timer_id)
            self.bot_chat_timer_id = None

    def cancel_timers(self):
        self.cancel_btting_timer()
        self.cancel_auto_reveal_timer()
        self.cancel_bot_chat_timer()
        self.clear_win_effect_timer()
        self.clear_win_amount_effect_timer()

    def cancel_btting_timer(self):
        if self.btting_timer_id:
            self.after_cancel(self.btting_timer_id)
            self.btting_timer_id = None
        if self.canvas_countdown_text_id:
            try:
                self.canvas.itemconfig(self.canvas_countdown_text_id, text='')
            except tk.TclError:
                pass

    def cancel_auto_reveal_timer(self):
        if self.auto_reveal_timer_id:
            self.after_cancel(self.auto_reveal_timer_id)
            self.auto_reveal_timer_id = None

    def on_close(self):
        print('Closing application.')
        self.cancel_timers()
        self.destroy()
TaiXiuFinalCorrectedGame().mainloop()
