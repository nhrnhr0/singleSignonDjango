<script>
	import { browser } from '$app/environment';
	import { createWritableLocalStore } from '$lib/stores.js';
	import { uuidv4 } from '$lib/utils';
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { AUTH_SERVER_URL } from '$lib/consts';

	// let auth_token = createWritableLocalStore('auth_token', {});
	// let screen_id = createWritableLocalStore('screen_id', undefined);
	let screen_url = createWritableLocalStore('screen_url', undefined);
	let screen_id = undefined;
	let qr_url = '';
	let login_url = '';
	/**
	 * @type {number | undefined}
	 */
	let check_interval = undefined;
	const CHECK_INTERVAL_TIMEOUT = 1000;
	function regenerate_screen_id() {
		screen_id = uuidv4();
		login_url = `${$page.url.origin}/activate-screen?screen_id=${screen_id}`;
		QRCode.toDataURL(login_url, { errorCorrectionLevel: 'H' }, function (err, url) {
			if (err) {
				console.error(err);
				return;
			}
			console.log(url);
			qr_url = url;
		});
	}
	onMount(() => {
		if ($screen_url) {
			window.location = $screen_url;
		}
		regenerate_screen_id();
		check_interval = start_interval();
	});

	function start_interval() {
		return setInterval(() => {
			// send POST request to <SSO-AUTH>/get-screen-access with screen_id
			// if the response is 200, parse the response:
			// from the JSON:
			// 	if status is success: set auth_token and screen_id in local storage and redirect to 'redirect_url' in response and clear interval
			// 	if status is error and error_type is 'credentials_sent': generate new screen_id and qr_url clear interval
			let url = `${AUTH_SERVER_URL}/get-screen-access/`;
			let data = { screen_id: screen_id };
			fetch(url, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify(data)
			})
				.then((response) => {
					if (response.status === 200) {
						return response.json();
					} else {
						throw new Error('Error in response');
					}
				})
				.then((data) => {
					if (data.status === 'success') {
						clearInterval(check_interval);
						let url = data.redirect_to;
						debugger;
						$screen_url = url;
						window.location.href = url;
					} else if (data.status === 'error' && data.error_type === 'credentials_sent') {
						regenerate_screen_id();
						clearInterval(check_interval);
						check_interval = start_interval();
					}
				})
				.catch((error) => {
					console.error('Error:', error);
				});
		}, CHECK_INTERVAL_TIMEOUT);
	}
</script>

{#if qr_url}
	<img src={qr_url} alt="QR Code" />
	<a target="_blank" href={login_url}>{login_url}</a>
{:else}
	<p>Generating QR Code...</p>
{/if}
