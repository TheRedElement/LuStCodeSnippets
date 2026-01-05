

export function range(start, stop, step=1) {
    let arr = [];
    let val = start;
    while (val < stop) {
        arr.push(val);
        val += step;
    }
    return arr
}
export function rand(n) {
    let arr = [];
    for (let i = 0; i < n; i++) {
        arr[i] = Math.random();
    }
    return arr
}
export function reshape(arr, chunkSize) {
    const reshaped = [];
    for (let i = 0; i < arr.length; i+=chunkSize) {
        reshaped.push(arr.slice(i, i+chunkSize));
    }
    return reshaped
}

