class keys: ## Contrôles 1J ##
    def __init__(self, keys_up=[],keys_down=[],keys_left=[],keys_right=[],keys_prev=[],keys_next=[],keys_reset=[]) -> None:
        self.keys_up = keys_up
        self.keys_down = keys_down
        self.keys_left = keys_left
        self.keys_right = keys_right
        self.keys_prev = keys_prev
        self.keys_next = keys_next
        self.keys_reset = keys_reset
        
if True:
    fl_g = 'left'
    fl_d = 'right'
    fl_h = 'up'
    fl_b = 'down'
    keys_up    = ['w', fl_h]
    keys_down  = ['s', fl_b]
    keys_left  = ['a', fl_g]
    keys_right = ['d', fl_d]
    keys_prev = ['p']
    keys_next     = ['n']
    keys_reset    = ['r']
    keys_j1 = keys(keys_up, keys_down, keys_left, keys_right, keys_prev, keys_next, keys_reset)
if False: ## Contrôles 2J ##
    ## J1 ##
    fl_g = 2424832
    fl_d = 2555904
    fl_h = 2490368
    fl_b = 2621440
    keys_hold = ['c']
    keys_soft_drop = [fl_b]
    keys_rotate = [fl_h]
    keys_left = [fl_g]
    keys_h_left = []
    keys_right = [fl_d]
    keys_h_right = []
    keys_pause = ['p']
    keys_rot_CCW = ['z']
    keys_rot_CW = ['x']
    rotate_clocwise = True
    ## J2 ##
    keys_hold = ['c']
    keys_soft_drop = [fl_b]
    keys_rotate = [fl_h]
    keys_left = [fl_g]
    keys_h_left = []
    keys_right = [fl_d]
    keys_h_right = []
    keys_pause = ['p']
    keys_rot_CCW = ['z']
    keys_rot_CW = ['x']
    rotate_clocwise = True