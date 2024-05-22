<script>
	import { AUTH_SERVER_URL } from '$lib/consts.js';
	import { auth_server_login } from '$lib/network';
	import { createWritableLocalStore } from '$lib/stores.js';
	import { page } from '$app/stores';
	import { goto } from '$app/navigation';
	import Spinner from '$lib/components/Spinner.svelte';
	import { auth_token } from '$lib/stores.js';
	let submit_enabled = false;
	let submiting = false;
	/**
	 * @type {string}
	 */
	let username;
	/**
	 * @type {string}
	 */
	let password;
	function submit(e) {
		console.log('submit');
		e.preventDefault();
		submiting = true;
		auth_server_login(username, password)
			.then((res) => {
				console.log(res);

				// navigate to the next page or home page
				if (res.status === 200) {
					alert('Login successful');
					res.json().then((data) => {
						auth_token.set(data);
						debugger;
						let auth_b64 = window.btoa(JSON.stringify($auth_token));
						let auth_b64Safe = encodeURIComponent(auth_b64);
						let next = $page.url.searchParams.has('next')
							? $page.url.searchParams.get('next')
							: '/';
						let next_url = new URL(next);
						next_url.searchParams.set('auth_token', auth_b64Safe);

						window.location.href = next_url;
					});
				} else {
					res.json().then((data) => {
						alert('Error logging in: ' + JSON.stringify(data));
					});
				}
			})
			.catch((err) => {
				debugger;
				console.error(err);
				alert('Error sending login request' + JSON.stringify(err));
			})
			.finally(() => {
				debugger;
				submiting = false;
			});
	}

	$: submit_enabled = username !== undefined && password !== undefined && !submiting;
</script>

<div class="container mt-3">
	<h1>Auth Login</h1>
	<form method="post" action="" on:submit={submit}>
		<div class="form-group">
			<label for="username">Username:</label>
			<input
				type="text"
				class="form-control"
				name="username"
				id="username"
				bind:value={username}
				required
			/>
		</div>

		<div class="form-group">
			<label for="password">Password:</label>
			<input
				type="password"
				class="form-control"
				name="password"
				id="password"
				bind:value={password}
				required
			/>
		</div>
		<button type="submit" class="btn btn-primary" disabled={!submit_enabled}>
			{#if submiting}
				Login <Spinner />
			{:else}
				Login
			{/if}
		</button>
	</form>
</div>
