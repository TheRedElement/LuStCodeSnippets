/**errors.js */

/**imports */

/**definitions */
/**
 * function to show a custom error message and highlight the faulty html element 
 * @param {HTMLElement} element 
 *  - element that caused the error
 * @param {*} message 
 *  - message to displace
 * @param {*} duration 
 *  - for how long to highlight the element
 */
export function showError(element, message, duration = 2000) {
    alert(message);                             //display error
    element.classList.add("error-highlight");   //highlight faulty element

    //remove highlight  
    setTimeout(() => {
        element.classList.remove("error-highlight");
    }, duration);
}