import json
from src.gui.dashboard import dashboard


def append_to_result_file(key, value, file):
    """
    Append to the result file
    :param file: result file
    :param key: is the Key of object
    :param value: is the value of object
    """
    # repo_name = self.github_repo["name"]
    try:
        with open(file, "r+") as outfile:
            # First we load existing data into a dict.
            file_data = json.load(outfile)
            # Join new_data with file_data inside emp_details
            if key not in file_data:
                file_data[key] = value
                # Sets file's current position at offset.
                outfile.seek(0)
                # convert back to json.
                json.dump(file_data, outfile, indent=4)
            outfile.close()
    except Exception as e:
        print("Error in appending to the result file", e, key, value)


def calculate_TTL(result_file, file_path):
    TTLs = [v for k, v in result_file.items() if k.startswith('TTL')]
    TTLs_number = len(TTLs)
    if TTLs_number == 0:
        append_to_result_file("Sum_TTL", 0, file_path)
        append_to_result_file("Average_TTL", 0, file_path)
    else:
        sum_TTL = 0
        for TTL in TTLs:
            sum_TTL = sum_TTL + TTL
        average_TTL = sum_TTL / TTLs_number
        append_to_result_file("Sum_TTL", sum_TTL, file_path)
        append_to_result_file("Average_TTL", average_TTL, file_path)
    print("------Done TTL------")


def calculate_TDiff(result_file, file_path):
    TDiffs = [v for k, v in result_file.items() if k.startswith('Tdiff')]
    TTLs_number = len(TDiffs)
    if TTLs_number == 0:
        append_to_result_file("Sum_TDiff", 0, file_path)
        append_to_result_file("AVG_TDiff", 0, file_path)

    else:
        sum_TDiff = 0
        for TDiff in TDiffs:
            sum_TDiff = sum_TDiff - TDiff
        average_TDiff = sum_TDiff / TTLs_number
        append_to_result_file("Sum_TDiff", sum_TDiff, file_path)
        append_to_result_file("AVG_TDiff", average_TDiff, file_path)
    print("------Done TDiff------")


def calculate_TLR(result_file, file_path):
    TLRs = [v for k, v in result_file.items() if k.startswith('TLR')]
    TLRs_number = len(TLRs)
    if TLRs_number == 0:
        append_to_result_file("Sum_TLR", 0, file_path)
        append_to_result_file("AVG_TLR", 0, file_path)

    else:
        sum_TLRs = 0
        for TLR in TLRs:
            sum_TLRs = sum_TLRs + TLR
        average_TLR = sum_TLRs / TLRs_number
        append_to_result_file("Sum_TLR", sum_TLRs, file_path)
        append_to_result_file("AVG_TLR", average_TLR, file_path)
    print("------Done TLR------")


def calculate_MTLR(result_file, file_path):
    MTLRs = [v for k, v in result_file.items() if k.startswith('MTLR')]
    MTLRs_number = len(MTLRs)
    if MTLRs_number == 0:
        append_to_result_file("Sum_MTLR", 0, file_path)
        append_to_result_file("AVG_MTLR", 0, file_path)

    else:
        sum_MTLRs = 0
        for MTLR in MTLRs:
            sum_MTLRs = sum_MTLRs + MTLR
        average_MTLR = sum_MTLRs / MTLRs_number
        append_to_result_file("Sum_MTLR", sum_MTLRs, file_path)
        append_to_result_file("AVG_MTLR", average_MTLR, file_path)
    print("------Done MTLR------")


def calculate_MRTL(result_file, file_path):
    MRTLs = [v for k, v in result_file.items() if k.startswith('MRTL')]
    MRTLs_number = len(MRTLs)
    if MRTLs_number == 0:
        append_to_result_file("Sum_MRTL", 0, file_path)
        append_to_result_file("AVG_MRTL", 0, file_path)

    else:
        sum_MRTLs = 0
        for MRTL in MRTLs:
            sum_MRTLs = sum_MRTLs + MRTL
        average_MRTL = sum_MRTLs / MRTLs_number
        append_to_result_file("Sum_MRTL", sum_MRTLs, file_path)
        append_to_result_file("AVG_MRTL", average_MRTL, file_path)
    print("------Done MRTL------")


def calculate_TMR(result_file, file_path):
    Tdiffs = [v for k, v in result_file.items() if k.startswith('Tdiff')]
    Pdiffs = [v for k, v in result_file.items() if k.startswith('Pdiff')]
    # MRTLs = [v for k, v in result_file.items() if k.startswith('MRTL')]
    TLRs = [v for k, v in result_file.items() if k.startswith('TLR')]
    # print("TDiff index", Tdiffs, Tdiffs[2])
    print(len(Tdiffs), len(Pdiffs), len(TLRs))
    sum_TMR = 0
    sum_MRTL = 0
    if len(Tdiffs) == 0 or len(Pdiffs) == 0:
        append_to_result_file("TMR", 0, file_path)
    else:
        for index, PDiff in enumerate(Pdiffs):
            # print("TDiff index", index)
            if PDiff > 0:
                MRTL = Tdiffs[index]/PDiff
                sum_MRTL = sum_MRTL + MRTL
            else:
                MRTL = Tdiffs[index]
                sum_MRTL = sum_MRTL + MRTL
            append_to_result_file(f"MRTL-{index}", MRTL, file_path)
        # for index, Tdiff in enumerate(Tdiffs):
            print("-----MRTL added----")
            if 0 < index < len(TLRs) - 1:
                # print("Here")

                # print("index", index, index - 1, TLRs[index-1])
            #     print(">>>>>", TLRs[index - 1])
            #     print("TLR index", TLRs[index - 1])
                if TLRs[index - 1]:
                    current_TMR = MRTL / TLRs[index - 1]
                    # print("current TMR", current_TMR)
                    sum_TMR = sum_TMR + current_TMR
                    append_to_result_file(f"TMR-{index}", current_TMR, file_path)
            else:
                current_TMR = MRTL
                sum_TMR = sum_TMR + current_TMR
                append_to_result_file(f"TMR-{index}", current_TMR, file_path)

        if len(TLRs) > 0:
            append_to_result_file("SUM_MRTL", sum_MRTL, file_path)
            append_to_result_file("AVG_MRTL", sum_TMR / len(TLRs), file_path)
            append_to_result_file("SUM_TMR", sum_TMR, file_path)
            append_to_result_file("AVG_TMR", sum_TMR/len(TLRs), file_path)
        else:
            append_to_result_file("SUM_MRTL", sum_MRTL, file_path)
            append_to_result_file("AVG_MRTL", sum_TMR / len(Tdiffs), file_path)
            append_to_result_file("SUM_TMR", sum_TMR, file_path)
            append_to_result_file("AVG_TMR", sum_TMR / len(Tdiffs), file_path)



    print("------Done TMR------")


def calculate_MRR(result_file, file_path):
    TDiffs = [v for k, v in result_file.items() if k.startswith('Tdiff')]
    NTR = [v for k, v in result_file.items() if k.startswith('NTR')]
    TDiffs_number = len(TDiffs)
    if TDiffs_number == 0:
        append_to_result_file("MRR", 0, file_path)
    else:
        MRR = 0
        for TDiff in TDiffs:
            if TDiff > 0:
                MRR = MRR + 1
        if NTR[0] > 0:
            ratio = MRR / NTR[0]
        else:
            ratio = 0
        append_to_result_file("MRR", ratio, file_path)
    print("------Done MRR------")


def run():
    dashboard()
