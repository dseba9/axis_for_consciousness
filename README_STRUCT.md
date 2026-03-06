# Proyecto SampEn

La carpeta ha sido reorganizada para mantener el orden y separar el código fuente, los datos y los resultados.

## Estructura de Carpetas

- **src/**: Contiene los scripts de Python activos para generar las figuras y análisis.
  - `generate_final_figures_v2.py`: Genera Figuras 2 y 3 (Violin plots).
  - `generate_figure1_sorted.py`: Genera Figura 1 (Raincloud plot).
  - `generate_2d_map_clean.py`: Genera Figura 4 (Mapa 2D).
  - Scripts de conceptos (`entropy_examples`, `sliding_window`, etc.).
- **data/**: Contiene los datos de entrada.
  - `all_data_combined.csv`: Dataset principal consolidado.
- **output/**: Carpeta destino para las figuras e imágenes generadas.
- **docs/**: Manuscrito y documentación.
  - `paper.md`: Texto del paper.
  - `paper.pdf`: PDF compilado.
- **archive/**: Contiene archivos antiguos, backups y scripts en desuso.

## Ejecución

Los scripts han sido configurados para buscar los datos en `../data` y guardar los resultados en `../output`.
Para ejecutarlos correctamente, **debes situarte en la carpeta `src`**:

```bash
cd src
python generate_final_figures_v2.py
```

Esto asegurará que las rutas relativas funcionen correctamente.
