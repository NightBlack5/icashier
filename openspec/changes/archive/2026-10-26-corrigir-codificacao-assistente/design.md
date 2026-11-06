# Design

Os textos serão armazenados como UTF-8 válido no código Python. Um teste de
regressão lerá o arquivo de estado em UTF-8 e rejeitará marcadores comuns de
mojibake (`Ã`, `Â` e `�`), evitando que uma conversão incorreta volte a quebrar
a interface.
