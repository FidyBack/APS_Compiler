import re

class PrePro:
	def filter(raw_text):
		new_text = re.sub(r'//.*', '', raw_text)
		new_text = re.sub(r'/\*(.|\n)*?\*/', '', new_text, flags=re.MULTILINE)

		if "/*" in new_text:
			raise Exception("Erro Léxico 🠊 '/*' encontrado no texto")
		elif "*/" in new_text:
			raise Exception("Erro Léxico 🠊 '*/' encontrado no texto")

		return new_text