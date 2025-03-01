def deviation_inj(param, param_1, param_2, param_3):
    ms_2_5 = param["ms_2_5"]
    ms_1_0 = param["ms_1_0"]
    ms_1_5 = param["ms_1_5"]
    div1 = 101 - (param_1 / ms_2_5 * 100)
    div2 = 101 - (param_2 / ms_1_0 * 100)
    div3 = 101 - (param_3 / ms_1_5 * 100)

    result = (div1 + div2 + div3) / 3
    return round(result)
