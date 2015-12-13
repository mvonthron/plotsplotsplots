
import acquisition
from plot import Plotter

def main():
    serial = acquisition.FakeSerial()
    plot = Plotter()

    serial.source.connect(plot.new_data)

    serial.start()
    plot.run()


if __name__ == '__main__':
    main()
