import sys
import os

src_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, src_dir)

from app import App

def main():
    app = App()
    app.run()

if __name__ == "__main__":
    main()