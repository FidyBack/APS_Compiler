import sys
from cparser import Parser
from pre_pro import PrePro
from nodes import SymbolTable

if __name__ == "__main__":
	try:
		with open(sys.argv[1], 'r', encoding = 'utf-8') as f:
			text = f.read()
		input_filtred = PrePro.filter(text)
		Parser.run(input_filtred).Evaluate(SymbolTable())

	except IndexError:
		raise Exception("Erro 🠊 Arquivado não especificado")

	except FileNotFoundError:
		raise Exception(f"Erro 🠊 Arquivo não encontrado 🠊 {sys.argv[1]}")
