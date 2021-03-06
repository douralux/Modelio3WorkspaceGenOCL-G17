"""
=========================================================
                       GenOCL.py
 Generate a USE OCL specification from a UML package
=========================================================

FILL THIS SECTION AS SHOWN BELOW AND LINES STARTING WITH ###
@author Xuan Shong TI WONG SHI <xuan.ti@mydomain.com>
@author Maria Shohie CEZAR LOPEZ DE ANDERA <maria.cezar@ujf-grenoble.fr>
@group  G17

Current state of the generator
----------------------------------
FILL THIS SECTION 
Explain which UML constructs are supported, which ones are not.
All UML constructs of the provided project UMLTestCases, (ClassModels) are supported except those which are not implemented in USE specifications like:
	- Attributes visiblity
	- Attributes cardinality
	
What is good in your generator?
	- Our generator covers most of use uml models and can be then used by end user easily
	
What are the current limitations?
	- The Nary association is considered like an 'association', it means that we haven't aggregation or composition generator for Nary asso but we believe that simple association can deal with it
	- Also with Nary association we didn't take account the case of Nary association class

Current state of the tests
--------------------------
FILL THIS SECTION 
Explain how did you test this generator.
   We tested our generator with class models which are in project UMLTestCases. And we believe that these models are sufficient to cover the most used models in UML to generate
   use OCL code.
   To test our generator on functional case we tested on CyberResidence Project. The result generated is loaded in USE app. The result for USE showed no errors.

Which test are working? 
	All tests work. 
	
Which are not?
	None.
	
Observations
------------
Additional observations could go there
	None
"""


#---------------------------------------------------------
#   Helpers on the source metamodel (UML metamodel)
#---------------------------------------------------------
# The functions below can be seen as extensions of the
# modelio metamodel. They define useful elements that 
# are missing in the current metamodel but that allow to
# explorer the UML metamodel with ease.
# These functions are independent from the particular 
# problem at hand and could be reused in other 
# transformations taken UML models as input.
#---------------------------------------------------------

# example
def isAssociationClass(clazz):
	""" 
	Return True if and only if the element is an association 
	that have an associated class, or if this is a class that
	has a associated association. (see the Modelio metamodel
	for details)
	"""
	if clazz.linkToAssociation is None:
		return False
	
	return True
    
 
#---------------------------------------------------------
#   Application dependent helpers on the source metamodel
#---------------------------------------------------------
# The functions below are defined on the UML metamodel
# but they are defined in the context of the transformation
# from UML Class diagramm to USE OCL. There are not
# intended to be reusable. 
#--------------------------------------------------------- 

# example
def associationsInPackage(package):
    """
    Return the list of all associations that start or
    arrive to a class which is recursively contained in
    a package.
    """

def inheritance(clazz):
	'''
	Check if a class is subclass of another class 
	then return the representation in OCL format
	'''	
	parents = clazz.parent
	i = 0
	size = len(parents)
	result = ' < '
	
	while i < (size - 1):
		p = parents.get(i)
		result = result + p.superType.name + ', '
		i = i + 1
	
	if size > 0:
		result = result + parents.get(i).superType.name
	else:
		result = ''
		
	return result

def abstract(clazz):
	'''
	Return 'abstract' if clazz is abstract
	'''
	if clazz.isIsAbstract():
		return 'abstract '
	
	return ''
	
def upcaseFirstLetter(str):
	'''
	Upcase the first letter of str
	'''
	if str == '':
		return ''
		
	return str[0].upper() + str[1:]
	
def associationRoleName(asso):
	'''
	Get the association end role name
	'''
	if len(asso.name) > 0:
		return ' role ' + upcaseFirstLetter(asso.name)
		
	return ''

def isAssociationRelationship(asso):
	'''
	Return true if asso is an association relationship, false if not
	Is merely the same as isAssociation class !
	'''
	if asso.linkToClass is None:
		return False
		
	return True
	
def associationClassString(asso):
	'''
	Return 'associationClass' if asso is an association class or 'association' | 'composition'
	| 'aggregation' if not
	'''
	if isAssociationRelationship(asso):
		return 'associationclass '
	
	# Try to find the kind of association
	kind = 'association '
	for end in asso.end:
		if end.aggregation == AggregationKind.KINDISCOMPOSITION:
			kind = 'composition '
			break
		if end.aggregation == AggregationKind.KINDISAGGREGATION:
			kind = 'aggregation '
			break
		
	return kind

def isUnspecifiedAssociation(asso):
	'''
	Return true if it's an unspecified asso (unamed)
	'''
	if len(asso.name) == 0:
		return True
		
	return False
	
def isNAryAssociation(asso):
	'''
	true if it's an NAry association
	'''
	 
	
def orderedEndKeyWord(end):
	'''
	Return the key word 'ordered' if endAsso is ordered
	'''
	if end.isIsOrdered():
		return ' ordered'
		
	return ''
	 
#---------------------------------------------------------
#   Helpers for the target representation (text)
#---------------------------------------------------------
# The functions below aims to simplify the production of
# textual languages. They are independent from the 
# problem at hand and could be reused in other 
# transformation generating text as output.
#---------------------------------------------------------


# for instance a function to indent a multi line string if
# needed, or to wrap long lines after 80 characters, etc.

#---------------------------------------------------------
#           Transformation functions: UML2OCL
#---------------------------------------------------------
# The functions below transform each element of the
# UML metamodel into relevant elements in the OCL language.
# This is the core of the transformation. These functions
# are based on the helpers defined before. They can use
# print statement to produce the output sequentially.
# Another alternative is to produce the output in a
# string and output the result at the end.
#---------------------------------------------------------



# examples

def umlEnumeration2OCL(enumeration):
	"""
	Generate USE OCL code for the enumeration
	"""
	i = 0
	values = enumeration.value
	n = len(values) 
	
	if n == 0:
		return
	
	print normalizeNote(umlNote2OCL(enumeration.descriptor))
	print 'enum ' + enumeration.name 
	print '{'
	
	while i < (n - 1):
		print '\t' + values.get(i).name + ','
		i = i + 1
	print '\t' + values.get(i).name
			
	print '}\n'
    

def umlBasicType2OCL(basicType):
	"""
	Generate USE OCL basic type. Note that
	type conversions are required.
	"""
	if basicType == 'float':
		return 'Real'
		
	return upcaseFirstLetter(basicType)

def normalizeNote(str):
	'''
	Replace \n by \n-- in order to avoid unencommented note
	'''
	if len(str) > 0:
		return str.replace('\n', '\n-- ')
		
	return str
	
def operationNotes(operation):
	'''
	Get an operation comment to OCL
	'''
	i = 0
	parameters = operation.getIO()
	n = len(parameters)
	
	result = normalizeNote(umlNote2OCL(operation.descriptor)) 
	
	if n == 0:
		return result
		
	while i < (n-1):
		result = result + normalizeNote(umlNote2OCL(parameters.get(i).descriptor)) + '\n'
		i = i + 1
	
	result = result + normalizeNote(umlNote2OCL(parameters.get(i).descriptor))
	
	return result

def parameter2OCL(parameters):
	"""
	Parameter representation in OCL
	"""
	i = 0
	n = len(parameters)
	result = ''
	
	if n == 0:
		return result
		
	while i < (n-1): 
		result = result + parameters.get(i).name + ' : ' + upcaseFirstLetter(parameters.get(i).type.name) + ', '
		i = i + 1

	result = result + parameters.get(i).name + ' : ' + upcaseFirstLetter(parameters.get(i).type.name)
	
	return result

def return2OCL(retur):
	'''
	OCL return representation
	'''
	result = ''

	if retur is None:
		return result
		
	if retur.multiplicityMax == '1' and retur.multiplicityMin == '1':
		result = ' : ' + upcaseFirstLetter(retur.type.name)
		
	else:
		result = ' : ' + 'Set(' + upcaseFirstLetter(retur.type.name) + ')'
	
	return result
	
def umlAttribute2OCL(attribute):
	"""
	UML attribute generation
	"""
	print '\t' + attribute.name + ' : ' + umlBasicType2OCL(attribute.type.name) + ' ' + normalizeNote(umlNote2OCL(attribute.descriptor))
	
def umlOperation2OCL(operation):
	"""
	UML operation generation
	"""
	
	print operationNotes(operation)
	print '\t' + operation.name + '(' + parameter2OCL(operation.getIO()) + ') ' + return2OCL(operation.getReturn())
	
def umlClass2OCL(clazz):
	"""
	UML class generation
	"""
	attributes = clazz.ownedAttribute
	operations = clazz.ownedOperation
	
	print normalizeNote(umlNote2OCL(clazz.descriptor))
	
	if not isAssociationClass(clazz):
		print abstract(clazz) + 'class ' + clazz.name + inheritance(clazz)	
		commonUmlClass2OCL(clazz)			
		print 'end\n'
	# else:
	# The else is handled by association generation
	# see umlAssociation2OCL(clazz)
	
	
	# UML association handling
	umlAssociation2OCL(clazz)

def commonUmlClass2OCL(clazz):
	'''
	Common class handling (association class or normal class) :
	<< Essentially class attributes and operations >>
	'''
	attributes = clazz.ownedAttribute
	operations = clazz.ownedOperation
	
	if len(attributes) > 0:
		print 'attributes'
		for attr in attributes:
			umlAttribute2OCL(attr)
	
	if len(operations) > 0:
		print 'operations'
		for op in operations:
			umlOperation2OCL(op)
	
def umlAssociation2OCL(clazz):
	'''
	UML association to OCL
	'''
	ownedEnds = clazz.ownedEnd
	global _global_assoAlreadyTreated
	global _global_asso_unspecified
	
	# For all ownedEnd 
	for owned in ownedEnds: 
		# Get the association
		asso = owned.association 
		
		# Avoid handling orphaned association ;)
		if asso is None:
			continue
		
		# Check if it's an unspecified asso
		assoName = ''
		if isUnspecifiedAssociation(asso):
			assoName = 'unspecifiedName_' + str(_global_asso_unspecified)
			_global_asso_unspecified = _global_asso_unspecified + 1
		else:
			assoName = asso.name
				
			
		# Check if association isn't treat yet
		if not (asso in _global_assoAlreadyTreated):
			# Add the asso to the set
			_global_assoAlreadyTreated.add(asso)
			
			print associationClassString(asso) + assoName + ' between'
			
			for end in asso.end:
				print '\t' + end.owner.name + '[' + end.multiplicityMin + '..' + end.multiplicityMax + ']' + associationRoleName(end) + orderedEndKeyWord(end)			
			
			if isAssociationRelationship(asso):
				# handle association class there
				commonUmlClass2OCL(asso.linkToClass.classPart)
				print 'end\n'
				# handle recursively asso's class association
				umlAssociation2OCL(asso.linkToClass.classPart)
			else:
				print 'end\n'			
	
	# Handle Nary there
	naryEnds = clazz.ownedNaryEnd
	for nary in naryEnds:
		naryAsso = nary.naryAssociation
		
		# Avoid handling orphaned association
		if naryAsso is None:
			continue
		
		# Handle unspecified association
		assoName = naryAsso.name
		if len(assoName) <= 0:
			assoName = 'unspecifiedName_' + str(_global_asso_unspecified)
			_global_asso_unspecified = _global_asso_unspecified + 1
		
		##
		if not(naryAsso in _global_assoAlreadyTreated):
			_global_assoAlreadyTreated.add(naryAsso)
			
			print 'association ' + assoName + ' between'
			
			for end in naryAsso.naryEnd:
				print '\t' + end.owner.name + '[' + end.multiplicityMin + '..' + end.multiplicityMax + ']' + associationRoleName(end) + orderedEndKeyWord(end)
			
			# Handle Nary asso class there not performed yet
			
			print 'end\n'
			
def constraint2OCL(constraint):
	'''
	constraint representation in OCL
	'''
	# Constraint are commented ('--') and let the user the freedom to add the body
	print '-- context ' + constraint.owner.name + ' inv ' + constraint.name 
	
	for note in constraint.descriptor:
		if len(note.content) != 0:
			print '\t-- ' + note.content
		
	print '\n'

def umlNote2OCL(notes):
	'''
	Note to OCL comments
	'''
	result = ''
	
	for note in notes:
		if len(note.content) > 0:
			result = result + '-- '+ note.content
	
	return result
#####

def package2OCL(package):
	"""
    Generate a complete OCL specification for a given package.
    The inner package structure is ignored. That is, all
    elements useful for USE OCL (enumerations, classes, 
    associationClasses, associations and invariants) are looked
    recursively in the given package and output in the OCL
    specification. The possibly nested package structure that
    might exist is not reflected in the USE OCL specification
    as USE is not supporting the concept of package.
    """
	elements = package.ownedElement
				
	for element in elements:		
		if isinstance(element, Class):
			umlClass2OCL(element)
		if isinstance(element, Package):
			package2OCL(element) # Handling other packages


def enumPackageGeneration(package):
	'''
	Generate enumerations for all packages : This allows us to have 
	enum declaration at the top of generated OCL code 
	(Mandatory in USE specs)
	'''
	elements = package.ownedElement
	
	for element in elements:
		if isinstance(element, Enumeration):
			umlEnumeration2OCL(element)
		if isinstance(element, Package):
			enumPackageGeneration(element) # Handle other packages

def constraintGeneration(package):
	'''
	Constraint generation
	'''
	elements = package.ownedElement

	for element in elements:
		if isinstance(element, Class):
			signals = element.ownedElement
			for signal in signals:
				if isinstance(signal, Signal):
					constraint2OCL(signal)
					
		if isinstance(element, Package):
			constraintGeneration(element) # treat other packages
			
#---------------------------------------------------------
#           User interface for the Transformation 
#---------------------------------------------------------
# The code below makes the link between the parameter(s)
# provided by the user or the environment and the 
# transformation functions above.
# It also produces the end result of the transformation.
# For instance the output can be written in a file or
# printed on the console.
#---------------------------------------------------------

# (1) computation of the 'package' parameter
# (2) call of package2OCL(package)
# (3) do something with the result

# Elements selected by user in Modelio
elements = selectedElements

# Check if a user has selected a package
isPackageSelected = False

# Contains associations whose OCL declaration are already generated
# Avoid duplicate declaration
global _global_assoAlreadyTreated 
_global_assoAlreadyTreated = set()
global _global_asso_unspecified
_global_asso_unspecified = 0

if len(elements) > 0:
	print 'model CyberResidences\n'

	for e in elements:
		if isinstance(e, Package):
			isPackageSelected = True
			# Generate enumerations first
			enumPackageGeneration(e)
			# Generate the rest
			package2OCL(e)
			# Generate the constraints
			constraintGeneration(e)
	
	if isPackageSelected == False:
		print '-- No selected valide package !'
else:
		print '-- No selected element !\n-- Please select one !'
				
	
	