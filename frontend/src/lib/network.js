

import { AUTH_SERVER_URL } from "./consts";
import { auth_token } from "./stores";
import { get } from "svelte/store";

/**
 * @param {string} url
 * @param {object|undefined} options
 **/
export function auth_server_fetch(url, options = undefined) {
    debugger;
    var _auth_token = get(auth_token);
    // if toke is undefined, null or empty dict, do not add the Authorization header
    if (_auth_token != undefined && _auth_token != null && Object.keys(_auth_token).length != 0)
    {
        if (!options)
        {
            options = {};
        }
        if (!options.headers)
        {
            options.headers = {};
        }
        options.headers["Authorization"] = `Token ${_auth_token.token}`;
    }
    return fetch(url, options);
}

/**
 * @param {string} username 
 * @param {string} password 
 * @returns {Promise<Response>}
 */
export function auth_server_login(username, password) {
    var raw = JSON.stringify({
        "username": username,
        "password": password
    });

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: raw,
        redirect: 'follow'
    };

    return fetch(`${AUTH_SERVER_URL}/api-token-auth/`, requestOptions);
}



export function network_register_screen(screen_id, screen_name) {
    var raw = JSON.stringify({
        "screen_id": screen_id,
        "screen_name": screen_name
    });

    var requestOptions = {
        method: 'POST',
        headers: {
            "Content-Type": "application/json"
        },
        body: raw,
        redirect: 'follow'
    };

    return auth_server_fetch(`${AUTH_SERVER_URL}/register-screen/`, requestOptions);
}

export function network_get_standalog_server_url() {
    return auth_server_fetch(`${AUTH_SERVER_URL}/get-standalog-server-url/`);
}