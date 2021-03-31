from gui import ChatbotGUI
import sys

def main():
    try:
        ChatbotGUI()
    except (KeyboardInterrupt, EOFError) as e:
        print("Exiting - Goodbye!", e)
        sys.exit()

if __name__ == '__main__':
    main()