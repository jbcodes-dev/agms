from app import App


def main():
    runtime = 60 * 60 * 24 * 14 # two weeks

    app = App(debug=True, cycle=0, control=True, cycle_length=runtime)

    app.run()


if __name__ == "__main__":
    main()
