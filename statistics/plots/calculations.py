def cpi(input_list):
    cpi = []
    cycles = []
    instrs_retired = []
    for i in range(len(input_list)):
        if input_list[i].variable == "cycles":
            cycles = input_list[i].get_list()

        if input_list[i].variable == "instructions":
            instrs_retired = input_list[i].get_list()

    for i in range(len(cycles)):
        cpi.append(float(cycles[i]) / float(instrs_retired[i]))

    return (cpi)
