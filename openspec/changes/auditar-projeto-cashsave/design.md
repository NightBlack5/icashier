# Design da auditoria

1. Usar o código Python, definições `.xs`, documentação, histórico de estado do
   Git e execução local como fontes independentes de evidência.
2. Separar fatos comprovados, hipóteses e recomendações; não considerar uma tela
   renderizada como prova de integração funcional.
3. Não expor valores de `.env`, tokens, senhas ou dados pessoais.
4. Executar somente comandos de leitura, compilação, testes isolados e smoke
   tests de navegador que não escrevam no Xano.
5. Manter o relatório como artefato de diagnóstico revisável; correções devem
   ser tratadas em mudanças posteriores.
