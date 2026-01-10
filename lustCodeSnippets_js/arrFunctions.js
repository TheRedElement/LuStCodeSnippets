/**arrFunctions.js */

/**imports */

/**definitions */
/**
 * - function imitating numpy's linspace
 * @param {Float} start 
 *  - arg, required
 *  - starting point of the sequence
 * @param {Float} stop 
 *  - arg, required
 *  - stopping point of the sequence
 * @param {Int} num 
 *  - arg, optional
 *  - number of points to generate between `start` and `stop`
 *  - the default is `100`
 * @returns {Array} arr
 *  - array with `num` entries ranging from `start` to `stop`
 */
export function linspace(start, stop, num = 100) {
    //init output
    const arr = [];
    
    //special cases
    if (num <= 0) return arr;
    if (num === 1) return [stop];

    //generate
    const step = (stop - start) / (num - 1);
    for (let i = 0; i < num; i++) {
        if (i === num - 1) {
            arr.push(stop);
        } else {
            arr.push(start + (step * i));
        }
    }
    return arr;
}
/**
 * - function implementing min-max-scaling
 * @param {*} arr
 *  - arg, required
 *  - input to be scaled 
 * @param {Float} xMin
 *  - kwarg, optional
 *  - minimum of target range
 *  - the default is `0.0`
 * @param {Float} xMax
 *  - kwarg, optional
 *  - maximum of target range
 *  - the default is `1.0`
 * @param {Float} xRefMin
 *  - kwarg, optional
 *  - reference value (minimum of original series)
 *  - the default is `null`
 *      - set to `Math.min(...arr)`
 * @param {Float} xRefMax
 *  - kwarg, optional
 *  - reference value (maximum of original series)
 *  - the default is `null`
 *      - set to `Math.min(...arr)`
 * @returns {Array} arrScaled
 *  - rescaled version of `arr`
 *  - contains values in the interval `xMin`, `xMax`
 */
export function minMaxScale(
        arr,
        {
            xMin=0.0, xMax=1.0,
            xrefMin=null, xrefMax=null,
        } = {}
    ) {
    
    xrefMin = xrefMin === null ? Math.min(...arr) : xrefMin;
    xrefMax = xrefMax === null ? Math.max(...arr) : xrefMax;


    let arrScaled = arr.map(xi => (xi - xrefMin)/(xrefMax-xrefMin));
    arrScaled = arrScaled.map(xs => xs * (xMax - xMin) + xMin);

    return arrScaled
}
/**
 * - function imitating numpy's `np.ones_like()`
 * @param {Array} arr 
 *  - arg, required
 *  - template array
 * @returns {Array}
 *  - array filled with `1` of same length as `arr`
 */
export function onesLike(arr) {
    return Array(arr.length).fill(1)
}
/**
 * - function imitating numpy's `np.random.randn()`
 * - based on Box-Muller transform
 * 
 * @param {Int} num
 *  - kwarg, optional
 *  - number of values to generate
 *  - the default is `1`
 * @param {Float} mean
 *  - kwarg, optional
 *  - mean of the sampled normal distribution
 *  - the default is `0`
 * @param {Float} std
 *  - kwarg, optional
 *  - standard deviation of the sampled normal distribution
 *  - the default is `1`
 * @returns {Array} out
 *  - array of length `num` filled with values sampled from a normal distribution with mean `mean` and standard deviation `std`
 */
export function randomNormal({
    num=1,
    mean=0, std=1,
    } = {}) {
    var out = [];
    for (let index = 0; index < num; index++) {
        const u = 1 - Math.random(); //convert [0,1) to (0,1]
        const v = Math.random();
        const z = Math.sqrt( -2.0 * Math.log(u) ) * Math.cos(2.0 * Math.PI * v);
        //transform to the desired mean and standard deviation (based on Box-Muller transform)
        out.push(z * std + mean);
    }
    return out
}
/**
 * - function defining a sigmoid
 * @param {Array} x 
 *  - arg, required
 *  - independent variable to evaluate sigmoid on
 * @param {Float} k 
 *  - arg, optional
 *  - slope parameter of the resulting sigmoid
 * @returns {Array} y
 *  - same length as `x`
 *  - sigmoid evaluated on `x`
 */
export function sigmoid(
    x, k=1
    ) {
    const y = x.map( xi => 1/(1 + Math.exp(-k*xi)));
    return y
}