from app import App


def main():
    app = App(debug=True, cycle=0, control=True, cycle_length=600)

    app.run()


if __name__ == "__main__":
    main()
