
import acquisition

def main():
    serial = acquisition.FakeSerial()

    # process = processing.DataProcess()
    # process.set_source(serial.source)

    # log = output.Logfile('experiment.log')
    # log.set_source(process.source)

    serial.start()

if __name__ == '__main__':
    main()
