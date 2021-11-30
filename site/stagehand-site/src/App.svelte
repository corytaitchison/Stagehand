<script lang="ts">
	import { fade} from "svelte/transition";
	export let name: string;
	let show: Boolean = false;
</script>

<main>
	<h1>Hello {name}!</h1>
	{#if show}
	<p transition:fade>
		Visit the <a href="https://svelte.dev/tutorial">Svelte tutorial</a> to
		learn how to build Svelte apps.
	</p>
	{/if}
	<button on:click="{() => {show = !show;}}">Click me!</button>
</main>

<style>
	main {
		text-align: center;
		padding: 1em;
		max-width: 240px;
		margin: 0 auto;
	}

	h1 {
		color: #ff3e00;
		text-transform: uppercase;
		font-size: 4em;
		font-weight: 100;
	}

	@media (min-width: 640px) {
		main {
			max-width: none;
		}
	}
</style>
