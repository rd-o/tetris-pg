import numpy as np

# Action map
start_y = 24

feature_names = [
    'agg_height', 'n_holes', 'bumpiness', 'cleared', 'num_pits', 'max_wells',
    'n_cols_with_holes', 'row_transitions', 'col_transitions'
]


def get_current_block_text(block_tile):
    match block_tile.shape:
        case 0:
            return 'T'
        case 1:
            return 'O'
        case 2:
            return 'I'
        case 3:
            return 'S'
        case 4:
            return 'Z'
        case 5:
            return 'L'
        case 6:
            return 'J'

def get_board_info(area, tetris, s_lines):
    """
    area: a numpy matrix representation of the board
    tetris: game wrapper
    s_lines: the starting number of cleared lines
    """
    # Columns heights
    peaks = get_peaks(area)
    highest_peak = np.max(peaks)

    # Aggregated height
    agg_height = np.sum(peaks)

    holes = get_holes(peaks, area)
    # Number of empty holes
    n_holes = np.sum(holes)
    # Number of columns with at least one hole
    n_cols_with_holes = np.count_nonzero(np.array(holes) > 0)

    # Row transitions
    row_transitions = get_row_transition(area, highest_peak)

    # Columns transitions
    col_transitions = get_col_transition(area, peaks)

    # Abs height differences between consecutive cols
    bumpiness = get_bumpiness(peaks)

    # Number of cols with zero blocks
    num_pits = np.count_nonzero(np.count_nonzero(area, axis=0) == 0)

    wells = get_wells(peaks)
    # Deepest well
    max_wells = np.max(wells)

    # The number of lines gained with the move
    cleared = (tetris.lines - s_lines) * 8

    return agg_height, n_holes, bumpiness, cleared, num_pits, max_wells, \
        n_cols_with_holes, row_transitions, col_transitions


def get_peaks(area):
    peaks = np.array([])
    for col in range(area.shape[1]):
        if 1 in area[:, col]:
            p = area.shape[0] - np.argmax(area[:, col], axis=0)
            peaks = np.append(peaks, p)
        else:
            peaks = np.append(peaks, 0)
    return peaks


def get_row_transition(area, highest_peak):
    sum = 0
    # From highest peak to bottom
    for row in range(int(area.shape[0] - highest_peak), area.shape[0]):
        for col in range(1, area.shape[1]):
            if area[row, col] != area[row, col - 1]:
                sum += 1
    return sum


def get_col_transition(area, peaks):
    sum = 0
    for col in range(area.shape[1]):
        if peaks[col] <= 1:
            continue
        for row in range(int(area.shape[0] - peaks[col]), area.shape[0] - 1):
            if area[row, col] != area[row + 1, col]:
                sum += 1
    return sum


def get_bumpiness(peaks):
    s = 0
    for i in range(9):
        s += np.abs(peaks[i] - peaks[i + 1])
    return s


def get_holes(peaks, area):
    # Count from peaks to bottom
    holes = []
    for col in range(area.shape[1]):
        start = -peaks[col]
        # If there's no holes i.e. no blocks on that column
        if start == 0:
            holes.append(0)
        else:
            holes.append(np.count_nonzero(area[int(start):, col] == 0))
    return holes


def get_wells(peaks):
    wells = []
    for i in range(len(peaks)):
        if i == 0:
            w = peaks[1] - peaks[0]
            w = w if w > 0 else 0
            wells.append(w)
        elif i == len(peaks) - 1:
            w = peaks[-2] - peaks[-1]
            w = w if w > 0 else 0
            wells.append(w)
        else:
            w1 = peaks[i - 1] - peaks[i]
            w2 = peaks[i + 1] - peaks[i]
            w1 = w1 if w1 > 0 else 0
            w2 = w2 if w2 > 0 else 0
            w = w1 if w1 >= w2 else w2
            wells.append(w)
    return wells


def check_needed_turn(block_tile):
    # Check how many turns we need to check for a block
    block = get_current_block_text(block_tile)
    if block == 'I' or block == 'S' or block == 'Z':
        return 2
    if block == 'O':
        return 1
    return 4


def check_needed_dirs(block_tile):
    # Return left, right moves needed
    block = get_current_block_text(block_tile)
    if block == 'S' or block == 'Z':
        return 3, 5
    if block == 'O':
        return 4, 4
    return 4, 5


def do_turn(tetris, real_move=False):
    if real_move:
        tetris.move('Rotate')
    else:
        tetris.simulate_move('Rotate', tetris.grid)


def do_sideway(tetris, action, real_move=False):
    if real_move:
        tetris.move(action)
    else:
        tetris.simulate_move(action, tetris.grid)

#def do_down(tetris):
#    tetris.send_input(action_map['Down'][0])
#    tetris.tick()
#    tetris.send_input(action_map['Down'][1])


def drop_down(tetris, real_move=False):
    if real_move:
        tetris.move('Down')
    else:
        tetris.simulate_move('Down', tetris.grid)


def do_action(action, tetris, n_dir, n_turn):
    for dir_count in range(1, n_dir + 1):
        for turn in range(1, n_turn + 1):
            # Turn
            for t in range(turn):
                do_turn(tetris, True)

            # Move in direction
            if action != 'Middle':
                for move in range(dir_count):
                    do_sideway(tetris, action)

            drop_down(tetris)

            yield {'Turn': turn,
                   'Left': dir_count if action == 'Left' else 0,
                   'Right': dir_count if action == 'Right' else 0}
