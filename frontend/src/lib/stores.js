import { browser } from '$app/environment';
import { writable } from 'svelte/store';


// function that givven a key, return a writeable store object that can be used to store data and when updated, save to local storage
/**
 * @param {string|undefined} key 
 * @param {object|string} startValue 
 * @returns 
 */
export function createWritableLocalStore(key, startValue) {
    let initialValue = undefined;
    if (browser)
    {
        initialValue = localStorage.getItem(key);
    }
    if (initialValue)
    {
        startValue = JSON.parse(initialValue);
    }
    let wtble = writable(startValue);
    // subscribe to the store and save the value to local storage
    wtble.subscribe(value => {
        if (browser)
        {
            if (value != undefined)
            {
                localStorage.setItem(key, JSON.stringify(value));
            }
        }
    });
    return wtble;


}



export let auth_token = createWritableLocalStore("auth_token", undefined);