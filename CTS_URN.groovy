package edu.harvard.chs.cts3


/**
* A class representing a reference to a text passage in a logical
* hierarchical scheme, expressed in the notation of the Canonical
* Text Services URN system.  This class parses URNs expressed as
* Strings, and makes the components of the URN programmatically accessible.
* In addition, this class can construct Pseudo-URNs.  See more on that
* in separate documentation.
* Note that while the automatically generated groovydoc output does not
* show get* methods for all the CtsUrn's member properties,
* Groovy  compilation automatically creates those public methods.
* See the included tests/testCtsUrn.groovy for examples.
*/
class CtsUrn {
    /*
      final static String libraryVersion = "cts3-beta-02"
      // really should be build automatically at build time
      final static String libraryDate = "June 28, 2009"

      // generate automatically at compile time:
      final static String compileDate
      */
      // All member properties are initialized in constructor,
      // so make them final:
      // the whole URN:
      final String asString

      // top-level components:
      final String ctsNamespace
      final String workComponent
      final String passageComponent

      // parts of workComponent:
      final String textGroup
      final String work
      final String version
      final String exemplar

      final int workLevel1
      final int workLevel2
      
      // parts of passageComponent
      final String passageNode
      final String rangeBegin
      final String rangeEnd

      final String subref1
      final int subrefIdx1
      final String subref2
      final int subrefIdx2


      final int passageLevel

      // useful constants
      final static int EXEMPLAR_LEVEL = 4
      final static int VERSION_LEVEL = 3
      final static int EDITION_LEVEL = 3
      final static int TRANSLATION_LEVEL = 3
      final static int WORK_LEVEL = 2
      final static int GROUP_LEVEL = 1


      /**
      * Private method assigns appropriate values to member properties
      * based on a Pseudo-Urn String submitted to constructor.
      * @param pseudoUrnString The values to assign, represented as a Pseudo-Urn String.
      */
      private void initializePseudoUrn(String pseudoUrnString) {
	     def components = pseudoUrnString.split(":")
	     if ((components[0] != 'psurn') ||  (components[1] != 'cts') ) {
	     		    throw new Exception("InitializeUrn: Bad syntax for pseudo-URN: ${urnString}")
	     }
	     this.ctsNamespace = null

	     // exploit fall through:
	     switch (components.size()) {

	     case 4:
	     this.passageComponent = 	 components[3]
	     case 3:
	     if (components[2]) {
	     	this.workComponent = components[2]
	     } else {
 	     	throw new Exception("Bad URN syntax: no textgroup in ${urnString}")
	     }
	     break

	     // must have at least a namespace + work identifier,
	     // in addition to required 'urn' prefix and namespace
	     // identifier:
	     default :
	     	     throw new Exception("Method initializeURN: bad syntax: ${urnString}")
	     break
	     } //switch

	     def splitWork = this.workComponent.split("[\\.]")
	     this.workLevel1 = splitWork.size()
	     switch (this.workLevel1) {
		case 3:
		this.version = splitWork[2]
		case 2:
		this.work = splitWork[1]
		default :
		this.textGroup = splitWork[0]
	     }

	     if (this.passageComponent) {
	     	def splitRange = this.passageComponent.split("[\\-]")
		switch (splitRange.size()) {
		case 2:
		this.rangeEnd = splitRange[1]
		this.rangeBegin = splitRange[0]
		break

		case 1:
		this.passageNode = splitRange[0]
		def splitPassageNode = this.passageNode.split("[\\.]")
		this.passageLevel = splitPassageNode.size()
		break		

		default : 
		// ??
		break
		}
	    }
      } // initializePseudoUrn


      /**
      * Private method assigns appropriate values to member properties
      * based on Urn String submitted to constructor.
      * @param urnString The values to assign, represented as a CTS Urn String.
      */
      private void initializeUrn(String urnString) {
	     def components = urnString.split(":")
	     if ((components[0] != 'urn') ||  (components[1] != 'cts') ) {
	     		    throw new Exception("InitializeUrn: Bad URN syntax: ${urnString}")
	     }

	     // exploit fall through:
	     switch (components.size()) {

	     case 5:
	     this.passageComponent = 	 components[4]

	     case 4:
	     if (components[3]) {
	     	this.workComponent = components[3]
	     	this.ctsNamespace = components[2]
	     } else {
 	     	throw new Exception("Bad URN syntax: no textgroup in ${urnString}")
	     }
	     break

	     // must have at least a namespace + work identifier,
	     // in addition to required 'urn' prefix and namespace
	     // identifier:
	     default :
	     	     throw new Exception("Method initializeURN: bad syntax: ${urnString}")
	     break
	     }
	     def splitWork = this.workComponent.split("[\\.]")
	     this.workLevel1 = splitWork.size()
	     switch (this.workLevel1) {
		case 3:
		this.version = splitWork[2]
		case 2:
		this.work = splitWork[1]
		default :
		this.textGroup = splitWork[0]
	     }

	     if (this.passageComponent) {
	     	def splitRange = this.passageComponent.split("[\\-]")
		switch (splitRange.size()) {
		case 2:
//		this.rangeEnd = splitRange[1]
//		this.rangeBegin = splitRange[0]

		initializeRange(splitRange[0], splitRange[1])

		break

		case 1:
/*
		this.passageNode = splitRange[0]
		def splitPassageNode = this.passageNode.split("[\\.]")
		this.passageLevel = splitPassageNode.size()
*/
		initializePoint(splitRange[0])
		break		

		default : 
		// ??
		break
		}
	     }
      }



      /**
      * "Private" method uses a regular expression to parse
      *  a subref String into a list of either 1 or 2 elements.  
      *  If there is an index value, it is the second element;
      *  the (possibly empty) substring value is the first element
      *  in the list.
      *	 @param str The subref String to parse.
      *  @returns A list with the string component of the substring
      *	 reference, and (if included) an integer index in the second
      *  element of the list.
      *  @throws SHOULD THROW A CTS EXCEPTION IF INDEX VALUE
      * DOES NOT PARSE AS A POSITIVE INTEGER:  NOT YET IMPLEMENTED.
      */
      private ArrayList indexSubref(String str) {
      	      ArrayList idx = []
	      def substrRE = /(.*)\Q[\E(.+)\Q]\E/
	      def matcher = (str =~ substrRE)
	      if (matcher.matches()) {
	      idx << matcher[0][1]
	      idx << matcher[0][2]

	      } else {
	      idx << str
	      }
	      return idx
      }



      /**
      * "Private" method assigns appropriate values ot member
      * properites if URN is a reference to a single node.
      * @param str The URN to parse, as a String.
      */    
      private void initializePoint(String str) {
      	      def splitSub = str.split(/#/)
      	      switch (splitSub.size()) {
	      case 1:
	      this.passageNode = splitSub[0]

	      break

	      case 2:
      	      this.passageNode = splitSub[0]
	      this.subref1 = splitSub[1]
	      ArrayList subrefParts = indexSubref(this.subref1)
	      this.subref1 = subrefParts[0]
	      if (subrefParts.size() == 2) {

	      // try..catch this:
	      this.subrefIdx1 = subrefParts[1].toInteger()
	      }
	      break
	      }
      	      
      }



      /**
      * "Private" method assigns appropriate values ot member
      * properites if URN is a reference to a range.
      * @param str The URN to parse, as a String.
      */    
      private void initializeRange(String str1, String str2) {

	def splitSub = str1.split(/#/)
      	      switch (splitSub.size()) {
	      case 1:
	      this.rangeBegin = splitSub[0]

	      break

	      case 2:
      	      this.rangeBegin = splitSub[0]
	      this.subref1 = splitSub[1]
	      ArrayList subrefParts = indexSubref(this.subref1)
 	      this.subref1 = subrefParts[0]
	      if (subrefParts.size() == 2) {

	      // try..catch this:
	      this.subrefIdx1 = subrefParts[1].toInteger()
	      }
	      break
	      }


	splitSub = str2.split(/#/)
      	     switch (splitSub.size()) {
	      case 1:
	      this.rangeEnd = splitSub[0]

	      break

	      case 2:
      	      this.rangeEnd = splitSub[0]
	      this.subref2= splitSub[1]
	      ArrayList subrefParts = indexSubref(this.subref2)
 	      this.subref2 = subrefParts[0]
	      if (subrefParts.size() == 2) {

	      // try..catch this:
	      this.subrefIdx2 = subrefParts[1].toInteger()
	      }
	      break
	      }
      }




      /** CtsUrns are constructed from a String conforming to the
      * syntax and semantics of the draft CTS URN proposal.
      */
      CtsUrn (String urnStr) {
      	     this.asString = urnStr
	     if (urnStr ==~ /^psurn:.*/) {
	     	initializePseudoUrn(urnStr)

	     } else if (urnStr ==~ /^urn:.*/) {
	       this.initializeUrn(urnStr)

	     }	else {
    	     	throw new Exception("Bad URN syntax: ${urnStr}")
	     }
      }
      
      /**
      * Returns the CTS URN object as a String in the notation defined by
      * the proposed CTS URN standard.
      * @returns The URN as a String.
      */
      String toString() {
      	     return asString
      }


      /**
      * Gets the full URN for the work-level reference, without any further
      * reference information.
      * @returns The full URN, as a String, down to the work-level.
      */
      String getUrnWithoutPassage() {
      	     return "urn:cts:" + this.ctsNamespace + ":" + this.workComponent
      }

    /**
    * Finds passage component of a URN, trimmed
    * to <code>limit</code> levels of the citation
    * hierarchy.
    * @param limit Number of levels of hierarchy to
    * include in resulting passage String.
    * @returns Requesed passage component of the URN,
    * or if limit exceeds the number of elements
    * in the passage component, returns the original URN.
    */
    String getPassage(int limit) {
	def psgVals = this.passageComponent.split(/\./)
	StringBuffer refBuff = new StringBuffer(psgVals[0])
	if (limit > psgVals.size()) {
	    return this.getPassageComponent()
	}
	def count = 1
	while (count < limit) {
	    refBuff.append("." + psgVals[count])
	    count++
	}
	return refBuff.toString()
    }

      /**
      * Gets the last (leaf-level) part of the URN's reference.
      * @return The right-most part of the passage or range reference.
      */
      String getLeafRefValue() {
        def refVals = this.passageComponent.split(/\./)
        return refVals[refVals.size() - 1]
      }


    /**
    * Counts depth of the citation hierarchy in a URN's 
    * passage component.
    * @returns Number of elements in a passage reference.
    */
    int getCitationDepth() {
        def refVals = this.passageComponent.split(/\Q.\E/)
        return refVals.size()
    }


      /**
      * Expresses the level of the work component's
      * reference with an English word.
      * @returns A label for this level of work citation.
      */
      String labelForWorkLevel() {
      	  switch (workLevel1) {
	  case CtsUrn.EXEMPLAR_LEVEL:
	  return "exemplar"

	  case CtsUrn.VERSION_LEVEL:
	  return "version"

	  case CtsUrn.WORK_LEVEL:
	  return "work"

	  case CtsUrn.GROUP_LEVEL:
	  return "group"

	  default:
	  return "Unknown type for work component of URN string ${asString}!"
      	  }
      }


      // For work components, override groovy's standard get* methods
      // in order to control inclusion/exclusion of CTS namespace
      /**
      * Returns the text group component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty.
      * @returns A String value for the text group.
      */
      String getTextGroup() {
       	     if ((ctsNamespace) && (ctsNamespace != ""))  {
		return "${ctsNamespace }:${textGroup}"
	     } else {
	       return textGroup
	     }
      }

      /**
      * Returns the text group component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty, or the
      * nsQualified parameter is false.
      * @param nsQualified True to include the CTS namespace,
      * false to omit it.
      * @returns A String value for the text group.
      */
      String getTextGroup(boolean nsQualified) {
      	     if ((nsQualified) && (ctsNamespace) && (ctsNamespace != "")) {
		   return "${ctsNamespace }:${textGroup}"
	      } else {
		  return textGroup
	      }
      }

      /**
      * Returns the work component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty.
      * @returns A String value for the work.
      */
      String getWork() {
       	     if ((ctsNamespace) && (ctsNamespace != ""))  {
		return "${ctsNamespace }:${work}"
	     } else {
	       return work
	     }
      }

      /**
      * Returns the work component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty, or the
      * nsQualified parameter is false.
      * @param nsQualified True to include the CTS namespace,
      * false to omit it.
      * @returns A String value for the work.
      */
      String getWork(boolean nsQualified) {
      	     if ((nsQualified) && (ctsNamespace) && (ctsNamespace != "")) {
		   return "${ctsNamespace }:${work}"
	      } else {
		  return work
	      }
      }

      /**
      * Returns the version component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty.
      * @returns A String value for the version.
      */
      String getVersion() {
       	     if ((ctsNamespace) && (ctsNamespace != ""))  {
		return "${ctsNamespace }:${version}"
	     } else {
	       return version
	     }
      }

      /**
      * Returns the version component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty, or the
      * nsQualified parameter is false.
      * @param nsQualified True to include the CTS namespace,
      * false to omit it.
      * @returns A String value for the version.
      */
      String getVersion(boolean nsQualified) {
      	     if ((nsQualified) && (ctsNamespace) && (ctsNamespace != "")) {
		   return "${ctsNamespace }:${version}"
	      } else {
		  return version
	      }
      }

      /**
      * Returns the exemplar component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty.
      * @returns A String value for the exemplar.
      */
      String getExemplar() {
       	     if ((ctsNamespace) && (ctsNamespace != ""))  {
		return "${ctsNamespace }:${exemplar}"
	     } else {
	       return exemplar
	     }
      }

      /**
      * Returns the exemplar component of the URN qualified by its
      * cts namespace, unless the cts namespace is empty, or the
      * nsQualified parameter is false.
      * @param nsQualified True to include the CTS namespace,
      * false to omit it.
      * @returns A String value for the exemplar.
      */
      String getExemplar(boolean nsQualified) {
      	     if ((nsQualified) && (ctsNamespace) && (ctsNamespace != "")) {
		   return "${ctsNamespace }:${exemplar}"
	      } else {
		  return exemplar
	      }
      }

      /**
      * Determines if the object is a valid Urn, or a Pseudo-Urn by
      * looking to see if the work reference is qualified
      * by a CTS namespace.
      * @returns True if the object is a valid Urn, otherwise false.
      */
      boolean isUrn() {
      	      if ((!ctsNamespace) || (ctsNamespace == "")) {
	      return false
	      } else {
	      return true
	      }
      }


      /**
      * Gets the numeric level of a citation categorized
      * by one of the standard text labels used in this library.
      * This method is the converse of labelForWorkLevel(),
      * with the asymmetry that "version", "edition" and "translation"
      * all correctly resolve to the same level, since edition and
      * translation can only be distinguished with further information
      * such as that supplied by a TextInventory.
      * @param label A standard String value for the work level of
      * this URN.
      * @returns An integer, ranging from 1 for text group to 4 for 
      * exemplar.
      */
      static int levelForLabel(String label) {
      	      switch(label){
	      case "group":
	      return 1

	      case "work":
	      return 2

	      // can only be disambiguated by a text inventory,
	      // but these are the standard CTS terms:
	      case "version":
	      case "edition":
	      case "translation":
	      return 3
	      
	      case "exemplar":
	      return 4

	      default:
	      return null
	      }
      }


      /**
      * Determines if the URN refers to a range of citation nodes,
      * or a single citation node.
      * @returns True if URN refers to a range of citation nodes.
      */
      boolean isRange() {
      return (this.rangeBegin != null)
      }


    /**
    * Trims the passage component to a 
    * specified level of the reference hierarchy.
    * @param level The number of levels of the citation
    * hierarchy to include.
    * @returns The trimmed URN, as a String.
    */
    public String trimPassage(int level) {
/*if (this.getPassage(level) == null) {
System.err.println "\tNo passage at ${level} from ${this}"
} */

//System.err.println "TRIM ${level}, ${this} -> " + this.getPassage(level)
   	   return this.getUrnWithoutPassage() + ":" + this.getPassage(level)
//   	   return this.getPassage(level)
    }

    /**
    * Formats a human-readable String with release and date
    * information.
    * @returns A human-readable summary of version information
    */

/*
    public static String getVersionInfo() {
	return "Part of the cts3 library, version ${libraryVersion}, packaged on ${libraryDate}."
    }
*/

}
