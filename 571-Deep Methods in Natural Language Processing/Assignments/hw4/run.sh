#!/bin/bash
#PCFG Generation
./hw4_topcfg.sh $1 $2

#Basic Parse
./hw4_parse.sh $2 $3 $4

#Improved Parse
./hw4_improved_parse.sh $2 $3 $5

#Evaluation
$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD $4 > $6
$TOOLS/evalb -p $TOOLS/COLLINS.prm $GOLD $5 > $7
