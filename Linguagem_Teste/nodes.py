class Node:
	def __init__(self, value, children):
		self.value = value
		self.children = children

	def Evaluate():
		pass


class BinOp(Node):
	def __init__(self, value, left, right):
		super().__init__(value, [left, right])

	def Evaluate(self, symbol_table):
		left_value, left_type = self.children[0].Evaluate(symbol_table)[0], self.children[0].Evaluate(symbol_table)[1]
		right_value, right_type = self.children[1].Evaluate(symbol_table)[0], self.children[1].Evaluate(symbol_table)[1]

		if left_type == 'inteiro' and right_type == 'inteiro':
			if self.value == '+':
				return (left_value + right_value, left_type)
			elif self.value == '-':
				return (left_value - right_value, left_type)
			elif self.value == '*':
				return (left_value * right_value, left_type)
			elif self.value == '/':
				return (left_value // right_value, left_type)

		if left_type == right_type:
			if self.value == '||':
				return (int(left_value or right_value), left_type)
			elif self.value == '&&':
				return (int(left_value and right_value), left_type)

		if self.value == '.':
			return (str(left_value) + str(right_value), 'palavra')
		if self.value == '==':
			return (int(left_value == right_value), 'inteiro')
		elif self.value == '>':
			return (int(left_value > right_value), 'inteiro')
		elif self.value == '<':
			return (int(left_value < right_value), 'inteiro')


class UnOp(Node):
	def __init__(self, value, child):
		super().__init__(value, [child])

	def Evaluate(self, symbol_table):
		child_value = self.children[0].Evaluate(symbol_table)[0]
		child_type = self.children[0].Evaluate(symbol_table)[1]

		if child_type == 'inteiro':	
			if self.value == '+':
				return (child_value, 'inteiro')
			elif self.value == '-':
				return (-child_value, 'inteiro')
		
		if self.value == '!':
			return int(not child_value), child_type


class IntVal(Node):
	def __init__(self, value):
		super().__init__(value, [])

	def Evaluate(self, symbol_table):
		return (self.value, 'inteiro')


class palavraVal(Node):
	def __init__(self, value):
		super().__init__(value, [])

	def Evaluate(self, symbol_table):
		return (self.value, 'palavra')


class NoOp(Node):
	def __init__(self):
		super().__init__('NoOp', [])

	def Evaluate(self, symbol_table):
		pass


class Block(Node):
	def __init__(self, statements):
		super().__init__('Block', statements)

	def Evaluate(self, symbol_table):
		for statement in self.children:
			if statement.value == 'Return':
				return statement.Evaluate(symbol_table)
			statement.Evaluate(symbol_table)


class Print(Node):
	def __init__(self, expression):
		super().__init__('Print', [expression])

	def Evaluate(self, symbol_table):
		value = self.children[0].Evaluate(symbol_table)[0]
		print(value)


class Read(Node):
	def __init__(self):
		super().__init__('Read', [])

	def Evaluate(self, symbol_table):
		inp = input()
		
		if inp.isdigit():
			return (int(inp), 'inteiro')
		else:
			raise Exception('Invalid input')


class While(Node):
	def __init__(self, condition, statement):
		super().__init__('While', [condition, statement])

	def Evaluate(self, symbol_table):
		while self.children[0].Evaluate(symbol_table)[0]:
			self.children[1].Evaluate(symbol_table)


class If(Node):
	def __init__(self, condition, statement, else_statement=None):
		super().__init__('If', [condition, statement, else_statement])

	def Evaluate(self, symbol_table):
		if self.children[0].Evaluate(symbol_table)[0]:
			return self.children[1].Evaluate(symbol_table)
		elif self.children[2]:
			return self.children[2].Evaluate(symbol_table)


class Return(Node):
	def __init__(self, expression):
		super().__init__('Return', [expression])

	def Evaluate(self, symbol_table):
		return self.children[0].Evaluate(symbol_table)

# ==================== Function Tables ====================
class FuncTable:
	table = {}

	@staticmethod
	def create(func_type: str, func_name: str, value) -> None:
		if func_name in FuncTable.table:
			raise Exception(f"Erro Sintático 🠊 Função '{func_name}' já está definida")

		FuncTable.table[func_name] = (func_type, value)

	@staticmethod
	def getter(var_name):
		if var_name not in FuncTable.table:
			raise Exception(f"Erro Sintático 🠊 Função '{var_name}' não está definida")

		func_type = FuncTable.table[var_name][0]
		func_ref = FuncTable.table[var_name][1]
		return func_type, func_ref


class FuncDec(Node):
	def __init__(self, func_type, func_name, params, block):
		super().__init__(func_name, [params, block])
		self.func_type = func_type

	def Evaluate(self, symbol_table):
		FuncTable.create(self.func_type, self.value, self)


class FuncCall(Node):
	def __init__(self, func_name, args=[]):
		super().__init__(func_name, args)

	def Evaluate(self, symbol_table):
		function = FuncTable.getter(self.value)
		func_type = function[0]
		func_ref = function[1]

		if len(self.children) != len(func_ref.children[0]):
			raise Exception(f"Erro Sintático 🠊 Função '{self.value}' espera por {len(func_ref.children[0])} argumentos, mas {len(self.children)} foram dados")

		local_st = SymbolTable()

		for i in range(len(self.children)):
			param = func_ref.children[0][i]
			arg = self.children[i].Evaluate(symbol_table)
			var_name, var_type, var_value = param.children.token_value, param.value, arg

			local_st.create(var_name, var_type)
			local_st.setter(var_name, var_value)

		result = func_ref.children[1].Evaluate(local_st)

		if result:
			if func_type != result[1]:
				raise Exception(f"Erro Sintático 🠊 Função '{self.value}' Espera o tipo de retorno '{func_type}', mas '{result[1]}' foi dado")
		return result


# ==================== Symbol Tables ====================
class SymbolTable:
	def __init__(self):
		self.table = {}

	def create(self, var_name, var_type):
		if var_name in self.table:
			raise Exception(f"Erro Sintático 🠊 '{var_name}' já está definido")

		self.table[var_name] = (None, var_type)

	def setter(self, var_name, value):
		if var_name not in self.table:
			raise Exception(f"Erro Sintático 🠊 '{var_name}' não está definido")

		table_type = self.table[var_name][1]
		var_type = value[1]

		if table_type == var_type:
			self.table[var_name] = (value[0], table_type)
		else:
			raise Exception(f"Erro Sintático 🠊 '{var_name}' é do tipo '{table_type}' mas '{var_type}' foi dado")

	def getter(self, var_name):
		if var_name not in self.table:
			raise Exception(f"Erro Sintático 🠊 '{var_name}' não está definido")

		var_value = self.table[var_name][0]
		var_type = self.table[var_name][1]
		return var_value, var_type


class VarDecl(Node):
	def __init__(self, vars_names, var_type):
		super().__init__(var_type, vars_names)

	def Evaluate(self, symbol_table):
		for var_name in self.children:
			symbol_table.create(var_name.token_value, self.value.token_value)


class Assign(Node):
	def __init__(self, ident, expr):
		super().__init__(ident, expr)

	def Evaluate(self, symbol_table):
		ident = self.value
		expr = self.children.Evaluate(symbol_table)

		symbol_table.setter(ident, expr)


class Ident(Node):
	def __init__(self, value):
		super().__init__(value, [])

	def Evaluate(self, symbol_table):
		return symbol_table.getter(self.value)