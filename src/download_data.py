"""Baixa o dataset Olist do Kaggle (via kagglehub) e copia os CSVs para data/raw/.

Na primeira execução, o kagglehub pode abrir o navegador para você autorizar
o acesso à sua conta Kaggle (ou usar um kaggle.json, se você já tiver um em
~/.kaggle/kaggle.json).
"""

import logging
import shutil
from pathlib import Path

import kagglehub

from config import RAW_DATA_DIR

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

DATASET = "olistbr/brazilian-ecommerce"


def main() -> None:
    logger.info("Baixando dataset '%s' via kagglehub...", DATASET)
    cache_path = Path(kagglehub.dataset_download(DATASET))
    logger.info("Download concluído em: %s", cache_path)

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    csv_files = list(cache_path.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"Nenhum CSV encontrado em {cache_path}")

    for csv_file in csv_files:
        destino = RAW_DATA_DIR / csv_file.name
        shutil.copy2(csv_file, destino)
        logger.info("Copiado: %s -> %s", csv_file.name, destino)

    logger.info("Pronto! %d arquivos CSV em %s", len(csv_files), RAW_DATA_DIR)


if __name__ == "__main__":
    main()
