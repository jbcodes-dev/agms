from app import App


def main():
    app = App(debug=False, cycle=0, control=True)

    app.run()


if __name__ == "__main__":
    main()
