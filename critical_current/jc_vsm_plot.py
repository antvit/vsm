import csv
from pathlib import Path
import matplotlib.pyplot as plt


def get_data_from_file():

    magnetic_field = []
    magnetic_moment = []

    while True:
        try:
            file_name = input("\nEnter file name with data in .csv format (please use for testing data_for_testing_jc.csv) >>>  ")
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    try:
                        if float(row[0]) >= 0:
                            magnetic_field.append(float(row[0]))
                            magnetic_moment.append(float(row[1]))
                    except ValueError:  # ValueError if value row[0] cannot be converted to float
                        pass
            return magnetic_field, magnetic_moment
        except FileNotFoundError:
            print("\nIncorrect file name. Try again!\nOr cancel process (Ctrl+C)")
            continue


def subtraction(magnetic_field, magnetic_moment):

    ascending_branch = []
    descending_branch = []
    subtracted_moment = []
    subtracted_branch = []

    # searching for number of indexes to remove in order to remove branches with negative field and first ascending run
    index_to_remove = 0
    for i, j in enumerate(magnetic_field[:-1]):
        if j <= magnetic_field[i + 1]:
            index_to_remove = i
        else:
            break

    del magnetic_field[0:index_to_remove + 1]
    del magnetic_moment[0:index_to_remove + 1]

    # Removing first measured run. "descending branch" is from the beginning of measured points' list.
    # "ascending branch" from the end of the measured points' list.
    for field_1, moment_1 in zip(magnetic_field[0:round(len(magnetic_moment) / 2) + 1],
                                 magnetic_moment[0:round(len(magnetic_moment) / 2) + 1]):
        descending_branch.append(tuple((field_1, moment_1)))

    for field_2, moment_2 in zip(magnetic_field[round(len(magnetic_moment) / 2) + 1:],
                                 magnetic_moment[round(len(magnetic_moment) / 2) + 1:]):
        ascending_branch.append(tuple((field_2, moment_2)))

    for des, asc in zip(sorted(descending_branch), ascending_branch):
        subtracted_moment.append(round(des[1] - asc[1], 5))

    for des, asc in zip(sorted(descending_branch), subtracted_moment):
        subtracted_branch.append(tuple((des[0], asc)))

    return subtracted_branch


def critical_current_calculation(subtracted_branch):
    
    msg = """Enter a sample size, where:
        'a' is a length
        'b' is a width
        'c' is a height. 
        Conditions: a >= b,  c < a and c < b.\n"""
    
    print(msg)

    while True:
        a = float(input("Enter parameter 'a' in centimeters (use 0.2 for testing): "))
        b = float(input("Enter parameter 'b' in centimeters (use 0.18 for testing): "))
        if a < b:
            print("\n'a' must be higher or equal to 'b'! a >= b\n")
            continue
        else:
            break

    while True:    
        c = float(input("Enter parameter 'c' in centimeters: (use 0.05 for testing): "))
        if c >= a or c >= b:
            print("\n'c' must be less than 'a' and 'b'!\n")
            continue
        else:
            break

    omega = 2 / (a * pow(b, 2) * c * (1 - b / (3*a)))

    print(f"omega: {round(omega, 2)}\n")
     
    critical_current_density = []

    for row in subtracted_branch:
        jc = row[1] * round(omega, 2) * 10
        critical_current_density.append(tuple((row[0], round(jc, 5))))

    return critical_current_density


def write_jc_to_file(jc):

    while True:
        filename_save_results = input("\nInput file name for results saving, such as for example 'results.csv' \n")

        if filename_save_results.endswith('.csv'):
            # check if file already exist
            check_file_exist = Path(filename_save_results)
            if check_file_exist.is_file():
                print(f"\nFile {filename_save_results} already exists!\n")
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

    with open(filename_save_results, 'w', newline='') as csv_file:
        fieldnames = ["Magnetic Field (Oe)", "Jc (A/cm^2)"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in jc:
            writer.writerow({"Magnetic Field (Oe)": row[0], "Jc (A/cm^2)": row[1]})


def jc_plot(jc):

    plt.style.use('bmh')
    plt.plot(*zip(*jc), '-bo', linewidth=2)
    plt.xlabel("Magnetic Field (Oe)")
    plt.ylabel("Jc (A/cm^2)")
    print("\nClose a graf for saving data to a file.")
    plt.show()


def main():

    magnetic_field, magnetic_moment = get_data_from_file()
    subtracted_branch = subtraction(magnetic_field, magnetic_moment)
    jc = critical_current_calculation(subtracted_branch)
    jc_plot(jc)
    write_jc_to_file(jc)

    print("\nDone!\n")


if __name__ == '__main__':
    main()
