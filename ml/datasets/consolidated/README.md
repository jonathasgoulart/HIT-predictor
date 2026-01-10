# Relatório de Consolidação de Datasets

Data: 2026-01-09 08:16:17

## Resumo

| Gênero | Músicas | Arquivo |
|--------|---------|---------|
| mpb | 1166 | mpb_consolidated.csv |
| rnb_brasil | 1144 | rnb_brasil_consolidated.csv |
| sertanejo | 95 | sertanejo_consolidated.csv |
| pagode | 32 | pagode_consolidated.csv |
| samba | 28 | samba_consolidated.csv |
| forro | 50 | forro_consolidated.csv |
| pop_urban_brasil | 61 | pop_urban_brasil_consolidated.csv |

## Próximos Passos

1. Retreinar modelos com datasets consolidados:
   ```bash
   python ml/retrain_models.py --use-consolidated
   ```

2. Comparar performance antes vs depois

3. Para expansão adicional, consultar: estrategia_expansao_datasets.md