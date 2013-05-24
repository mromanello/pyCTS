## Notes about topology

These are the values that topology can take:

	enum Topology {
	     EQUALS, PRECEDES, FOLLOWS, CONTAINS, IS_CONTAINED_BY, PRECEDES_AND_OVERLAPS, OVERLAPS_AND_FOLLOWS
	}
	
And these care the possible cases for comparison of URNs:

	Topology urnTopology(CtsUrn urn1, CtsUrn urn2) {
	        // 3 cases to consider:

	        if ((!urn1.isRange()) &&  (!urn2.isRange())) {
	            return twoPointTopology(urn1, urn2)
            
	        } else if ((!urn1.isRange()) && (urn2.isRange())) {
	            return pointToRangeTopology(urn1, urn2)


	        } else if ((urn1.isRange()) && (!urn2.isRange())) {
	            return rangeToPointTopology(urn1, urn2)

	        } else if ((urn1.isRange()) && (urn2.isRange())) {
	            return rangeToRangeTopology(urn1,urn2)

	        } else {
	            return null
	        }
	    }