#!/usr/bin/python
# -*- coding: utf-8 -*-
# author: Matteo Romanello, matteo.romanello@gmail.com

from __future__ import print_function

class BadCtsUrnSyntax(Exception):
	"""docstring for BadCtsUrnSyntax"""
	pass

class CTS_URN(object):
	"""
	docstring for CTS_URN
	
	This class is basically a port of <https://bitbucket.org/neelsmith/cts/src/9932c604928f77f311b0d679b5f724097548f86d/src/edu/harvard/chs/cts3/CtsUrn.groovy?at=default>
	for Python.
	
	>>> urn_string = "urn:cts:greekLit:tlg0003.tlg001"
	>>> urn = CTS_URN(urn_string)
	
	>>> urn_string = u"urn:cts:greekLit:tlg0008.tlg001:173f#δημήτριος"
	>>> print(CTS_URN(urn_string))
	urn:cts:greekLit:tlg0008.tlg001:173f#δημήτριος
	
	"""
	def __init__(self,inp_string):
		self._as_string  = inp_string
		self._cts_namespace = None
		self._passage_component = None
		self._work_component = None
		self._version = None
		self._work = None
		self._textgroup = None
		self._passage_node = None
		self._range_begin = None
		self._range_end = None
		self._subref1 = None
		self._subref_idx1 = None
		self._subref2 = None
		self._subref_idx2 = None
		
		try:
			self._initialize_URN(inp_string)
		except Exception as e:
			raise e
	
	@property
	def passage_component(self):
		"""docstring for passage_component"""
		return self._passage_component
	
	@property
	def work_component(self):
		"""docstring for work_component"""
		return self._work_component
	
	@property
	def cts_namespace(self):
		"""docstring for fname"""
		return self._cts_namespace
	
	@property
	def version(self):
		"""docstring for version"""
		return self._version
	
	@property
	def work(self):
		"""docstring for work"""
		return self._work
	
	@property
	def textgroup(self):
		"""docstring for textgroup"""
		return self._textgroup
	
	def is_range(self):
		"""docstring for is_range"""
		return self._range_begin is not None
	
	def _initialize_URN(self,urn_string):
		"""
		docstring for initialize_URN
		
		>>> bogus_string = "abc:def"
		>>> bogus_urn = CTS_URN(bogus_string)
		
		"""
		components = urn_string.split(":")
		try:
			assert components[0]=="urn" and components[1]=="cts"
		except Exception as e:
			raise BadCtsUrnSyntax("Bad syntax for pseudo-URN: \"%s\""%urn_string)
		
		size = len(components)
		# split the URN into its main components
		if(size == 5):
			self._passage_component = components[4]
			if(components[3]):
				self._work_component = components[3]
				self._cts_namespace = components[2]
			else:
				raise BadCtsUrnSyntax("Bad URN syntax: no textgroup in \"%s\""%urn_string)
		elif(size == 4):
			if(components[3]):
				self._work_component = components[3]
				self._cts_namespace = components[2]
			else:
				raise BadCtsUrnSyntax("Bad URN syntax: no textgroup in \"%s\""%urn_string)
		else:
			raise BadCtsUrnSyntax("Method initializeURN: bad syntax: \"%s\""%urn_string)
		# split the work_component into its sub-parts
		work_components = self.work_component.split('.')
		size = len(work_components)
		if(size == 3):
			self._version = work_components[2]
			self._work = work_components[1]
			self._textgroup = work_components[0]
		elif(size == 2):
			self._work = work_components[1]
			self._textgroup = work_components[0]
		else:
			self._textgroup = work_components[0]
		#
		if(self.passage_component):
			range_components = self.passage_component.split('-')
			size = len(range_components)
			if(size == 2):
				self._initialize_range(range_components[0],range_components[1])
			elif(size == 1):
				self._initialize_point(range_components[0])
		return
	
	def _index_subref(self,istring):
		"""docstring for _index_subref"""
		import re
		regexp = re.compile(r'(.*)\[(.+)\]')
		match = regexp.match(istring)
		if(match is not None):
			return match.groups()
		else:
			return (istring,)
	
	def _parse_scope(self,istring):
		"""docstring for _parse_scope"""
		result = None
		split_sub = istring.split('#')
		size = len(split_sub)
		if(size ==1):
			return (split_sub[0],)
		elif(size == 2):
			return (split_sub[0],) + self._index_subref(split_sub[1])
		return result
	
	def _initialize_range(self,str1,str2):
		"""docstring for initialize_range"""	
		temp = self._parse_scope(str1)
		if(len(temp)==1):
			self._range_begin = temp[0]
		elif(len(temp)==2):
			self._range_begin = temp[0]
			self._subref1 = temp[1]
		elif(len(temp)==3):
			self._range_begin = temp[0]
			self._subref1 = temp[1]
			self._subref_idx1 = int(temp[2])
		else:
			raise BadCtsUrnSyntax("Bad URN syntax in \"%s\""%point)
			
		temp = self._parse_scope(str2)
		if(len(temp)==1):
			self._range_end = temp[0]
		elif(len(temp)==2):
			self._range_end = temp[0]
			self._subref2 = temp[1]
		elif(len(temp)==3):
			self._range_end = temp[0]
			self._subref2 = temp[1]
			self._subref_idx2 = int(temp[2])
		else:
			raise BadCtsUrnSyntax("Bad URN syntax in \"%s\""%point)
	
	def _initialize_point(self,point):
		"""
		docstring for initialize_range
		"""
		temp = self._parse_scope(point)
		if(len(temp)==1):
			self._passage_node = temp[0]
		elif(len(temp)==2):
			self._passage_node = temp[0]
			self._subref1 = temp[1]
		elif(len(temp)==3):
			self._passage_node = temp[0]
			self._subref1 = temp[1]
			self._subref_idx1 = int(temp[2])
		else:
			raise BadCtsUrnSyntax("Bad URN syntax in \"%s\""%point)
	
	def get_urn_without_passage(self):
		"""docstring for get_urn_without_passage"""
		return u"urn:cts:%s:%s"%(self._cts_namespace,self._work_component)
	
	def get_passage(self,limit):
		"""docstring for get_passage"""
		psg_vals = self._passage_component.split('.')
		passage = [psg_vals[0]]
		count = 1
		if(limit > len(psg_vals)):
			return self._passage_component
		else:
			while(count < limit):
				passage.append(psg_vals[count])
				count += 1
			return ".".join(passage)
			
	
	def get_leaf_ref_value(self):
		"""docstring for get_leaf_ref_value"""
		pass
	
	def get_citation_depth(self):
		"""docstring for get_citation_depth"""
		return len(self._passage_component.split('.'))
	
	def trim_passage(self,limit):
		"""docstring for trim_passage"""
		return "%s:%s"%(self.get_urn_without_passage(),self.get_passage(limit))
	
	def __unicode__(self):
		return self._as_string
	
	def __str__(self):
		"""
		docstring for __str__
		"""
		return unicode(self).encode('utf-8')

	def __repr__(self):
		return self._as_string
	
if __name__ == "__main__":
	import doctest
	doctest.testmod()
