<script>
	import { protected_route } from '$lib/utils';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';
	import { network_register_screen } from '$lib/network';
	import Spinner from '$lib/components/Spinner.svelte';
	import { browser } from '$app/environment';
	import { auth_token } from '$lib/stores.js';

	let screen_id = browser && $page.url.searchParams.get('screen_id');
	let screen_name;
	let submiting = false;
	let error_msg = '';
	protected_route();
	onMount(() => {
		console.log('onMount');
	});

	function submit(e) {
		e.preventDefault();
		console.log('submit');
		network_register_screen(screen_id, screen_name).then(([res, json]) => {
			// if res.status == 200 and json.status == 'success': redirect to redirect_to
			// if res.status == 200 and json.status == 'error': show error message
			// if res.status != 200: show error message
			console.log(res);
			console.log(json);

			if (res.status === 200 && json.status === 'success') {
				window.location.href = json.redirect_to;
			} else {
				console.log('error');
				debugger;
				error_msg = json.detail;
			}
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
		{#if error_msg}
			<div class="error-msg">
				{error_msg}
			</div>
		{/if}
	</form>
</div>

<style lang="scss">
	.error-msg {
		color: red;
	}
</style>
