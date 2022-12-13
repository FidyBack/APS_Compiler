from caracters import *

class Token:
	def __init__(self, token_value, token_type):
		self.token_value = token_value
		self.token_type = token_type


class Tokenizer:
	def __init__(self, origin):
		self.origin = origin
		self.position = 0
		self.actual = Token(0, 'inteiro')

	
	def selectNext(self):
		"""
		Verifica se o token é válido e define cada um de acordo com o Alfabeto
		"""
		try:
			# ==================== Elimina caracteres de espaçamento ====================
			if self.origin[self.position] in private_filters:
				while self.origin[self.position] in private_filters:
					self.position += 1

			# ==================== Operadores simples e duplos com o mesmo sinal ====================
			if self.origin[self.position] in private_operators:
				op = self.origin[self.position]
				self.actual = Token(op, private_operators[op])
				self.position += 1

				if self.position < len(self.origin) and op + self.origin[self.position] in private_operators:
					op += self.origin[self.position]
					self.actual = Token(op, private_operators[op])
					self.position += 1

			# ==================== Token duplos idependentes ====================
			elif self.origin[self.position] + self.origin[self.position + 1] in private_operators:
				op = self.origin[self.position] + self.origin[self.position + 1]
				self.actual = Token(op, private_operators[op])
				self.position += 2

			# ==================== Token para os numeros ====================
			elif self.origin[self.position].isdigit():
				self.actual = Token(self.origin[self.position], 'inteiro')
				self.position += 1

				while self.position < len(self.origin) and self.origin[self.position].isdigit():
					self.actual.token_value += self.origin[self.position]
					self.position += 1

				self.actual.token_value = int(self.actual.token_value)

			# ==================== Token para identifiers, palavras reservadas e types ====================
			elif self.origin[self.position].isalpha():
				self.actual = Token(self.origin[self.position], 'IDENTIFIER')
				self.position += 1

				while self.position < len(self.origin) and (self.origin[self.position].isalnum() or self.origin[self.position] == '_'):
					self.actual.token_value += self.origin[self.position]
					self.position += 1

				if self.actual.token_value in private_words:
					self.actual.token_type = self.actual.token_value.upper()
				elif self.actual.token_value in private_types:
					self.actual.token_type = 'TYPE'
					
			# ==================== Token para palavras ====================
			elif self.origin[self.position] == '"':
				self.actual = Token('', 'palavra')
				self.position += 1

				while self.position < len(self.origin) and self.origin[self.position] != '"':
					self.actual.token_value += self.origin[self.position]
					self.position += 1

				self.position += 1

			else:
				raise Exception(f"Erro Léxico 🠊 Token Inválido 🠊 {self.origin[self.position]}")
		
		except IndexError as e:
			# ==================== EOF ====================
			if self.position >= len(self.origin):
				self.actual = Token('', 'EOF')

			else:
				raise e