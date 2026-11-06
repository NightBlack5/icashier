# Design

O `FinancialOrchestrator` identifica intenção de escrita antes de chamar o
modelo. Para perguntas de saldo, gastos, categorias, orçamento e metas, ele
monta uma resposta com cálculos locais e não depende de texto gerado para os
números. Perguntas educativas continuam usando Ollama, mas recebem instruções
explícitas para não inventar identidade, empresa, valores ou ações realizadas.

O histórico enviado ao modelo fica limitado e o contexto não contém credenciais.
Nenhuma resposta pode representar uma escrita como concluída.
