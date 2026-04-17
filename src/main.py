from amgs.application import Application
    
def main():
    config = {
        "runtime": 691200, # run for 8 days, started dying after day 8 in second cycle
        "interval": 30,
        "cycle": "three",
        "debug": True,
    }

    app = Application(config)
    app.mainloop()


if __name__ == "__main__":
    main()

