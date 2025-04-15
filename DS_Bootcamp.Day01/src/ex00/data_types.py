def data_types():
	a_int = 21
	b_str = 'school 21'
	c_float = 21.0
	d_bool = True
	f_list = [a_int, b_str, c_float, d_bool]
	e_dict = {'a': 1, 'b': 2}
	g_tuple = (a_int, b_str, c_float, d_bool)
	h_set = {a_int, b_str, c_float, d_bool}
	
	vars = [a_int, b_str, c_float, d_bool, f_list, e_dict, g_tuple, h_set]
	types = [type(var).__name__ for var in vars]
	print('[' + ', '.join(types) + ']')


if __name__ == "__main__":
	data_types()