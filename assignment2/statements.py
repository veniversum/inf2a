# File: statements.py
# Template file for Informatics 2A Assignment 2:
# 'A Natural Language Query System in Python/NLTK'

# John Longley, November 2012
# Revised November 2013 and November 2014 with help from Nikolay Bogoychev
# Revised November 2015 by Toms Bergmanis and Shay Cohen
# Revised November 2016 by Adam Lopez

# PART A: Processing statements


def add(lst, item):
	if item not in lst:
		lst.insert(len(lst), item)


class Lexicon:
	def __init__(self):
		self.cat_dict = {}

	def add(self, stem, cat):
		self.cat_dict.setdefault(cat, set()).add(stem)

	def getAll(self, cat):
		return sorted(self.cat_dict.get(cat, set()))


class FactBase:
	def __init__(self):
		self.unary_facts = set()
		self.binary_facts = set()
		pass

	def addUnary(self, pred, e1):
		self.unary_facts.add((pred, e1))

	def queryUnary(self, pred, e1):
		return (pred, e1) in self.unary_facts

	def addBinary(self, pred, e1, e2):
		self.binary_facts.add((pred, e1, e2))

	def queryBinary(self, pred, e1, e2):
		return (pred, e1, e2) in self.binary_facts


import re
from nltk.corpus import brown

brown_taggedset = set(brown.tagged_words())


def verb_stem(s):
	def match(pattern):
		return re.match(pattern + '$', s, re.IGNORECASE)

	stem = ''
	if match('.*(?<!.[sxyzaeiou]|ch|sh)s'):
		stem = s[:-1]
	elif match('.*[aeiou]ys'):
		stem = s[:-1]
	elif match('.*.[^aeiou]ies'):
		stem = s[:-3] + 'y'
	elif match('[^aeiou]ies'):
		stem = s[:-1]
	elif match('.*([ox]|ch|sh|ss|zz)es'):
		stem = s[:-2]
	elif match('.*([^s]se|[^z]ze)s'):
		stem = s[:-1]
	elif match('have'):  # we ignore is -> be and does -> do, those are handled by function_words_tags
		return 'has'
	elif match('.*(?<!.[iosxz]|ch|sh)es'):
		stem = s[:-1]
	if (s, 'VBZ') not in brown_taggedset and (stem, 'VB') not in brown_taggedset:
		return ''
	return stem


def add_proper_name(w, lx):
	"""adds a name to a lexicon, checking if first letter is uppercase"""
	if ('A' <= w[0] and w[0] <= 'Z'):
		lx.add(w, 'P')
		return ''
	else:
		return (w + " isn't a proper name")


def process_statement(lx, wlist, fb):
	"""analyses a statement and updates lexicon and fact base accordingly;
	returns '' if successful, or error message if not."""
	# Grammar for the statement language is:
	#   S  -> P is AR Ns | P is A | P Is | P Ts P
	#   AR -> a | an
	# We parse this in an ad hoc way.
	msg = add_proper_name(wlist[0], lx)
	if (msg == ''):
		if (wlist[1] == 'is'):
			if (wlist[2] in ['a', 'an']):
				lx.add(wlist[3], 'N')
				fb.addUnary('N_' + wlist[3], wlist[0])
			else:
				lx.add(wlist[2], 'A')
				fb.addUnary('A_' + wlist[2], wlist[0])
		else:
			stem = verb_stem(wlist[1])
			if (len(wlist) == 2):
				lx.add(stem, 'I')
				fb.addUnary('I_' + stem, wlist[0])
			else:
				msg = add_proper_name(wlist[2], lx)
				if (msg == ''):
					lx.add(stem, 'T')
					fb.addBinary('T_' + stem, wlist[0], wlist[2])
	return msg

# End of PART A.
