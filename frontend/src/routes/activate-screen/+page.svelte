<script>
	import { protected_route } from '$lib/utils';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { network_get_standalog_server_url, network_register_screen } from '$lib/network';
	import Spinner from '$lib/components/Spinner.svelte';
	import { browser } from '$app/environment';
	import { auth_token } from '$lib/stores.js';

	let screen_id = browser && $page.url.searchParams.get('screen_id');
	let screen_name;
	let submiting = false;
	onMount(() => {
		console.log('onMount');
		protected_route();
	});

	function submit(e) {
		e.preventDefault();
		console.log('submit');
		network_register_screen(screen_id, screen_name)
			.then((res) => {
				console.log(res);
				if (res.status === 200) {
					alert('Screen activated');
					// find the standalog server URL and redirect to it
					network_get_standalog_server_url()
						.then((res) => {
							if (res.status === 200) {
								res.json().then((data) => {
									console.log(data);
									debugger;
									let auth_b64 = window.btoa(JSON.stringify($auth_token));
									let auth_b64Safe = encodeURIComponent(auth_b64);
									let url = `${data.url}/display/?screen_id=${screen_id}&auth_token=${auth_b64Safe}`;
									console.log(url);
									debugger;
									window.location.href = url;
								});
							} else {
								res.json().then((data) => {
									debugger;
									alert(data.detail);
								});
							}
						})
						.catch((err) => {
							console.error(err);
							alert('Error getting standalog server URL');
						});
				} else {
					res.json().then((data) => {
						debugger;
						alert(data.detail);
					});
				}
			})
			.catch((err) => {
				console.error(err);
				alert('Error activating screen' + err);
			});
	}
</script>

<div class="container mt-3">
	<h1>Activate Screen</h1>
	<p>Screen ID: {screen_id}</p>
	<form method="post" action="" on:submit={submit}>
		<div class="form-group">
			<label for="name">Name:</label>
			<input
				type="text"
				class="form-control"
				name="name"
				id="name"
				bind:value={screen_name}
				required
			/>
		</div>
		<button type="submit" class="btn btn-primary">
			{#if submiting}
				Activate <Spinner />
			{:else}
				Activate
			{/if}
		</button>
	</form>
</div>
