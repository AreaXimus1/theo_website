import shutil
import os
import pandas as pd


def iupred_processing(DATA_FOLDER, UPLOAD_FOLDER):
    try:
        shutil.rmtree(f"{DATA_FOLDER}/raw_results_folder")
    except FileNotFoundError:
        pass
    os.makedirs(f"{DATA_FOLDER}/raw_results_folder")

    # with open(f"{UPLOAD_FOLDER}/iupred.txt") as raw_data:

    #     iupred_number = 0
    #     for line in raw_data:
    #         if "################" in line:
    #             iupred_number += 1

    counter = 0
    with open(f"{UPLOAD_FOLDER}/iupred.txt") as raw_data:
        for line in raw_data:
            if line.startswith("################"):

                file_number = f"{counter:04d}"
                with open(f"{DATA_FOLDER}/raw_results_folder/results{file_number}.txt", mode="a") as file, open(f"{DATA_FOLDER}/dump_file.txt", mode="r") as dump:
                    for line2 in dump:
                        file.write(line2)

                # print(f"IUPred file read progress: {counter}/{iupred_number}")
                counter += 1
                os.remove(f"{DATA_FOLDER}/dump_file.txt")

            elif not line.startswith("#"):
                with open(f"{DATA_FOLDER}/dump_file.txt", mode="a") as dump:
                    dump.write(line)


def nuclear_processing(DATA_FOLDER, UPLOAD_FOLDER):
    df = pd.read_csv(
        f"{UPLOAD_FOLDER}/nuclear.csv",
        usecols=["Entry ID", "Nucleus"]
        )
    df[["a", "Identifier", "b"]] = df["Entry ID"].str.split("_", n=2, expand=True)
    df = df[["Identifier", "Nucleus"]].copy()

    df.to_csv(f"{DATA_FOLDER}/nuclear_data.csv")


def raw_processing(DATA_FOLDER, UPLOAD_FOLDER):
    iupred_processing(DATA_FOLDER, UPLOAD_FOLDER)
    nuclear_processing(DATA_FOLDER, UPLOAD_FOLDER)
