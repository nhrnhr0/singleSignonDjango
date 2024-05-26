import { browser } from "$app/environment";
import { goto } from "$app/navigation";
import { auth_token } from "./stores";
import { get } from "svelte/store";


export function uuidv4() {
    return "10000000-1000-4000-8000-100000000000".replace(/[018]/g, c =>
        (+c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> +c / 4).toString(16)
    );
}


export function protected_route() {
    if (!browser) return;
    let token = get(auth_token);
    console.log('protected_route:', token);
    if (get(auth_token) == undefined || get(auth_token) == null || Object.keys(get(auth_token)).length == 0)
    {
        goto("/login?next=" + window.location.href);
    }

}