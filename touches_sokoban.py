class keys: ## Contrôles 1J ##
    def __init__(self, keys_up=[],keys_down=[],keys_left=[],keys_right=[],keys_prev=[],keys_next=[],keys_reset=[],keys_endg=[]) -> None:
        self.keys_up = keys_up
        self.keys_down = keys_down
        self.keys_left = keys_left
        self.keys_right = keys_right
        self.keys_prev = keys_prev
        self.keys_next = keys_next
        self.keys_reset = keys_reset
        self.keys_endg = keys_endg
        
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
    keys_endg     = ['esc']
    keys_j1 = keys(keys_up, keys_down, keys_left, keys_right, keys_prev, keys_next, keys_reset, keys_endg)