#!/bin/bash

if test 0 -ne $(python query-open-tree.py 'Rattus feliceus' 'Rattus hainaldi' 'Rattus hoogerwerfi')
then
    echo "Rattus polytomy did not return 0"
    exit 1
fi

if test 2 -ne $(python query-open-tree.py 'Alces alces' 'Rattus norvegicus'  'Meles meles')
then
    echo "Fereungulates failed to return 2"
    exit 1
fi



if test 1 -ne $(python query-open-tree.py 'Rattus norvegicus' 'Alces alces' 'Meles meles')
then
    echo "Fereungulates failed to return 1"
    exit 1
fi


if python query-open-tree.py 'Rattus norvegicus' 'Alces alces' 'Meles mele' 2>/dev/null
then
    echo "typo in badger did not result in failure"
    exit 1
fi

