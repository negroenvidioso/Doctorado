###################################################################################
#                                                                                 #
#                         FASTA_MotifScanner                                      #
#                                                                                 #
# Este script analiza archivos FASTA para identificar y escanear motivos          #
# específicos dentro de las secuencias.                                           #
#                                                                                 #
# Autor: Allan Javier Peñaloza Otárola                                            #
# Contacto: allan.penaloza@ug.uchile.cl                                           #
# Fecha: 26/12/2024                                                               #
#                                                                                 #
###################################################################################

import argparse
from Bio import SeqIO
import re
from multiprocessing import Pool, cpu_count

# Definir los motivos
zic2_motifs = ["TGAGGCT", "GCGTGGG", "TGGGAGG"]
ctcf_motif = "CCGCGNGGNGGCAG"

# Generar todas las combinaciones posibles para el motivo CTCF
def generate_combinations(motif):
    if 'N' not in motif:
        return [motif]
    else:
        combinations = []
        for base in 'ACGT':
            combinations += generate_combinations(motif.replace('N', base, 1))
        return combinations

ctcf_combinations = generate_combinations(ctcf_motif)

# Función para filtrar secuencias basadas en los motivos
def filter_sequence(record):
    sequence = str(record.seq)
    zic2_match = any(motif in sequence for motif in zic2_motifs)
    ctcf_match = any(re.search(motif, sequence) for motif in ctcf_combinations)
    return record, zic2_match, ctcf_match

def filter_sequences(fasta_file, cores):
    with Pool(cores) as pool:
        results = pool.map(filter_sequence, SeqIO.parse(fasta_file, "fasta"))
    return results

def main():
    parser = argparse.ArgumentParser(description="Script para filtrar secuencias FASTA basado en motivos específicos. Escrito por Allan Peñaloza - Otarola")
    parser.add_argument('-q', '--query', required=True, help='Archivo FASTA a procesar')
    parser.add_argument('-o', '--output', required=True, help='Archivo de salida en formato FASTA con las coincidencias')
    parser.add_argument('-c', '--cores', type=int, default=2, help='Número de núcleos a utilizar (por defecto 2)')
    
    args = parser.parse_args()
    
    fasta_file = args.query
    output_file = args.output
    cores = args.cores if args.cores <= cpu_count() else cpu_count()
    
    results = filter_sequences(fasta_file, cores)
    
    total_sequences = len(results)
    zic2_matches = sum(1 for _, zic2_match, _ in results if zic2_match)
    ctcf_matches = sum(1 for _, _, ctcf_match in results if ctcf_match)
    both_matches = sum(1 for _, zic2_match, ctcf_match in results if zic2_match and ctcf_match)
    no_matches = total_sequences - (zic2_matches + ctcf_matches - both_matches)
    
    filtered_sequences = [record for record, zic2_match, ctcf_match in results if zic2_match and ctcf_match]
    
    with open(output_file, "w") as output_handle:
        SeqIO.write(filtered_sequences, output_handle, "fasta")
    
    print(f"Total de secuencias analizadas: {total_sequences}")
    print(f"Secuencias que cumplen con los motivos zic2_motifs: {zic2_matches}")
    print(f"Secuencias que cumplen con el motivo ctcf_motif: {ctcf_matches}")
    print(f"Secuencias que cumplen con al menos un motivo de zic2_motifs y un motivo ctcf_motif: {both_matches}")
    print(f"Secuencias que no cumplen con ninguno de los motivos: {no_matches}")

if __name__ == "__main__":
    main()
