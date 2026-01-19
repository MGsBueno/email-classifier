type Classificacao = "Produtivo" | "Improdutivo";
interface ResultadoEmail {
    classificacao: Classificacao;
    justificativa: string;
    respostaSugerida: string;
}
declare const fileInput: HTMLInputElement;
declare const textarea: HTMLTextAreaElement;
declare const form: HTMLFormElement;
declare const cardsContainer: HTMLDivElement;
declare const botaoTeste: HTMLButtonElement;
declare const botaoCancelarArquivo: HTMLButtonElement;
declare function classificarEmail(conteudo: string): ResultadoEmail;
declare function gerarCard(r: ResultadoEmail): string;
declare function renderizarResultado(r: ResultadoEmail): void;
declare function configurarCopiar(): void;
//# sourceMappingURL=email-classifier.d.ts.map