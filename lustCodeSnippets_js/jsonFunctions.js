/**jsonFunctions.js */

/**imports */

/**definitions */
/**
 * - method to stringify a JSON object up to a depth of `maxDepth`
 *      - all deeper layers are contracted into one-line JSON-objects
 * - executes replacements to make sure the resulting object can be parsed via `JSON.parse()`
 * @param {Object} obj
 * 	- json object to be stringified
 * @param {Int} maxDepth 
 * 	- maximum depth until which to expand
 * 	- everything deeper than that will be collapsed
 * 	- if `-1` no collapse will be applied
 * @param {Int} indent
 * 	- number of spaces to use for the indentation
 * @returns {String} stringified
 * 	- stringified version of `obj`
 */
export function stringifyJSONToDepth(obj, maxDepth = 3, indent = 2) {
	const seen = new WeakSet();

	function helper(value, depth) {
		if (value === null || typeof value !== "object") {
			//check for leaf (stop recursion when no more nested values found)
			return value;
		}

		if (seen.has(value)) {
			//in case a circular reference detected return marker string
			return "[Circular]";
		}
		seen.add(value);	//add last value to seen values

		if (depth >= maxDepth) {
			//convert all levels below to string
			return JSON.stringify(value);
		}

		if (Array.isArray(value)) {
			//recurse
			return value.map(v => helper(v, depth + 1));
		}

		//apply for all top-level entries
		const result = {};
		for (const [k, v] of Object.entries(value)) {
			result[k] = helper(v, depth + 1);
		}
		return result;
	}

	//apply stringification
	if (maxDepth === -1) {
		//no stringification
		return JSON.stringify(obj, null, indent);
		
	}
	let stringified = JSON.stringify(helper(obj, 0), null, indent);
	
	
	// //replace some characters to have collapsed part still be its original type and not a string
	stringified = stringified.replaceAll(/\\"/g, "'")								//temporarily get rid of escaped quotes
	stringified = stringified.replaceAll(/(\s+)\"(.+')(.+)\"(,*)$/gm, "$1$2$3$4")	//remove quotes denoting a string
	stringified = stringified.replaceAll(/'/g, '"')									//add the quotes back

	return stringified
}
