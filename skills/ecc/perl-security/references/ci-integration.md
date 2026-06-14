# CI integration
perlcritic --severity 4 --theme security --quiet lib/ || exit 1
```