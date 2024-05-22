<script>
	import { browser } from '$app/environment';
	import { createWritableLocalStore } from '$lib/stores.js';
	import { uuidv4 } from '$lib/utils';
	import QRCode from 'qrcode';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	let auth_token = createWritableLocalStore('auth_token', {});
	let screen_id = createWritableLocalStore('screen_id', undefined);
	let qr_url = '';
	let login_url = '';
	onMount(() => {
		debugger;
		console.log('onMount', $screen_id);
		if ($screen_id === undefined) {
			$screen_id = uuidv4();
		}
		login_url = `${$page.url.origin}/activate-screen?screen_id=${$screen_id}`;
		console.log(login_url);
		QRCode.toDataURL(login_url, { errorCorrectionLevel: 'H' }, function (err, url) {
			if (err) {
				console.error(err);
				return;
			}
			console.log(url);
			qr_url = url;
		});
	});
</script>

{#if qr_url}
	<img src={qr_url} alt="QR Code" />
	<a target="_blank" href={login_url}>Activate Screen</a>
{:else}
	<p>Generating QR Code...</p>
{/if}
