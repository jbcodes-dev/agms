from terrarium import Terrarium


def main():
    terrarium = Terrarium()

    for sub_entry in terrarium.subsystems:
        print(sub_entry)

        for mod_entry in terrarium.subsystems[sub_entry].modules:
            print(f"Module Name: {terrarium.subsystems[sub_entry].modules[mod_entry].name}\nModule Desc: {terrarium.subsystems[sub_entry].modules[mod_entry].desc}")


if __name__ == "__main__":
    main()

