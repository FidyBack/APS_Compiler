%%

"{" { return '{'; }
"}" { return '}'; }
"(" { return '('; }
")" { return ')'; }
";" { return ';'; }
[0-9]+ { return NUMBER; }
"return" { return RETURN; }
"int" { return TYPE; }
"main" { return IDENTIFIER; }

%%
