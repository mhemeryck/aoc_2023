FILENAME: str = "input.txt"


def main():
    with open(FILENAME, "r") as fh:
        lines = fh.readlines()

    digits = [[int(c) for c in line if c.isdigit()] for line in lines]
    answer = sum([d[0] * 10 + d[-1] for d in digits])
    print(answer)


if __name__ == "__main__":
    main()
