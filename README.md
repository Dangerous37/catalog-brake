# Catalog Brake

Build a catalog update plan before applying an import. Incomplete exports can update known rows, but only a complete, bounded snapshot can propose deletions.

## Run locally

Use Python 3.12. The project uses the standard library. From the repository root:

```sh
python cli.py example.json
python -m unittest -v
```

The included example is synthetic. Pass a different UTF-8 JSON file to inspect your own input. The command prints JSON to stdout. Invalid input returns status 2 and an explanation on stderr. See [CONTRACT.md](CONTRACT.md) for input fields and interpretation.

## Operational limits

Completeness relies on a trustworthy upstream page count and immutable snapshot. A threshold limits the blast radius but cannot detect incorrect product values.

## Resumen en español

Previsualiza un lote de catálogo y protege las bajas cuando faltan páginas o desaparece una proporción inesperada de productos.
