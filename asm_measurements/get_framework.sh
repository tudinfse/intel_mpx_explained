#!/usr/bin/env bash

# get the framework
wget http://www.agner.org/optimize/testp.zip
unzip testp.zip

mkdir TestScripts/
mv TestScripts.zip TestScripts/
cd TestScripts/
unzip TestScripts.zip
rm TestScripts.zip
cd ..

mkdir PMCTest/
mv PMCTest.zip PMCTest/
cd PMCTest/
unzip PMCTest.zip
rm PMCTest.zip
cd ..

# copy our files
cp *.sh1 TestScripts/
cp *.inc TestScripts/
