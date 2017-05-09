import signal

if __name__ == "__main__":
    originalSigint = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, gracefulExit)
    connection = requests.session()
    app =  groupmebot(connection)
    app.main()
