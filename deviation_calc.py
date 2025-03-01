def deviation_inj(param, param_1, param_2, param_3):
    ms_2_5 = param["ms_2_5"]
    ms_1_0 = param["ms_1_0"]
    ms_1_5 = param["ms_1_5"]
    div1 = 101 - (param_1 / ms_2_5 * 100)
    div2 = 101 - (param_2 / ms_1_0 * 100)
    div3 = 101 - (param_3 / ms_1_5 * 100)

    result = (div1 + div2 + div3) / 3
    return round(result)


# param = {'inj_number': '06h906036h', 'alt_inj_number_1': '0261500074', 'alt_inj_number_2': None, 'engine': '1.8 FSI', 'ms_2_5': 56, 'ms_1_0': 25, 'ms_1_5': 35}
# param1 = 55
# param2 = 23
# param3 = 33
#
# res = deviation_inj(param,param1, param2, param3)
# print(res)