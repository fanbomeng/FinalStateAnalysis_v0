#!/usr/bin/env python

from rootpy.io import open
from FinalStateAnalysis.TMegaSelector.megaselect import TMegaPySelector

# test_file.root can be generated by the CPP unit test
file = open('test_file.root')

tree = file.Get("TestTree")
print "Got tree with %i entries" % tree.GetEntries()

print "Running process"
tree.Process("TMegaPySelector", "TestSelector")
#tree.Process("TPySelector", "TestSelector")

print "Done"
