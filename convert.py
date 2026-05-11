import sys
from pathlib import Path
from ddm.text import save_olg, old_load_olg

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <path>")
        return
    
    path = Path(sys.argv[1])

    A, label_vec = old_load_olg(path)
    save_olg(A, label_vec, path)



if __name__ == "__main__":
    main()