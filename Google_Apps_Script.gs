const NOME_ABA = "Planilha 2";
const LINHA_ID = 2;
const COLUNA_INICIAL_ID = 3;
const API_TOKEN = "MUSICALIZANDO_2026";

function doGet(e) {
  try {
    if ((e.parameter.token || "") !== API_TOKEN) {
      return respostaJSON({sucesso:false, erro:"Token inválido."});
    }
    if (e.parameter.acao === "novo_id") {
      return respostaJSON(gerarNovoId());
    }
    return respostaJSON({sucesso:false, erro:"Ação GET inválida."});
  } catch (erro) {
    return respostaJSON({sucesso:false, erro:erro.message});
  }
}

function doPost(e) {
  try {
    const dados = JSON.parse(e.postData.contents);
    if (dados.token !== API_TOKEN) {
      return respostaJSON({sucesso:false, erro:"Token inválido."});
    }

    if (dados.acao === "salvar_participante") {
      return respostaJSON(salvarParticipante(dados));
    }

    if (dados.acao === "registrar_resposta") {
      return respostaJSON(registrarResposta(dados));
    }

    if (dados.acao === "sincronizar_participante") {
      return respostaJSON(sincronizarParticipante(dados));
    }

    return respostaJSON({sucesso:false, erro:"Ação POST inválida."});
  } catch (erro) {
    return respostaJSON({sucesso:false, erro:erro.message});
  }
}

function obterAba() {
  const aba = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(NOME_ABA);
  if (!aba) throw new Error("A aba '" + NOME_ABA + "' não foi encontrada.");
  return aba;
}

function encontrarLinha(label) {
  const aba = obterAba();
  const ultimaLinha = aba.getLastRow();
  const valores = aba.getRange(1, 2, ultimaLinha, 1).getDisplayValues();

  for (let i = 0; i < valores.length; i++) {
    if (String(valores[i][0]).trim() === label) return i + 1;
  }

  throw new Error("Não encontrei a linha '" + label + "' na coluna B.");
}

function encontrarColunaPorId(id) {
  const aba = obterAba();
  const ultimaColuna = aba.getLastColumn();

  if (ultimaColuna < COLUNA_INICIAL_ID) {
    throw new Error("Ainda não existem colunas de participantes.");
  }

  const quantidade = ultimaColuna - COLUNA_INICIAL_ID + 1;
  const valores = aba.getRange(
    LINHA_ID, COLUNA_INICIAL_ID, 1, quantidade
  ).getDisplayValues()[0];

  for (let i = 0; i < valores.length; i++) {
    if (String(valores[i]).trim() === String(id).trim()) {
      return COLUNA_INICIAL_ID + i;
    }
  }

  throw new Error("O participante '" + id + "' não foi encontrado.");
}

function gerarNovoId() {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    const aba = obterAba();
    const ultimaColuna = aba.getLastColumn();
    let maiorNumero = 0;

    if (ultimaColuna >= COLUNA_INICIAL_ID) {
      const quantidade = ultimaColuna - COLUNA_INICIAL_ID + 1;
      const ids = aba.getRange(
        LINHA_ID, COLUNA_INICIAL_ID, 1, quantidade
      ).getDisplayValues()[0];

      ids.forEach(function(valor) {
        const resultado = String(valor).trim().match(/^MUS-(\d+)$/);
        if (resultado) {
          const numero = parseInt(resultado[1], 10);
          if (numero > maiorNumero) maiorNumero = numero;
        }
      });
    }

    const id = "MUS-" + String(maiorNumero + 1).padStart(4, "0");
    const novaColuna = Math.max(ultimaColuna + 1, COLUNA_INICIAL_ID);

    aba.getRange(LINHA_ID, novaColuna).setValue(id);

    return {sucesso:true, id:id, coluna:novaColuna};
  } finally {
    lock.releaseLock();
  }
}

function salvarParticipante(dados) {
  if (!dados.id) throw new Error("ID do participante não informado.");

  const aba = obterAba();
  const coluna = encontrarColunaPorId(dados.id);

  aba.getRange(encontrarLinha("Usuário"), coluna).setValue(dados.usuario || "");
  aba.getRange(encontrarLinha("Idade"), coluna).setValue(dados.idade || "");
  aba.getRange(encontrarLinha("Série"), coluna).setValue(dados.serie || "");

  return {sucesso:true, id:dados.id, coluna:coluna};
}

function registrarResposta(dados) {
  if (!dados.id) throw new Error("ID do participante não informado.");
  if (!dados.pergunta) throw new Error("Pergunta não informada.");

  const aba = obterAba();
  const coluna = encontrarColunaPorId(dados.id);
  const linha = encontrarLinha(dados.pergunta);

  aba.getRange(linha + 1, coluna).setValue(dados.resposta || "");
  aba.getRange(linha + 2, coluna).setValue(dados.correta ? "Sim" : "Não");

  if (dados.tempo !== null && dados.tempo !== undefined && dados.tempo !== "") {
    aba.getRange(linha + 3, coluna).setValue(Number(dados.tempo));
  } else {
    aba.getRange(linha + 3, coluna).setValue("");
  }

  return {sucesso:true, id:dados.id, pergunta:dados.pergunta};
}

function sincronizarParticipante(dados) {
  const lock = LockService.getScriptLock();
  lock.waitLock(30000);

  try {
    if (!dados.id) throw new Error("ID do participante não informado.");

    const aba = obterAba();
    const coluna = encontrarColunaPorId(dados.id);

    aba.getRange(encontrarLinha("Usuário"), coluna).setValue(dados.usuario || "");
    aba.getRange(encontrarLinha("Idade"), coluna).setValue(dados.idade || "");
    aba.getRange(encontrarLinha("Série"), coluna).setValue(dados.serie || "");

    ["fase1", "fase2", "fase3"].forEach(function(fase) {
      (dados[fase] || []).forEach(function(registro) {
        if (!registro.pergunta) return;

        const linha = encontrarLinha(registro.pergunta);
        aba.getRange(linha + 1, coluna).setValue(registro.resposta || "");
        aba.getRange(linha + 2, coluna).setValue(registro.correta ? "Sim" : "Não");

        if (registro.tempo_resposta !== null &&
            registro.tempo_resposta !== undefined &&
            registro.tempo_resposta !== "") {
          aba.getRange(linha + 3, coluna).setValue(
            Number(registro.tempo_resposta)
          );
        }
      });
    });

    return {sucesso:true, id:dados.id, coluna:coluna};
  } finally {
    lock.releaseLock();
  }
}

function respostaJSON(objeto) {
  return ContentService
    .createTextOutput(JSON.stringify(objeto))
    .setMimeType(ContentService.MimeType.JSON);
}
