import csv
from pathlib import Path
import matplotlib.pyplot as plt


def get_data_from_file():

    total_branch = []

    while True:
        try:
            file_name = input("\nEnter file name with data in .csv format (please use for testing data_for_testing_fp.csv)>>>  ")
            with open(file_name, 'r') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for row in csv_reader:
                    try:
                        if isinstance(float(row[0]), float):
                            total_branch.append(tuple((float(row[0]), float(row[1]))))
                    except ValueError:  # ValueError if value row[0] cannot be converted to float
                        pass
            # return magnetic_field, magnetic_moment
            return total_branch
        except FileNotFoundError:
            print("\nIncorrect file name. Try again!\nOr cancel process (Ctrl+C)")
            continue


def fp_calculation(total_branch):

    pinning_force_density = []

    for row in total_branch:
        fp = row[0] * row[1]
        pinning_force_density.append(tuple((round(row[0], 2), round(fp, 2))))

    fp_max = max([x[1] for x in pinning_force_density])
    bp_max = [item for item in pinning_force_density if item[1] == fp_max]

    pinning_force_normalized = []

    for row in pinning_force_density:
        bp_norm = row[0] / bp_max[0][0]
        fp_norm = row[1] / fp_max
        pinning_force_normalized.append(tuple((round(bp_norm, 4), round(fp_norm, 4))))

    return pinning_force_normalized


def write_fp_to_file(fp_norm):

    while True:
        filename_save_results = input("\nInput file name for results saving, such as for example 'results.csv' \n")

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

    with open(filename_save_results, 'w', newline='') as csv_file:
        fieldnames = ['B/Bp.max', 'Normalized Fp']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in fp_norm:
            writer.writerow({'B/Bp.max': row[0], 'Normalized Fp': row[1]})


def fp_norm_plot(fp_norm):

    plt.style.use('bmh')
    plt.plot(*zip(*fp_norm), '-bo', linewidth=2)
    plt.xlabel("B/Bp.max")
    plt.ylabel("Normalized Fp")
    print("\nClose a graf for saving data to a file.")
    plt.show()


def main():

    total_branch = get_data_from_file()
    fp_norm = fp_calculation(total_branch)
    fp_norm_plot(fp_norm)
    write_fp_to_file(fp_norm)

    print("\nDone!\n")


if __name__ == '__main__':
    main()
