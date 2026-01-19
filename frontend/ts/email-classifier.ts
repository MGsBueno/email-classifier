type Classificacao = "Produtivo" | "Improdutivo";

interface ResultadoEmailAPI {
  classificacao: Classificacao;
  justificativa: string;
  respostaSugerida: string; // vem assim do backend (camelCase)
}

const API_BASE = "http://localhost:8000";

// Helpers
function escapeHtml(s: string): string {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

function renderizarLoading(cardsContainer: HTMLElement) {
  cardsContainer.innerHTML = `<p class="loading">🔎 Analisando...</p>`;
}

function renderizarErro(cardsContainer: HTMLElement, msg: string) {
  cardsContainer.innerHTML = `
    <div class="card improdutivo">
      <span class="badge">Erro</span>
      <h3>Não foi possível analisar</h3>
      <p>${escapeHtml(msg)}</p>
    </div>
  `;
}

function gerarCard(r: ResultadoEmailAPI): string {
  const classe = r.classificacao === "Produtivo" ? "produtivo" : "improdutivo";

  return `
    <div class="card ${classe}">
      <span class="badge">${r.classificacao}</span>
      <h3>${r.classificacao}</h3>

      <p><strong>Justificativa:</strong><br>${escapeHtml(r.justificativa)}</p>

      <p><strong>Resposta sugerida:</strong></p>
      <pre class="resposta-texto">${escapeHtml(r.respostaSugerida)}</pre>

      <button class="btn-copiar" data-resposta="${encodeURIComponent(
        r.respostaSugerida,
      )}">📋 Copiar resposta</button>
    </div>
  `;
}

function configurarCopiar() {
  document.querySelectorAll<HTMLButtonElement>(".btn-copiar").forEach((b) => {
    b.onclick = async () => {
      const texto = decodeURIComponent(b.dataset.resposta || "");
      await navigator.clipboard.writeText(texto);
      b.textContent = "✅ Copiado!";
      setTimeout(() => (b.textContent = "📋 Copiar resposta"), 1500);
    };
  });
}

function renderizarResultado(
  cardsContainer: HTMLElement,
  r: ResultadoEmailAPI,
) {
  cardsContainer.innerHTML = gerarCard(r);
  configurarCopiar();
}

// Chamadas ao backend
async function classificarPorTexto(texto: string): Promise<ResultadoEmailAPI> {
  const resp = await fetch(`${API_BASE}/classificar`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ texto }),
  });

  if (resp.status === 422) {
    // FastAPI geralmente manda {"detail": ...} mas pode variar
    const data = await resp.json().catch(() => null);
    throw new Error(
      data?.detail
        ? "Texto inválido. Verifique se não está vazio."
        : "Texto inválido.",
    );
  }

  if (!resp.ok) {
    throw new Error(`Erro no servidor (${resp.status}).`);
  }

  return (await resp.json()) as ResultadoEmailAPI;
}

async function classificarPorArquivo(file: File): Promise<ResultadoEmailAPI> {
  const formData = new FormData();
  formData.append("file", file);

  const resp = await fetch(`${API_BASE}/classificar/arquivo`, {
    method: "POST",
    body: formData,
  });

  if (resp.status === 415) {
    throw new Error("Tipo de arquivo não suportado. Envie .txt ou .pdf.");
  }

  if (resp.status === 422) {
    const data = await resp.json().catch(() => null);
    const detail = data?.detail ? String(data.detail) : "Arquivo inválido.";
    throw new Error(detail);
  }

  if (!resp.ok) {
    throw new Error(`Erro no servidor (${resp.status}).`);
  }

  return (await resp.json()) as ResultadoEmailAPI;
}

// Inicialização segura
function init() {
  const fileInput = document.getElementById(
    "emailFile",
  ) as HTMLInputElement | null;
  const textarea = document.getElementById(
    "body_email",
  ) as HTMLTextAreaElement | null;
  const form = document.querySelector("form") as HTMLFormElement | null;
  const cardsContainer = document.getElementById(
    "cards",
  ) as HTMLDivElement | null;
  const botaoTeste = document.getElementById(
    "testarCards",
  ) as HTMLButtonElement | null;
  const botaoCancelarArquivo = document.getElementById(
    "cancelarArquivo",
  ) as HTMLButtonElement | null;

  // Se algum elemento principal não existir, não quebra a página
  if (
    !fileInput ||
    !textarea ||
    !form ||
    !cardsContainer ||
    !botaoCancelarArquivo
  ) {
    console.error(
      "HTML não contém todos os elementos esperados. IDs conferem?",
    );
    console.error({
      fileInput,
      textarea,
      form,
      cardsContainer,
      botaoCancelarArquivo,
      botaoTeste,
    });
    return;
  }

  // UX: controle arquivo ↔ texto
  fileInput.addEventListener("change", () => {
    if (fileInput.files && fileInput.files.length > 0) {
      textarea.value = "";
      textarea.disabled = true;
      botaoCancelarArquivo.style.display = "inline-block";
    }
  });

  textarea.addEventListener("input", () => {
    if (textarea.value.trim()) {
      fileInput.value = "";
      botaoCancelarArquivo.style.display = "none";
      textarea.disabled = false;
    }
  });

  botaoCancelarArquivo.addEventListener("click", () => {
    fileInput.value = "";
    textarea.disabled = false;
    botaoCancelarArquivo.style.display = "none";
  });

  // Submit (3 cases)
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    try {
      renderizarLoading(cardsContainer);

      // 1) textarea
      const texto = textarea.value.trim();
      if (texto) {
        const resultado = await classificarPorTexto(texto);
        renderizarResultado(cardsContainer, resultado);
        return;
      }

      // 2) arquivo (txt/pdf)
      if (!fileInput.files || fileInput.files.length === 0) {
        renderizarErro(
          cardsContainer,
          "Envie um arquivo (.txt/.pdf) ou cole o texto do email.",
        );
        return;
      }

      const arquivo = fileInput.files[0];
      if (!arquivo) {
        renderizarErro(cardsContainer, "Arquivo inválido. Tente novamente.");
        return;
      }

      const resultado = await classificarPorArquivo(arquivo);
      renderizarResultado(cardsContainer, resultado);
    } catch (err) {
      const msg = err instanceof Error ? err.message : "Erro desconhecido.";
      renderizarErro(cardsContainer, msg);
    }
  });

  // Botão de teste (BACKEND REAL)
  if (botaoTeste) {
    botaoTeste.addEventListener("click", async () => {
      try {
        renderizarLoading(cardsContainer);
        const resultado = await classificarPorTexto(
          "Estou com erro no sistema e preciso de suporte urgente.",
        );
        renderizarResultado(cardsContainer, resultado);
      } catch (err) {
        const msg = err instanceof Error ? err.message : "Erro desconhecido.";
        renderizarErro(cardsContainer, msg);
      }
    });
  }
}

init();
