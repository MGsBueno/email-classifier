def gerar_resposta(classificacao: str) -> str:
    if classificacao == "Produtivo":
        return (
            "Olá,\n\n"
            "Recebemos sua solicitação e ela já foi registrada.\n"
            "Nossa equipe irá analisar o caso e retornaremos assim que possível.\n\n"
            "Atenciosamente,\n"
            "Equipe de Suporte"
        )

    return (
        "Olá,\n\n"
        "Obrigado pela mensagem e pelo contato.\n"
        "No momento, não é necessária nenhuma ação adicional.\n\n"
        "Atenciosamente,\n"
        "Equipe de Atendimento"
    )
