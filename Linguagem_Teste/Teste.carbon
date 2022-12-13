funcao Soma(a, b: inteiro) -> inteiro
{
    variavel c: inteiro;
    c = leia();
    retorne  a -- b + c;
}

funcao TextoSaida(total: inteiro, pal: palavra) -> palavra
{
    retorne "Resultado é " . pal . total;

}

funcao Principal()
{
    variavel saida: palavra;
    variavel soma_total: inteiro;
    soma_total = Soma(10, 20);

    enquanto(soma_total > 20+10) {
        soma_total = soma_total-1;
        se (soma_total > 35){
            escreva(TextoSaida(soma_total, "maior que 35: "));
        } senao se (soma_total == 35) {
            escreva(TextoSaida(soma_total, "igual a 35: "));
        } senao {
            escreva(TextoSaida(soma_total, "menor que 35: "));
        }
        saida = TextoSaida(soma_total, "");
    }

    escreva(saida);
}