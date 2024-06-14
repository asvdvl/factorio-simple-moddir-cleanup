# factorio-simple-moddir-cleanup

Automatically deletes (moves to subfolders) mod files. The process occurs in 2 stages.
1. moving outdated mods to `./old`
2. moving disabled ones in `mod-list.json` file to `./disabled`

Run:
```
python ./main.py <path to moddir>
```
example
```
python ./main.py ~/.factorio/mods
```

the script has created 2 folders `./old` and `./disabled`, the remaining files are working mods.