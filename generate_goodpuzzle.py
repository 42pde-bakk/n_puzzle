import subprocess
import shutil

TEMPFILE = 'tmp.log'
PUZZLE_SIZE = 3
TARGET_MOVES = 31

puzzlecmd = f'python npuzzle-gen.py 3 -s > {TEMPFILE}'
searchcmd = f'python srcs/main.py {TEMPFILE} --manhattan'
maxmoves = i = 0
while True:
    i += 1
    subprocess.Popen(puzzlecmd, stdout=subprocess.PIPE, shell=True)
    p = subprocess.Popen(searchcmd, stdout=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    out = out.decode('utf-8')
    print(out)
    if p.returncode >= TARGET_MOVES:
        shutil.move(TEMPFILE, f'puzzles/{TARGET_MOVES}moves.txt')
        print(f'gottem in {p.returncode} moves and it only took me {i} tries')
        break
