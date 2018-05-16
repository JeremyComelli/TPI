from sources import main_window
import configparser


parser = configparser.ConfigParser()

parser.read("config.ini")
window = main_window.MainWindow(parser['MAIN_WINDOW'])



