from time import sleep

def s(txt, d=0.04):
    for i in txt:
        print(i, end='', flush=True)
        sleep(d)
    print()

def main():
    s("Welcome to Music Lyrics Saver -> Bhavyansh Soni!")
    s("Here you can save Musics Lyrics!")
    s("\nLet's Get Started!")

    