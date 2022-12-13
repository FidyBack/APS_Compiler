from tokenizer import Tokenizer
from nodes import *

class Parser:
	tokens = None

	def parseProgram():
		"""
		Início do Program
		"""
		children = []
		while Parser.tokens.actual.token_type != 'EOF':
			children.append(Parser.parseDeclaration())

		return Block(children)


	def funcParams(params):
		"""
		Declaração de Parâmetros de Função
		"""
		loc_parms = []
		if Parser.tokens.actual.token_type == 'IDENTIFIER':
			loc_parms.append(VarDecl(Parser.tokens.actual, None))
			Parser.tokens.selectNext()

			while Parser.tokens.actual.token_type == 'COMMA':
				Parser.tokens.selectNext()

				if Parser.tokens.actual.token_type != 'IDENTIFIER':
					raise Exception(f"Erro Sintático 🠊 esperado Identificador 🠊 {Parser.tokens.actual.token_value}")
				loc_parms.append(VarDecl(Parser.tokens.actual, None))
				Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'COLON':
				raise Exception(f"Erro Sintático 🠊 esperado ':' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'TYPE':
				raise Exception(f"Erro Sintático 🠊 esperado Tipagem 🠊 {Parser.tokens.actual.token_value}")
			var_type = Parser.tokens.actual.token_value
			for var in loc_parms:
				var.value = var_type
				params.append(var)

			Parser.tokens.selectNext()

		elif Parser.tokens.actual.token_type != 'RPAR':
			raise Exception(f"Erro Sintático 🠊 esperado Identificador 🠊 {Parser.tokens.actual.token_value}")


	def parseDeclaration():
		"""
		Início do Declaration
		"""
		if Parser.tokens.actual.token_type != 'FUNCAO':
			raise Exception(f"Erro Sintático 🠊 esperado 'funcao' 🠊 {Parser.tokens.actual.token_value}")
		Parser.tokens.selectNext()

		if Parser.tokens.actual.token_type != 'IDENTIFIER':
			raise Exception(f"Erro Sintático 🠊 esperado Identificador 🠊 {Parser.tokens.actual.token_value}")
		ident = Parser.tokens.actual.token_value
		Parser.tokens.selectNext()

		if Parser.tokens.actual.token_type != 'LPAR':
			raise Exception(f"Erro Sintático 🠊 esperado '(' 🠊 {Parser.tokens.actual.token_value}")
		Parser.tokens.selectNext()
		params = []

		# ==================== Diversos Parâmetros ====================
		Parser.funcParams(params)

		while Parser.tokens.actual.token_type == 'COMMA':
			Parser.tokens.selectNext()
			Parser.funcParams(params)

		if Parser.tokens.actual.token_type != 'RPAR':
			raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
		Parser.tokens.selectNext()

		# ==================== Tipo da Função ====================
		if Parser.tokens.actual.token_type == 'ARROW':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'TYPE':
				raise Exception(f"Erro Sintático 🠊 esperado Tipagem 🠊 {Parser.tokens.actual.token_value}")
			func_type = Parser.tokens.actual.token_value
			Parser.tokens.selectNext()
		else:
			func_type = None

		# ==================== Retorno da Função ====================
		return FuncDec(func_type, ident, params, Parser.parseBlock())


	def parseBlock():
		"""
		Início do Block
		"""
		if Parser.tokens.actual.token_type != 'LBRACE':
			raise Exception(f"Erro Sintático 🠊 esperado '{{' 🠊 {Parser.tokens.actual.token_value}")
		Parser.tokens.selectNext()
		nodes = []

		while Parser.tokens.actual.token_type != 'RBRACE':
			nodes.append(Parser.parseStatement())
		Parser.tokens.selectNext()

		return Block(nodes)


	def parseStatement():
		"""
		Início do Statement
		"""
		# ==================== Apenas ';' ====================
		if Parser.tokens.actual.token_type == 'SEMICOLON':
			Parser.tokens.selectNext()
			resultado = NoOp()

		# ==================== Atribuir Variáveis / Chamar Função ====================
		elif Parser.tokens.actual.token_type == 'IDENTIFIER':
			ident = Parser.tokens.actual.token_value
			Parser.tokens.selectNext()

			# ==================== Atribuição ====================
			if Parser.tokens.actual.token_type == 'EQUAL':
				Parser.tokens.selectNext()
				resultado = Assign(ident, Parser.parseRelExpression())

				if Parser.tokens.actual.token_type != 'SEMICOLON':
					raise Exception(f"Erro Sintático 🠊 esperado ';' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()

			# ==================== Chamada de Função ====================
			elif Parser.tokens.actual.token_type == 'LPAR':
				Parser.tokens.selectNext()
				args = []

				if Parser.tokens.actual.token_type != 'RPAR':
					args.append(Parser.parseRelExpression())

					while Parser.tokens.actual.token_type == 'COMMA':
						Parser.tokens.selectNext()
						args.append(Parser.parseRelExpression())

				if Parser.tokens.actual.token_type != 'RPAR':
					raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()

				if Parser.tokens.actual.token_type != 'SEMICOLON':
					raise Exception(f"Erro Sintático 🠊 esperado ';' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()
				resultado = FuncCall(ident, args)

			else:
				raise Exception(f"Erro Sintático 🠊 esperado '=' ou '(' 🠊 {Parser.tokens.actual.token_value}")

		# ==================== Print ====================
		elif Parser.tokens.actual.token_type == 'ESCREVA':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'LPAR':
				raise Exception(f"Erro Sintático 🠊 esperado '(' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

			resultado = Print(Parser.parseRelExpression())

			if Parser.tokens.actual.token_type != 'RPAR':
				raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'SEMICOLON':
				raise Exception(f"Erro Sintático 🠊 esperado ';' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

		# ==================== Declarar Variáveis ====================
		elif Parser.tokens.actual.token_type == 'VARIAVEL':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type == 'IDENTIFIER':
				ident = [Parser.tokens.actual]
				Parser.tokens.selectNext()

				while Parser.tokens.actual.token_type == 'COMMA':
					Parser.tokens.selectNext()

					if Parser.tokens.actual.token_type != 'IDENTIFIER':
						raise Exception(f"Erro Sintático 🠊 esperado Identificador 🠊 {Parser.tokens.actual.token_value}")

					ident.append(Parser.tokens.actual)
					Parser.tokens.selectNext()

				if Parser.tokens.actual.token_type != 'COLON':
					raise Exception(f"Erro Sintático 🠊 esperado ':' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()

				if Parser.tokens.actual.token_type != 'TYPE':
					raise Exception(f"Erro Sintático 🠊 esperado Tipagem 🠊 {Parser.tokens.actual.token_value}")
				var_type = Parser.tokens.actual
				Parser.tokens.selectNext()

				if Parser.tokens.actual.token_type != 'SEMICOLON':
					raise Exception(f"Erro Sintático 🠊 esperado ';' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()

				resultado = VarDecl(ident, var_type)

			else:
				raise Exception(f"Erro Sintático 🠊 esperado Identificador 🠊 {Parser.tokens.actual.token_value}")

		# ==================== Return ====================
		elif Parser.tokens.actual.token_type == 'RETORNE':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'SEMICOLON':
				resultado = Return(Parser.parseRelExpression())
			else:
				resultado = Return()

			if Parser.tokens.actual.token_type != 'SEMICOLON':
				raise Exception(f"Erro Sintático 🠊 esperado ';' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

		# ==================== While ====================
		elif Parser.tokens.actual.token_type == 'ENQUANTO':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'LPAR':
				raise Exception(f"Erro Sintático 🠊 esperado '(' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()
			condition = Parser.parseRelExpression()

			if Parser.tokens.actual.token_type != 'RPAR':
				raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()
			resultado = While(condition, Parser.parseStatement())

		# ==================== If ====================
		elif Parser.tokens.actual.token_type == 'SE':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'LPAR':
				raise Exception(f"Erro Sintático 🠊 esperado '(' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()
			condition = Parser.parseRelExpression()

			if Parser.tokens.actual.token_type != 'RPAR':
				raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()
			resultado = If(condition, Parser.parseStatement())

			if Parser.tokens.actual.token_type == 'SENAO':
				Parser.tokens.selectNext()
				resultado = If(condition, resultado, Parser.parseStatement())

		# ==================== Block ====================
		else:
			resultado = Parser.parseBlock()

		return resultado


	def parseRelExpression():
		"""
		RelExpression -> Expression, { (ISEQUAL | GREATER | LESS), Expression }
		"""
		resultado = Parser.parseExpression()
		operation = {
			'ISEQUAL': '==',
			'GREATER': '>',
			'LESS': '<'
		}

		if Parser.tokens.actual.token_type in operation:
			oper = Parser.tokens.actual.token_type
			Parser.tokens.selectNext()
			resultado = BinOp(operation[oper], resultado, Parser.parseExpression())

		return resultado


	def parseExpression():
		"""
		Expression -> Term, { (PLUS | MINUS | OR | DOT), Term }
		"""
		resultado = Parser.parseTerm()
		operation = {
			'PLUS': '+',
			'MINUS': '-',
			'OR': '||',
			'DOT': '.'
		}

		while Parser.tokens.actual.token_type in operation:
			oper = Parser.tokens.actual.token_type
			Parser.tokens.selectNext()
			resultado = BinOp(operation[oper], resultado, Parser.parseTerm())

		return resultado


	def parseTerm():
		"""
		Term -> Factor, { (MULT | DIV | AND), Factor }
		"""
		resultado = Parser.parseFactor()
		operation = {
			'MULT': '*',
			'DIV': '/',
			'AND': '&&'
		}

		while Parser.tokens.actual.token_type in operation:
			oper = Parser.tokens.actual.token_type
			Parser.tokens.selectNext()
			resultado = BinOp(operation[oper], resultado, Parser.parseFactor())

		return resultado


	def parseFactor():
		"""
		Início do Factor
		"""
		resultado = None
		operation = {
			'PLUS': '+',
			'MINUS': '-',
			'NOT': '!'
		}

		# ==================== Number ====================
		if Parser.tokens.actual.token_type == 'inteiro':
			resultado = IntVal(Parser.tokens.actual.token_value)
			Parser.tokens.selectNext()
		
		# ==================== palavra ====================
		elif Parser.tokens.actual.token_type == 'palavra':
			resultado = palavraVal(Parser.tokens.actual.token_value)
			Parser.tokens.selectNext()

		# ==================== Identifier ====================
		elif Parser.tokens.actual.token_type == 'IDENTIFIER':
			resultado = Ident(Parser.tokens.actual.token_value)
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type == 'LPAR':
				Parser.tokens.selectNext()
				arguments = []

				while Parser.tokens.actual.token_type != 'RPAR':
					arguments.append(Parser.parseRelExpression())

					if Parser.tokens.actual.token_type == 'COMMA':
						Parser.tokens.selectNext()

				resultado = FuncCall(resultado.value, arguments)

				if Parser.tokens.actual.token_type != 'RPAR':
					raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
				Parser.tokens.selectNext()

		# ==================== UnOp ====================
		elif Parser.tokens.actual.token_type in operation:
			oper = Parser.tokens.actual.token_type
			Parser.tokens.selectNext()
			resultado = UnOp(operation[oper], Parser.parseFactor())

		# ==================== Parentheses ====================
		elif Parser.tokens.actual.token_type == 'LPAR':
			Parser.tokens.selectNext()
			resultado = Parser.parseRelExpression()

			if Parser.tokens.actual.token_type != 'RPAR':
				raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

		# ==================== Read ====================
		elif Parser.tokens.actual.token_type == 'LEIA':
			Parser.tokens.selectNext()

			if Parser.tokens.actual.token_type != 'LPAR':
				raise Exception(f"Erro Sintático 🠊 esperado '(' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()
			resultado = Read()

			if Parser.tokens.actual.token_type != 'RPAR':
				raise Exception(f"Erro Sintático 🠊 esperado ')' 🠊 {Parser.tokens.actual.token_value}")
			Parser.tokens.selectNext()

		else:
			raise Exception(f"Erro Sintático 🠊 Expressão Inválida 🠊 '{Parser.tokens.actual.token_value}'")

		return resultado


	def run(input_text):
		"""
		Roda o Parser
		"""
		Parser.tokens = Tokenizer(input_text)
		Parser.tokens.selectNext()
		resultado = Parser.parseProgram()
		resultado.children.append(FuncCall('Principal'))

		if Parser.tokens.actual.token_type != 'EOF':
			raise Exception(f"Erro Sintático 🠊 Expressão Inválida 🠊 '{Parser.tokens.actual.token_value}'")

		return resultado