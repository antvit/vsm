import csv
from pathlib import Path
import matplotlib.pyplot as plt


def get_data_from_file():

    total_branch = []

    while True:
        try:
            file_name = input("\nEnter file name with data in .csv format (please use for testing data_for_testing_tc.csv) >>>  ")
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    # print(f"row: {row}")
                    try:
                        if isinstance(float(row[0]), float):
                            total_branch.append(tuple((float(row[0]), float(row[1]))))
                    except ValueError:  # ValueError if value row[0] cannot be converted to float
                        pass
            return total_branch
        except FileNotFoundError:
            print("\nIncorrect file name. Try again!\nOr cancel process (Ctrl+C)")
            continue


def normalization(total_branch):

    normalized_branch = []

    smallest_moment = [x[1] for x in total_branch]
    smallest_moment.sort()

    s = -(smallest_moment[0])

    for row in total_branch:
        normalized_branch.append(tuple((round(row[0], 2), round(row[1] / s, 3))))

    return normalized_branch


def get_critical_temperature(normalized_branch, point):

    if point == 0:
        for row in normalized_branch:
            # find first positive magnetic moment, that means Tc,onset
            if row[1] >= 0:
                return row[0]
    else:
        # https://stackoverflow.com/questions/12141150/from-list-of-integers-get-number-closest-to-a-given-value
        # determine the closest magnetic moment to a certain point
        moment_at_point = min([x[1] for x in normalized_branch], key=lambda x: abs(x + point))
        tc_point = [item for item in normalized_branch if item[1] == moment_at_point]

        return tc_point[0][0]


def tc_analise(normalized_branch):

    # [0][0] at the end of get_critical_moments(normalized_branch, 0.9)[0][0] gets the first element of a tuple
    # Tc at 90% of a transition curve
    tc_90 = get_critical_temperature(normalized_branch, 0.9)
    tc_10 = get_critical_temperature(normalized_branch, 0.1)
    tc_50 = get_critical_temperature(normalized_branch, 0.5)
    tc_onset = get_critical_temperature(normalized_branch, 0)

    return tc_50, tc_onset, round(tc_10 - tc_90, 3)


def write_tc_to_file(normalized_branch, tc_50, tc_onset, tc_width):

    while True:
        filename_save_results = input("\nInput file name for results saving, such as for example 'results.csv'\n")

        if filename_save_results.endswith('.csv'):
            # check if file already exist
            check_file_exist = Path(filename_save_results)
            if check_file_exist.is_file():
                print(f"File {filename_save_results} already exists!\n")
                rewrite = input("Do you want to rewrite it? (yes/no or y/n) >>> ")
                if rewrite == "yes" or rewrite == "y":
                    break
                else:
                    continue
            else:
                break
        else:
            print("\nIncorrect file name! A file name must have format '.csv'. For example 'results.csv'")
            print("Do not use capital letters. Try again!\n")
            continue

    with open(filename_save_results, 'a', newline='') as csv_file:
        fieldnames = ['Temperature (K)', 'Normalized magnetic moment', 'Tc, onset (K)',
                      'Tc, 50% (K)', 'Transition width (K)']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Tc, onset (K)': tc_onset, 'Tc, 50% (K)': tc_50, 'Transition width (K)': tc_width})
        for row in normalized_branch:
            writer.writerow({'Temperature (K)': row[0], 'Normalized magnetic moment': row[1]})


def tc_plot(normalized_branch, tc_50, tc_onset, tc_width):

    plt.style.use('bmh')
    plt.plot(*zip(*normalized_branch), '-bo', linewidth=2)
    plt.xlabel("Temperature (K)")
    plt.ylabel("Normalized magnetic moment")
    plt.figtext(.2, .7, f"Tc,onset = {tc_onset} K")
    plt.figtext(.2, .65, f"Tc,50% = {tc_50} K")
    plt.figtext(.2, .60, f"Transition width = {tc_width} K")
    print("\nClose a graf for saving data to a file.")
    plt.show()


def main():

    total_branch = get_data_from_file()
    normalized_branch = normalization(total_branch)
    tc_50, tc_onset, tc_width = tc_analise(normalized_branch)

    print(f"\nTc,onset = {tc_onset} K")
    print(f"Tc 50% = {tc_50} K")
    print(f"Transition width = {tc_width} K")

    tc_plot(normalized_branch, tc_50, tc_onset, tc_width)
    write_tc_to_file(normalized_branch, tc_50, tc_onset, tc_width)

    print("\nDone!\n")


if __name__ == '__main__':
    main()
