# RLE Compressor for Silesia Corpus

Este projeto implementa um compressor e descompressor usando Run-Length Encoding (RLE) em Python, aplicável tanto a ficheiros binários genéricos como a imagens (PNG, JPEG, BMP). Inclui cálculo de métricas de compressão, geração de gráficos e tratamento inteligente de casos onde a compressão não é vantajosa.

---

## Estrutura do Projeto

```
Multimedia/
├── CorpusSilesia/           # Pasta de input com ficheiros do corpus Silesia (texto e binários)
├── io_utils.py              # Leitura/escrita de ficheiros em bytes
├── rle.py                   # Implementação de RLE com limiar e escape
├── metrics.py               # Cálculo de métricas e geração de CSV
└── main.py                  # Script principal: processamento, fallback e gráficos
```

---

## Requisitos

* Python 3.7+
* Bibliotecas Python:

  ```bash
  pip install pillow pandas matplotlib
  ```

---

## Uso

No diretório `Multimedia/`, execute:

```bash
python main.py --input <path_para_CorpusSilesia> --output <pasta_output>
```

Exemplo:

```bash
python main.py --input .\CorpusSilesia\ --output .\RLE_Output\
```

* Os ficheiros comprimidos (ou originais, se RLE não ajudar) ficam em `RLE_Output/compressed/`.
* Os ficheiros restaurados ficam em `RLE_Output/decompressed/` (originais perfeitamente recuperados).
* Métricas são escritas em CSV em `RLE_Output/results/metrics.csv`.
* Gráficos gerados:

  * `RLE_Output/results/compression_ratios.png`
  * `RLE_Output/results/times.png`

---

## Módulos

### io\_utils.py

* `read_file_bytes(path: str) -> bytes` — lê ficheiro em binário.
* `write_file_bytes(path: str, data: bytes) -> None` — escreve binário criando diretórios.

### rle.py

Implementa RLE com:

* **ESC** (0x00) como marcador de início.
* **THRESHOLD** (default 4) mínimo para codificar runs.
* Funções:

  * `rle_encode(data: bytes) -> bytes`
  * `rle_decode(encoded: bytes) -> bytes`

### metrics.py

* `compute_compression_ratio(original: bytes, encoded: bytes) -> float`
* `time_function(func, *args) -> (result, elapsed_seconds)`
* `write_metrics_csv(results: list, path: str) -> None` — grava CSV com colunas:
  `file, orig_size, enc_size, compression_ratio, encode_time_s, decode_time_s`

### main.py

Orquestra todo o fluxo:

1. **Argumentos**: `--input`, `--output`.
2. **Processamento** de cada ficheiro/pasta:

   * Detecta imagens vs binários.
   * Carrega dados crus (pixels RGB para imagens).
   * Executa RLE, mede tempos e razão.
   * Se **razão < 1**, grava o ficheiro original em vez do comprimido.
   * Caso contrário, grava `.rle` e restaura original em `decompressed/`.
3. Gera **CSV** de métricas.
4. Plota **gráficos** de razão e tempos e grava PNG.

---

## Customização

* Ajuste do limiar de codificação: edite o valor `THRESHOLD` em `rle.py`.
* Suporte a novos formatos de imagem: adicione à lista `is_image` em `main.py`.

---
