# FASTA_MotifScanner

Este script permite filtrar secuencias en un archivo FASTA basado en motivos específicos. Fue desarrollado por Allan Peñaloza - Otárola.

## Descripción

El script analiza secuencias de un archivo FASTA y filtra aquellas que contienen motivos específicos de ZIC2 y CTCF. Utiliza procesamiento paralelo para mejorar la eficiencia.

## Motivos

- **Motivos ZIC2**: `TGAGGCT`, `GCGTGGG`, `TGGGAGG`
- **Motivo CTCF**: `CCGCGNGGNGGCAG` (se generan todas las combinaciones posibles reemplazando `N` por `A`, `C`, `G` o `T`)

## Requisitos

- Python 3.x
- Biopython
- Multiprocessing

## Instalación

Instala las dependencias necesarias usando pip:

```bash
pip install biopython
```

## Uso

```bash
python script.py -q <archivo_fasta> -o <archivo_salida> [-c <núcleos>]
```

### Argumentos

- `-q`, `--query`: Archivo FASTA a procesar (obligatorio).
- `-o`, `--output`: Archivo de salida en formato FASTA con las coincidencias (obligatorio).
- `-c`, `--cores`: Número de núcleos a utilizar (opcional, por defecto 2).

### Ejemplo

```bash
python script.py -q secuencias.fasta -o filtradas.fasta -c 4
```

## Salida

El script genera un archivo FASTA con las secuencias que contienen al menos un motivo de ZIC2 y un motivo de CTCF. Además, imprime estadísticas sobre el análisis:

- Total de secuencias analizadas.
- Secuencias que cumplen con los motivos ZIC2.
- Secuencias que cumplen con el motivo CTCF.
- Secuencias que cumplen con al menos un motivo de ZIC2 y un motivo de CTCF.
- Secuencias que no cumplen con ninguno de los motivos.

## Autor

Allan Peñaloza - Otárola
